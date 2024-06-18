from contextlib import asynccontextmanager
from fastapi import UploadFile

from aiobotocore.session import get_session
from botocore.exceptions import ClientError


class BucketNotSpecifiedError(Exception):
    pass


class BucketAlreadyExistsError(Exception):
    pass


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str = None,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    # создать бакет
    async def create_bucket(self, bucket_name):
        try:
            async with self.get_client() as client:
                await client.create_bucket(Bucket=bucket_name)
                self.bucket_name = bucket_name
        except ClientError as e:
            raise ClientError

    # загрузить файл в S3
    async def upload_file(
            self,
            file: UploadFile,
    ):
        if not self.bucket_name:
            raise BucketNotSpecifiedError("Bucket is not exists")
        object_name = file.filename
        try:
            async with self.get_client() as client:
                file_content = await file.read()
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_content,
                )
                return f"{self.config['endpoint_url']}/{self.bucket_name}/{object_name}"
        except ClientError as e:
            raise ClientError

    # удалить файл
    async def delete_file(self, object_name: str):
        if not self.bucket_name:
            raise BucketNotSpecifiedError("Bucket is not exists")
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)

        except ClientError as e:
            raise ClientError

    # получить файл
    async def get_file(self, object_name: str, destination_path: str):
        if not self.bucket_name:
            raise BucketNotSpecifiedError("Bucket is not exists")
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
        except ClientError as e:
            raise ClientError
