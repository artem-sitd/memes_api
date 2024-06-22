import os
import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from media_api.s3connect import S3Client
from settings import db_settings
from main import app
from public_api.models import Base
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

# Настройка базы данных
test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    def get_test_db():
        yield db_session

    app.dependency_overrides[db_settings.get_session] = get_test_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# бакет надо создать заранее
@pytest.fixture(scope="session")
async def s3_client_test():
    s3 = S3Client(
        access_key=TEST_S3_ACCESS_KEY,
        secret_key=TEST_S3_SECRET_KEY,
        endpoint_url=TEST_S3_ENDPOINT_URL,
        bucket_name=TEST_S3_BUCKET_NAME
    )
    async with s3.get_client() as client:
        yield client
