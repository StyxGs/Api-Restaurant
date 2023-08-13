from uuid import UUID

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def is_valid_uuid(val) -> bool:
    try:
        UUID(val)
        return True
    except (AttributeError, ValueError,):
        return False


def get_data_admin() -> Worksheet:
    wp: Workbook = load_workbook('admin/Menu.xlsx')
    ws: Worksheet = wp.active
    return ws
