from uuid import UUID

from src.core.models.dto.menu import MenuDTO
from src.core.services.errors import not_found
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.models import Menu


async def service_create_menu(dto: MenuDTO, dao: MenuDAO) -> Menu:
    result: Menu = await dao.create(dto.get_data, Menu)
    await dao.commit()
    return result


async def service_get_menus(dao: MenuDAO) -> list[MenuDTO]:
    result: list[tuple] = await dao.get_list()
    return [MenuDTO(id=menu[0], title=menu[1], description=menu[2], submenus_count=menu[3], dishes_count=menu[4])
            for menu in result]


async def service_get_menu(menu_id: UUID, dao: MenuDAO) -> MenuDTO:
    result: tuple = await dao.get_one(menu_id)
    await not_found(result, 'menu not found')
    return MenuDTO(id=result[0], title=result[1], description=result[2], submenus_count=result[3],
                   dishes_count=result[4])


async def service_update_menu(dto: MenuDTO, menu_id: UUID, dao: MenuDAO) -> MenuDTO:
    result: tuple = await dao.update(dto.get_data, menu_id)
    await not_found(result, 'menu not found')
    await dao.commit()
    menu: tuple = await dao.get_one(menu_id)
    return MenuDTO(id=menu[0], title=menu[1], description=menu[2], submenus_count=menu[3], dishes_count=menu[4])


async def service_delete_menu(menu_id: UUID, dao: MenuDAO) -> dict:
    result = await dao.delete(menu_id)
    await not_found(result, 'menu not found')
    await dao.commit()
    return {'status': True, 'message': 'The menu has been deleted'}
