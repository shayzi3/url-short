import random

from string import digits, ascii_letters
from pydantic import BaseModel, field_validator

from app.core.security import sync_hashed_password


class CreateAPIKey(BaseModel):
     key: str
     
     
     @field_validator("key")
     @classmethod
     def key_validator(cls, key: str) -> str:
          return sync_hashed_password(key)
     
     
     @staticmethod
     def create_key() -> str:
          symbols = digits + ascii_letters
          return "".join([random.choice(symbols) for _ in range(15)])