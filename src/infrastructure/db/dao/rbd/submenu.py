from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rbd.base import BaseDAO
from src.infrastructure.db.models.submenu import SubMenu


class SubMenuDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(SubMenu, session)