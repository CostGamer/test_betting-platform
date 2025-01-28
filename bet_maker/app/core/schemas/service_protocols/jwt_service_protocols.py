from typing import Protocol

from fastapi import Request
from pydantic import UUID4

from bet_maker.app.core.models.pydantic_models import JWTUser


class JWTServiceProtocol(Protocol):
    async def validate_password(
        self,
        password: str,
        hash_password: bytes,
    ) -> bool:
        """Validate the provided password against the stored hash"""
        pass

    async def validate_auth_user(self, email: str, password: str) -> JWTUser:
        """Validate the user's credentials and return a JWTUser object"""
        pass

    async def encode_jwt(
        self,
        payload: dict,
        secret: str = ...,
        algorithm: str = ...,
        expire_minutes: int = ...,
        expire_timedelta: int | None = ...,
    ) -> str:
        """Generate a JWT token with the given payload and expiration settings"""
        pass

    async def decode_jwt(
        self,
        token: str | bytes,
        secret: str = ...,
        algorithm: str = ...,
    ) -> dict:
        """Decode and validate a JWT token, returning its payload"""
        pass

    async def create_jwt(
        self,
        token_type: str,
        token_data: dict,
        expire_minutes: int = ...,
        expire_timedelta: int | None = ...,
    ) -> str:
        """Create a custom JWT token of the specified type"""
        pass

    async def create_access_token(self, user_id: UUID4) -> str:
        """Generate an access token for the given user ID"""
        pass

    async def create_refresh_token(self, user_id: UUID4) -> str:
        """Generate a refresh token for the given user ID"""
        pass

    async def validation_token_type(self, jwt_type: str, payload: dict) -> bool:
        """Check token type is correct"""
        pass

    async def get_token_from_response(self, request: Request) -> str:
        """Decode JWT from request"""
        pass
