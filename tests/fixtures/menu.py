import pytest
from fastapi import BackgroundTasks

from src.api.models.responses import PyMenu
from src.core.models.dto.dish import DishDTO
from src.core.models.dto.menu import MenuDTO
from src.core.models.dto.submenu import SubMenuDTO
from src.core.services.dish import service_create_dish
from src.core.services.menu import service_create_menu
from src.core.services.submenu import service_create_submenu
from src.infrastructure.db.dao.holder import HolderDAO


@pytest.fixture
async def get_test_menu(dao: HolderDAO) -> dict:
    dto = MenuDTO(title='my menu test', description='description test')
    result: MenuDTO = await service_create_menu(dto, dao.menu, dao.redis, bg=BackgroundTasks())
    menu = PyMenu.model_validate(result).model_dump()
    menu['id'] = str(menu['id'])
    return menu


@pytest.fixture
async def get_full_menu(dao: HolderDAO) -> list:
    menu: MenuDTO = await service_create_menu(MenuDTO(title='my menu test', description='description test'), dao.menu,
                                              dao.redis, bg=BackgroundTasks())
    submenu: SubMenuDTO = await service_create_submenu(menu.id,
                                                       SubMenuDTO(title='my submenu test',
                                                                  description='submenu description test'),
                                                       dao.submenu, dao.redis, bg=BackgroundTasks())
    dish: DishDTO = await service_create_dish(menu.id, submenu.id,
                                              DishDTO(title='my dish test', description='dish description test',
                                                      price='14.57'),
                                              dao.dish, dao.redis, bg=BackgroundTasks())
    data = [{
        'id': str(menu.id),
        'title': menu.title,
        'description': menu.description,
        'submenus': [{
            'id': str(submenu.id),
            'title': submenu.title,
            'description': submenu.description,
            'dishes': [{
                'id': str(dish.id),
                'title': dish.title,
                'description': dish.description,
                'price': dish.price,
            }],
        }],
    }, ]
    return data
