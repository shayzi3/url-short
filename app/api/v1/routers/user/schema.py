from typing_extensions import Self
from pydantic import BaseModel, EmailStr

from app.core.security import sync_hashed_password



class SignUpModel(BaseModel):
     username: str
     password: str
     email: EmailStr
     
     
     def password_hashed(self) -> Self:
          self.password = sync_hashed_password(self.password)
          return self
     
     
class LogInModel(BaseModel):
     username: str
     password: str