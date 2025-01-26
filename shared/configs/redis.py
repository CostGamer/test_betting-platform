from redis.asyncio import ConnectionPool, Redis

from shared.configs.settings import RedisSettings


class RedisBase:
    def __init__(self, redis_settings: RedisSettings):
        self._redis_settings = redis_settings
        self._pool: ConnectionPool | None = None

    async def get_redis_connection(self) -> Redis:
        if not self._pool:
            self._pool = ConnectionPool(
                host=self._redis_settings.redis_host,
                port=self._redis_settings.redis_port,
                db=self._redis_settings.redis_db,
                max_connections=self._redis_settings.redis_max_conn,
            )
        return Redis(connection_pool=self._pool)

    async def close(self) -> None:
        if self._pool:
            await self._pool.disconnect()
