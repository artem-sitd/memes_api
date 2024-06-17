import uvicorn
from fastapi import FastAPI

from public_api.crud import router

app = FastAPI()

app.include_router(router)
if __name__ == "__main__":
    uvicorn.run(app, reload=True)
