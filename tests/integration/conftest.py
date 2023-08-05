from typing import AsyncGenerator

import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.common.congif.db import load_db_config, load_redis_config
from src.infrastructure.db.congif.moleds.db import DBConfig
from src.infrastructure.db.dao.holder import HolderDAO
from src.infrastructure.db.factory import create_redis


@pytest.fixture(scope='session')
def engine() -> AsyncEngine:
    config: DBConfig = load_db_config('../../../tests/config_env/.env')
    engine_: AsyncEngine = create_async_engine(url=config.make_url)
    yield engine_


@pytest.fixture(scope='session')
def pool(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool_ = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    return pool_


@pytest.fixture(scope='session')
def redis() -> Redis:
    redis: Redis = create_redis(load_redis_config('../../../tests/config_env/.env'))
    return redis


@pytest.fixture
async def session(pool: async_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session_:
        yield session_


@pytest.fixture
async def dao(session: AsyncSession, redis: Redis) -> HolderDAO:
    dao_ = HolderDAO(session=session, redis=redis)
    return dao_
