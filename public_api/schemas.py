from pydantic import BaseModel


class PostMemesSchema(BaseModel):
    id: int
    src: str
    description: str
