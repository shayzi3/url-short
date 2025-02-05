from app.db.models import User
from .repository import ParentRepository
from app.schemas import UserModel


class UserRepository(ParentRepository[UserModel]):
     model = User