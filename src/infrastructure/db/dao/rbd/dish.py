from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models.dish import Dish


class DishDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(Dish, session)

    async def get_list(self, submenu_id: UUID) -> list:
        result = await self.session.scalars(
            select(Dish).filter(Dish.submenu_id == submenu_id))
        dishes = result.all()
        return [dish.to_dto() for dish in dishes]

    async def get_one(self, submenu_id: UUID, dish_id: UUID):
        result = await self.session.scalars(
            select(Dish).filter(Dish.submenu_id == submenu_id, Dish.id == dish_id))
        dish = result.first()
        if dish:
            return dish.to_dto()
        else:
            return None

    async def update(self, data: dict, submenu_id: UUID, dish_id: UUID) -> None:
        await self.session.execute(update(Dish).values(data).filter(Dish.id == dish_id, Dish.submenu_id == submenu_id))

    async def delete(self, submenu_id: UUID, dish_id: UUID) -> None:
        await self.session.execute(delete(Dish).filter(Dish.id == dish_id, Dish.submenu_id == submenu_id))

    async def insert_or_update(self, data: list):
        stmt = insert(Dish).values(data)
        stmt_dish = stmt.on_conflict_do_update(index_elements=['id'],
                                               set_=dict(title=stmt.excluded.title,
                                                         description=stmt.excluded.description,
                                                         price=stmt.excluded.price))
        await self.session.execute(stmt_dish)

    async def get_all_id(self):
        result = await self.session.scalars(select(Dish.id))
        return result.all()

    async def delete_data_list(self, dishes_id: list):
        await self.session.execute(delete(Dish).filter(Dish.id.in_(dishes_id)))
