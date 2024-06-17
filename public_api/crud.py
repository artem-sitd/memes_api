from fastapi import APIRouter

router = APIRouter()


@router.delete("/delete_memes/{id}")
def delete_memes_id(id: int):
    pass


@router.put("/put_memes/{id}")
def put_memes_id(id: int):
    pass


@router.get("/get_memes/{id}")
def get_memes_id(id: int):
    pass


@router.get("/get_memes")
def get_all_memes():
    pass


@router.post("/post_memes")
def create_memes():
    pass


@router.get("/")
def hello():
    return {"message": "Все работает"}
