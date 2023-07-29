import pytest

from src.api.models.responses import PyMenu
from src.core.models.dto.menu import MenuDTO
from src.core.services.menu import service_create_menu
from src.infrastructure.db.dao.holder import HolderDAO
from src.infrastructure.db.models import Menu


@pytest.fixture
async def get_test_menu(dao: HolderDAO) -> dict:
    dto = MenuDTO(title='my menu test', description='description test')
    result: Menu = await service_create_menu(dto, dao.menu)
    menu = PyMenu.model_validate(result).model_dump()
    menu['id'] = str(menu['id'])
    return menu
