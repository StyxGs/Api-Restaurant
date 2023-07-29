import asyncio
from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.api import dependencies
from src.api import routers as setup_routers
from src.api.main_factory import create_app
from src.infrastructure.db import models
from tests.fixtures.menu import get_test_menu
from tests.fixtures.submenu import get_test_submenu


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def prepare_database(engine: AsyncEngine):
    async with engine.begin() as coon:
        await coon.run_sync(models.Base.metadata.create_all)
    yield
    async with engine.begin() as coon:
        await coon.run_sync(models.Base.metadata.drop_all)


@pytest.fixture(scope='session')
def app(pool: AsyncSession):
    app: FastAPI = create_app()
    dependencies.setup(app=app, pool=pool)
    routers = setup_routers.setup()
    app.include_router(routers)
    return app


@pytest.fixture(scope='session')
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test/') as ac:
        yield ac
