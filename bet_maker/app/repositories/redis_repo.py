import json

from redis.asyncio import Redis


class RedisRepo:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def send_message(self, message: str, redis_key: str = "line_events") -> None:
        await self._redis.set(redis_key, message)

    async def get_message(self, redis_key: str = "line_events") -> list[dict]:
        return json.loads(await self._redis.get(redis_key))
