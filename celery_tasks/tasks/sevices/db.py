from celery_tasks.tasks.sevices.redis import redis_delete_keys
from src.infrastructure.db.dao.holder import HolderDAO


async def add_or_update_db(menus: list[dict], submenus: list[dict], dishes: list[dict], dao: HolderDAO) -> str:
    if menus:
        await dao.menu.insert_or_update(menus)
        if submenus:
            await dao.submenu.insert_or_update(submenus)
        if dishes:
            await dao.dish.insert_or_update(dishes)
        await redis_delete_keys(dao=dao.redis, menus=menus, submenus=submenus, dishes=dishes)
        for dao_db, data in zip((dao.dish, dao.submenu, dao.menu,), (dishes, submenus, menus)):
            db_id: set = set(await dao_db.get_all_id())  # type: ignore
            admin_ud: set = {dt['id'] for dt in data}
            delete_id = list(db_id ^ admin_ud)
            await dao_db.delete_data_list(delete_id)  # type: ignore
        await dao.commit()
        return 'Данные обновлены!'
    else:
        return 'Файл пустой!'
