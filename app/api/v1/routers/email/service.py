from fastapi import BackgroundTasks, status

from app.db.bases import UserService
from app.services.redis import RedisPool
from app.services.email import EmailSender
from app.schemas import ResponseModel
from .schema import Email




class EmailService:
     def __init__(
          self,
          user_service: UserService,
          email_sender: EmailSender,
          redis: RedisPool,
          
     ) -> None:
          self.user_service = user_service
          self.email_sender = email_sender
          self.redis = redis
          
     
     async def send_email(
          self, 
          email: Email, 
          username: str, 
          bg_task: BackgroundTasks
     ) -> ResponseModel:
          already_send = await self.email_sender.already_send(username)
          if already_send == 0:
               bg_task.add_task(
                    self.email_sender.send_verification_code, 
                    email_str=email.email, 
                    username=username
               )
               return ResponseModel(
                    message="Success",
                    status=status.HTTP_200_OK
               )
               
          return ResponseModel(
               message="You already send code! Wait 3 minute.",
               status=status.HTTP_408_REQUEST_TIMEOUT
          )
          
          
     async def check_email(self, code: str, username: str) -> tuple[bool, ResponseModel]:
          check_code = await self.email_sender.check_verfication_code(
               username=username,
               code=code
          )
          if check_code is True:
               await self.user_service.update(
                    where={"username": username},
                    is_verifed=True
               )
               return True, ResponseModel(message="Success", status=status.HTTP_200_OK)
          return False, ResponseModel(message="Invalid code!", status=status.HTTP_400_BAD_REQUEST)
          
          
async def get_email_service() -> EmailService:
     return EmailService(
          user_service=UserService(),
          email_sender=EmailSender(),
          redis=RedisPool()
     )