from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import dao_provider
from src.api.models.requests import RQSTMenu
from src.api.models.responses import PyMenu
from src.core.services.menu import (service_create_menu, service_delete_menu,
                                    service_get_menu, service_get_menus,
                                    service_update_menu)
from src.infrastructure.db.dao.holder import HolderDAO


async def create_menu_router(menu: RQSTMenu, dao: HolderDAO = Depends(dao_provider)):
    return await service_create_menu(dto=menu.to_dto(), dao=dao.menu)


async def get_list_menus(dao: HolderDAO = Depends(dao_provider)):
    return await service_get_menus(dao=dao.menu)


async def get_specific_menu(menu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    return await service_get_menu(menu_id=menu_id, dao=dao.menu)


async def update_menu(menu: RQSTMenu, menu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    return await service_update_menu(dto=menu.to_dto(), menu_id=menu_id, dao=dao.menu)


async def delete_menu(menu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    return await service_delete_menu(menu_id=menu_id, dao=dao.menu)


def setup(router: APIRouter):
    router.add_api_route('/api/v1/menus', create_menu_router, response_model=PyMenu, methods=['POST'], status_code=201)
    router.add_api_route('/api/v1/menus', get_list_menus, response_model=list[PyMenu], methods=['GET'], status_code=200)
    router.add_api_route('/api/v1/menus/{menu_id}', get_specific_menu, response_model=PyMenu, methods=['GET'],
                         status_code=200)
    router.add_api_route('/api/v1/menus/{menu_id}', update_menu, response_model=PyMenu, methods=['PATCH'],
                         status_code=200)
    router.add_api_route('/api/v1/menus/{menu_id}', delete_menu, methods=['DELETE'], status_code=200)
