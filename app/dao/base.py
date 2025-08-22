from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text


class BaseDAO:
    table = None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, data_id):
        """Получение записи по ID"""
        query = text("""
            SELECT * FROM %s WHERE id = :data_id;
        """ % (cls.table, )).bindparams(data_id=data_id)
        result = await session.execute(query)

        return result.one_or_none()