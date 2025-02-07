from fastapi import status, HTTPException

from app.api.dependencies.url import Payload
from app.core.security import generate_prefix
from app.db.bases import UrlRepository
from app.services.redis import RedisPool
from .schema import ReturnUrl



class UrlService:
     
     def __init__(
          self,
          url_repository: UrlRepository,
          redis: RedisPool
     ) -> None:
          
          self.url_repository = url_repository
          self.redis = redis
          
          
     async def get_short_url(self, current_user: Payload, url: str) -> ReturnUrl:
          url_exists = await self.url_repository.read(url=url)
          if url_exists is not None:
               raise HTTPException(
                    detail="This url already exists",
                    status_code=status.HTTP_400_BAD_REQUEST
               )
               
          url_id = generate_prefix()
          await self.url_repository.create(
               id=url_id,
               url=url,
               user_name=current_user.username
          )
          redirect_url = "http://127.0.0.1:8000/url/" + url_id
          return ReturnUrl(url=redirect_url)
          
          
          
     async def get_url_by_id(self, id: str) -> str:
          url_redis = await self.redis.get(f"url:{id}")
          if url_redis is not None:
               return url_redis.decode()
          
          url_exists = await self.url_repository.read(id=id)
          if url_exists is None:
               return "http://127.0.0.1:8000/not_found"
          
          await self.redis.set(
               name=f"url:{id}",
               value=url_exists.url,
               ex=1000
          )
          return url_exists.url
     
     
          
async def get_url_service() -> UrlService:
     return UrlService(
          url_repository=UrlRepository(),
          redis=RedisPool()
     )