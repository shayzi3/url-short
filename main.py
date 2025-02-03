import uvicorn

from fastapi import FastAPI, status

from app.schemas import ResponseModel
from app.api.v1 import include_routers
from app.api.middlewares import include_middleware


app = FastAPI(
     title="URLShort"
)
include_routers(app)
include_middleware(app)


@app.get("/")
async def root() -> ResponseModel:
     return ResponseModel(message="Welcome to API!", status=status.HTTP_200_OK)


if __name__ == "__main__":
     uvicorn.run("main:app", reload=True)