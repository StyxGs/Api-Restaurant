from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.db.dao.holder import HolderDAO


def dao_provider() -> HolderDAO:
    raise NotImplementedError


class DBProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def dao(self):
        async with self.pool() as session:
            yield HolderDAO(session=session)
