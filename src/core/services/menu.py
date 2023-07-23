from uuid import UUID

from src.core.models.dto.menu import MenuDTO
from src.core.services.errors import not_found
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.models import Menu


async def service_create_menu(dto: MenuDTO, dao: MenuDAO):
    result: Menu = await dao.create(data=dto.get_data)
    await dao.commit()
    return result


async def service_get_menus(dao: MenuDAO):
    result: list[tuple] = await dao.get_list_menus()
    return result


async def service_get_menu(menu_id: UUID, dao: MenuDAO):
    result: tuple = await dao.get_menu(menu_id)
    await not_found(result, 'menu not found')
    return result


async def service_update_menu(dto: MenuDTO, menu_id: UUID, dao: MenuDAO):
    result: tuple = await dao.update_menu(dto.get_data, menu_id)
    await not_found(result, 'menu not found')
    await dao.commit()
    menu: tuple = await dao.get_menu(menu_id)
    return menu


async def service_delete_menu(menu_id: UUID, dao: MenuDAO):
    result = await dao.delete_menu(menu_id)
    await not_found(result, 'menu not found')
    await dao.commit()
    return {"status": True, "message": "The menu has been deleted"}
