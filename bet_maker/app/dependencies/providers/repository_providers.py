from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.app.core.schemas.repo_protocols import (
    AuthRepoProtocol,
    BetRepoProtocol,
    CommonRepoProtocol,
    RedisRepoProtocol,
    UserRepoProtocol,
)
from bet_maker.app.repositories.auth_repo import AuthRepo
from bet_maker.app.repositories.bets_repo import BetRepo
from bet_maker.app.repositories.common_repo import CommonRepo
from bet_maker.app.repositories.redis_repo import RedisRepo
from bet_maker.app.repositories.user_repo import UserRepo


class RepoProvidersBet(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_redis_repo(self, redis: Redis) -> RedisRepoProtocol:
        return RedisRepo(redis)

    @provide(scope=Scope.REQUEST)
    async def get_bet_repo(self, con: AsyncSession) -> BetRepoProtocol:
        return BetRepo(con)

    @provide(scope=Scope.REQUEST)
    async def get_user_repo(self, con: AsyncSession) -> UserRepoProtocol:
        return UserRepo(con)

    @provide(scope=Scope.REQUEST)
    async def get_auth_repo(self, con: AsyncSession) -> AuthRepoProtocol:
        return AuthRepo(con)

    @provide(scope=Scope.REQUEST)
    async def get_common_repo(self, con: AsyncSession) -> CommonRepoProtocol:
        return CommonRepo(con)
