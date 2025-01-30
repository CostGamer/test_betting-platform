from typing import Protocol

from pydantic import UUID4

from bet_maker.app.core.models.pydantic_models import ActiveBets, GetBet, PostBetDTO


class BetRepoProtocol(Protocol):
    async def make_bet(self, bet_data: PostBetDTO) -> GetBet:
        """Insert new bet to DB"""
        pass

    async def fetch_active_bet(self, user_id: UUID4) -> list[GetBet]:
        """Retrieve active user bets"""
        pass

    async def fetch_all_user_bets(self, user_id: UUID4) -> list[GetBet]:
        """Retrieve user bets history"""
        pass

    async def fetch_all_active_bets(self) -> list[ActiveBets]:
        """Retrieve all active bets"""

    async def change_bet_status(
        self, result: int, name: str, event_id: UUID4
    ) -> list[GetBet]:
        """Change bet status (win/lose)"""
        pass
