from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import dao_provider
from src.api.models.requests import RQSTSubMenu, RQSTSubMenuUpdate
from src.api.models.responses import PySubMenu
from src.core.services.submenu import (
    service_create_submenu,
    service_delete_submenu,
    service_get_submenu,
    service_get_submenus,
    service_update_submenu,
)
from src.infrastructure.db.dao.holder import HolderDAO


async def create_submenu(menu_id: UUID, submenu: RQSTSubMenu, dao: HolderDAO = Depends(dao_provider)):
    return await service_create_submenu(menu_id=menu_id, dto=submenu.to_dto(), dao=dao.submenu, redis=dao.redis)


async def get_list_submenus(menu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    return await service_get_submenus(menu_id=menu_id, dao=dao.submenu, redis=dao.redis)


async def get_specific_submenu(menu_id: UUID, submenu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    return await service_get_submenu(submenu_id=submenu_id, menu_id=menu_id, dao=dao.submenu, redis=dao.redis)


async def update_submenu(menu_id: UUID, submenu: RQSTSubMenuUpdate, submenu_id: UUID,
                         dao: HolderDAO = Depends(dao_provider)):
    return await service_update_submenu(dto=submenu.to_dto(), submenu_id=submenu_id, menu_id=menu_id, dao=dao.submenu,
                                        redis=dao.redis)


async def delete_submenu(menu_id: UUID, submenu_id: UUID, dao: HolderDAO = Depends(dao_provider)):
    return await service_delete_submenu(menu_id=menu_id, submenu_id=submenu_id, dao=dao.submenu, redis=dao.redis)


def setup(router: APIRouter):
    router.add_api_route('/menus/{menu_id}/submenus', create_submenu, response_model=PySubMenu,
                         methods=['POST'], status_code=201, tags=['SubMenu'])
    router.add_api_route('/menus/{menu_id}/submenus', get_list_submenus, response_model=list[PySubMenu],
                         methods=['GET'],
                         status_code=200, tags=['SubMenu'])
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}', get_specific_submenu, response_model=PySubMenu,
                         methods=['GET'],
                         status_code=200, tags=['SubMenu'])
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}', update_submenu, response_model=PySubMenu,
                         methods=['PATCH'],
                         status_code=200, tags=['SubMenu'])
    router.add_api_route('/menus/{menu_id}/submenus/{submenu_id}', delete_submenu, methods=['DELETE'], status_code=200,
                         tags=['SubMenu'])
