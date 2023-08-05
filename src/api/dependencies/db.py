from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.db.dao.holder import HolderDAO


def dao_provider() -> HolderDAO:
    raise NotImplementedError


class DBProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession], redis):
        self.pool = pool
        self.redis = redis

    async def dao(self):
        async with self.pool() as session:
            yield HolderDAO(session=session, redis=self.redis)
