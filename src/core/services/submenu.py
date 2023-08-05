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


async def service_create_submenu(menu_id: UUID, dto: SubMenuDTO, dao: SubMenuDAO, redis: RedisDAO) -> SubMenu:
    try:
        data: dict = dto.get_data_without_none
        data['menu_id'] = menu_id
        result: SubMenu = await dao.create(data, SubMenu)
        await redis.delete(keys['submenus'] + str(menu_id), keys['menus'])
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
        result: list[tuple] = await dao.get_list(menu_id)
        if all(not element for element in result[0]):
            return []
        else:
            submenus = [
                SubMenuDTO(id=menu[0], title=menu[1], description=menu[2], dishes_count=menu[3]) for
                menu in result
            ]
            await redis.save(key, json.dumps([submenu.get_data for submenu in submenus]))
    return submenus


async def service_get_submenu(submenu_id: UUID, menu_id: UUID, dao: SubMenuDAO, redis: RedisDAO) -> SubMenuDTO | dict:
    key: str = keys['submenu'] + str(submenu_id)
    if await redis.check_exist_key(key):
        data: str = await redis.get(key)
        submenu = json.loads(data)
    else:
        result: tuple = await dao.get_one(submenu_id, menu_id)
        await not_found(result, 'submenu not found')
        submenu = SubMenuDTO(id=result[0], title=result[1], description=result[2], dishes_count=result[3])
        await redis.save(key, json.dumps(submenu.get_data))
    return submenu


async def service_update_submenu(dto: SubMenuDTO, menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO,
                                 redis: RedisDAO) -> SubMenuDTO:
    result: tuple = await dao.update(dto.get_data_without_none, submenu_id, menu_id)
    await not_found(result, 'submenu not found')
    await redis.delete(keys['submenus'] + str(menu_id), keys['submenu'] + str(submenu_id))
    await dao.commit()
    submenu: tuple = await dao.get_one(submenu_id, menu_id)
    return SubMenuDTO(id=submenu[0], title=submenu[1], description=submenu[2], dishes_count=submenu[3])


async def service_delete_submenu(menu_id: UUID, submenu_id: UUID, dao: SubMenuDAO, redis: RedisDAO) -> dict:
    result = await dao.delete(submenu_id, menu_id)
    await not_found(result, 'submenu not found')
    await redis.delete(keys['submenus'] + str(menu_id), keys['submenu'] + str(submenu_id), keys['menus'],
                       keys['menu'] + str(menu_id))
    await dao.commit()
    return {'status': True, 'message': 'The submenu has been deleted'}
