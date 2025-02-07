from typing import Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request



class Timeout:
     users = {}
     
     def __init__(
          self,
          route: str,
          microseconds: float = 0,
          milliseconds: float = 0,
          seconds: float = 0,
          minutes: float = 0,
          hours: float = 0,
          days: float = 0,
          weeks: float = 0
     ) -> None:
          
          self.route = route
          self.microseconds = microseconds
          self.milliseconds = milliseconds
          self.seconds = seconds
          self.minutes = minutes
          self.hours = hours
          self.days = days
          self.weeks = weeks
          
          if self.route not in self.users.keys():
               self.users[self.route] = {}
                    
          
     @property
     def config(self) -> dict[str, Any]:
          kwargs = {}
          for key, value in self.__dict__.items():
               if (isinstance(value, int) is True) and (value != 0):
                    kwargs[key] = value
          return kwargs
     
          
     @property
     def detail(self) -> str:
          string = "Request timeout. Wait"
          for key, value in self.config.items():
               string += f" {value} {key}"
          return string
     
     
     def time(self) -> datetime:
          return datetime.utcnow() + timedelta(**self.config)
          
          
     async def __call__(self, request: Request) -> None:
          client = request.client.host
           
          if client not in self.users[self.route].keys():
               self.users[self.route][client] = self.time()
               return None
          
          if datetime.utcnow() > self.users[self.route][client]:
               self.users[self.route][client] = self.time()
               return None
          
          raise HTTPException(
               detail=self.detail,
               status_code=status.HTTP_408_REQUEST_TIMEOUT
          )