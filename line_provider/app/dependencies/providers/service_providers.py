from dishka import Provider, Scope, provide

from line_provider.app.core.schemas.repos_protocols import (
    BackgroundTaskRepoProtocol,
    EventRepoProtocol,
)
from line_provider.app.core.schemas.services_protocols import (
    CheckStatusServiceProtocol,
    CreateEventServiceProtocol,
    GetAllActiveEventsProtocol,
    GetAllEventsProtocol,
    GetEventServiceProtocol,
    PostEventProtocol,
    ProducerServiceProtocol,
)
from line_provider.app.services.background_task_service import (
    CheckStatusService,
    CreateEventService,
)
from line_provider.app.services.event_service import (
    GetAllActiveEvents,
    GetAllEvents,
    GetEventService,
    PostEvent,
)
from line_provider.app.services.producer_service import ProducerService
from shared.configs.rabbitmq import RabbitBaseConnection
from shared.configs.settings import Settings


class ServiceProvidersLine(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_event_service(
        self, event_repo: EventRepoProtocol
    ) -> GetEventServiceProtocol:
        return GetEventService(event_repo)

    @provide(scope=Scope.REQUEST)
    async def get_check_status_service(
        self,
        bg_task_repo: BackgroundTaskRepoProtocol,
        event_repo: EventRepoProtocol,
    ) -> CheckStatusServiceProtocol:
        return CheckStatusService(bg_task_repo, event_repo)

    @provide(scope=Scope.REQUEST)
    async def get_producer_service(
        self, rbmq_config: RabbitBaseConnection, settings: Settings
    ) -> ProducerServiceProtocol:
        return ProducerService(rbmq_config, settings)

    @provide(scope=Scope.REQUEST)
    async def get_create_event_service(
        self, bg_task_repo: BackgroundTaskRepoProtocol
    ) -> CreateEventServiceProtocol:
        return CreateEventService(bg_task_repo)

    @provide(scope=Scope.REQUEST)
    async def get_all_active_events(
        self, event_repo: EventRepoProtocol
    ) -> GetAllActiveEventsProtocol:
        return GetAllActiveEvents(event_repo)

    @provide(scope=Scope.REQUEST)
    async def get_all_events(
        self, event_repo: EventRepoProtocol
    ) -> GetAllEventsProtocol:
        return GetAllEvents(event_repo)

    @provide(scope=Scope.REQUEST)
    async def get_post_event(self, event_repo: EventRepoProtocol) -> PostEventProtocol:
        return PostEvent(event_repo)
