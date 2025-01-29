from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from pydantic import UUID4

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
    "/event/{event_id}",
    response_model=Event,
    responses=get_event_responses,
    description="Retrieve detailed information about an event by its unique identifier",
)
@inject
async def get_event(
    event_id: str, event_service: FromDishka[GetEventServiceProtocol]
) -> Event:
    return await event_service(event_id)


@events_router.get(
    "/active",
    response_model=list[Event | None],
    description="Retrieve a list of all active events currently available",
)
@inject
async def get_active_events(
    event_service: FromDishka[GetAllActiveEventsProtocol],
) -> list[Event | None]:
    return await event_service()


@events_router.get(
    "/",
    response_model=list[Event | None],
    description="Retrieve a list of all possible events, both active and inactive",
)
@inject
async def get_all_possible_events(
    event_service: FromDishka[GetAllEventsProtocol],
) -> list[Event | None]:
    return await event_service()


@events_router.post(
    "/create_event",
    response_model=UUID4,
    description="Create a new event and return its unique identifier",
)
@inject
async def create_new_event(
    event: EventCreate,
    event_service: FromDishka[PostEventProtocol],
) -> UUID4:
    return await event_service(event)
