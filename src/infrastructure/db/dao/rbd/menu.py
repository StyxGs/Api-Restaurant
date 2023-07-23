from src.infrastructure.db.dao.rbd.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models.menu import Menu


class MenuDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(Menu, session)
