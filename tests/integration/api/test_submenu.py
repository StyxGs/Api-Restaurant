from uuid import uuid4

from httpx import AsyncClient


async def test_get_specific_submenu(get_test_submenu: dict, client: AsyncClient, reverse):
    submenu: dict = get_test_submenu['submenu']
    url: str = reverse('get_specific_submenu', menu_id=get_test_submenu['menu_id'],
                       submenu_id=submenu['id'])
    result = await client.get(url)
    assert result.status_code == 200
    assert result.json() == submenu


async def test_create_submenu(get_test_menu: dict, client: AsyncClient, reverse):
    url_post: str = reverse('create_submenu', menu_id=get_test_menu['id'])
    result = await client.post(url_post, json={'title': 'my_submenu_1_test', 'description': 'description_test'})
    assert result.status_code == 201
    submenu: dict = result.json()
    url_get: str = reverse('get_specific_submenu', menu_id=get_test_menu['id'], submenu_id=submenu['id'])
    submenu_api = await client.get(url_get)
    assert submenu_api.status_code == 200
    assert submenu_api.json() == submenu


async def test_get_list_submenus(get_test_submenu: dict, client: AsyncClient, reverse):
    url: str = reverse('get_list_submenus', menu_id=get_test_submenu['menu_id'])
    submenu: dict = get_test_submenu['submenu']
    result = await client.get(url)
    assert result.status_code == 200
    assert result.json() == [submenu]


async def test_update_submenu(get_test_submenu: dict, client: AsyncClient, reverse):
    submenu: dict = get_test_submenu['submenu']
    url: str = reverse('update_submenu', menu_id=get_test_submenu['menu_id'], submenu_id=submenu['id'])
    result = await client.patch(url,
                                json={'title': 'update submenu title', 'description': 'update submenu description'})
    assert result.status_code == 200
    submenu['title'] = 'update submenu title'
    submenu['description'] = 'update submenu description'
    assert result.json() == submenu


async def test_delete_submenu(get_test_submenu: dict, client: AsyncClient, reverse):
    url_delete: str = reverse('delete_submenu', menu_id=get_test_submenu['menu_id'],
                              submenu_id=get_test_submenu['submenu']['id'])
    result_delete = await client.delete(url_delete)
    assert result_delete.status_code == 200
    assert result_delete.json() == {'status': True, 'message': 'The submenu has been deleted'}
    url_get: str = reverse('get_list_submenus', menu_id=get_test_submenu['menu_id'])
    result = await client.get(url_get)
    assert result.status_code == 200
    assert result.json() == []


async def test_404_get_specific_submenu(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('get_specific_submenu', menu_id=get_test_menu['id'], submenu_id=str(uuid4()))
    result = await client.get(url)
    assert result.status_code == 404
    assert result.json() == {'detail': 'submenu not found'}


async def test_404_update_submenu(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('update_submenu', menu_id=get_test_menu['id'], submenu_id=str(uuid4()))
    result = await client.patch(url,
                                json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 404
    assert result.json() == {'detail': 'submenu not found'}


async def test_404_delete_submenu(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('delete_submenu', menu_id=get_test_menu['id'], submenu_id=str(uuid4()))
    result = await client.delete(url)
    assert result.status_code == 404
    assert result.json() == {'detail': 'submenu not found'}


async def test_400_create_submenu(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('create_submenu', menu_id=str(uuid4()))
    result = await client.post(url, json={'title': 'my_submenu_1_test', 'description': 'description_test'})
    assert result.status_code == 400
    assert result.json() == {'detail': 'already exists or not found'}
