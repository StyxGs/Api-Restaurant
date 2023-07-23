from uuid import UUID

from sqlalchemy.exc import IntegrityError

from src.core.models.dto.submenu import SubMenuDTO
from src.core.services.errors import not_found, exists
from src.infrastructure.db.dao.rbd.submenu import SubMenuDAO
from src.infrastructure.db.models import Menu


async def service_create_submenu(menu_id: UUID, dto: SubMenuDTO, dao: SubMenuDAO):
    try:
        data: dict = dto.get_data
        data['menu_id'] = menu_id
        result: Menu = await dao.create(data)
        await dao.commit()
        return result
    except IntegrityError:
        await exists()


async def service_get_submenus(menu_id: UUID, dao: SubMenuDAO):
    result: list[tuple] = await dao.get_list_submenus(menu_id)
    return [SubMenuDTO(id=menu[0], title=menu[1], description=menu[2], dishes_count=menu[3]) for
            menu in result]


async def service_get_submenu(submenu_id: UUID, menu_id: UUID, dao: SubMenuDAO):
    result: tuple = await dao.get_submenu(submenu_id, menu_id)
    await not_found(result, 'submenu not found')
    return SubMenuDTO(id=result[0], title=result[1], description=result[2], dishes_count=result[3])


async def service_update_submenu(dto: SubMenuDTO, menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO):
    result: tuple = await dao.update_submenu(dto.get_data, submenu_id, menu_id)
    await not_found(result, 'submenu not found')
    await dao.commit()
    menu: tuple = await dao.get_submenu(submenu_id, menu_id)
    return SubMenuDTO(id=menu[0], title=menu[1], description=menu[2], dishes_count=menu[3])


async def service_delete_submenu(menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO):
    result = await dao.delete_submenu(submenu_id, menu_id)
    await not_found(result, 'submenu not found')
    await dao.commit()
    return {"status": True, "message": "The submenu has been deleted"}
