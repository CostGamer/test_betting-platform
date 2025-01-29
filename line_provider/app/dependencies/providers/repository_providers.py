from dishka import Provider, Scope, provide

from line_provider.app.core.schemas.repos_protocols import (
    BackgroundTaskRepoProtocol,
    EventRepoProtocol,
)
from line_provider.app.repositories.background_task_repo import BackgroundTaskRepo
from line_provider.app.repositories.events_repo import EventRepo


class RepoProvidersLine(Provider):
    @provide(scope=Scope.APP)
    async def get_background_task_repo(self) -> BackgroundTaskRepoProtocol:
        return BackgroundTaskRepo()

    @provide(scope=Scope.REQUEST)
    async def get_event_repo(self) -> EventRepoProtocol:
        return EventRepo()
