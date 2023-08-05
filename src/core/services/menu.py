import json
from uuid import UUID

from src.common.congif.key_redis import keys
from src.core.models.dto.menu import MenuDTO
from src.core.services.errors import not_found
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import Menu


async def service_create_menu(dto: MenuDTO, dao: MenuDAO, redis: RedisDAO) -> Menu:
    result: Menu = await dao.create(dto.get_data_without_none, Menu)
    await redis.delete(keys['menus'])
    await dao.commit()
    return result


async def service_get_menus(dao: MenuDAO, redis: RedisDAO) -> list:
    if await redis.check_exist_key(keys['menus']):
        data: str = await redis.get(keys['menus'])
        menus = json.loads(data)
    else:
        result: list[tuple] = await dao.get_list()
        menus = [
            MenuDTO(id=menu[0], title=menu[1], description=menu[2], submenus_count=menu[3], dishes_count=menu[4])
            for menu in result
        ]
        await redis.save(keys['menus'], json.dumps([menu.get_data for menu in menus]))
    return menus


async def service_get_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> MenuDTO | dict:
    key: str = keys['menu'] + str(menu_id)
    if await redis.check_exist_key(key):
        data: str = await redis.get(key)
        menu = json.loads(data)
    else:
        result: tuple = await dao.get_one(menu_id)
        await not_found(result, 'menu not found')
        menu = MenuDTO(id=result[0], title=result[1], description=result[2], submenus_count=result[3],
                       dishes_count=result[4])
        await redis.save(key, json.dumps(menu.get_data))
    return menu


async def service_update_menu(dto: MenuDTO, menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> MenuDTO:
    result: tuple = await dao.update(dto.get_data_without_none, menu_id)
    await not_found(result, 'menu not found')
    await redis.delete(keys['menus'], keys['menu'] + str(menu_id))
    await dao.commit()
    menu: tuple = await dao.get_one(menu_id)
    return MenuDTO(id=menu[0], title=menu[1], description=menu[2], submenus_count=menu[3], dishes_count=menu[4])


async def service_delete_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> dict:
    result = await dao.delete(menu_id)
    await not_found(result, 'menu not found')
    await redis.delete(keys['menus'], keys['menu'] + str(menu_id))
    await dao.commit()
    return {'status': True, 'message': 'The menu has been deleted'}
