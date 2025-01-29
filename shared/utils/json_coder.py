from typing import Any

from pydantic import UUID4

from line_provider.app.core.models import Event


async def change_transfer_data(event_data: dict[UUID4, Event]) -> list[dict[str, Any]]:
    return [
        {
            "name": event.name,
            "coefficient": float(event.coefficient),
            "status": event.status,
            "event_id": str(event.event_id),
        }
        for event in event_data.values()
    ]
