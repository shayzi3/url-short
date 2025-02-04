from __future__ import annotations

import json

from typing_extensions import Self, Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Any
from pydantic import BaseModel, field_validator


if TYPE_CHECKING:
     from app.db.models import Url, User




class ResponseModel(BaseModel):
     message: str
     status: int
     
     
     
class UserModel(BaseModel):
     username: str
     is_verifed: bool
     is_banned: bool
     created_at: datetime
     urls: list[UrlForUserModel]
     
     @field_validator("urls")
     @classmethod
     def urls_validator(cls, urls: list[Url | None]) -> list[UrlForUserModel | None]:
          return [UrlForUserModel(**url_model.__dict__) for url_model in urls]
     
     
     def to_redis(self) -> str:
          self.created_at = self.created_at.timestamp()
          return json.dumps(self.__dict__)
     
     
     @classmethod
     def from_redis(cls, obj: str) -> Self:
          model = json.loads(obj)
          
          model["created_at"] = datetime.fromtimestamp(model["created_at"])
          return cls(**model)
     
     
     
class UrlModel(BaseModel):
     id: str
     url: str
     user: UserForUrlModel | None
     
     @field_validator("user")
     @classmethod
     def user_validator(cls, user: User) -> UserForUrlModel | None:
          if user is None:
               return None
          return UserForUrlModel(**user.__dict__)
     
     
     
class UserForUrlModel(BaseModel):
     username: str
     phone: int
     created_at: datetime
     
     
class UrlForUserModel(BaseModel):
     id: str
     url: str
     
     
     
class TokenModel(BaseModel):
     token: str
     type: str = "Bearer"
     
     def __str__(self) -> str:
          return self.token
     
     
     
class TokenPayloadModel(BaseModel):
     username: str
     is_banned: bool
     is_verifed: bool
     exp: datetime
     iat: datetime
     
     @property
     def verifed_is_true(self) -> dict[str, Any]:
          self.is_verifed = True
          return self.__dict__
     
     @property
     def redis_value(self) -> Sequence[str]:
          return [f"user:{self.username}"]
     
     @property
     def redis_str_value(self) -> str:
          return f"user:{self.username}"