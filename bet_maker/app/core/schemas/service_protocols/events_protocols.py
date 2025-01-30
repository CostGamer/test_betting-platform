from typing import Protocol

from bet_maker.app.core.models.pydantic_models import Event


class GetEventsServiceProtocol(Protocol):
    async def get_active_events(self) -> list[Event | None]:
        """Retrieve a list of active events"""
        pass

    def _filter_events(self, events: list[dict]) -> list[Event | None]:
        """Filter events to include only active ones based on their status"""
        pass

    async def get_all_events(self) -> list[Event | None]:
        """Retrieve a list of events"""
        pass
