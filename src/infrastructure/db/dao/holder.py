from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rbd.dish import DishDAO
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.dao.rbd.submenu import SubMenuDAO


class HolderDAO:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.menu = MenuDAO(session)
        self.submenu = SubMenuDAO(session)
        self.dish = DishDAO(session)
