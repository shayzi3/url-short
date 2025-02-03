from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import (
     ForeignKey,
     BigInteger,
)
from app.schemas import (
     UserModel, 
     UrlModel, 
)



class Base(AsyncAttrs, DeclarativeBase):
     ...


class User(Base):
     __tablename__ = "users"
     pydantic_model = UserModel
     
     username: Mapped[str] = mapped_column(primary_key=True, unique=True)
     password: Mapped[str] = mapped_column()
     phone: Mapped[int] = mapped_column(BigInteger)
     created_at: Mapped[datetime] = mapped_column(default=datetime.now())
     is_verifed: Mapped[bool] = mapped_column(default=False)
     is_banned: Mapped[bool] = mapped_column(default=False)
     api_key: Mapped[str] = mapped_column(nullable=True)
     urls: Mapped[list["Url"]] = relationship(back_populates="user", uselist=True, lazy="joined")
          


class Url(Base):
     __tablename__ = "urls"
     pydantic_model = UrlModel

     id: Mapped[str] = mapped_column(primary_key=True, unique=True)
     url: Mapped[str] = mapped_column()
     user_name: Mapped[str] = mapped_column(ForeignKey("users.username"))
     user: Mapped[User] = relationship(back_populates="urls", lazy="joined")