from typing import Optional, Protocol

from fastapi import Request
from pydantic import UUID4

from bet_maker.app.core.models.pydantic_models import Event, GetBet, PostBet


class PostBetServiceProtocol(Protocol):
    async def __call__(self, bet_data: PostBet, request: Request) -> GetBet:
        """Logic of betting"""
        pass

    def _find_event_by_name(
        self, name: str, events_list: list[Event]
    ) -> Optional[Event]:
        """Find an event by its name in the list of events."""
        pass

    async def _get_user_id(self, request: Request) -> UUID4:
        """Extract user ID from the JWT token in the request."""
        pass
