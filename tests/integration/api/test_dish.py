from uuid import uuid4

from httpx import AsyncClient


async def test_get_specific_dish(get_test_dish: dict, client: AsyncClient, reverse):
    dish: dict = get_test_dish['dish']
    url: str = reverse('get_specific_dish', menu_id=get_test_dish['menu_id'], submenu_id=get_test_dish['submenu_id'],
                       dish_id=dish['id'])
    result = await client.get(url)
    assert result.status_code == 200
    assert result.json() == dish


async def test_create_dish(get_test_submenu: dict, client: AsyncClient, reverse):
    url_post: str = reverse('create_dish', menu_id=get_test_submenu['menu_id'],
                            submenu_id=get_test_submenu['submenu']['id'])
    result = await client.post(url_post,
                               json={'title': 'my_dish_1_test', 'description': 'description_dish_test',
                                     'price': '14.56'})
    assert result.status_code == 201
    dish = result.json()
    url_get: str = reverse('get_specific_dish', menu_id=get_test_submenu['menu_id'],
                           submenu_id=get_test_submenu['submenu']['id'],
                           dish_id=dish['id'])
    dish_api = await client.get(url_get)
    assert dish_api.status_code == 200
    assert dish_api.json() == dish


async def test_get_list_dish(get_test_dish: dict, client: AsyncClient, reverse):
    dish: dict = get_test_dish['dish']
    url: str = reverse('get_list_dish', menu_id=get_test_dish['menu_id'], submenu_id=get_test_dish['submenu_id'])
    result = await client.get(url)
    assert result.status_code == 200
    assert result.json() == [dish]


async def test_update_dish(get_test_dish: dict, client: AsyncClient, reverse):
    dish: dict = get_test_dish['dish']
    url: str = reverse('update_dish', menu_id=get_test_dish['menu_id'], submenu_id=get_test_dish['submenu_id'],
                       dish_id=dish['id'])
    result = await client.patch(url,
                                json={'title': 'update dish title', 'description': 'update dish description'})
    assert result.status_code == 200
    dish['title'] = 'update dish title'
    dish['description'] = 'update dish description'
    assert result.json() == dish


async def test_delete_dish(get_test_dish: dict, client: AsyncClient, reverse):
    dish: dict = get_test_dish['dish']
    url_delete: str = reverse('delete_dish', menu_id=get_test_dish['menu_id'], submenu_id=get_test_dish['submenu_id'],
                              dish_id=dish['id'])
    result_delete = await client.delete(url_delete)
    assert result_delete.status_code == 200
    assert result_delete.json() == {'status': True, 'message': 'The dish has been deleted'}
    url_get: str = reverse('get_list_dish', menu_id=get_test_dish['menu_id'], submenu_id=get_test_dish['submenu_id'])
    result_get = await client.get(url_get)
    assert result_get.status_code == 200
    assert result_get.json() == []


async def test_404_get_specific_dish(get_test_submenu: dict, client: AsyncClient, reverse):
    url: str = reverse('get_specific_dish', menu_id=get_test_submenu['menu_id'],
                       submenu_id=get_test_submenu['submenu']['id'],
                       dish_id=str(uuid4()))
    result = await client.get(url)
    assert result.status_code == 404
    assert result.json() == {'detail': 'dish not found'}


async def test_404_update_dish(get_test_submenu: dict, client: AsyncClient, reverse):
    url: str = reverse('update_dish', menu_id=get_test_submenu['menu_id'], submenu_id=get_test_submenu['submenu']['id'],
                       dish_id=str(uuid4()))
    result = await client.patch(url,
                                json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 404
    assert result.json() == {'detail': 'dish not found'}


async def test_404_delete_dish(get_test_submenu: dict, client: AsyncClient, reverse):
    url: str = reverse('delete_dish', menu_id=get_test_submenu['menu_id'], submenu_id=get_test_submenu['submenu']['id'],
                       dish_id=str(uuid4()))
    result = await client.delete(url)
    assert result.status_code == 404
    assert result.json() == {'detail': 'dish not found'}


async def test_400_create_dish(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('create_dish', menu_id=get_test_menu['id'], submenu_id=str(uuid4()))
    result = await client.post(url,
                               json={'title': 'my_submenu_1_test', 'description': 'description_test', 'price': '14.57'})
    assert result.status_code == 400
    assert result.json() == {'detail': 'already exists or not found'}
