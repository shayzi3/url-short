from typing import Annotated
from fastapi import APIRouter, Security

from app.schemas import TokenPayloadModel
from app.core.security import access_security



api_key_router = APIRouter(prefix="/api/v1/key", tags=["API Key"])


@api_key_router.get(path="/")
async def get_api_key(
     current_user: Annotated[TokenPayloadModel, Security(access_security)]
) -> None:
     ...
     

@api_key_router.patch(path="/")
async def update_api_key() -> None:
     ...
     
     
@api_key_router.delete(path="/")
async def delete_api_key() -> None:
     ...