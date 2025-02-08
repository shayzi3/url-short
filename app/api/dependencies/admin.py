from fastapi import Request, HTTPException, status

from app.core.security import access_security
from app.schemas import TokenPayloadModel



async def access_security_admin(request: Request) -> TokenPayloadModel:
     token = request.cookies.get("access_token")
     if token is None:
          raise HTTPException(
               detail="Invalid token!",
               status_code=status.HTTP_401_UNAUTHORIZED
          )
     
     decode_token = await access_security.decode_token(token)
     if decode_token.is_admin is False:
          raise HTTPException(
               detail="You not admin!",
               status_code=status.HTTP_400_BAD_REQUEST
          )
     return decode_token
     