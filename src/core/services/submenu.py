import json
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.common.congif.key_redis import keys
from src.core.models.dto.submenu import SubMenuDTO
from src.core.services.errors import not_found
from src.infrastructure.db.dao.rbd.submenu import SubMenuDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import SubMenu


async def service_create_submenu(menu_id: UUID, dto: SubMenuDTO, dao: SubMenuDAO, redis: RedisDAO) -> SubMenuDTO:
    try:
        data: dict = dto.get_data_without_none
        data['menu_id'] = menu_id
        result: SubMenuDTO = await dao.create(data, SubMenu)
        result.dishes_count = 0
        await redis.delete(keys['submenus'] + str(menu_id), keys['menus'], keys['menu'] + str(menu_id))
        await dao.commit()
        return result
    except IntegrityError:
        raise HTTPException(status_code=400, detail='already exists or not found')


async def service_get_submenus(menu_id: UUID, dao: SubMenuDAO, redis: RedisDAO) -> list:
    key: str = keys['submenus'] + str(menu_id)
    if await redis.check_exist_key(key):
        data: str = await redis.get(key)
        submenus = json.loads(data)
    else:
        submenus = await dao.get_list(menu_id)
        await redis.save(key, json.dumps([submenu.get_data for submenu in submenus]))
    return submenus


async def service_get_submenu(submenu_id: UUID, menu_id: UUID, dao: SubMenuDAO, redis: RedisDAO) -> SubMenuDTO | dict:
    key: str = keys['submenu'] + str(submenu_id)
    if await redis.check_exist_key(key):
        data: str = await redis.get(key)
        submenu = json.loads(data)
    else:
        submenu = await dao.get_one(submenu_id, menu_id)
        await not_found(submenu, 'submenu not found')
        await redis.save(key, json.dumps(submenu.get_data))
    return submenu


async def service_update_submenu(dto: SubMenuDTO, menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO,
                                 redis: RedisDAO) -> SubMenuDTO:
    result: int = await dao.update(dto.get_data_without_none, submenu_id, menu_id)
    await not_found(result, 'submenu not found')
    await redis.delete(keys['submenus'] + str(menu_id), keys['submenu'] + str(submenu_id))
    await dao.commit()
    submenu: SubMenuDTO = await dao.get_one(submenu_id, menu_id)
    return submenu


async def service_delete_submenu(menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO, redis: RedisDAO) -> dict:
    dishes_id: list = await dao.get_one_submenu(submenu_id, menu_id)
    result: int = await dao.delete(submenu_id, menu_id)
    await not_found(result, 'submenu not found')
    await dao.delete(submenu_id, menu_id)
    await redis.delete(*dishes_id, keys['submenus'] + str(menu_id), keys['submenu'] + str(submenu_id), keys['menus'],
                       keys['menu'] + str(menu_id), keys['dishes'] + str(submenu_id))
    await dao.commit()
    return {'status': True, 'message': 'The submenu has been deleted'}
