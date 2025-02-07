import uvicorn

from fastapi import FastAPI, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.schemas import ResponseModel
from app.api.v1 import include_routers
from app.api.middlewares import include_middleware


template = Jinja2Templates(directory="app/templates")



app = FastAPI(
     title="URLShort",
     version="1.0.0"
)
include_routers(app)
include_middleware(app)


@app.get("/")
async def root() -> ResponseModel:
     return ResponseModel(message="Welcome to API!", status=status.HTTP_200_OK)


@app.get("/not_found", response_class=HTMLResponse)
async def not_found(request: Request):
     return template.TemplateResponse(
          request=request,
          name="index.html"
     )


if __name__ == "__main__":
     uvicorn.run("main:app", reload=True)