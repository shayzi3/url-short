from datetime import datetime, timedelta
from typing import Sequence
from fastapi import (
     status, 
     FastAPI,
     Request,
     HTTPException,
)
from starlette.middleware.base import (
     BaseHTTPMiddleware, 
     RequestResponseEndpoint,
)
from .response import HTTPResponse
from app.core.security import access_security
          


class AccessMiddleware(BaseHTTPMiddleware):
     
     @staticmethod
     def filter_url(url: str, args: Sequence[str]) -> bool:
          for arg in args:
               if arg in url:
                    return True
          return False
     
     
     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
          fil = self.filter_url(str(request.url), ["key", "admin"])
          if fil is False:
               return await call_next(request)
          
          try:
               current_user = await access_security(request)
          except HTTPException as ex:
               return HTTPResponse(content=ex, status_code=status.HTTP_401_UNAUTHORIZED)
          
          if current_user.is_banned is True:
               return HTTPResponse(content="You banned", status_code=status.HTTP_403_FORBIDDEN)
               
          if current_user.is_verifed is False:
               return HTTPResponse(content="You not verifed", status_code=status.HTTP_403_FORBIDDEN)
          return await call_next(request)
     
     
     
class TimeoutMiddleware(BaseHTTPMiddleware):
     query = {}
     
     
     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
          client = request.client.host
          
          if client not in self.query.keys():
               self.query[client] = {
                    "exp": datetime.utcnow() + timedelta(seconds=2),
               }
               return await call_next(request)
          
          if datetime.utcnow() >= self.query[client]["exp"]:
               self.query[client]["exp"] = datetime.utcnow() + timedelta(seconds=3)
               return await call_next(request)
          
          return HTTPResponse(
               content="Request timeout. 3 seconds", 
               status_code=status.HTTP_408_REQUEST_TIMEOUT
          )
               
          
          

def include_middleware(app: FastAPI) -> None:
     __middlewares__ = [
          AccessMiddleware,
          TimeoutMiddleware,
     ]
     for middle in __middlewares__:
          app.add_middleware(middle)
     
     


