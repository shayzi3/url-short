import asyncio
import random
import smtplib

from string import digits
from email.mime.text import MIMEText

from app.core.config import settings
from app.services.redis import RedisPool



class EmailSender:
     redis = RedisPool()
     
     @property
     def get_text(self) -> str:
          code = "".join([random.choice(digits) for _ in range(6)])
          return f"Code: {code}", code
     
     
     async def already_send(self, username: str) -> int:
          """not exists in redis, return 0"""
          return await self.redis.exists(f"code:{username}")
     
     
     async def send_verification_code(self, email_str: str, username: str) -> None:
          text, code = self.get_text
          
          msg = MIMEText(text)
          msg["Subject"] = "Verification code"
          msg["From"] = settings.email
          msg["To"] = email_str

          try:
               with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
                    server.login(settings.email, settings.email_password)
                    server.sendmail(settings.email, email_str, msg.as_string())
                    
                    await self.redis.set(name=f"code:{username}", value=code, ex=180)
          except Exception as ex:
               print(ex)
               return
               
          
     async def check_verfication_code(self, username: str, code: str) -> bool:
          user_code = await self.redis.get(f"code:{username}")
          return user_code.decode() == code