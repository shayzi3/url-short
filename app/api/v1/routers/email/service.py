from fastapi import BackgroundTasks, status

from app.db.bases import UserService
from app.services.redis import RedisPool
from app.services.email import EmailSender
from app.schemas import ResponseModel, TokenPayloadModel


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
          current_user: TokenPayloadModel, 
          bg_task: BackgroundTasks
     ) -> ResponseModel:
          already_send = await self.email_sender.already_send(current_user.username)
          if already_send == 0:
               email = await self.user_service.read("email", username=current_user.username)
               bg_task.add_task(
                    self.email_sender.send_verification_code, 
                    email_str=email[0], 
                    username=current_user.username
               )
               return ResponseModel(
                    message="Success",
                    status=status.HTTP_200_OK
               )
               
          return ResponseModel(
               message="You already send code! Wait 3 minute.",
               status=status.HTTP_408_REQUEST_TIMEOUT
          )
          
          
     async def check_email(
          self, 
          code: str, 
          current_user: TokenPayloadModel
     ) -> tuple[bool, ResponseModel]:
          check_code = await self.email_sender.check_verfication_code(
               username=current_user.username,
               code=code
          )
          if check_code is True:
               await self.user_service.update(
                    where={"username": current_user.username},
                    redis_values=current_user.redis_value,
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