from fastapi import HTTPException, status

from app.core.security import generate_api_key, hashed_password, generate_prefix
from app.schemas import TokenPayloadModel, ResponseModel
from app.db.bases import APIKeyService, UserService
from .schema import APIKey


class ApiKeyService:
     
     def __init__(
          self,
          api_service: APIKeyService,
          user_service: UserService
     ) -> None:
          self.user_service = user_service
          self.api_service = api_service
          
          
     async def get_api_key(self, current_user: TokenPayloadModel) -> APIKey:
          api_key = await self.api_service.read(user_name=current_user.username)
          if api_key is not None:
               raise HTTPException(
                    detail="API key already exists for this user.",
                    status_code=status.HTTP_400_BAD_REQUEST
               )
          prefix = await self.user_service.read(
               "prefix",
               username=current_user.username
          )
          gen_api_key = await generate_api_key(prefix[0])
          key_to_db = await hashed_password(gen_api_key)
          
          await self.api_service.create(
               user_name=current_user.username,
               key=key_to_db
          )
          return APIKey(key=gen_api_key)
          
          
     
     async def update_api_key(self, current_user: TokenPayloadModel) -> APIKey:
          api_key = await self.api_service.read(user_name=current_user.username)
          if api_key is None:
               raise HTTPException(
                    detail="API Key not found for this user!",
                    status_code=status.HTTP_400_BAD_REQUEST
               )
          new_prefix = generate_prefix()
          new_api_key = await generate_api_key(new_prefix)
          key_to_db = await hashed_password(new_api_key)
          
          await self.api_service.update(
               where=api_key.where,
               key=key_to_db
          )
          await self.user_service.update(
               where=current_user.where,
               prefix=new_prefix
          )
          return APIKey(key=new_api_key)
     
     
     async def delete_api_key(self, current_user: TokenPayloadModel) -> ResponseModel:
          api_key = await self.api_service.read(user_name=current_user.username)
          if api_key is None:
               raise HTTPException(
                    detail="API key not found for this user.",
                    status_code=status.HTTP_400_BAD_REQUEST
               )
          await self.api_service.delete(**api_key.where)
          return ResponseModel(
               message="API Key success deleted.",
               status=status.HTTP_200_OK
          )
     
     
async def get_api_key_service() -> APIKeyService:
     return ApiKeyService(
          api_service=APIKeyService(),
          user_service=UserService()
     )