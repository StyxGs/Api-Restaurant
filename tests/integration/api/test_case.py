import pytest
from httpx import AsyncClient


@pytest.mark.usefixtures('prepare_database')
@pytest.mark.usefixtures('redis_clear')
@pytest.mark.usefixtures('data')
class TestCase:
    async def test_create_menu(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('create_menu')
        result = await client.post(url, json={'title': 'My menu 1', 'description': 'My menu description 1'})
        assert result.status_code == 201
        menu: dict = result.json()
        assert menu
        data['menu'] = menu

    async def test_create_submenu(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('create_submenu', menu_id=data['menu']['id'])
        result = await client.post(url,
                                   json={'title': 'My submenu 1', 'description': 'My submenu description 1'})
        assert result.status_code == 201
        submenu: dict = result.json()
        assert submenu
        data['submenu'] = submenu
        data['menu']['submenus_count'] += 1

    async def test_create_dish_1(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('create_dish', menu_id=data['menu']['id'], submenu_id=data['submenu']['id'])
        result = await client.post(url,
                                   json={'title': 'My dish 2', 'description': 'My dish description 2',
                                         'price': '13.50'})
        assert result.status_code == 201
        dish_1: dict = result.json()
        assert dish_1
        data['dish_1'] = dish_1
        data['submenu']['dishes_count'] += 1
        data['menu']['dishes_count'] += 1

    async def test_create_dish_2(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('create_dish', menu_id=data['menu']['id'], submenu_id=data['submenu']['id'])
        result = await client.post(url,
                                   json={'title': 'My dish 1', 'description': 'My dish description 1',
                                         'price': '12.50'})
        assert result.status_code == 201
        dish_2: dict = result.json()
        assert dish_2
        data['dish_2'] = dish_2
        data['submenu']['dishes_count'] += 1
        data['menu']['dishes_count'] += 1

    async def test_get_specific_menu(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('get_specific_menu', menu_id=data['menu']['id'])
        result = await client.get(url)
        assert result.status_code == 200
        assert result.json() == data['menu']

    async def test_get_specific_submenu(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('get_specific_submenu', menu_id=data['menu']['id'], submenu_id=data['submenu']['id'])
        result = await client.get(url)
        assert result.status_code == 200
        assert result.json() == data['submenu']

    async def test_delete_submenu(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('delete_submenu', menu_id=data['menu']['id'], submenu_id=data['submenu']['id'])
        result = await client.delete(url)
        assert result.status_code == 200
        assert result.json() == {'status': True, 'message': 'The submenu has been deleted'}
        keys = ['dish_1', 'dish_2']
        [data.pop(key) for key in keys]
        data['menu']['submenus_count'] = 0
        data['menu']['dishes_count'] = 0

    async def test_get_list_submenus(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('get_list_submenus', menu_id=data['menu']['id'])
        result = await client.get(url)
        assert result.status_code == 200
        assert result.json() == []

    async def test_get_list_dish(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('get_list_dish', menu_id=data['menu']['id'], submenu_id=data['submenu']['id'])
        result = await client.get(url)
        assert result.status_code == 200
        assert result.json() == []

    async def test_get_specific_menu_(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('get_specific_menu', menu_id=data['menu']['id'])
        result = await client.get(url)
        assert result.status_code == 200
        assert result.json() == data['menu']

    async def test_delete_menu(self, data: dict, client: AsyncClient, reverse):
        url: str = reverse('delete_menu', menu_id=data['menu']['id'])
        result = await client.delete(url)
        assert result.status_code == 200
        assert result.json() == {'status': True, 'message': 'The menu has been deleted'}

    async def test_get_list_menus(self, client: AsyncClient, reverse):
        url: str = reverse('get_list_menus')
        result = await client.get(url)
        assert result.status_code == 200
        assert result.json() == []
