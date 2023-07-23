from uuid import UUID

from sqlalchemy import Delete, Update, delete, distinct, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models import Dish, SubMenu
from src.infrastructure.db.models.menu import Menu


class MenuDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(Menu, session)

    async def create(self, data: dict):
        result = await self.session.scalars(insert(Menu).values(data).returning(Menu))
        return result.first()

    async def get_list(self):
        result = await self.session.execute(
            select(Menu.id, Menu.title, Menu.description, func.count(SubMenu.id), func.count(Dish.id)).outerjoin(
                Menu.submenu).outerjoin(
                SubMenu.dishes).group_by(Menu.id))
        return result.all()

    async def get_one(self, menu_id: UUID):
        result = await self.session.execute(
            select(Menu.id, Menu.title, Menu.description, func.count(distinct(SubMenu.id)), func.count(distinct(Dish.id))).outerjoin(
                Menu.submenu).outerjoin(
                SubMenu.dishes).filter(Menu.id == menu_id).group_by(Menu.id, SubMenu.id))
        return result.first()

    async def update(self, data: dict, menu_id: UUID):
        result: Update = await self.session.execute(update(Menu).values(data).filter(Menu.id == menu_id))
        return result.rowcount

    async def delete(self, menu_id: UUID):
        result: Delete = await self.session.execute(delete(Menu).filter(Menu.id == menu_id))
        return result.rowcount
