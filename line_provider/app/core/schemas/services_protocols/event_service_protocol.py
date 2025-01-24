from typing import Protocol

from pydantic import UUID4

from line_provider.app.core.models import Event, EventCreate


class GetEventServiceProtocol(Protocol):
    async def __call__(self, event_id: str) -> Event:
        """Retrieve an event by its unique identifier"""
        pass


class GetAllActiveEventsProtocol(Protocol):
    async def __call__(self) -> list[Event | None]:
        """Retrieve all active events"""
        pass


class GetAllEventsProtocol(Protocol):
    async def __call__(self) -> list[Event | None]:
        """Retrieve all events"""
        pass


class PostEventProtocol(Protocol):
    async def __call__(self, post_event_data: EventCreate) -> UUID4:
        """Create a new event and return its unique identifier"""
        pass

    def _generate_random_uuid(self) -> UUID4:
        """Generate a random UUID"""
        pass
