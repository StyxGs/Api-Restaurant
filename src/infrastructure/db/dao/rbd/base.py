from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, model, session: AsyncSession):
        self.model = model
        self.session = session

    async def commit(self):
        await self.session.commit()
