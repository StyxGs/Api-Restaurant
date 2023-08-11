import pickle
from uuid import UUID

from src.infrastructure.db.dao.redis.redis_dao import RedisDAO


def removing_keys_with_value_of_none(func):
    def wrapp(obj, **keys):
        keys_without_none = {key: value for key, value in keys.items() if value}
        return func(obj, **keys_without_none)

    return wrapp


async def get_data(dao, key: str, redis: RedisDAO, data_id: UUID | None = None) -> list:
    if await redis.check_exist_key(key):
        data = await redis.get(key)
        obj = pickle.loads(data)
    else:
        if data_id:
            obj = await dao.get_list(data_id)
        else:
            obj = await dao.get_list()
        await redis.save(key, pickle.dumps(obj))
    return obj
