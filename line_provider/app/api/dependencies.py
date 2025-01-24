from fastapi import Depends

from line_provider.app.core.schemas.repos_protocols import EventRepoProtocol
from line_provider.app.core.schemas.services_protocols import (
    GetAllActiveEventsProtocol,
    GetAllEventsProtocol,
    GetEventServiceProtocol,
    PostEventProtocol,
)
from line_provider.app.repositories.events_repo import EventRepo
from line_provider.app.services.event_service import (
    GetAllActiveEvents,
    GetAllEvents,
    GetEventService,
    PostEvent,
)


def get_event_repo() -> EventRepoProtocol:
    return EventRepo()


def get_event_service(
    event_repo: EventRepoProtocol = Depends(get_event_repo),
) -> GetEventServiceProtocol:
    return GetEventService(event_repo)


def get_all_active_events(
    event_repo: EventRepoProtocol = Depends(get_event_repo),
) -> GetAllActiveEventsProtocol:
    return GetAllActiveEvents(event_repo)


def get_all_events(
    event_repo: EventRepoProtocol = Depends(get_event_repo),
) -> GetAllEventsProtocol:
    return GetAllEvents(event_repo)


def get_post_event(
    event_repo: EventRepoProtocol = Depends(get_event_repo),
) -> PostEventProtocol:
    return PostEvent(event_repo)
