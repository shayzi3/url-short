from fastapi import HTTPException, status

from app.core.security import generate_api_key, hashed_password, generate_prefix
from app.schemas import TokenPayloadModel, ResponseModel
from app.db.bases import UserService
from .schema import APIKey




class APIKeyService:
     def __init__(
          self,
          user_service: UserService
     ) -> None:
          self.user_service = user_service
          
          
     async def get_api_key(self, current_user: TokenPayloadModel) -> APIKey:
          api_key, prefix = await self.user_service.read(
               "api_key",
               "prefix",
               username=current_user.username
          )
          if api_key is not None:
               raise HTTPException(
                    detail="APIKey already exists!",
                    status_code=status.HTTP_400_BAD_REQUEST
               )
          gen_api_key = await generate_api_key(prefix)
          key_to_db = await hashed_password(gen_api_key)
          
          await self.user_service.update(
               where=current_user.where,
               api_key=key_to_db
          )
          return APIKey(key=gen_api_key)
     
     
     async def update_api_key(self, current_user: TokenPayloadModel) -> APIKey:
          api_key = await self.user_service.read("api_key", username=current_user.username)
          if api_key[0] is None:
               raise HTTPException(
                    detail="API Key not found!",
                    status_code=status.HTTP_400_BAD_REQUEST
               )
          new_prefix = generate_prefix()
          new_api_key = await generate_api_key(new_prefix)
          key_to_db = await hashed_password(new_api_key)
          
          await self.user_service.update(
               where=current_user.where,
               api_key=key_to_db,
               prefix=new_prefix
          )
          return APIKey(key=new_api_key)
     
     
     async def delete_api_key(self, current_user: TokenPayloadModel) -> ResponseModel:
          api_key = await self.user_service.read("api_key", username=current_user.username)
          if api_key[0] is None:
               raise HTTPException(
                    detail="API Key not found!",
                    status_code=status.HTTP_400_BAD_REQUEST
               )
          await self.user_service.update(
               where=current_user.where,
               api_key=None
          )
          return ResponseModel(
               message="API Key success deleted.",
               status=status.HTTP_200_OK
          )
     
     
async def get_api_key_service() -> APIKeyService:
     return APIKeyService(user_service=UserService())