from typing import Protocol

from fastapi import Request
from pydantic import UUID4

from bet_maker.app.core.models.pydantic_models import UserModel


class BaseUserServiceProtocol(Protocol):
    async def _get_user_id(self, request: Request) -> UUID4:
        """Retrieve user id from JWT"""
        pass


class GetUserInfoServiceProtocol(Protocol):
    async def __call__(self, request: Request) -> UserModel:
        """Give user info"""
        pass


class BalanceServiceProtocol(Protocol):
    async def top_up(self, amount: float, request: Request) -> float:
        """Logic of top up the balance"""
        pass

    async def withdraw(self, amount: float, request: Request) -> float:
        """Logic of withdraw the balance"""
        pass
