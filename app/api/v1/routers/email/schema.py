from pydantic import BaseModel, EmailStr, field_validator


class Email(BaseModel):
     email: EmailStr
     
     
     @field_validator("email")
     @classmethod
     def email_validate(cls, email: str) -> str:
          if "@mail.ru" not in email:
               raise ValueError("Email must be from service MailRu")
          return email
     
     
     
class Code(BaseModel):
     code: str
     
     @field_validator("code")
     @classmethod
     def code_validator(cls, code: str) -> str:
          if code.isdigit() is False:
               raise ValueError("Code must be a digit")
          
          if len(code) > 6:
               raise ValueError("Len code must be 6 symbols")
          return code