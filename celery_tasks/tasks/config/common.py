from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.common.congif.db import load_db_config, load_redis_config
from src.infrastructure.db.factory import create_pool, create_redis

pool: async_sessionmaker[AsyncSession] = create_pool(load_db_config())
redis: Redis = create_redis(load_redis_config())
