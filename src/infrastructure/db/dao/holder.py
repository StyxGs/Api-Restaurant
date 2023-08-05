from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rbd.dish import DishDAO
from src.infrastructure.db.dao.rbd.menu import MenuDAO
from src.infrastructure.db.dao.rbd.submenu import SubMenuDAO
from src.infrastructure.db.dao.redis.redis_dao import RedisDAO


class HolderDAO:
    def __init__(self, session: AsyncSession, redis):
        self.session = session
        self.menu = MenuDAO(session)
        self.submenu = SubMenuDAO(session)
        self.dish = DishDAO(session)
        self.redis = RedisDAO(redis)
