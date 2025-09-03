from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from dao.base import BaseDAO


class UserDAO(BaseDAO):
    table = "users"

    @classmethod
    async def get_user_by_username(cls, session: AsyncSession, username: str):
        query = text("""
            SELECT * FROM %s WHERE username = :username;
        """ % (cls.table, )).bindparams(username=username)
        result = await session.execute(query)

        return result.one_or_none()

    @classmethod
    async def get_user_by_username_and_email(cls, session: AsyncSession, username: str, email: EmailStr):
        query = text("""
                SELECT * FROM %s WHERE username = :username OR email = :email;
            """ % (cls.table,)).bindparams(username=username, email=email)
        result = await session.execute(query)

        return result.scalars().first()

    @classmethod
    async def add_user(cls, session: AsyncSession, username: str, email: EmailStr, password: str):
        query = text("""
            INSERT INTO %s (username, email, password) VALUES (:username, :email, :password) RETURNING id;
        """ % (cls.table, )).bindparams(username=username, email=email, password=password)
        result = await session.execute(query)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        return result.scalar()