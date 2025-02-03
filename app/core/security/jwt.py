import jwt

from fastapi import HTTPException, status, Request
from datetime import datetime, timedelta

from app.schemas import TokenModel, TokenPayloadModel
from app.core.config import settings




class AccessToken:
     
     def __init__(
          self,
          secret_key: str,
          alg: str
     ) -> None:
          self.secret_key = secret_key
          self.alg = alg
          
          self.__error = HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid token!"
          )
          
          
     async def create_token(self, **kwargs) -> TokenModel:
          payload = {
               "exp": datetime.utcnow() + timedelta(days=1),
               "iat": datetime.utcnow()
          }
          payload.update(kwargs)
          
          token = jwt.encode(
               payload=payload,
               key=self.secret_key,
               algorithm=self.alg
          )
          return TokenModel(token=token)
     
     
     async def decode_token(self, token: str) -> TokenPayloadModel:
          try:
               payload = jwt.decode(
                    jwt=token,
                    key=self.secret_key,
                    algorithms=self.alg
               )
          except Exception:
               raise self.__error
          return TokenPayloadModel(**payload)
               
               
     async def __call__(self, request: Request):
          # Get current user
          token = request.cookies.get("access_token")
          if token is None:
               raise self.__error
          return await self.decode_token(token)
     
     
access_security = AccessToken(
     secret_key=settings.jwt_secret,
     alg=settings.jwt_alg,
)