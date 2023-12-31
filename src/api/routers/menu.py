from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.dependencies import dao_provider
from src.api.models.requests import RQSTMenu, RQSTMenuUpdate
from src.api.models.responses import PyMenu
from src.core.services.menu import (
    service_create_menu,
    service_delete_menu,
    service_get_full_info_menus,
    service_get_menu,
    service_get_menus,
    service_update_menu,
)
from src.infrastructure.db.dao.holder import HolderDAO


async def create_menu(menu: RQSTMenu, bg: BackgroundTasks, dao: HolderDAO = Depends(dao_provider)):
    """Создать меню."""
    return await service_create_menu(dto=menu.to_dto(), dao=dao.menu, redis=dao.redis, bg=bg)


async def get_full_info_menus(dao: HolderDAO = Depends(dao_provider)):
    """Получить всю информацию о всех меню их подменю и блюда."""
    return await service_get_full_info_menus(dao=dao.menu, redis=dao.redis)


async def get_list_menus(dao: HolderDAO = Depends(dao_provider)):
    """Получить список всех меню."""
    return await service_get_menus(dao=dao.menu, redis=dao.redis)


async def get_specific_menu(menu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    """Получить меню по id."""
    return await service_get_menu(menu_id=menu_id, dao=dao.menu, redis=dao.redis)


async def update_menu(menu: RQSTMenuUpdate, bg: BackgroundTasks, menu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    """Обновить меню."""
    return await service_update_menu(dto=menu.to_dto(), menu_id=menu_id, dao=dao.menu, redis=dao.redis, bg=bg)


async def delete_menu(menu_id: UUID, bg: BackgroundTasks, dao: HolderDAO = Depends(dao_provider)):
    """Удалить меню."""
    return await service_delete_menu(menu_id=menu_id, dao=dao.menu, redis=dao.redis, bg=bg)


def setup(router: APIRouter):
    router.add_api_route('/menus', create_menu, response_model=PyMenu, methods=['POST'], status_code=201,
                         tags=['Menu'])
    router.add_api_route('/full-menu', get_full_info_menus, status_code=200, tags=['Menu'])
    router.add_api_route('/menus', get_list_menus, response_model=list[PyMenu], methods=['GET'], status_code=200,
                         tags=['Menu'])
    router.add_api_route('/menus/{menu_id}', get_specific_menu, response_model=PyMenu, methods=['GET'],
                         status_code=200, tags=['Menu'])
    router.add_api_route('/menus/{menu_id}', update_menu, response_model=PyMenu, methods=['PATCH'],
                         status_code=200, tags=['Menu'])
    router.add_api_route('/menus/{menu_id}', delete_menu, methods=['DELETE'], status_code=200, tags=['Menu'])
