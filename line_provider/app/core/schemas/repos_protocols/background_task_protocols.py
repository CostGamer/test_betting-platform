from typing import Protocol

from pydantic import UUID4

from line_provider.app.core.models import Event
from line_provider.app.core.models.events import EventStatus


class BackgroundTaskRepoProtocol(Protocol):
    async def change_event_status(
        self, event_id: UUID4, status: EventStatus
    ) -> Event | None:
        """Change the status of an event by its unique identifier"""
        pass

    async def create_event(self, event: Event) -> UUID4:
        """Create a new event and return its unique identifier"""
        pass
