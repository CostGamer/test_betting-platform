from logging import getLogger
from types import TracebackType

from redis.asyncio import ConnectionPool, Redis

from shared.configs.settings import RedisSettings

logger = getLogger(__name__)


class RedisBase:
    def __init__(self, redis_settings: RedisSettings):
        self._redis_settings = redis_settings
        self._pool: ConnectionPool | None = None
        self._redis_connection: Redis | None = None

    async def get_redis_connection(self) -> Redis:
        if not self._pool:
            self._pool = ConnectionPool(
                host=self._redis_settings.redis_host,
                port=self._redis_settings.redis_port,
                db=self._redis_settings.redis_db,
                max_connections=self._redis_settings.redis_max_conn,
            )
        logger.info("Redis connection pool created.")
        return Redis(connection_pool=self._pool)

    async def close(self) -> None:
        if self._redis_connection:
            await self._redis_connection.close()

    async def __aenter__(self) -> Redis:
        self._redis_connection = await self.get_redis_connection()
        return self._redis_connection

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
