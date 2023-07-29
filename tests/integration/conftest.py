from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from src.common.congif.db import load_db_config
from src.infrastructure.db.congif.moleds.db import DBConfig
from src.infrastructure.db.dao.holder import HolderDAO


@pytest.fixture(scope='session')
def engine() -> AsyncEngine:
    config: DBConfig = load_db_config('../../../tests/config_env/.env')
    engine_: AsyncEngine = create_async_engine(url=config.make_url)
    yield engine_


@pytest.fixture(scope='session')
def pool(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool_ = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    return pool_


@pytest.fixture
async def session(pool: async_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session_:
        yield session_


@pytest.fixture
async def dao(session: AsyncSession) -> HolderDAO:
    dao_ = HolderDAO(session=session)
    return dao_
