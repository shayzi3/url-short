from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings



class Session:
     engine = create_async_engine(settings.postgres, echo=True)
     session = async_sessionmaker(engine)