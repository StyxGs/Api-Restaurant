from uuid import uuid4

from httpx import AsyncClient


async def test_get_specific_menu(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('get_specific_menu', menu_id=get_test_menu['id'])
    result = await client.get(url)
    assert result.status_code == 200
    assert result.json() == get_test_menu


async def test_create_menu(client: AsyncClient, reverse):
    url_post: str = reverse('create_menu')
    result = await client.post(url_post, json={'title': 'my_menu_1_test', 'description': 'description_test'})
    assert result.status_code == 201
    menu: dict = result.json()
    url_get: str = reverse('get_specific_menu', menu_id=menu['id'])
    menu_api = await client.get(url_get)
    assert menu_api.status_code == 200
    assert menu_api.json() == menu


async def test_get_full_info_menus(get_full_menu: list, client: AsyncClient, reverse):
    url: str = reverse('get_full_info_menus')
    result = await client.get(url)
    assert result.status_code == 200
    assert result.json() == get_full_menu


async def test_get_list_menus(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('get_list_menus')
    result = await client.get(url)
    assert result.status_code == 200
    assert result.json() == [get_test_menu]


async def test_update_menu(get_test_menu: dict, client: AsyncClient, reverse):
    url: str = reverse('update_menu', menu_id=get_test_menu['id'])
    result = await client.patch(url, json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 200
    get_test_menu['title'] = 'update title'
    get_test_menu['description'] = 'update description'
    assert result.json() == get_test_menu


async def test_delete_menu(get_test_menu: dict, client: AsyncClient, reverse):
    url_delete: str = reverse('delete_menu', menu_id=get_test_menu['id'])
    result_delete = await client.delete(url_delete)
    assert result_delete.status_code == 200
    assert result_delete.json() == {'status': True, 'message': 'The menu has been deleted'}
    url_get: str = reverse('get_list_menus')
    result_get = await client.get(url_get)
    assert result_get.status_code == 200
    assert result_get.json() == []


async def test_404_get_specific_menu(client: AsyncClient, reverse):
    url: str = reverse('get_specific_menu', menu_id=str(uuid4()))
    result = await client.get(url)
    assert result.status_code == 404
    assert result.json() == {'detail': 'menu not found'}


async def test_404_update_menu(client: AsyncClient, reverse):
    url: str = reverse('update_menu', menu_id=str(uuid4()))
    result = await client.patch(url, json={'title': 'update title', 'description': 'update description'})
    assert result.status_code == 404
    assert result.json() == {'detail': 'menu not found'}


async def test_404_delete_menu(client: AsyncClient, reverse):
    url: str = reverse('delete_menu', menu_id=str(uuid4()))
    result = await client.delete(url)
    assert result.status_code == 404
    assert result.json() == {'detail': 'menu not found'}
