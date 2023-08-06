from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import dao_provider
from src.api.models.requests import RQSTDish, RQSTDishUpdate
from src.api.models.responses import PyDish
from src.core.services.dish import (
    service_create_dish,
    service_delete_dish,
    service_get_dish,
    service_get_dishes,
    service_update_dish,
)
from src.infrastructure.db.dao.holder import HolderDAO


async def create_dish(menu_id: UUID, submenu_id: UUID, dish: RQSTDish, dao: HolderDAO = Depends(dao_provider)):
    """Создать блюдо."""
    return await service_create_dish(menu_id=menu_id, submenu_id=submenu_id, dto=dish.to_dto(), dao=dao.dish,
                                     redis=dao.redis)


async def get_list_dish(menu_id: UUID, submenu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    """Получить список всех блюд из определенного подменю."""
    return await service_get_dishes(menu_id=menu_id, submenu_id=submenu_id, dao=dao.dish, redis=dao.redis)


async def get_specific_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    """Получить блюдо по id."""
    return await service_get_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, dao=dao.dish,
                                  redis=dao.redis)


async def update_dish(menu_id: UUID, dish: RQSTDishUpdate, submenu_id: UUID, dish_id: UUID,
                      dao: HolderDAO = Depends(dao_provider)):
    """Обновить блюдо."""
    return await service_update_dish(dto=dish.to_dto(), menu_id=menu_id, submenu_id=submenu_id,
                                     dish_id=dish_id, dao=dao.dish, redis=dao.redis)


async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    """Удалить блюдо."""
    return await service_delete_dish(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, dao=dao.dish,
                                     redis=dao.redis)


def setup(router: APIRouter):
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}/dishes', create_dish, response_model=PyDish,
                         methods=['POST'], status_code=201, tags=['Dish'])
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}/dishes', get_list_dish, response_model=list[PyDish],
                         methods=['GET'],
                         status_code=200, tags=['Dish'])
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', get_specific_dish,
                         response_model=PyDish,
                         methods=['GET'],
                         status_code=200, tags=['Dish'])
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', update_dish, response_model=PyDish,
                         methods=['PATCH'],
                         status_code=200, tags=['Dish'])
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', delete_dish, methods=['DELETE'],
                         status_code=200,
                         tags=['Dish'])
