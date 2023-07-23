from uuid import UUID

from sqlalchemy import Delete, Update, delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models.dish import Dish


class DishDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(Dish, session)

    async def create(self, data: dict):
        result = await self.session.scalars(insert(Dish).values(data).returning(Dish))
        return result.first()

    async def get_list(self, submenu_id: UUID):
        result = await self.session.scalars(
            select(Dish).filter(Dish.submenu_id == submenu_id))
        return result.all()

    async def get_one(self, submenu_id: UUID, dish_id: UUID):
        result = await self.session.scalars(
            select(Dish).filter(Dish.submenu_id == submenu_id, Dish.id == dish_id))
        return result.first()

    async def update(self, data: dict, submenu_id: UUID, dish_id: UUID):
        result: Update = await self.session.execute(
            update(Dish).values(data).filter(Dish.id == dish_id, Dish.submenu_id == submenu_id))
        return result.rowcount

    async def delete(self, submenu_id: UUID, dish_id: UUID, ):
        result: Delete = await self.session.execute(
            delete(Dish).filter(Dish.id == dish_id, Dish.submenu_id == submenu_id))
        return result.rowcount
