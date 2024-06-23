from pydantic import BaseModel, ConfigDict


class PostMemesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    src: str
    description: str


class BucketSchema(BaseModel):
    name: str
