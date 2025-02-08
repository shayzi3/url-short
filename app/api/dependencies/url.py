from typing import Union
from fastapi import Request, HTTPException, status

from app.schemas import TokenPayloadModel, UserForApiKeyModel
from app.core.security import access_security, request_api_key



Payload = Union[TokenPayloadModel, UserForApiKeyModel]


async def get_access_or_api(request: Request) -> Payload:
     access_token = request.cookies.get("access_token")
     api_key = request.headers.get("x-api-key")
     
     if access_token is not None:
          return await access_security.decode_token(access_token)
     
     elif api_key is not None:
          return await request_api_key.decode_api_key(api_key)
     
     else:
          raise HTTPException(
               detail="You must send request with JWT Token or API Key",
               status_code=status.HTTP_400_BAD_REQUEST
          )