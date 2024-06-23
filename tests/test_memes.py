import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from sqlalchemy.ext.asyncio import async_session, async_sessionmaker, create_async_engine
import os
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


@pytest.mark.asyncio
async def test_all_routes():
    async_engine = create_async_engine(TEST_DATABASE_URL)
    async_session = async_sessionmaker()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "все работает"}
