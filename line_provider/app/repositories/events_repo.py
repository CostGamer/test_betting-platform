from pydantic import UUID4

from line_provider.app.core.models import Event, EventStatus
from line_provider.app.storage import events


class EventRepo:
    async def get_event(self, event_id: UUID4) -> Event | None:
        return events.get(event_id, None)

    async def get_all_active_events(self) -> list[Event | None]:
        return [event for event in events.values() if event.status == EventStatus.NEW]

    async def get_all_events(self) -> list[Event | None]:
        return list(events.values())

    async def post_event(self, event_data: Event) -> UUID4:
        events[event_data.event_id] = event_data
        return event_data.event_id

    async def check_uuid_uniqness(self, generated_uuid: UUID4) -> bool:
        return events.get(generated_uuid, None) is not None
