from dishka import Provider, Scope, provide

from shared.configs.rabbitmq import RabbitBaseConnection
from shared.configs.settings import Settings


class RabbitMQProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_rabbitmq_connection(self, settings: Settings) -> RabbitBaseConnection:
        return RabbitBaseConnection(settings)
