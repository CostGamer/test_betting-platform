from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from bet_maker.app.core.models.pydantic_models import Event
from bet_maker.app.services.events_service import GetEventsService

events_router = APIRouter(prefix="/events", tags=["events"])


@events_router.get(
    "/events",
    response_model=list[Event | None],
    description="Get all possible events for betting",
)
@inject
async def get_events(
    events_service: FromDishka[GetEventsService],
) -> list[Event | None]:
    return await events_service.get_active_events()
