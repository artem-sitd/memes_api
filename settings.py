import os
from pathlib import Path
from typing import ClassVar
from media_api.s3connect import S3Client
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

env_file = Path(__file__).parent / ".env.docker" if os.getenv("USE_DOCKER") else Path(
    __file__).parent / ".env"


class DatabaseEnv(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=env_file, env_file_encoding='utf-8')
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str


class DatabaseConnect(BaseSettings):
    db_env: ClassVar[DatabaseEnv] = DatabaseEnv()
    db_url: ClassVar[
        str] = f"postgresql+asyncpg://{db_env.POSTGRES_USER}:{db_env.POSTGRES_PASSWORD}@{db_env.POSTGRES_HOST}/{db_env.POSTGRES_DB}"

    engine: ClassVar = create_async_engine(db_url)
    async_session: ClassVar = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False
                                                 )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session


class S3clientSetting(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=env_file, env_file_encoding='utf-8')
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str = None


s3_env = S3clientSetting()
s3_client = S3Client(access_key=s3_env.access_key,
                     secret_key=s3_env.secret_key,
                     endpoint_url=s3_env.endpoint_url,
                     bucket_name=s3_env.bucket_name
                     )
async def get_s3_client():
    return s3_client

db_settings = DatabaseConnect()
