import json
from uuid import UUID

from src.common.congif.key_redis import keys
from src.core.models.dto.menu import MenuDTO
from src.core.services.errors import not_found
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import Menu


async def service_create_menu(dto: MenuDTO, dao: MenuDAO, redis: RedisDAO) -> MenuDTO:
    result: MenuDTO = await dao.create(dto.get_data_without_none, Menu)
    result.submenus_count = 0
    result.dishes_count = 0
    await redis.delete(keys['menus'])
    await dao.commit()
    return result


async def service_get_menus(dao: MenuDAO, redis: RedisDAO) -> list:
    if await redis.check_exist_key(keys['menus']):
        data: str = await redis.get(keys['menus'])
        menus = json.loads(data)
    else:
        menus = await dao.get_list()
        await redis.save(keys['menus'], json.dumps([menu.get_data for menu in menus]))
    return menus


async def service_get_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> MenuDTO | dict:
    key: str = keys['menu'] + str(menu_id)
    if await redis.check_exist_key(key):
        data: str = await redis.get(key)
        menu = json.loads(data)
    else:
        menu = await dao.get_one(menu_id)
        await not_found(menu, 'menu not found')
        await redis.save(key, json.dumps(menu.get_data))
    return menu


async def service_update_menu(dto: MenuDTO, menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> MenuDTO:
    result: int = await dao.update(dto.get_data_without_none, menu_id)
    await not_found(result, 'menu not found')
    await redis.delete(keys['menus'], keys['menu'] + str(menu_id))
    await dao.commit()
    menu: MenuDTO = await dao.get_one(menu_id)
    return menu


async def service_delete_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> dict:
    data_id: dict = await dao.get_one_menu(menu_id)
    result: int = await dao.delete(menu_id)
    await not_found(result, 'menu not found')
    await redis.delete(*data_id['submenus'],
                       *data_id['dishes'], keys['menus'], keys['menu'] + str(menu_id), keys['submenus'] + str(menu_id))
    await dao.commit()
    return {'status': True, 'message': 'The menu has been deleted'}
