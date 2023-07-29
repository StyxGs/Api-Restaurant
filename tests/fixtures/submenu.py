import pytest

from src.api.models.responses import PySubMenu
from src.core.models.dto.menu import MenuDTO
from src.core.models.dto.submenu import SubMenuDTO
from src.core.services.menu import service_create_menu
from src.core.services.submenu import service_create_submenu
from src.infrastructure.db.dao.holder import HolderDAO


@pytest.fixture
async def get_test_submenu(dao: HolderDAO) -> dict:
    menu = await service_create_menu(MenuDTO(title='my menu test', description='description test'), dao.menu)
    result = await service_create_submenu(menu.id,
                                          SubMenuDTO(title='my sub menu test', description='submenu description test'),
                                          dao.submenu)
    submenu: dict = PySubMenu.model_validate(result).model_dump()
    submenu['id'] = str(submenu['id'])
    return {'submenu': submenu, 'menu_id': menu.id}
