from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker


async def get_async_session():
    """Получение асинхронной сессии"""
    async with async_session_maker() as session:
        yield session

AsyncSessionDep: type[AsyncSession] = Annotated[AsyncSession, Depends(get_async_session)]