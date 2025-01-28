from fastapi import Depends, Response
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.app.core.schemas.repo_protocols import (
    AuthRepoProtocol,
    BetRepoProtocol,
    CommonRepoProtocol,
    RedisRepoProtocol,
    UserRepoProtocol,
)
from bet_maker.app.core.schemas.service_protocols import (
    EstablishCookiesProtocol,
    GetEventsServiceProtocol,
    JWTServiceProtocol,
    LoginAuthServiceProtocol,
    PostBetServiceProtocol,
    RegisterAuthServiceProtocol,
    ReissueTokenServiceProtocol,
)
from bet_maker.app.repositories.auth_repo import AuthRepo
from bet_maker.app.repositories.bets_repo import BetRepo
from bet_maker.app.repositories.common_repo import CommonRepo
from bet_maker.app.repositories.redis_repo import RedisRepo
from bet_maker.app.repositories.user_repo import UserRepo
from bet_maker.app.services.auth_service import (
    LoginAuthService,
    RegisterAuthService,
    ReissueTokenService,
)
from bet_maker.app.services.bet_service import PostBetService
from bet_maker.app.services.cookie_service import EstablishCookies
from bet_maker.app.services.events_service import GetEventsService
from bet_maker.app.services.jwt_service import JWTService
from shared.configs.database import get_session
from shared.configs.redis import get_redis_connection


def get_auth_repo(session: AsyncSession = Depends(get_session)) -> AuthRepoProtocol:
    return AuthRepo(session)


def get_common_repo(session: AsyncSession = Depends(get_session)) -> CommonRepoProtocol:
    return CommonRepo(session)


def get_cookie_service(response: Response) -> EstablishCookiesProtocol:
    return EstablishCookies(response)


def get_jwt_service(
    common_repo: CommonRepoProtocol = Depends(get_common_repo),
) -> JWTServiceProtocol:
    return JWTService(common_repo)


def get_register_service(
    auth_repo: AuthRepoProtocol = Depends(get_auth_repo),
    common_repo: CommonRepoProtocol = Depends(get_common_repo),
) -> RegisterAuthServiceProtocol:
    return RegisterAuthService(auth_repo, common_repo)


def get_login_service(
    jwt_service: JWTServiceProtocol = Depends(get_jwt_service),
    cookie_service: EstablishCookiesProtocol = Depends(get_cookie_service),
) -> LoginAuthServiceProtocol:
    return LoginAuthService(jwt_service, cookie_service)


def get_reissue_service(
    jwt_service: JWTServiceProtocol = Depends(get_jwt_service),
    cookie_service: EstablishCookiesProtocol = Depends(get_cookie_service),
    common_repo: CommonRepoProtocol = Depends(get_common_repo),
) -> ReissueTokenServiceProtocol:
    return ReissueTokenService(jwt_service, cookie_service, common_repo)


def get_redis_repo(
    redis_con: Redis = Depends(get_redis_connection),
) -> RedisRepoProtocol:
    return RedisRepo(redis_con)


def get_events_service(
    redis_repo: RedisRepoProtocol = Depends(get_redis_repo),
) -> GetEventsServiceProtocol:
    return GetEventsService(redis_repo)


def get_bet_repo(
    session: AsyncSession = Depends(get_session),
) -> BetRepoProtocol:
    return BetRepo(session)


def get_user_repo(
    session: AsyncSession = Depends(get_session),
) -> UserRepoProtocol:
    return UserRepo(session)


def get_post_bet_service(
    bet_repo: BetRepoProtocol = Depends(get_bet_repo),
    event_service: GetEventsServiceProtocol = Depends(get_events_service),
    user_repo: UserRepoProtocol = Depends(get_user_repo),
    jwt_service: JWTServiceProtocol = Depends(get_jwt_service),
) -> PostBetServiceProtocol:
    return PostBetService(bet_repo, event_service, user_repo, jwt_service)
