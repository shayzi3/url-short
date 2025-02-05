from fastapi import HTTPException, status

from app.schemas import TokenModel, UserModel, TokenPayloadModel
from app.db.bases import UserRepository
from app.core.security import access_security
from app.core.security import check_password
from app.services.redis import RedisPool
from .schema import SignUpModel, LogInModel




class AuthService:
     def __init__(self, user_service: UserRepository, redis: RedisPool):
          self.user_service = user_service
          self.redis = redis
          
          self.__login_error = HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail="Invalid email or password!"
          )
          
          
     async def signup(self, data: SignUpModel) -> TokenModel:
          user = await self.user_service.read(username=data.username)
          if user is not None:
               raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="User already exists"
               )
          await self.user_service.create(data.password_hashed())
          
          token = await access_security.create_token(
               username=data.username,
               is_banned=False,
               is_verifed=False
          )
          return token
     
     
     async def login(self, data: LogInModel) -> TokenModel:
          user = await self.user_service.read(
               "password",
               "is_banned",
               "is_verifed",
               username=data.username
          ) # read return list[password_user, is_banned, is_verifed]
          if user is None:
               raise self.__login_error
          
          true_psw = await check_password(
               password=data.password, 
               old_password=user[0]
          )
          if true_psw is False:
               raise self.__login_error
          
          token = await access_security.create_token(
               username=data.username,
               is_banned=user[1],
               is_verifed=user[2]
          )
          return token
     
     
     async def get_user(self, name: str | None, current_user: TokenPayloadModel) -> UserModel:
          if name is None:
               name = current_user.username
               
          from_redis = await self.redis.get(f"user:{name}")
          if from_redis is not None:
               return UserModel.from_redis(from_redis)
          
          user = await self.user_service.read(username=name)
          if user is None:
               raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not exists"
               )
              
          await self.redis.set(
               name=f"user:{name}",
               value=user.copy().to_redis(),
               ex=250
          ) 
          return user
          
         
          
async def get_auth_service() -> AuthService:
     return AuthService(
          user_service=UserRepository(),
          redis=RedisPool()
     )