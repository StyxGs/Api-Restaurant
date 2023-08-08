from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, data: dict, model):
        result = await self.session.scalars(insert(model).values(data).returning(model))
        mdl = result.first()
        return mdl.to_dto()

    async def commit(self):
        await self.session.commit()
