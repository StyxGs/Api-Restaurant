from uuid import UUID

from sqlalchemy import delete, distinct, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api.models.responses import FullMenu
from src.core.models.dto.menu import MenuDTO
from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models import Dish, SubMenu
from src.infrastructure.db.models.menu import Menu


class MenuDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(Menu, session)

    async def get_full_menu(self) -> list[FullMenu]:
        result = await self.session.scalars(
            select(Menu).options(selectinload(Menu.submenus).selectinload(SubMenu.dishes)))
        return [FullMenu.model_validate(rt) for rt in result.all()]

    async def get_list(self) -> list[MenuDTO]:
        result = await self.session.execute(
            select(Menu.id, Menu.title, Menu.description, func.count(distinct(SubMenu.id)),
                   func.count(distinct(Dish.id))).outerjoin(
                Menu.submenus).outerjoin(
                SubMenu.dishes).group_by(Menu.id))
        menus: list = [
            MenuDTO(id=menu[0], title=menu[1], description=menu[2], submenus_count=menu[3], dishes_count=menu[4])
            for menu in result
        ]
        return menus

    async def get_one(self, menu_id: UUID) -> MenuDTO | None:
        result = await self.session.execute(
            select(Menu.id, Menu.title, Menu.description, func.count(distinct(SubMenu.id)),
                   func.count(distinct(Dish.id))).outerjoin(
                Menu.submenus).outerjoin(
                SubMenu.dishes).filter(Menu.id == menu_id).group_by(Menu.id, SubMenu.id))
        menu = result.first()
        if menu:
            return MenuDTO(id=menu[0], title=menu[1], description=menu[2], submenus_count=menu[3],
                           dishes_count=menu[4])
        else:
            return None

    @staticmethod
    async def get_id_submenus_and_dishes(menu: Menu) -> dict:
        all_id: dict = {'submenus_id': [], 'dishes_id': []}
        for submenu in menu.submenus:
            all_id['submenus_id'].append(str(submenu.id))
            for dish in submenu.dishes:
                all_id['dishes_id'].append(str(dish.id))
        return all_id

    async def get_one_menu(self, menu_id: UUID) -> dict | None:
        """Получаем Меню и все её подменю и блюда этих подменю."""
        result = await self.session.scalars(
            select(Menu).options(joinedload(Menu.submenus).joinedload(SubMenu.dishes)).filter(Menu.id == menu_id))
        menu = result.first()
        if menu:
            return await self.get_id_submenus_and_dishes(menu)
        else:
            return None

    async def update(self, data: dict, menu_id: UUID) -> None:
        await self.session.execute(update(Menu).values(data).filter(Menu.id == menu_id))

    async def delete(self, menu_id: UUID) -> None:
        await self.session.execute(delete(Menu).filter(Menu.id == menu_id))

    async def insert_or_update(self, data: list):
        stmt = insert(Menu).values(data)
        stmt_menu = stmt.on_conflict_do_update(index_elements=['id'],
                                               set_=dict(title=stmt.excluded.title,
                                                         description=stmt.excluded.description))
        await self.session.execute(stmt_menu)

    async def get_all_id(self) -> list[Menu]:
        result = await self.session.scalars(select(Menu.id))
        return result.all()

    async def delete_data_list(self, menus_id: list):
        await self.session.execute(delete(Menu).filter(Menu.id.in_(menus_id)))
