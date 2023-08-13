import pickle
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.exc import IntegrityError

from src.core.models.dto.submenu import SubMenuDTO
from src.core.utils import get_data
from src.infrastructure.db.dao.rbd.submenu import SubMenuDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import SubMenu


async def service_create_submenu(menu_id: UUID | None, dto: SubMenuDTO, dao: SubMenuDAO, redis: RedisDAO,
                                 bg: BackgroundTasks) -> SubMenuDTO:
    try:
        data: dict = dto.get_data_without_none
        data['menu_id'] = menu_id
        result: SubMenuDTO = await dao.create(data, SubMenu)
        result.dishes_count = 0
        bg.add_task(redis.delete, redis.keys.get_keys(submenus={'menus_id': [menu_id]},
                                                      menus={'list_menus': 'list_menus', 'menus_id': [menu_id],
                                                             'full_menus': 'full_menus'}))
        await dao.commit()
        return result
    except IntegrityError:
        raise HTTPException(status_code=400, detail='already exists or not found')


async def service_get_submenus(menu_id: UUID, dao: SubMenuDAO, redis: RedisDAO) -> list:
    key: str = redis.keys.get_keys(submenus={'menus_id': [menu_id]})[0]
    return await get_data(dao=dao, redis=redis, key=key, data_id=menu_id)


async def service_get_submenu(submenu_id: UUID, menu_id: UUID, dao: SubMenuDAO, redis: RedisDAO) -> SubMenuDTO | dict:
    key: str = redis.keys.get_keys(submenus={'submenus_id': [submenu_id]})[0]
    if await redis.check_exist_key(key):
        data = await redis.get(key)
        submenu = pickle.loads(data)
    else:
        submenu = await dao.get_one(submenu_id, menu_id)
        if submenu:
            await redis.save(key, pickle.dumps(submenu))
        else:
            raise HTTPException(status_code=404, detail='submenu not found')
    return submenu


async def service_update_submenu(dto: SubMenuDTO, menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO,
                                 redis: RedisDAO, bg: BackgroundTasks) -> SubMenuDTO:
    if await dao.check_exists_value_in_db(SubMenu, submenu_id):
        await dao.update(dto.get_data_without_none, submenu_id, menu_id)
        bg.add_task(redis.delete, redis.keys.get_keys(submenus={'submenus_id': [submenu_id], 'menus_id': [menu_id]},
                                                      menus={'full_menus': 'full_menus'}))
        await dao.commit()
        submenu: SubMenuDTO = await dao.get_one(submenu_id, menu_id)
        return submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


async def service_delete_submenu(menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO, redis: RedisDAO, bg: BackgroundTasks) -> dict:
    if await dao.check_exists_value_in_db(SubMenu, submenu_id):
        dishes_id: list = await dao.get_all_dish_id(submenu_id, menu_id)
        await dao.delete(submenu_id, menu_id)
        bg.add_task(redis.delete,
                    redis.keys.get_keys(
                        menus={'menus_id': [menu_id], 'list_menus': 'list_menus', 'full_menus': 'full_menus'},
                        submenus={'menus_id': [menu_id], 'submenus_id': [submenu_id]},
                        dishes={'submenus_id': [submenu_id],
                                'dishes_id': dishes_id}))
        await dao.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='submenu not found')
