from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert


class BaseDAO:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: dict, model):
        result = await self.session.scalars(insert(model).values(data).returning(model))
        return result.first()

    async def commit(self):
        await self.session.commit()
