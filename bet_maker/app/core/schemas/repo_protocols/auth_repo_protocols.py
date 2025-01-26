from typing import Protocol

from pydantic import UUID4

from bet_maker.app.core.models.pydantic_models import RegisterUser


class AuthRepoProtocol(Protocol):
    async def register_user(self, user: RegisterUser) -> UUID4:
        """Registering a new user"""
        pass

    async def _hash_password(self, password: str) -> bytes:
        """Hashing user password"""
        pass
