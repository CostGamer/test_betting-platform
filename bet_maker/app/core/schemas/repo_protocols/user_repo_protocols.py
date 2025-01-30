from typing import Protocol

from pydantic import UUID4

from bet_maker.app.core.models.pydantic_models import UserModel


class UserRepoProtocol(Protocol):
    async def get_user_balance(self, user_id: UUID4) -> float:
        """Extract specific user balance"""
        pass

    async def change_user_balance(self, user_id: UUID4, amount: float) -> float:
        """Decreese or increase user balance"""
        pass

    async def get_user_info(
        self,
        user_id: UUID4,
    ) -> UserModel:
        """Extract user info"""
        pass
