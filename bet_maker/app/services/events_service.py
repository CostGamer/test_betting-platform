from bet_maker.app.core.models.pydantic_models import Event
from bet_maker.app.core.schemas.repo_protocols import RedisRepoProtocol


class GetEventsService:
    def __init__(self, redis_repo: RedisRepoProtocol) -> None:
        self._redis_repo = redis_repo

    async def get_active_events(self) -> list[Event | None]:
        all_events = await self._redis_repo.get_message()
        events = self._filter_events(all_events)
        return events

    def _filter_events(self, events: list[dict]) -> list[Event | None]:
        return [Event(**event) for event in events if event.get("status") == 1]
