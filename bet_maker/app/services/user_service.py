from fastapi import Request
from pydantic import UUID4

from bet_maker.app.core.custom_exceptions import NotEnoughMoneyError
from bet_maker.app.core.models.pydantic_models.user_models import UserModel
from bet_maker.app.core.schemas.repo_protocols import UserRepoProtocol
from bet_maker.app.core.schemas.service_protocols import CommonServiceProtocol


class BaseUserService:
    def __init__(
        self, user_repo: UserRepoProtocol, common_service: CommonServiceProtocol
    ):
        self._user_repo = user_repo
        self._common_service = common_service

    async def _get_user_id(self, request: Request) -> UUID4:
        return await self._common_service._get_user_id(request)


class GetUserInfoService(BaseUserService):
    async def __call__(self, request: Request) -> UserModel:
        user_id = await self._get_user_id(request)
        return await self._user_repo.get_user_info(user_id)


class BalanceService(BaseUserService):
    async def top_up(self, amount: float, request: Request) -> float:
        user_id = await self._get_user_id(request)
        return await self._user_repo.change_user_balance(user_id, amount)

    async def withdraw(self, amount: float, request: Request) -> float:
        user_id = await self._get_user_id(request)
        balance = await self._user_repo.get_user_balance(user_id)
        if balance - amount < 0:
            raise NotEnoughMoneyError
        return await self._user_repo.change_user_balance(user_id, -amount)
