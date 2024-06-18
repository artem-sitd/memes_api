from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

env_file = Path(__file__).parent / ".env.docker" if os.getenv("USE_DOCKER") else Path(
    __file__).parent / ".env"


class S3clientSetting(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=env_file, env_file_encoding='utf-8')
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str


s3_env = S3clientSetting()

print(s3_env)
