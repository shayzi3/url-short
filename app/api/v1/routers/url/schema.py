from pydantic import BaseModel, HttpUrl


class UserSendUrl(BaseModel):
     url: HttpUrl
     
     
class ReturnUrl(BaseModel):
     url: str