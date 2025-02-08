from typing import Union
from enum import Enum



Banned = Union["Ban", "Unban"]
Admin = Union["Take", "Give"] 


class EnumProtocol:
     message: str = "Success"
     error: str
     boolean: bool
     


class Ban(EnumProtocol):
     message = "User success banned"
     error = "User already banned"
     boolean = True
     
     
class Unban(EnumProtocol):
     message = "User success unbanned"
     error = "User already unbanned"
     boolean = False
     
     
     
class Take(EnumProtocol):
     error = "User already not admin"
     boolean = False
          
     
class Give(EnumProtocol):
     error = "User already admin"
     boolean = True




class BanUnban(Enum):
     BAN = "ban"
     UNBAN = "unban"
     
     @property
     def value_to_class(self) -> Banned:
          return Ban if self.value == "ban" else Unban
     
     
class TakeGive(Enum):
     TAKE = "take"
     GIVE = "give"
     
     
     @property
     def value_to_class(self) -> Admin:
          return Give if self.value == "give" else Take