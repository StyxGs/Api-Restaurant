import pickle
from uuid import UUID

from src.core.models.dto.menu import MenuDTO
from src.core.services.errors import not_found
from src.core.utils import get_data
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import Menu


async def service_create_menu(dto: MenuDTO, dao: MenuDAO, redis: RedisDAO) -> MenuDTO:
    result: MenuDTO = await dao.create(dto.get_data_without_none, Menu)
    result.submenus_count = 0
    result.dishes_count = 0
    await redis.delete(redis.keys.get_keys(menus={'list_menus': 'list_menus', 'full_menus': 'full_menus'}))
    await dao.commit()
    return result


async def service_get_full_info_menus(dao: MenuDAO, redis: RedisDAO) -> list:
    key: str = redis.keys.get_keys(menus={'full_menus': 'full_menus'})[0]
    if await redis.check_exist_key(key):
        data = await redis.get(key)
        menus = pickle.loads(data)
    else:
        menus = await dao.get_full_menu()
        await redis.save(key, pickle.dumps(menus))
    return menus


async def service_get_menus(dao: MenuDAO, redis: RedisDAO) -> list:
    key: str = redis.keys.get_keys(menus={'list_menus': 'list_menus'})[0]
    return await get_data(dao=dao, redis=redis, key=key)


async def service_get_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> MenuDTO | dict:
    key: str = redis.keys.get_keys(menus={'menus_id': [menu_id]})[0]
    if await redis.check_exist_key(key):
        data = await redis.get(key)
        menu = pickle.loads(data)
    else:
        menu = await dao.get_one(menu_id)
        await not_found(menu, 'menu not found')
        await redis.save(key, pickle.dumps(menu))
    return menu


async def service_update_menu(dto: MenuDTO, menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> MenuDTO:
    result: int = await dao.update(dto.get_data_without_none, menu_id)
    await not_found(result, 'menu not found')
    await redis.delete(
        redis.keys.get_keys(menus={'menus_id': [menu_id], 'list_menus': 'list_menus', 'full_menus': 'full_menus'}))
    await dao.commit()
    menu: MenuDTO = await dao.get_one(menu_id)
    return menu


async def service_delete_menu(menu_id: UUID, dao: MenuDAO, redis: RedisDAO) -> dict:
    data_id: dict = await dao.get_one_menu(menu_id)
    result: int = await dao.delete(menu_id)
    await not_found(result, 'menu not found')
    await redis.delete(
        redis.keys.get_keys(menus={'menus_id': [menu_id], 'list_menus': 'list_menus', 'full_menus': 'full_menus'},
                            submenus={'menus_id': [menu_id], 'submenus_id': data_id['submenus_id']},
                            dishes={'submenus_id': data_id['submenus_id'],
                                    'dishes_id': data_id['dishes_id']}))
    await dao.commit()
    return {'status': True, 'message': 'The menu has been deleted'}
