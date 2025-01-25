from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import UUID4

from line_provider.app.core.custom_exceptions import EventNotFoundError, InvalidIDError
from line_provider.app.core.models import Event, EventCreate, EventStatus
from line_provider.app.core.schemas.repos_protocols import EventRepoProtocol


class GetEventService:
    def __init__(self, event_repo: EventRepoProtocol) -> None:
        self._event_repo = event_repo

    async def __call__(self, event_id: str) -> Event:
        try:
            event_uuid = UUID(event_id, version=4)
        except ValueError:
            raise InvalidIDError

        res_event = await self._event_repo.get_event(event_uuid)
        if not res_event:
            raise EventNotFoundError

        return res_event


class GetAllActiveEvents:
    def __init__(self, event_repo: EventRepoProtocol) -> None:
        self._event_repo = event_repo

    async def __call__(self) -> list[Event | None]:
        return await self._event_repo.get_all_active_events()


class GetAllEvents:
    def __init__(self, event_repo: EventRepoProtocol) -> None:
        self._event_repo = event_repo

    async def __call__(self) -> list[Event | None]:
        return await self._event_repo.get_all_events()


class PostEvent:
    def __init__(self, event_repo: EventRepoProtocol) -> None:
        self._event_repo = event_repo

    async def __call__(self, post_event_data: EventCreate) -> UUID4:
        new_uuid_flag = False
        while not new_uuid_flag:
            generated_uuid = self._generate_random_uuid()
            new_uuid_flag = await self._event_repo.check_uuid_uniqness(
                generated_uuid=generated_uuid
            )

        event = Event(
            name=post_event_data.name,
            coefficient=post_event_data.coefficient,
            deadline=int(datetime.now(timezone.utc).timestamp())
            + post_event_data.deadline,
            status=EventStatus.NEW,
            event_id=generated_uuid,
        )
        return await self._event_repo.post_event(event)

    def _generate_random_uuid(self) -> UUID4:
        return uuid4()
