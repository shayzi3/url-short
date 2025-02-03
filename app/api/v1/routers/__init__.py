from .user import user_router
from .email import email_router


__v1_routers__ = [
     user_router,
     email_router,
]