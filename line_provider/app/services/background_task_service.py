import asyncio
import random
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from line_provider.app.core.fc_storage import football_teams
from line_provider.app.core.models import Event, EventStatus
from line_provider.app.core.schemas.repos_protocols import (
    BackgroundTaskRepoProtocol,
    EventRepoProtocol,
)


class CheckStatusService:
    def __init__(
        self, bg_task_repo: BackgroundTaskRepoProtocol, event_repo: EventRepoProtocol
    ) -> None:
        self._bg_task_repo = bg_task_repo
        self._event_repo = event_repo

    async def _check_event_status(self, event: Event, current_time: datetime) -> None:
        if (
            event.deadline is not None
            and int(current_time.timestamp()) >= event.deadline
        ):
            if event.status == EventStatus.NEW:
                status = random.choice(
                    [EventStatus.FINISHED_WIN, EventStatus.FINISHED_LOSE]
                )
                await self._bg_task_repo.change_event_status(event.event_id, status)

    async def check_all_events(self) -> None:
        while True:
            current_time = datetime.now(timezone.utc)
            events = await self._event_repo.get_all_events()
            for event in events:
                if event:
                    await self._check_event_status(event, current_time)
            await asyncio.sleep(1)


class CreateEventService:
    def __init__(self, bg_task_repo: BackgroundTaskRepoProtocol) -> None:
        self._bg_task_repo = bg_task_repo

    async def _create_random_event(self) -> None:
        team_1 = random.choice(football_teams)
        team_2 = random.choice([team for team in football_teams if team != team_1])
        coefficient = Decimal(str(round(random.uniform(1.5, 2.5), 2)))
        deadline = int(datetime.now(timezone.utc).timestamp()) + random.randint(50, 400)
        event_id = uuid4()

        event = Event(
            name=f"{team_1} - {team_2}",
            coefficient=coefficient,
            deadline=deadline,
            event_id=event_id,
            status=EventStatus.NEW,
        )

        await self._bg_task_repo.create_event(event)

    async def create_events_periodically(self) -> None:
        while True:
            try:
                await self._create_random_event()
            except Exception as e:
                print(f"Error creating event: {e}")
            await asyncio.sleep(30)
