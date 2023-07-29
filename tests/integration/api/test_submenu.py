from json import loads
from uuid import uuid4

from httpx import AsyncClient


async def test_get_specific_submenu(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}')
    assert result.status_code == 200
    assert loads(result.content) == submenu


async def test_create_submenu(get_test_menu: dict, client: AsyncClient):
    result = await client.post(f'/api/v1/menus/{get_test_menu["id"]}/submenus',
                               json={'title': 'my_submenu_1_test', 'description': 'description_test'})
    assert result.status_code == 201
    submenu: dict = loads(result.content)
    submenu_api = await client.get(f'/api/v1/menus/{get_test_menu["id"]}/submenus/{submenu["id"]}')
    assert submenu_api.status_code == 200
    assert loads(submenu_api.content) == submenu


async def test_get_list_submenus(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert result.status_code == 200
    assert loads(result.content) == [submenu]


async def test_update_submenu(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result = await client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}',
                                json={'title': 'update submenu title', 'description': 'update submenu description'})
    assert result.status_code == 200
    submenu['title'] = 'update submenu title'
    submenu['description'] = 'update submenu description'
    assert loads(result.content) == submenu


async def test_delete_submenu(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result_delete = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}')
    assert result_delete.status_code == 200
    result_get = await client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert result_get.status_code == 200
    assert loads(result_get.content) == []


async def test_404_get_list_submenus(client: AsyncClient):
    result = await client.get(f'/api/v1/menus/{str(uuid4())}/submenus')
    assert result.status_code == 404
    assert loads(result.content) == {'detail': 'submenu not found'}


async def test_404_get_specific_submenus(get_test_menu: dict, client: AsyncClient):
    result = await client.get(f'/api/v1/menus/{get_test_menu["id"]}/submenus/{str(uuid4())}')
    assert result.status_code == 404
    assert loads(result.content) == {'detail': 'submenu not found'}


async def test_404_update_submenu(get_test_menu: dict, client: AsyncClient):
    result = await client.patch(f'/api/v1/menus/{get_test_menu["id"]}/submenus/{str(uuid4())}',
                                json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 404
    assert loads(result.content) == {'detail': 'submenu not found'}


async def test_404_delete_submenu(get_test_menu: dict, client: AsyncClient):
    result = await client.delete(f'/api/v1/menus/{get_test_menu["id"]}/submenus/{str(uuid4())}')
    assert result.status_code == 404
    assert loads(result.content) == {'detail': 'submenu not found'}


async def test_404_create_submenu(get_test_menu: dict, client: AsyncClient):
    result = await client.post(f'/api/v1/menus/{str(uuid4())}/submenus',
                               json={'title': 'my_submenu_1_test', 'description': 'description_test'})
    assert result.status_code == 400
    assert loads(result.content) == {'detail': 'submenu already exists or menu not exists'}
