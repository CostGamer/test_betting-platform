from redis.asyncio import Redis


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def send_message(self, message: str, redis_key: str = "line_events") -> None:
        await self._redis.set(redis_key, message)
