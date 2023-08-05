from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.db.congif.moleds.db import DBConfig, RedisConfig


def create_pool(db_config: DBConfig) -> async_sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_engine(db_config)
    return create_session_marker(engine=engine)


def create_engine(db_config: DBConfig):
    return create_async_engine(db_config.make_url)


def create_session_marker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, class_=AsyncSession,
                                                                expire_on_commit=False)
    return pool


def create_redis(config: RedisConfig):
    return Redis(host=config.host, port=int(config.port),
                 encoding='utf-8', decode_responses=True)
