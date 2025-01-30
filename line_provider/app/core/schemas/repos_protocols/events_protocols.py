from typing import Protocol

from pydantic import UUID4

from line_provider.app.core.models import Event


class EventRepoProtocol(Protocol):
    async def get_event(self, event_id: UUID4) -> Event | None:
        """Retrieve an event by its unique identifier"""
        pass

    async def get_all_active_events(self) -> list[Event | None]:
        """Retrieve all active events"""
        pass

    async def get_all_events(self) -> list[Event | None]:
        """Retrieve all events"""
        pass

    async def post_event(self, event_data: Event) -> UUID4:
        """Create a new event and return its unique identifier"""
        pass

    async def check_uuid_uniqness(self, generated_uuid: UUID4) -> bool:
        """Check if the generated UUID is unique"""
        pass
