from sqlalchemy.ext.asyncio import AsyncSession

from celery_tasks.tasks.config.common import pool, redis
from celery_tasks.tasks.sevices.admin import add_db
from src.infrastructure.db.dao.holder import HolderDAO


async def get_session():
    async with pool() as session:
        return session


async def main_func_admin() -> str:
    session: AsyncSession = await get_session()
    return await add_db(dao=HolderDAO(session=session, redis=redis))
