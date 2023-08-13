from src.infrastructure.db.dao.redis.redis_dao import RedisDAO


async def redis_delete_keys(dao: RedisDAO, menus: list[dict], submenus: list[dict], dishes: list[dict]):
    menus_id: list = [menu['id'] for menu in menus]
    submenus_id: list = [submenu['id'] for submenu in submenus]
    dishes_id: list = [dish['id'] for dish in dishes]
    keys: list = dao.keys.get_keys(
        menus={'menus_id': menus_id, 'list_menus': 'list_menus',
               'full_menus': 'full_menus'},
        submenus={'menus_id': menus_id,
                  'submenus_id': submenus_id},
        dishes={'submenus_id': submenus_id,
                'dishes_id': dishes_id})
    await dao.delete(keys)
