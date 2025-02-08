from typing import Any, Callable, Awaitable
from functools import wraps
from fastapi import HTTPException, status

from app.schemas.enums import Banned, Admin
from app.db.models import ApiKey, Url
from app.schemas import ResponseModel, UserModel
from app.db.bases import UserRepository, UrlRepository, APIKeyRepository




class AdminService:
     def __init__(
          self,
          user_repository: UserRepository,
          url_repository: UrlRepository,
          api_key_repository: APIKeyRepository
     ) -> None:
          
          self.user_repository = user_repository
          self.url_repository = url_repository
          self.api_key_repository = api_key_repository
          
          
     @staticmethod
     def username_exists(model_return: bool = False) -> Callable:
          def decorator(func: Awaitable) -> Awaitable:
               
               @wraps(func)
               async def wrapper(self, username: str, *args, **kwargs) -> Any:
                    username_exists: UserModel | None = await self.user_repository.read(username=username)
                    if username_exists is None:
                         raise HTTPException(
                              detail="Username not found",
                              status_code=status.HTTP_404_NOT_FOUND
                         )
                         
                    if model_return is False:
                         return await func(self, username, *args, **kwargs)
                    return await func(self, username_exists, *args, **kwargs)
               return wrapper
          return decorator
               
          
          
     async def admin_delete_url(self, url_id: str) -> ResponseModel:
          status_delete = await self.url_repository.delete(
               redis_values=[f"url:{url_id}"],
               returning=[Url.url],
               id=url_id
          )
          if status_delete == "not_found":
               raise HTTPException(
                    detail="URL not found",
                    status_code=status.HTTP_404_NOT_FOUND
               )
          
          return ResponseModel(
               message="Deleted success",
               status=status.HTTP_200_OK
          )
          
          
     @username_exists()
     async def admin_delete_api_key(self, username: str) -> ResponseModel:
          status_delete = await self.api_key_repository.delete(
               returning=[ApiKey.user_name],
               user_name=username
          )
          if status_delete == "not_found":
               raise HTTPException(
                    detail=f"API key at user {username} not found",
                    status_code=status.HTTP_404_NOT_FOUND
               )
          return ResponseModel(
               message="Deleted success",
               status=status.HTTP_200_OK
          )
     
     
     @username_exists(model_return=True)
     async def admin_ban_user(self, user: UserModel, mode: Banned) -> ResponseModel:
          if user.is_banned is mode.boolean:
               raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=mode.error
               )
          await self.user_repository.update(
               where=user.where,
               redis_values=user.redis_values,
               is_banned=mode.boolean
          )
          return ResponseModel(
               message=mode.message,
               status=status.HTTP_200_OK
          )
          
     
     @username_exists(model_return=True)
     async def admin_give(self, user: UserModel, mode: Admin) -> ResponseModel:
          if user.is_admin is mode.boolean:
               raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=mode.error
               )
          await self.user_repository.update(
               where=user.where,
               redis_values=user.redis_values,
               is_admin=mode.boolean
          )
          return ResponseModel(
               message=mode.message,
               status=status.HTTP_200_OK
          )
          

async def get_admin_service() -> AdminService:
     return AdminService(
          user_repository=UserRepository(),
          url_repository=UrlRepository(),
          api_key_repository=APIKeyRepository()
     )