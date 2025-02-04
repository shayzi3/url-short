from typing import Annotated
from fastapi import APIRouter, Depends, Response, Security

from app.core.security import access_security
from app.schemas import TokenModel, TokenPayloadModel, UserModel
from .schema import SignUpModel, LogInModel
from .service import get_auth_service, AuthService



user_router = APIRouter(prefix="/api/v1/user", tags=["User"])


@user_router.post("/signup/")
async def signup(
     register_data: SignUpModel,
     service: Annotated[AuthService, Depends(get_auth_service)],
     response: Response
) -> TokenModel:
     token = await service.signup(
          data=register_data
     )
     response.set_cookie(
          key="access_token",
          value=token.token,
          secure=True
     )
     return token
     
     
     
@user_router.post("/login/")
async def login(
     login_data: LogInModel,
     service: Annotated[AuthService, Depends(get_auth_service)],
     response: Response
) -> TokenModel:
     token = await service.login(
          data=login_data
     )
     response.set_cookie(
          key="access_token",
          value=token.token,
          secure=True
     )
     return token



@user_router.get("/")
async def get_user(
     current_user: Annotated[TokenPayloadModel, Security(access_security)],
     service: Annotated[AuthService, Depends(get_auth_service)],
     username: str | None = None
) -> UserModel:
     return await service.get_user(
          name=username, 
          current_user=current_user
     )