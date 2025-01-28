from typing import Protocol

from pydantic import UUID4


class UserRepoProtocol(Protocol):
    async def get_user_balance(self, user_id: UUID4) -> float:
        """Show specific user balance"""
        pass

    async def change_user_balance(self, user_id: UUID4, amount: float) -> float:
        """Decreese or increase user balance"""
        pass
