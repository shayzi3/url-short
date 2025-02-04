from .service import ParentService
from app.schemas import ApiKeyModel
from app.db.models import ApiKey


class APIKeyService(ParentService[ApiKeyModel]):
     model = ApiKey