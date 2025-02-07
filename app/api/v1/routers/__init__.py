from .user import user_router
from .email import email_router
from .api_key import api_key_router
from .url import url_router


__v1_routers__ = [
     user_router,
     email_router,
     api_key_router,
     url_router,
]