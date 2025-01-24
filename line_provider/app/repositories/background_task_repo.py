from datetime import datetime, timezone

from pydantic import UUID4

from line_provider.app.core.models import Event, EventStatus
from line_provider.app.storage import events


class BackgroundTaskRepo:
    async def change_event_status(
        self, event_id: UUID4, status: EventStatus
    ) -> Event | None:
        event = events.get(event_id)
        if event:
            event.status = status
            event.updated_at = datetime.now(timezone.utc)
            return event
        return None

    async def create_event(self, event: Event) -> UUID4:
        events[event.event_id] = event
        return event.event_id
