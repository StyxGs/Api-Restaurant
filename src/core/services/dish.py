import json
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.core.models.dto.dish import DishDTO
from src.core.services.errors import not_found
from src.infrastructure.db.dao.rbd.dish import DishDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import Dish


async def service_create_dish(menu_id: UUID, submenu_id: UUID, dto: DishDTO, dao: DishDAO, redis: RedisDAO) -> DishDTO:
    try:
        data: dict = dto.get_data_without_none
        data['submenu_id'] = submenu_id
        result: DishDTO = await dao.create(data, Dish)
        await redis.delete(redis.keys.get_keys(menus={'list_menus': 'list_menus', 'menus_id': [menu_id]},
                                               submenus={'menus_id': [menu_id], 'submenus_id': [submenu_id]},
                                               dishes={'submenus_id': [submenu_id]}))
        await dao.commit()
        return result
    except IntegrityError:
        raise HTTPException(status_code=400, detail='already exists or not found')


async def service_get_dishes(menu_id: UUID, submenu_id: UUID, dao: DishDAO, redis: RedisDAO) -> list:
    key: str = redis.keys.get_keys(dishes={'submenus_id': [submenu_id]})[0]
    if await redis.check_exist_key(key):
        data: str = await redis.get(key)
        dishes = json.loads(data)
    else:
        dishes = await dao.get_list(submenu_id)
        await redis.save(key, json.dumps([dish.get_data for dish in dishes]))
    return dishes


async def service_get_dish(submenu_id: UUID, menu_id: UUID, dish_id: UUID, dao: DishDAO,
                           redis: RedisDAO) -> DishDTO | dict:
    key: str = redis.keys.get_keys(dishes={'dishes_id': [dish_id]})[0]
    if await redis.check_exist_key(key):
        data: str = await redis.get(key)
        dish = json.loads(data)
    else:
        dish = await dao.get_one(submenu_id, dish_id)
        await not_found(dish, 'dish not found')
        await redis.save(key, json.dumps(dish.get_data))
    return dish


async def service_update_dish(dto: DishDTO, menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: DishDAO,
                              redis: RedisDAO) -> DishDTO:
    result: int = await dao.update(dto.get_data_without_none, submenu_id, dish_id)
    await not_found(result, 'dish not found')
    await redis.delete(redis.keys.get_keys(dishes={'submenus_id': [submenu_id], 'dishes_id': [dish_id]}))
    await dao.commit()
    dish: DishDTO = await dao.get_one(submenu_id, dish_id)
    return dish


async def service_delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: DishDAO, redis: RedisDAO) -> dict:
    result: int = await dao.delete(submenu_id, dish_id)
    await not_found(result, 'dish not found')
    await redis.delete(redis.keys.get_keys(menus={'menus_id': [menu_id], 'list_menus': 'list_menus'},
                                           submenus={'menus_id': [menu_id], 'submenus_id': [submenu_id]},
                                           dishes={'submenus_id': [submenu_id],
                                                   'dishes_id': [dish_id]}))
    await dao.commit()
    return {'status': True, 'message': 'The dish has been deleted'}
