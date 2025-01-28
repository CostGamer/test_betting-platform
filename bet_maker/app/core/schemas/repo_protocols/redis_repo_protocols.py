from typing import Protocol


class RedisRepoProtocol(Protocol):
    async def send_message(self, message: str, redis_key: str = ...) -> None:
        """Send a message to Redis with the specified key"""
        pass

    async def get_message(self, redis_key: str = ...) -> list:
        """Retrieve a message from Redis by the specified key"""
        pass
