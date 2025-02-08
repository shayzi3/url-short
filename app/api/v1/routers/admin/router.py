from typing import Annotated
from fastapi import APIRouter, Depends, Security

from app.schemas.enums import BanUnban, TakeGive
from app.api.dependencies.admin import access_security_admin
from app.schemas import ResponseModel, TokenPayloadModel
from .service import AdminService, get_admin_service



admin_router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@admin_router.delete(path="/url")
async def admin_delete_url(
     url_id: str,
     service: Annotated[AdminService, Depends(get_admin_service)],
     _: Annotated[TokenPayloadModel, Security(access_security_admin)]
) -> ResponseModel:
     return await service.admin_delete_url(
          url_id=url_id
     )
     
     
@admin_router.delete(path="/key")
async def admin_delete_api_key(
     username: str,
     service: Annotated[AdminService, Depends(get_admin_service)],
     _: Annotated[TokenPayloadModel, Security(access_security_admin)]
) -> ResponseModel:
     return await service.admin_delete_api_key(
          username=username
     )
     
     
@admin_router.get(path="/ban")
async def admin_ban_user(
     username: str,
     mode: BanUnban,
     service: Annotated[AdminService, Depends(get_admin_service)],
     _: Annotated[TokenPayloadModel, Security(access_security_admin)]
) -> ResponseModel:
     return await service.admin_ban_user(
          username=username,
          mode=mode.value_to_class
     )
     
     
@admin_router.get(path="/")
async def admin_give(
     username: str,
     mode: TakeGive,
     service: Annotated[AdminService, Depends(get_admin_service)],
     _: Annotated[TokenPayloadModel, Security(access_security_admin)]
) -> ResponseModel:
     return await service.admin_give(
          username=username,
          mode=mode.value_to_class
     )
     
     
