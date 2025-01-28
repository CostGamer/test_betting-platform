from typing import Protocol

from pydantic import UUID4

from bet_maker.app.core.models.pydantic_models import GetBet, PostBetDTO


class BetRepoProtocol(Protocol):
    async def make_bet(self, bet_data: PostBetDTO) -> GetBet:
        """Insert new bet to DB"""
        pass

    async def fetch_active_bet(self, user_id: UUID4) -> list[GetBet]:
        """Retrieve active bets"""
        pass

    async def fetch_all_user_bets(self, user_id: UUID4) -> list[GetBet]:
        """Retrieve bets history"""
        pass
