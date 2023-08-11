from dataclasses import dataclass

from src.core.utils import removing_keys_with_value_of_none
from src.infrastructure.db.models.redis.redis import Base


class MenuRedisKey(Base):
    def __init__(self, **keys):
        self.keys = keys

    def get_menu_keys(self, menus_id: list) -> list:
        return [self.keys['menu'] + str(menu_id) for menu_id in menus_id]

    @removing_keys_with_value_of_none
    def get_keys(self, **keys_menus) -> list:
        general: list = []
        for key_menu, value in keys_menus.items():
            if key_menu == 'list_menus' or key_menu == 'full_menus':
                general.append(value)
            elif key_menu == 'menus_id':
                general.extend(self.get_menu_keys(value))
        return general


class SubMenuRedisKey(Base):
    def __init__(self, **keys):
        self.keys = keys

    def get_submenus_list_keys(self, menus_id: list) -> list:
        return [self.keys['submenus'] + str(menu_id) for menu_id in menus_id]

    def get_submenu_keys(self, submenus_id: list) -> list:
        return [self.keys['submenu'] + str(submenu_id) for submenu_id in submenus_id]

    @removing_keys_with_value_of_none
    def get_keys(self, **keys_submenus) -> list:
        general: list = []
        for key_submenu, value in keys_submenus.items():
            if key_submenu == 'submenus_id':
                general.extend(self.get_submenu_keys(value))
            elif key_submenu == 'menus_id':
                return self.get_submenus_list_keys(value)
        return general


class DishRedisKey(Base):
    def __init__(self, **keys):
        self.keys = keys

    def get_dishes_list_keys(self, submenus_id: list) -> list:
        return [self.keys['dishes'] + str(submenu_id) for submenu_id in submenus_id]

    def get_dish_keys(self, dishes_id: list) -> list:
        return [self.keys['dish'] + str(dish_id) for dish_id in dishes_id]

    @removing_keys_with_value_of_none
    def get_keys(self, **keys_dishes) -> list:
        general: list = []
        for key_dish, value in keys_dishes.items():
            if key_dish == 'dishes_id':
                return self.get_dish_keys(value)
            elif key_dish == 'submenus_id':
                return self.get_dishes_list_keys(value)
        return general


@dataclass
class RedisKeys:
    keys_menu: MenuRedisKey = MenuRedisKey(menus='list_menus', menu='menu_', full_menus='full_menus')
    keys_submenu: SubMenuRedisKey = SubMenuRedisKey(submenus='list_submenus_', submenu='submenu_')
    keys_dish: DishRedisKey = DishRedisKey(dishes='list_dishes_', dish='dish_')

    def get_keys(self, menus: dict | None = None,
                 submenus: dict | None = None,
                 dishes: dict | None = None) -> list:
        keys = []
        if menus:
            menus_id = menus.get('menus_id')
            list_menus = menus.get('list_menus')
            full_menus = menus.get('full_menus')
            keys.extend(self.keys_menu.get_keys(menus_id=menus_id, list_menus=list_menus, full_menus=full_menus))
        if submenus:
            submenus_id = submenus.get('submenus_id')
            menus_id = submenus.get('menus_id')
            keys.extend(self.keys_submenu.get_keys(submenus_id=submenus_id, menus_id=menus_id))
        if dishes:
            dishes_id = dishes.get('dishes_id')
            submenus_id = dishes.get('submenus_id')
            keys.extend(self.keys_dish.get_keys(dishes_id=dishes_id, submenus_id=submenus_id))
        return keys
