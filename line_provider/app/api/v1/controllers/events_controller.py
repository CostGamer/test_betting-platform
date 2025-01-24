from fastapi import APIRouter, Depends
from pydantic import UUID4

from line_provider.app.api.dependencies import (
    get_all_active_events,
    get_all_events,
    get_event_service,
    get_post_event,
)
from line_provider.app.api.exception_responses.responses import get_event_responses
from line_provider.app.core.models import Event
from line_provider.app.core.models.events import EventCreate
from line_provider.app.core.schemas.services_protocols import (
    GetAllActiveEventsProtocol,
    GetAllEventsProtocol,
    GetEventServiceProtocol,
    PostEventProtocol,
)

events_router = APIRouter(prefix="/events", tags=["/events"])


@events_router.get(
    "event/{event_id}",
    response_model=Event,
    responses=get_event_responses,
    description="Retrieve detailed information about an event by its unique identifier",
)
async def get_event(
    event_id: str, event_service: GetEventServiceProtocol = Depends(get_event_service)
) -> Event:
    return await event_service(event_id)


@events_router.get(
    "/active",
    response_model=list[Event | None],
    description="",
)
async def get_active_events(
    event_service: GetAllActiveEventsProtocol = Depends(get_all_active_events),
) -> list[Event | None]:
    return await event_service()


@events_router.get(
    "/",
    response_model=list[Event | None],
    description="",
)
async def get_all_possible_events(
    event_service: GetAllEventsProtocol = Depends(get_all_events),
) -> list[Event | None]:
    return await event_service()


@events_router.post(
    "/create_event",
    response_model=UUID4,
    description="",
)
async def create_new_event(
    event: EventCreate, event_service: PostEventProtocol = Depends(get_post_event)
) -> UUID4:
    return await event_service(event)
