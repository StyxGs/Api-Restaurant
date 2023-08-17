import pickle
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.exc import IntegrityError

from src.core.models.dto.dish import DishDTO
from src.core.utils import get_data
from src.infrastructure.db.dao.rbd.dish import DishDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO
from src.infrastructure.db.models import Dish


async def service_create_dish(menu_id: UUID | None, submenu_id: UUID | None, dto: DishDTO, dao: DishDAO,
                              redis: RedisDAO, bg: BackgroundTasks) -> DishDTO:
    try:
        data: dict = dto.get_data_without_none
        data['submenu_id'] = submenu_id
        result: DishDTO = await dao.create(data, Dish)
        bg.add_task(redis.delete,
                    redis.keys.get_keys(
                        menus={'list_menus': 'list_menus', 'menus_id': [menu_id], 'full_menus': 'full_menus'},
                        submenus={'menus_id': [menu_id], 'submenus_id': [submenu_id]},
                        dishes={'submenus_id': [submenu_id]}))
        await dao.commit()
        return result
    except IntegrityError:
        raise HTTPException(status_code=400, detail='already exists or not found')


async def service_get_dishes(menu_id: UUID, submenu_id: UUID, dao: DishDAO, redis: RedisDAO) -> list:
    key: str = redis.keys.get_keys(dishes={'submenus_id': [submenu_id]})[0]
    return await get_data(dao=dao, redis=redis, key=key, data_id=submenu_id)


async def service_get_dish(submenu_id: UUID, menu_id: UUID, dish_id: UUID, dao: DishDAO,
                           redis: RedisDAO) -> DishDTO | dict:
    key: str = redis.keys.get_keys(dishes={'dishes_id': [dish_id]})[0]
    if await redis.check_exist_key(key):
        data = await redis.get(key)
        dish = pickle.loads(data)
    else:
        dish: dict | None = await dao.get_one(submenu_id, dish_id)  # type: ignore
        if dish:
            await redis.save(key, pickle.dumps(dish))
        else:
            raise HTTPException(status_code=404, detail='dish not found')
    return dish


async def service_update_dish(dto: DishDTO, menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: DishDAO,
                              redis: RedisDAO, bg: BackgroundTasks) -> DishDTO:
    if await dao.check_exists_value_in_db(Dish, dish_id):
        await dao.update(dto.get_data_without_none, submenu_id, dish_id)
        bg.add_task(redis.delete, redis.keys.get_keys(dishes={'submenus_id': [submenu_id], 'dishes_id': [dish_id]},
                                                      menus={'full_menus': 'full_menus'}))
        await dao.commit()
        dish: DishDTO = await dao.get_one(submenu_id, dish_id)  # type: ignore
        return dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


async def service_delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: DishDAO, redis: RedisDAO,
                              bg: BackgroundTasks) -> dict:
    if await dao.check_exists_value_in_db(Dish, dish_id):
        await dao.delete(submenu_id, dish_id)
        bg.add_task(redis.delete,
                    redis.keys.get_keys(
                        menus={'menus_id': [menu_id], 'list_menus': 'list_menus', 'full_menus': 'full_menus'},
                        submenus={'menus_id': [menu_id], 'submenus_id': [submenu_id]},
                        dishes={'submenus_id': [submenu_id],
                                'dishes_id': [dish_id]}))
        await dao.commit()
        return {'status': True, 'message': 'The dish has been deleted'}
    else:
        raise HTTPException(status_code=404, detail='dish not found')
