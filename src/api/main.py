from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.api import dependencies
from src.api.main_factory import create_app
from src.common.congif.db import load_db_config
from src.infrastructure.db.factory import create_pool


def main() -> FastAPI:
    app: FastAPI = create_app()
    pool: async_sessionmaker[AsyncSession] = create_pool(load_db_config())
    dependencies.setup(app=app, pool=pool)


def run():
    pass


if __name__ == '__main__':
    run()
