from typing import Optional, Protocol

from fastapi import Request

from bet_maker.app.core.models.pydantic_models import Event, GetBet, PostBet


class PostBetServiceProtocol(Protocol):
    async def __call__(self, bet_data: PostBet, request: Request) -> GetBet:
        """Logic of betting"""
        pass

    def _find_event_by_name(
        self, name: str, events_list: list[Event | None]
    ) -> Optional[Event]:
        """Find an event by its name in the list of events"""
        pass


class GetBetsServiceProtocol(Protocol):
    async def __call__(self, request: Request) -> list[GetBet]:
        """Retrieve all user bets"""
        pass


class GetActiveBetsServiceProtocol(Protocol):
    async def __call__(self, request: Request) -> list[GetBet]:
        """Retrieve all user active bets"""
        pass
