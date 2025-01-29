from dishka import make_async_container

from bet_maker.app.dependencies.providers import (
    ConfigsProvider,
    DatabaseConnectionProvider,
    RabbitMQProvider,
    RedisProvider,
    RepoProvidersBet,
    ServiceProvidersLine,
)

container = make_async_container(
    DatabaseConnectionProvider(),
    RedisProvider(),
    RepoProvidersBet(),
    ServiceProvidersLine(),
    ConfigsProvider(),
    RabbitMQProvider(),
)
