import pytest

from src.api.models.responses import PyMenu
from src.core.models.dto.menu import MenuDTO
from src.core.services.menu import service_create_menu
from src.infrastructure.db.dao.holder import HolderDAO


@pytest.fixture
async def get_test_menu(dao: HolderDAO) -> dict:
    dto = MenuDTO(title='my menu test', description='description test')
    result: MenuDTO = await service_create_menu(dto, dao.menu, dao.redis)
    menu = PyMenu.model_validate(result).model_dump()
    menu['id'] = str(menu['id'])
    return menu
