from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from pydantic import UUID4

from bet_maker.app.core.custom_exceptions import InvalidUsernameOrPasswordError
from bet_maker.app.core.models.pydantic_models import JWTUser
from bet_maker.app.core.schemas.repo_protocols.common_repo_protocols import (
    CommonRepoProtocol,
)
from shared.configs import all_settings
from shared.configs.settings import ACCESS_TOKEN, REFRESH_TOKEN, TOKEN_TYPE_FIELD


class JWTService:
    def __init__(self, common_repo: CommonRepoProtocol) -> None:
        self._common_repo = common_repo

    async def validate_password(
        self,
        password: str,
        hash_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hash_password,
        )

    async def validate_auth_user(self, email: str, password: str) -> JWTUser:
        check_user_exists_by_email = await self._common_repo.check_user_exists_by_email(
            email
        )
        if not check_user_exists_by_email:
            raise InvalidUsernameOrPasswordError

        user_data = await self._common_repo.get_user_data(email)
        check_password_correctness = await self.validate_password(
            password=password, hash_password=user_data.password
        )
        if not check_password_correctness:
            raise InvalidUsernameOrPasswordError
        return user_data

    async def encode_jwt(
        self,
        payload: dict,
        secret: str = all_settings.jwt.jwt_secret,
        algorithm: str = all_settings.jwt.jwt_algorithm,
        expire_minutes: int = all_settings.jwt.jwt_access_token_expire_minutes,
        expire_timedelta: int | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        expire = (
            now + timedelta(days=expire_timedelta)
            if expire_timedelta
            else now + timedelta(minutes=expire_minutes)
        )
        to_encode.update(iat=now, exp=expire)
        encoded = jwt.encode(payload=to_encode, key=secret, algorithm=algorithm)
        return encoded

    async def decode_jwt(
        self,
        token: str | bytes,
        secret: str = all_settings.jwt.jwt_secret,
        algorithm: str = all_settings.jwt.jwt_algorithm,
    ) -> dict:
        decoded = jwt.decode(jwt=token, key=secret, algorithms=[algorithm])
        return decoded

    async def create_jwt(
        self,
        token_type: str,
        token_data: dict,
        expire_minutes: int = all_settings.jwt.jwt_access_token_expire_minutes,
        expire_timedelta: int | None = None,
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return await self.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    async def create_access_token(self, user_id: UUID4) -> str:
        jwt_payload = {"sub": str(user_id)}
        return await self.create_jwt(
            token_type=ACCESS_TOKEN,
            token_data=jwt_payload,
            expire_minutes=all_settings.jwt.jwt_access_token_expire_minutes,
        )

    async def create_refresh_token(self, user_id: UUID4) -> str:
        jwt_payload = {"sub": str(user_id)}
        return await self.create_jwt(
            token_type=REFRESH_TOKEN,
            token_data=jwt_payload,
            expire_timedelta=all_settings.jwt.jwt_refresh_token_expire_days,
        )

    async def validation_token_type(self, jwt_type: str, payload: dict) -> bool:
        current_token_type = payload.get(TOKEN_TYPE_FIELD)
        if current_token_type == jwt_type:
            return True
        return False
