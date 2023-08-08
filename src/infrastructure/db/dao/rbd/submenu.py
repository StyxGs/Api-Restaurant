from uuid import UUID

from sqlalchemy import Delete, Update, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.common.congif.key_redis import keys
from src.core.models.dto.submenu import SubMenuDTO
from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models import Dish
from src.infrastructure.db.models.submenu import SubMenu


class SubMenuDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(SubMenu, session)

    async def get_list(self, menu_id: UUID) -> list:
        result = await self.session.execute(
            select(SubMenu.id, SubMenu.title, SubMenu.description, func.count(Dish.id)).outerjoin(
                SubMenu.dishes).filter(SubMenu.menu_id == menu_id).group_by(SubMenu.id))
        submenus = [
            SubMenuDTO(id=menu[0], title=menu[1], description=menu[2], dishes_count=menu[3]) for
            menu in result
        ]
        return submenus

    async def get_one(self, submenu_id: UUID, menu_id: UUID):
        result = await self.session.execute(
            select(SubMenu.id, SubMenu.title, SubMenu.description, func.count(Dish.id)).outerjoin(
                SubMenu.dishes).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).group_by(SubMenu.id))
        submenu = result.first()
        if submenu:
            return SubMenuDTO(id=submenu[0], title=submenu[1], description=submenu[2], dishes_count=submenu[3])
        else:
            return None

    @staticmethod
    async def get_id_dishes(submenu: SubMenu) -> list:
        return [keys['dish'] + str(dish_id.id) for dish_id in submenu.dishes]

    async def get_one_submenu(self, submenu_id: UUID, menu_id: UUID):
        """Получаем Подменю и все его блюда"""
        result = await self.session.scalars(
            select(SubMenu).options(joinedload(SubMenu.dishes)).filter(SubMenu.id == submenu_id,
                                                                       SubMenu.menu_id == menu_id))
        submenu = result.first()
        if submenu:
            return await self.get_id_dishes(submenu)
        else:
            return None

    async def update(self, data: dict, submenu_id: UUID, menu_id: UUID) -> int:
        result: Update = await self.session.execute(
            update(SubMenu).values(data).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        return result.rowcount

    async def delete(self, submenu_id: UUID, menu_id: UUID) -> int:
        result: Delete = await self.session.execute(
            delete(SubMenu).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))
        return result.rowcount
