from app.db.models import Url
from .service import ParentService
from app.schemas import UrlModel



class UrlService(ParentService[UrlModel]):
     model = Url