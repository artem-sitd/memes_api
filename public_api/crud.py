from fastapi import APIRouter, UploadFile, HTTPException, status

from media_api.s3connect import BucketNotSpecifiedError
from settings import db_settings, s3_client
from .models import Memes
from .schemas import PostMemesSchema, BucketSchema
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.delete("/delete_memes/{id}")
async def delete_memes_id(id: int):
    async with db_settings.async_session() as session:
        target_memes = session.query(Memes).get(id)
        if not target_memes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")
        return


@router.put("/put_memes/{id}")
async def put_memes_id(id: int, file: UploadFile):
    try:
        filename = file.filename
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="ошибка при загрузке файла")

    try:
        async with db_settings.async_session() as session:
            target_memes = session.query(Memes).get(id)
            if not target_memes:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")
    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": id}


@router.get("/get_memes/{id}")
async def get_memes_id(id: int):
    try:
        ...

    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_memes")
async def get_all_memes():
    try:
        ...
    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error")


# создание бакета
@router.post("/create_bucket", response_model=BucketSchema)
async def create_bucket(name: BucketSchema) -> BucketSchema:
    s3_client.create_bucket(name)
    return BucketSchema(name=name)


@router.get("/")
async def hello() -> dict:
    return {"message": "все работает"}
