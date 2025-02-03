from fastapi import FastAPI

from app.api.v1.routers import __v1_routers__




def include_routers(app: FastAPI) -> None:
     for v1_router in __v1_routers__:
          app.include_router(v1_router)
       
