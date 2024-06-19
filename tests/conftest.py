import os

import pytest
import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from settings import db_settings
from main import app
from public_api.models import Base, Memes
from aiobotocore.session import get_session
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

# Настройки для тестовой базы данных и S3
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("test_db")
TEST_DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

TEST_S3_ENDPOINT_URL = os.getenv("endpoint_url")
TEST_S3_ACCESS_KEY = os.getenv("access_key")
TEST_S3_SECRET_KEY = os.getenv("secret_key")
TEST_S3_BUCKET_NAME = os.getenv("test_bucket_name")

test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


# перед началом всех тестов создаются таблицы с моделями, после окончания тестов - все таблицы удаляются
@pytest.fixture(scope="session")
async def db_engine():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


# аналог сессии из settings.py
@pytest.fixture(scope="function")
async def db_session(db_engine):
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session):
    def get_test_db():
        yield db_session

    app.dependency_overrides[db_settings.get_session] = get_test_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
async def s3_client():
    session = get_session()
    async with session.create_client(
            's3',
            endpoint_url=TEST_S3_ENDPOINT_URL,
            aws_access_key_id=TEST_S3_ACCESS_KEY,
            aws_secret_access_key=TEST_S3_SECRET_KEY
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def setup_s3(s3_client):
    try:
        await s3_client.create_bucket(Bucket=TEST_S3_BUCKET_NAME)
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        pass
    yield
    # код ниже - это типа, что необходимо выполнить, после выполнения тестов
    # (удалить все данные из тестового бакета)
    async for key in s3_client.list_objects_v2(Bucket=TEST_S3_BUCKET_NAME)['Contents']:
        await s3_client.delete_object(Bucket=TEST_S3_BUCKET_NAME, Key=key['Key'])
