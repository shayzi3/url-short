from app.db.models import User
from .service import ParentService
from app.schemas import UserModel


class UserService(ParentService[UserModel]):
     model = User