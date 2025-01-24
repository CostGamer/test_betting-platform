from fastapi import APIRouter, Depends

from line_provider.app.api.dependencies import get_event_service
from line_provider.app.api.exception_responses.responses import get_event_responses
from line_provider.app.core.models import Event
from line_provider.app.core.schemas.services_protocols import (
    GetEventServiceProtocol,
)

events_router = APIRouter(prefix="/events", tags=["/events"])


@events_router.get(
    "/{event_id}",
    response_model=Event,
    responses=get_event_responses,
    description="Retrieve detailed information about an event by its unique identifier",
)
async def get_event(
    event_id: str, event_service: GetEventServiceProtocol = Depends(get_event_service)
) -> Event:
    return await event_service(event_id)
