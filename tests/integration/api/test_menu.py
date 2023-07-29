from json import loads
from uuid import uuid4

from httpx import AsyncClient


async def test_create_menu(client: AsyncClient):
    result = await client.post('/api/v1/menus', json={'title': 'my_menu_1_test', 'description': 'description_test'})
    assert result.status_code == 201


async def test_get_list_menus(get_test_menu: dict, client: AsyncClient):
    result = await client.get('/api/v1/menus')
    assert result.status_code == 200
    assert loads(result.content) == [get_test_menu]


async def test_get_specific_menu(get_test_menu: dict, client: AsyncClient):
    result = await client.get(f'/api/v1/menus/{get_test_menu["id"]}')
    assert result.status_code == 200
    assert loads(result.content) == get_test_menu


async def test_update_menu(get_test_menu: dict, client: AsyncClient):
    result = await client.patch(f'/api/v1/menus/{get_test_menu["id"]}',
                                json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 200
    get_test_menu['title'] = 'update title'
    get_test_menu['description'] = 'update description'
    assert loads(result.content) == get_test_menu


async def test_delete_menu(get_test_menu: dict, client: AsyncClient):
    result = await client.delete(f'/api/v1/menus/{get_test_menu["id"]}')
    assert result.status_code == 200
    result = await client.get('/api/v1/menus')
    assert result.status_code == 200
    assert loads(result.content) == []


async def test_404_get_specific_menu(client: AsyncClient):
    result = await client.get(f'/api/v1/menus/{str(uuid4())}')
    assert result.status_code == 404
    assert loads(result.content) == {'detail': 'menu not found'}


async def test_404_update_menu(client: AsyncClient):
    result = await client.patch(f'/api/v1/menus/{str(uuid4())}',
                                json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 404
    assert loads(result.content) == {'detail': 'menu not found'}


async def test_404_delete_menu(client: AsyncClient):
    result = await client.delete(f'/api/v1/menus/{str(uuid4())}')
    assert result.status_code == 404
    assert loads(result.content) == {'detail': 'menu not found'}
