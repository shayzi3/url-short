from app.db.models import Url
from .repository import ParentRepository
from app.schemas import UrlModel



class UrlRepository(ParentRepository[UrlModel]):
     model = Url