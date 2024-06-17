import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

env_file = Path(__file__).parent / ".env.docker" if os.getenv("USE_DOCKER") else Path(
    __file__).parent / ".env"


class DatabaseEnv(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding='utf-8')
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str


class DatabaseConnect(BaseSettings):
    db_env = DatabaseEnv()
    db_url = f"postgresql+asyncpg://{db_env.POSTGRES_USER}:{db_env.POSTGRES_PASSWORD}@{db_env.POSTGRES_HOST}/{db_env.POSTGRES_DB}"

    engine = create_async_engine(db_url, echo=True)
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session


class Settings(BaseSettings):
    pass


db_settings = DatabaseConnect()
