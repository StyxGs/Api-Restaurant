import pytest

from src.api.models.responses import PyDish
from src.core.models.dto.dish import DishDTO
from src.core.models.dto.menu import MenuDTO
from src.core.models.dto.submenu import SubMenuDTO
from src.core.services.dish import service_create_dish
from src.core.services.menu import service_create_menu
from src.core.services.submenu import service_create_submenu
from src.infrastructure.db.dao.holder import HolderDAO
from src.infrastructure.db.models import Menu, SubMenu, Dish


@pytest.fixture
async def get_test_dish(dao: HolderDAO) -> dict:
    menu: Menu = await service_create_menu(MenuDTO(title='my menu test', description='description test'), dao.menu)
    submenu: SubMenu = await service_create_submenu(menu.id,
                                                    SubMenuDTO(title='my submenu test',
                                                               description='submenu description test'),
                                                    dao.submenu)
    result: Dish = await service_create_dish(menu.id, submenu.id,
                                             DishDTO(title='my dish test', description='dish description test',
                                                     price='14.57'),
                                             dao.dish)
    dish: dict = PyDish.model_validate(result).model_dump()
    dish['id'] = str(dish['id'])
    return {'dish': dish, 'submenu_id': submenu.id, 'menu_id': menu.id}
