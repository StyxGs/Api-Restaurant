from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.api.dependencies.db import DBProvider, dao_provider


def setup(app: FastAPI, pool: async_sessionmaker[AsyncSession], redis):
    db_provider = DBProvider(pool=pool, redis=redis)
    app.dependency_overrides[dao_provider] = db_provider.dao
