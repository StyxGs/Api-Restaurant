from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.api import dependencies
from src.api import routers as setup_routers
from src.api.main_factory import create_app
from src.common.congif.db import load_db_config
from src.infrastructure.db.factory import create_pool


def main() -> FastAPI:
    app: FastAPI = create_app()
    pool: async_sessionmaker[AsyncSession] = create_pool(load_db_config())
    dependencies.setup(app=app, pool=pool)
    routers = setup_routers.setup()
    app.include_router(routers)
    return app


app = main()
