from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

from .config import settings

# URL для подключения к БД, берется из настроек проекта
DATABASE_URL = settings.db_url
# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL)
# Создание асинхронной сессии
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
