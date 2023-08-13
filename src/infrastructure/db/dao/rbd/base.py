from uuid import UUID

from sqlalchemy import exists, select
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

    async def check_exists_value_in_db(self, model, model_id: UUID):
        result = await self.session.scalars(select(exists().where(model.id == model_id)))
        return result.first()

    async def commit(self):
        await self.session.commit()
