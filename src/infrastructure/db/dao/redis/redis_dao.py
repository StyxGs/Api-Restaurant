from redis.asyncio import Redis

from src.core.models.redis import RedisKeys


class RedisDAO:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.keys = RedisKeys()

    async def save(self, key: str, data: str):
        await self.redis.set(key, data, ex=600)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def check_exist_key(self, key: str) -> int:
        return await self.redis.exists(key)

    async def delete(self, keys: list):
        await self.redis.delete(*keys)
