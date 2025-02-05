from typing import Annotated
from fastapi import APIRouter, Security, Depends

from app.api.dependencies.timeout import Timeout
from app.schemas import TokenPayloadModel, ResponseModel
from app.core.security import access_security
from .schema import APIKey
from .service import APIKeyService, get_api_key_service



api_key_router = APIRouter(prefix="/api/v1/key", tags=["API Key"])



@api_key_router.get(path="/", dependencies=[Depends(Timeout(minutes=5, route="get_key"))])
async def get_api_key(
     current_user: Annotated[TokenPayloadModel, Security(access_security)],
     service: Annotated[APIKeyService, Depends(get_api_key_service)]
) -> APIKey:
     return await service.get_api_key(current_user)
     


@api_key_router.patch(path="/", dependencies=[Depends(Timeout(minutes=5, route="patch_key"))])
async def update_api_key(
     current_user: Annotated[TokenPayloadModel, Security(access_security)],
     service: Annotated[APIKeyService, Depends(get_api_key_service)]
) -> APIKey:
     return await service.update_api_key(current_user)
     
 
     
@api_key_router.delete(path="/", dependencies=[Depends(Timeout(minutes=3, route="del_key"))])
async def delete_api_key(
     current_user: Annotated[TokenPayloadModel, Security(access_security)],
     service: Annotated[APIKeyService, Depends(get_api_key_service)]
) -> ResponseModel:
     return await service.delete_api_key(current_user)