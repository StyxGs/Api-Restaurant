from uuid import UUID

from sqlalchemy import Delete, Update, delete, distinct, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models import Dish, Menu
from src.infrastructure.db.models.submenu import SubMenu


class SubMenuDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(SubMenu, session)

    async def create(self, data: dict):
        result = await self.session.scalars(insert(SubMenu).values(data).returning(SubMenu))
        return result.first()

    async def get_list(self, menu_id: UUID):
        result = await self.session.execute(
            select(SubMenu.id, SubMenu.title, SubMenu.description, func.count(Dish.id)).outerjoin(
                Menu.submenu).outerjoin(
                SubMenu.dishes).filter(Menu.id == menu_id).group_by(SubMenu.id, Menu.id))
        return result.all()

    async def get_one(self, submenu_id: UUID, menu_id: UUID):
        result = await self.session.execute(
            select(SubMenu.id, SubMenu.title, SubMenu.description, func.count(distinct(Dish.id))).outerjoin(
                SubMenu.dishes).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).group_by(SubMenu.id,
                                                                                                      Dish.id))
        return result.first()

    async def update(self, data: dict, submenu_id: UUID, menu_id: UUID):
        result: Update = await self.session.execute(
            update(SubMenu).values(data).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        return result.rowcount

    async def delete(self, submenu_id: UUID, menu_id: UUID):
        result: Delete = await self.session.execute(
            delete(SubMenu).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        return result.rowcount
