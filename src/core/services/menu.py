import json
from uuid import UUID

from src.core.models.dto.menu import MenuDTO
from src.core.services.errors import not_found
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import Menu


async def service_create_menu(dto: MenuDTO, dao: MenuDAO, redis: RedisDAO) -> MenuDTO:
    result: MenuDTO = await dao.create(dto.get_data_without_none, Menu)
    result.submenus_count = 0
    result.dishes_count = 0
    await redis.delete(redis.keys.get_keys(menus={'list_menus': 'list_menus'}))
    await dao.commit()
    return result


async def service_get_menus(dao: MenuDAO, redis: RedisDAO) -> list:
    key_menus: str = redis.keys.get_keys(menus={'list_menus': 'list_menus'})[0]
    if await redis.check_exist_key(key_menus):
        data: str = await redis.get(key_menus)
        menus = json.loads(data)
    else:
        menus = await dao.get_list()
        await redis.save(key_menus, json.dumps([menu.get_data for menu in menus]))
    return menus


async def service_get_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> MenuDTO | dict:
    key: str = redis.keys.get_keys(menus={'menus_id': [menu_id]})[0]
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
    await redis.delete(redis.keys.get_keys(menus={'menus_id': [menu_id], 'list_menus': 'list_menus'}))
    await dao.commit()
    menu: MenuDTO = await dao.get_one(menu_id)
    return menu


async def service_delete_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> dict:
    data_id: dict = await dao.get_one_menu(menu_id)
    result: int = await dao.delete(menu_id)
    await not_found(result, 'menu not found')
    await redis.delete(redis.keys.get_keys(menus={'menus_id': [menu_id], 'list_menus': 'list_menus'},
                                           submenus={'menus_id': [menu_id], 'submenus_id': data_id['submenus_id']},
                                           dishes={'submenus_id': data_id['submenus_id'],
                                                   'dishes_id': data_id['dishes_id']}))
    await dao.commit()
    return {'status': True, 'message': 'The menu has been deleted'}
