from typing import Protocol

from bet_maker.app.core.models.pydantic_models import JWTUser


class CommonRepoProtocol(Protocol):
    async def check_user_exists_by_email(self, email: str) -> bool:
        """Check email already in DB"""
        pass

    async def get_user_data(self, email: str) -> JWTUser:
        """Retrieve user's data for JWT"""
        pass

    async def get_user_data_by_token_sub(self, payload: dict) -> JWTUser:
        """Retrieve uses's data from JWT"""
        pass
