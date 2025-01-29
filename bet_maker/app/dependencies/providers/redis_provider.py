from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from shared.configs.redis import RedisBase
from shared.configs.settings import Settings


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_redis_base(self, settings: Settings) -> RedisBase:
        return RedisBase(settings.redis)

    @provide(scope=Scope.APP)
    async def get_redis_connection(
        self, redis_base: RedisBase, settings: Settings
    ) -> Redis:
        return await redis_base.get_redis_connection(settings.redis)
