from uuid import UUID

from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.worksheet.worksheet import Worksheet
from sqlalchemy.exc import IntegrityError

from celery_tasks.tasks.sevices.db import add_or_update_db
from celery_tasks.tasks.utils import get_data_admin, is_valid_uuid
from src.infrastructure.db.dao.holder import HolderDAO


async def add_db(dao: HolderDAO) -> str:
    try:
        data: Worksheet = get_data_admin()
        flag_menu = True
        flag_submenu = False
        menus: list = []
        submenus: list = []
        dishes: list = []
        for row in data.iter_rows(min_col=1, values_only=True):
            if row[0]:
                if is_valid_uuid(row[0]):
                    menus.append(dict(id=UUID(row[0]), title=row[1], description=row[2]))
                    flag_menu = True
                else:
                    flag_menu = False
            elif row[1] and flag_menu:
                if is_valid_uuid(row[1]):
                    submenus.append(dict(id=UUID(row[1]), title=row[2], description=row[3], menu_id=menus[-1]['id']))
                    flag_submenu = True
                else:
                    flag_submenu = False
            elif row[2] and is_valid_uuid(row[2]) and flag_submenu and isinstance(row[5], (float, int,)):
                dishes.append(
                    dict(id=UUID(row[2]), title=row[3], description=row[4], price=str(row[5]),
                         submenu_id=submenus[-1]['id']))
        return await add_or_update_db(dao=dao, menus=menus, submenus=submenus, dishes=dishes)
    except FileNotFoundError:
        return 'Файл не найден'
    except InvalidFileException:
        return 'Файл поврежден'
    except IsADirectoryError:
        return 'Неверный формат файла'
    except IntegrityError as e:
        return f'Ошибка: {e}'
    except Exception as e:
        return f'Ошибка: {e}'
