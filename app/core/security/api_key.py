import random

from typing import TYPE_CHECKING
from fastapi import Request, HTTPException, status
from string import ascii_letters, digits

from app.schemas import UserForApiKeyModel
from app.db.bases import UserRepository
from .password import check_password


if TYPE_CHECKING:
     from app.db.models import ApiKey


symbols = ascii_letters + digits


def generate_prefix() -> str:
     return "".join([random.choice(symbols) for _ in range(7)])


async def generate_api_key(prefix: str) -> str:
     return prefix + "".join([random.choice(symbols) for _ in range(40)])




class RequestAPIKey:
     
     def __init__(self, user_repository: UserRepository) -> None:
          self.user_repository = user_repository
          
          self.__error = HTTPException(
               detail="API KEY not valid!",
               status_code=status.HTTP_400_BAD_REQUEST
          )

     
     async def decode_api_key(self, key: str) -> UserForApiKeyModel:
          user: list[ApiKey, str, str] = await self.user_repository.read(
               "api_key", 
               "username",
               "prefix",
               "is_banned",
               "is_verifed",
               prefix=key[:7]
          )
          if user is None:
               raise self.__error
          
          check_token = await check_password(key, user[0].key)
          if check_token is True:
               return UserForApiKeyModel(
                    username=user[1],
                    prefix=user[2],
                    is_banned=[3],
                    is_verifed=user[4],
               )
          raise self.__error
     
     
     async def __call__(self, request: Request):
          key = request.headers.get("x-api-key")
          if key is None:
               raise self.__error
          return await self.decode_api_key(key)
               
               
request_api_key = RequestAPIKey(
     user_repository=UserRepository()
)
          