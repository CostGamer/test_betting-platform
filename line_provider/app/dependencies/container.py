from dishka import make_async_container

from line_provider.app.dependencies.providers import (
    ConfigsProvider,
    RabbitMQProvider,
    RepoProvidersLine,
    ServiceProvidersLine,
)

container = make_async_container(
    ConfigsProvider(), RabbitMQProvider(), ServiceProvidersLine(), RepoProvidersLine()
)
