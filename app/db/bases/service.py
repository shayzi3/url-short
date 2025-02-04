from typing import Any, TypeVar, Generic, Union, Sequence
from abc import ABC, abstractmethod
from sqlalchemy import select, update, delete, insert

from app.db.models import User, Url
from app.db.session import Session
from app.services.redis import RedisPool



PYDANTIC_MODEL = TypeVar("PYDANTIC_MODEL")
ORM_MODELS = Union[User, Url, None]



class Service(ABC, Generic[PYDANTIC_MODEL]):
     
     @abstractmethod
     async def read(
          self, 
          *values, 
          **extras
     ) -> PYDANTIC_MODEL:
          raise NotImplementedError
     
     
     @abstractmethod
     async def create(
          self, 
          *args, 
          **extras
     ) -> None:
          raise NotImplementedError
     
     
     @abstractmethod
     async def update(
          self, 
          where: dict[str, Any], 
          redis_values: Sequence[str] = [],
          **extras
     ) -> None:
          raise NotImplementedError
     
     
     @abstractmethod
     async def delete(
          self, 
          redis_values: Sequence[str] = [],
          **where
     ) -> None:
          raise NotImplementedError
     
     

class ParentService(Service, Generic[PYDANTIC_MODEL], Session):
     model: ORM_MODELS = None
     
     
     async def read(
          self, 
          *values, 
          **extras
     ) -> PYDANTIC_MODEL | None | list[Any]:
          async with self.session() as session:
               sttm = select(self.model).filter_by(**extras)
               result = await session.execute(sttm)
               out = result.scalar()
               
               if out is None:
                    return None
               
               if values:
                    return [out.__dict__.get(key) for key in values]
               return out.pydantic_model(**out.__dict__)
               
          
     async def create(
          self, 
          *args, 
          **extras
     ) -> None:
          async with self.session.begin() as session:
               if args:
                    extras = args[0].__dict__ # Pydantic model
               sttm = insert(self.model).values(**extras)
               await session.execute(sttm)
          
          
          
     async def update(
          self, 
          where: dict[str, Any], 
          redis_values: Sequence[str] = [], 
          **extras
     ) -> None:
          async with self.session.begin() as session:
               sttm = update(self.model).filter_by(**where).values(**extras)
               await session.execute(sttm)
               await RedisPool().delete(*redis_values)
          
          
     async def delete(
          self, 
          redis_values: Sequence[str] = [],
          **where
     ) -> None:
          async with self.session.begin() as session:
               sttm = delete(self.model).filter_by(**where)
               await session.exevute(sttm)
               await RedisPool().delete(*redis_values)
               
     