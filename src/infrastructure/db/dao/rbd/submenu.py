from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models.dto.submenu import SubMenuDTO
from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models import Dish
from src.infrastructure.db.models.submenu import SubMenu


class SubMenuDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(SubMenu, session)

    async def get_list(self, menu_id: UUID) -> list[SubMenuDTO]:
        result = await self.session.execute(
            select(SubMenu.id, SubMenu.title, SubMenu.description, func.count(Dish.id)).outerjoin(
                SubMenu.dishes).filter(SubMenu.menu_id == menu_id).group_by(SubMenu.id))
        submenus = [
            SubMenuDTO(id=menu[0], title=menu[1], description=menu[2], dishes_count=menu[3]) for
            menu in result
        ]
        return submenus

    async def get_one(self, submenu_id: UUID, menu_id: UUID) -> SubMenuDTO | None:
        result = await self.session.execute(
            select(SubMenu.id, SubMenu.title, SubMenu.description, func.count(Dish.id)).outerjoin(
                SubMenu.dishes).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id).group_by(SubMenu.id))
        submenu = result.first()
        if submenu:
            return SubMenuDTO(id=submenu[0], title=submenu[1], description=submenu[2], dishes_count=submenu[3])
        else:
            return None

    async def get_all_dish_id(self, submenu_id: UUID, menu_id: UUID) -> list | None:
        """Получаем Все id блюд относящиеся к одному подменю."""
        result = await self.session.scalars(
            select(SubMenu).options(joinedload(SubMenu.dishes)).filter(SubMenu.id == submenu_id,
                                                                       SubMenu.menu_id == menu_id))
        submenu: SubMenu = result.first()
        if submenu:
            return [dish.id for dish in submenu.dishes]
        else:
            return None

    async def update(self, data: dict, submenu_id: UUID, menu_id: UUID) -> None:
        await self.session.execute(
            update(SubMenu).values(data).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))

    async def delete(self, submenu_id: UUID, menu_id: UUID) -> None:
        await self.session.execute(delete(SubMenu).filter(SubMenu.id == submenu_id, SubMenu.menu_id == menu_id))

    async def insert_or_update(self, data: list):
        stmt = insert(SubMenu).values(data)
        stmt_menu = stmt.on_conflict_do_update(index_elements=['id'],
                                               set_=dict(title=stmt.excluded.title,
                                                         description=stmt.excluded.description))
        await self.session.execute(stmt_menu)

    async def get_all_id(self) -> list:
        result = await self.session.scalars(select(SubMenu.id))
        return result.all()

    async def delete_data_list(self, submenus_id: list):
        await self.session.execute(delete(SubMenu).filter(SubMenu.id.in_(submenus_id)))
