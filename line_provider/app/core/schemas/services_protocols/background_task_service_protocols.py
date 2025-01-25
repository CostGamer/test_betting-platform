from datetime import datetime
from typing import Protocol

from line_provider.app.core.models import Event


class CheckStatusServiceProtocol(Protocol):
    async def _check_event_status(self, event: Event, current_time: datetime) -> None:
        """Check and change event status"""
        pass

    async def check_all_events(self) -> None:
        """Constanly check all events"""
        pass


class CreateEventServiceProtocol(Protocol):
    async def _create_random_event(self) -> None:
        """Generate random event"""
        pass

    async def create_events_periodically(self) -> None:
        """Loop for creating events"""
        pass
