from pydantic import BaseModel, EmailStr, field_validator
     
     
     
class Code(BaseModel):
     code: str
     
     @field_validator("code")
     @classmethod
     def code_validator(cls, code: str) -> str:
          if code.isdigit() is False:
               raise ValueError("Code must be a digit")
          
          if len(code) != 6:
               raise ValueError("Len code must be 6 symbols")
          return code