from src.infrastructure.db.dao.rbd.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models.dish import Dish


class DishDAO(BaseDAO):

    def __init__(self, session: AsyncSession):
        super().__init__(Dish, session)
