from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.app.core.schemas.repo_protocols import (
    AuthRepoProtocol,
    CommonRepoProtocol,
)
from bet_maker.app.core.schemas.service_protocols import (
    EstablishCookiesProtocol,
    JWTServiceProtocol,
    LoginAuthServiceProtocol,
    RegisterAuthServiceProtocol,
    ReissueTokenServiceProtocol,
)
from bet_maker.app.repositories.auth_repo import AuthRepo
from bet_maker.app.repositories.common_repo import CommonRepo
from bet_maker.app.services.auth_service import (
    LoginAuthService,
    RegisterAuthService,
    ReissueTokenService,
)
from bet_maker.app.services.cookie_service import EstablishCookies
from bet_maker.app.services.jwt_service import JWTService
from shared.configs.database import get_session


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
