from fastapi import APIRouter, UploadFile, HTTPException, status
from settings import db_settings
from .models import Memes
from .schemas import PostMemesSchema
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.delete("/delete_memes/{id}")
async def delete_memes_id(id: int):
    pass


@router.put("/put_memes/{id}")
async def put_memes_id(id: int, file: UploadFile):
    try:
        filename = file.filename
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="ошибка при загрузке файла")

    async with db_settings.async_session() as session:
        target_memes = session.query(Memes).get(id)
        if not target_memes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")

    return {"message": id}


@router.get("/get_memes/{id}")
async def get_memes_id(id: int):
    pass


@router.get("/get_memes")
async def get_all_memes():
    pass


@router.post("/post_memes", response_model=PostMemesSchema)
async def create_memes(file: UploadFile) -> PostMemesSchema:
    try:
        filename = file.filename
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="ошибка при загрузке файла")

    try:
        async with db_settings.async_session() as session:
            new_meme = Memes(src=filename, description='zxc')
            session.add(new_meme)
            await session.commit()
        return PostMemesSchema(**new_meme.__dict__)

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error")


@router.get("/")
async def hello() -> dict:
    return {"message": "все работает"}
