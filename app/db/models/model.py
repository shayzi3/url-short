from datetime import datetime, timedelta
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import (
     ForeignKey,
)
from app.schemas import (
     UserModel, 
     UrlModel,
     ApiKeyModel,
)
from app.core.security import generate_prefix



class Base(AsyncAttrs, DeclarativeBase):
     ...


class User(Base):
     __tablename__ = "users"
     pydantic_model = UserModel
     
     username: Mapped[str] = mapped_column(primary_key=True, unique=True)
     password: Mapped[str] = mapped_column()
     email: Mapped[str] = mapped_column()
     created_at: Mapped[datetime] = mapped_column(default=datetime.now())
     is_verifed: Mapped[bool] = mapped_column(default=False)
     is_banned: Mapped[bool] = mapped_column(default=False)
     prefix: Mapped[str] = mapped_column(default=generate_prefix())
     
     urls: Mapped[list["Url"]] = relationship(back_populates="user", uselist=True, lazy="joined")
          


class Url(Base):
     __tablename__ = "urls"
     pydantic_model = UrlModel

     id: Mapped[str] = mapped_column(primary_key=True, unique=True)
     url: Mapped[str] = mapped_column()
     user_name: Mapped[str] = mapped_column(ForeignKey("users.username"))
     
     user: Mapped[User] = relationship(back_populates="urls", lazy="joined")
     
     
     
class ApiKey(Base):
     __tablename__ = "keys"
     pydantic_model = ApiKeyModel
     
     key: Mapped[str] = mapped_column(primary_key=True, unique=True)
     exp: Mapped[float] = mapped_column(default=(datetime.utcnow() + timedelta(weeks=1)).timestamp())
     user_name: Mapped[str] = mapped_column(ForeignKey("users.username"))