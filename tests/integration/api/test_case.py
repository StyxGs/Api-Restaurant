from json import loads

import pytest
from httpx import AsyncClient


@pytest.mark.usefixtures('prepare_database')
@pytest.mark.usefixtures('data')
class TestCase:
    async def test_create_menu(self, data: dict, client: AsyncClient):
        result = await client.post('/api/v1/menus', json={'title': 'My menu 1', 'description': 'My menu description 1'})
        assert result.status_code == 201
        menu: dict = loads(result.content)
        assert menu
        data['menu'] = menu

    async def test_create_submenu(self, data: dict, client: AsyncClient):
        result = await client.post(f'/api/v1/menus/{data["menu"]["id"]}/submenus',
                                   json={'title': 'My submenu 1', 'description': 'My submenu description 1'})
        assert result.status_code == 201
        submenu: dict = loads(result.content)
        assert submenu
        data['submenu'] = submenu
        data['menu']['submenus_count'] += 1

    async def test_create_dish_1(self, data: dict, client: AsyncClient):
        result = await client.post(f'/api/v1/menus/{data["menu"]["id"]}/submenus/{data["submenu"]["id"]}/dishes',
                                   json={'title': 'My dish 2', 'description': 'My dish description 2',
                                         'price': '13.50'})
        assert result.status_code == 201
        dish_1: dict = loads(result.content)
        assert dish_1
        data['dish_1'] = dish_1
        data['submenu']['dishes_count'] += 1
        data['menu']['dishes_count'] += 1

    async def test_create_dish_2(self, data: dict, client: AsyncClient):
        result = await client.post(f'/api/v1/menus/{data["menu"]["id"]}/submenus/{data["submenu"]["id"]}/dishes',
                                   json={'title': 'My dish 1', 'description': 'My dish description 1',
                                         'price': '12.50'})
        assert result.status_code == 201
        dish_2: dict = loads(result.content)
        assert dish_2
        data['dish_2'] = dish_2
        data['submenu']['dishes_count'] += 1
        data['menu']['dishes_count'] += 1

    async def test_get_specific_menu(self, data: dict, client: AsyncClient):
        result = await client.get(f'/api/v1/menus/{data["menu"]["id"]}')
        assert result.status_code == 200
        assert loads(result.content) == data['menu']

    async def test_get_specific_submenu(self, data: dict, client: AsyncClient):
        result = await client.get(f'/api/v1/menus/{data["menu"]["id"]}/submenus/{data["submenu"]["id"]}')
        assert result.status_code == 200
        assert loads(result.content) == data['submenu']

    async def test_delete_submenu(self, data: dict, client: AsyncClient):
        result = await client.delete(f'/api/v1/menus/{data["menu"]["id"]}/submenus/{data["submenu"]["id"]}')
        assert result.status_code == 200
        assert loads(result.content) == {'status': True, 'message': 'The submenu has been deleted'}
        keys = ['dish_1', 'dish_2']
        [data.pop(key) for key in keys]
        data['menu']['submenus_count'] = 0
        data['menu']['dishes_count'] = 0

    async def test_get_list_submenus(self, data: dict, client: AsyncClient):
        result = await client.get(f'/api/v1/menus/{data["menu"]["id"]}/submenus')
        assert result.status_code == 200
        assert loads(result.content) == []

    async def test_get_list_dish(self, data: dict, client: AsyncClient):
        result = await client.get(f'/api/v1/menus/{data["menu"]["id"]}/submenus/{data["submenu"]["id"]}/dishes')
        assert result.status_code == 200
        assert loads(result.content) == []

    async def test_get_specific_menu_(self, data: dict, client: AsyncClient):
        result = await client.get(f'/api/v1/menus/{data["menu"]["id"]}')
        assert result.status_code == 200
        assert loads(result.content) == data['menu']

    async def test_delete_menu(self, data: dict, client: AsyncClient):
        result_delete = await client.delete(f'/api/v1/menus/{data["menu"]["id"]}')
        assert result_delete.status_code == 200
        assert loads(result_delete.content) == {'status': True, 'message': 'The menu has been deleted'}

    async def test_get_list_menus(self, data: dict, client: AsyncClient):
        result = await client.get('/api/v1/menus')
        assert result.status_code == 200
        assert loads(result.content) == []
