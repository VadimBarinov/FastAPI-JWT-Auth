from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from .config import settings


DATABASE_URL = settings.db_url
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
