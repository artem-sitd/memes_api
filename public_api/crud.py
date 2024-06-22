from fastapi import APIRouter, UploadFile, HTTPException, status, Depends

from media_api.s3connect import BucketNotSpecifiedError, BucketAlreadyExistsError
from settings import db_settings, s3_client
from .models import Memes
from .schemas import PostMemesSchema, BucketSchema
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from botocore.exceptions import ClientError

router = APIRouter()


# удаление файла из S3 и postgres
@router.delete("/delete_memes/{id}")
async def delete_memes_id(id: int, session: AsyncSession = Depends(db_settings.get_session)):
    target_memes = await session.get(Memes, id)
    if not target_memes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")
    try:
        await s3_client.delete_file(target_memes.description)
        await session.delete(target_memes)
        await session.commit()
        return {"message": f"Meme id: {id} deleted"}

    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ClientError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"ClientError: {str(e)}")

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Internal server error: {str(e)}")


@router.put("/put_memes/{id}")
async def put_memes_id(id: int, file: UploadFile, session: AsyncSession = Depends(db_settings.get_session)):
    try:
        filename = file.filename
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="ошибка при загрузке файла")

    try:
        target_memes = await session.get(Memes, id)
        if not target_memes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")

        await s3_client.delete_file(target_memes.description)
        file_url = await s3_client.upload_file(file)
        target_memes.src = file_url
        target_memes.description = filename
        await session.commit()
        return target_memes
    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error")


@router.get("/get_memes/{id}")
async def get_memes_id(id: int, session: AsyncSession = Depends(db_settings.get_session)):
    try:
        target_memes = await session.get(Memes, id)
        if not target_memes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meme not found")
        return target_memes
    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_memes")
async def get_all_memes(page: int = 1, page_size: int = 10, session: AsyncSession = Depends(db_settings.get_session)):
    try:
        offset = (page - 1) * page_size
        query = select(Memes).order_by(Memes.id).offset(offset).limit(page_size)
        result = await session.execute(query)
        memes = result.scalars().all()
        return {"memes": memes, "page": page, "page_size": page_size}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))


# отправка файла в S3 и postgresql
@router.post("/post_memes", response_model=PostMemesSchema)
async def create_memes(file: UploadFile, session: AsyncSession = Depends(db_settings.get_session)) -> PostMemesSchema:
    try:
        filename = file.filename
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="ошибка при загрузке файла")

    try:
        file_url = await s3_client.upload_file(file)
        new_meme = Memes(src=file_url, description=filename)
        session.add(new_meme)
        await session.commit()

        # если указать через распакову ** тогда тесты не проходят
        return PostMemesSchema(
            id=new_meme.id,
            src=new_meme.src,
            description=new_meme.description
        )

    except BucketNotSpecifiedError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f">>> Database error: {e}")

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error{e}")


# создание бакета
@router.post("/create_bucket", response_model=BucketSchema)
async def create_bucket(name: BucketSchema) -> BucketSchema:
    try:
        await s3_client.create_bucket(name.name)
        return BucketSchema(name=name.name)
    except BucketAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ClientError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"ClientError: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/")
async def hello() -> dict:
    return {"message": "все работает"}
