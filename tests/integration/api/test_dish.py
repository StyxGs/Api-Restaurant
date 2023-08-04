from uuid import uuid4

from httpx import AsyncClient


async def test_get_specific_dish(get_test_dish: dict, client: AsyncClient):
    menu_id: str = get_test_dish['menu_id']
    submenu_id: str = get_test_dish['submenu_id']
    dish: dict = get_test_dish['dish']
    result = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish["id"]}')
    assert result.status_code == 200
    assert result.json() == dish


async def test_create_dish(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result = await client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}/dishes',
                               json={'title': 'my_dish_1_test', 'description': 'description_dish_test',
                                     'price': '14.56'})
    assert result.status_code == 201
    dish = result.json()
    dish_api = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}/dishes/{dish["id"]}')
    assert dish_api.status_code == 200
    assert dish_api.json() == dish


async def test_get_list_dish(get_test_dish: dict, client: AsyncClient):
    menu_id: str = get_test_dish['menu_id']
    submenu_id: str = get_test_dish['submenu_id']
    dish: dict = get_test_dish['dish']
    result = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert result.status_code == 200
    assert result.json() == [dish]


async def test_update_dish(get_test_dish: dict, client: AsyncClient):
    menu_id: str = get_test_dish['menu_id']
    submenu_id: str = get_test_dish['submenu_id']
    dish: dict = get_test_dish['dish']
    result = await client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish["id"]}',
                                json={'title': 'update dish title', 'description': 'update dish description'})
    assert result.status_code == 200
    dish['title'] = 'update dish title'
    dish['description'] = 'update dish description'
    assert result.json() == dish


async def test_delete_dish(get_test_dish: dict, client: AsyncClient):
    menu_id: str = get_test_dish['menu_id']
    submenu_id: str = get_test_dish['submenu_id']
    dish: dict = get_test_dish['dish']
    result_delete = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish["id"]}')
    assert result_delete.status_code == 200
    assert result_delete.json() == {'status': True, 'message': 'The dish has been deleted'}
    result_get = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert result_get.status_code == 200
    assert result_get.json() == []


async def test_404_get_specific_dish(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result = await client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}/dishes/{str(uuid4())}')
    assert result.status_code == 404
    assert result.json() == {'detail': 'dish not found'}


async def test_404_update_dish(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result = await client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}/dishes/{str(uuid4())}',
                                json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 404
    assert result.json() == {'detail': 'dish not found'}


async def test_404_delete_dish(get_test_submenu: dict, client: AsyncClient):
    menu_id: str = get_test_submenu['menu_id']
    submenu: dict = get_test_submenu['submenu']
    result = await client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu["id"]}/dishes/{str(uuid4())}')
    assert result.status_code == 404
    assert result.json() == {'detail': 'dish not found'}


async def test_400_create_dish(get_test_menu: dict, client: AsyncClient):
    result = await client.post(f'/api/v1/menus/{get_test_menu["id"]}/submenus/{str(uuid4())}/dishes',
                               json={'title': 'my_submenu_1_test', 'description': 'description_test', 'price': '14.57'})
    assert result.status_code == 400
    assert result.json() == {'detail': 'already exists or not found'}
