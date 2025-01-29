from email_validator import validate_email
from email_validator.exceptions_types import EmailNotValidError
from jwt.exceptions import InvalidTokenError
from pydantic import UUID4

from bet_maker.app.core.custom_exceptions import (
    ExpectRefreshTokenError,
    UserWithThisEmailExistsError,
)
from bet_maker.app.core.models.pydantic_models import (
    JWTTokenInfo,
    RegisterUser,
)
from bet_maker.app.core.schemas.repo_protocols import (
    AuthRepoProtocol,
    CommonRepoProtocol,
)
from bet_maker.app.core.schemas.service_protocols import (
    JWTServiceProtocol,
)
from shared.configs.settings import REFRESH_TOKEN


class RegisterAuthService:
    def __init__(
        self, auth_repo: AuthRepoProtocol, common_repo: CommonRepoProtocol
    ) -> None:
        self._auth_repo = auth_repo
        self._common_repo = common_repo

    async def __call__(self, user_data: RegisterUser) -> UUID4:
        try:
            validate_email(user_data.email)
        except Exception:
            raise EmailNotValidError

        check_user_exists_by_email = await self._common_repo.check_user_exists_by_email(
            user_data.email
        )
        if check_user_exists_by_email:
            raise UserWithThisEmailExistsError

        res = await self._auth_repo.register_user(user_data)
        return res


class LoginAuthService:
    def __init__(self, jwt_service: JWTServiceProtocol) -> None:
        self._jwt_service = jwt_service
        # self._cookie_service = cookie_service

    async def __call__(
        self,
        email: str,
        password: str,
    ) -> JWTTokenInfo:
        user = await self._jwt_service.validate_auth_user(email, password)
        access_token = await self._jwt_service.create_access_token(user.id)
        refresh_token = await self._jwt_service.create_refresh_token(user.id)
        # await self._cookie_service.send_access_token(access_token)
        # await self._cookie_service.send_refresh_token(refresh_token)
        return JWTTokenInfo(access_token=access_token, refresh_token=refresh_token)


class ReissueTokenService:
    def __init__(
        self,
        jwt_service: JWTServiceProtocol,
        common_repo: CommonRepoProtocol,
    ) -> None:
        self._jwt_service = jwt_service
        # self._cookie_service = cookie_service
        self._common_repo = common_repo

    async def __call__(self, token: str) -> JWTTokenInfo:
        try:
            token_payload = await self._jwt_service.decode_jwt(token)
        except Exception:
            raise InvalidTokenError

        if not await self._jwt_service.validation_token_type(
            REFRESH_TOKEN, token_payload
        ):
            raise ExpectRefreshTokenError

        user_data = await self._common_repo.get_user_data_by_token_sub(token_payload)

        access_token = await self._jwt_service.create_access_token(user_data.id)
        # await self._cookie_service.send_access_token(access_token)

        return JWTTokenInfo(access_token=access_token)
