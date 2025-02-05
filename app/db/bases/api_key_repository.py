from .repository import ParentRepository
from app.schemas import ApiKeyModel
from app.db.models import ApiKey


class APIKeyRepository(ParentRepository[ApiKeyModel]):
     model = ApiKey