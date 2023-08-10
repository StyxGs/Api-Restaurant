from dataclasses import dataclass

from src.infrastructure.db.models.redis import Base


class MenuRedisKey(Base):
    def __init__(self, **keys):
        self.keys = keys

    def get_menu_keys(self, menus_id: list):
        return [self.keys['menu'] + str(menu_id) for menu_id in menus_id]

    def get_keys(self, menus_id: list | None = None, list_menus: str | None = None):
        keys: list = []
        if menus_id and list_menus:
            keys.extend(self.get_menu_keys(menus_id))
            keys.append(self.keys['menus'])
        elif menus_id:
            keys.extend(self.get_menu_keys(menus_id))
        elif list_menus:
            keys.append(self.keys['menus'])
        return keys


class SubMenuRedisKey(Base):
    def __init__(self, **keys):
        self.keys = keys

    def get_submenus_list_keys(self, menus_id: list):
        return [self.keys['submenus'] + str(menu_id) for menu_id in menus_id]

    def get_submenu_keys(self, submenus_id: list):
        return [self.keys['submenu'] + str(submenu_id) for submenu_id in submenus_id]

    def get_keys(self, submenus_id: list | None = None, menus_id: list | None = None):
        if submenus_id and menus_id:
            return self.get_submenus_list_keys(menus_id) + self.get_submenu_keys(submenus_id)
        elif submenus_id:
            return self.get_submenu_keys(submenus_id)
        elif menus_id:
            return self.get_submenus_list_keys(menus_id)
        else:
            return []


class DishRedisKey(Base):
    def __init__(self, **keys):
        self.keys = keys

    def get_dishes_list_keys(self, submenus_id: list):
        return [self.keys['dishes'] + str(submenu_id) for submenu_id in submenus_id]

    def get_dish_keys(self, dishes_id: list):
        return [self.keys['dish'] + str(dish_id) for dish_id in dishes_id]

    def get_keys(self, dishes_id: list | None = None, submenus_id: list | None = None):
        if dishes_id and submenus_id:
            return self.get_dish_keys(dishes_id) + self.get_dishes_list_keys(submenus_id)
        elif dishes_id:
            return self.get_dish_keys(dishes_id)
        elif submenus_id:
            return self.get_dishes_list_keys(submenus_id)
        else:
            return []


@dataclass
class RedisKeys:
    keys_menu: MenuRedisKey = MenuRedisKey(menus='list_menus', menu='menu_')
    keys_submenu: SubMenuRedisKey = SubMenuRedisKey(submenus='list_submenus_', submenu='submenu_')
    keys_dish: DishRedisKey = DishRedisKey(dishes='list_dishes_', dish='dish_')

    def get_keys(self, menus: dict | None = None,
                 submenus: dict | None = None,
                 dishes: dict | None = None):
        keys = []
        if menus:
            menus_id = menus.get('menus_id')
            list_menus = menus.get('list_menus')
            keys.extend(self.keys_menu.get_keys(menus_id=menus_id, list_menus=list_menus))
        if submenus:
            submenus_id = submenus.get('submenus_id')
            menus_id = submenus.get('menus_id')
            keys.extend(self.keys_submenu.get_keys(submenus_id=submenus_id, menus_id=menus_id))
        if dishes:
            dishes_id = dishes.get('dishes_id')
            submenus_id = dishes.get('submenus_id')
            keys.extend(self.keys_dish.get_keys(dishes_id=dishes_id, submenus_id=submenus_id))
        return keys
