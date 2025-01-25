from types import TracebackType

from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from aio_pika.exceptions import AMQPConnectionError

from .settings import RabbitSettings


class RabbitBase:
    def __init__(self, rbmq_settings: RabbitSettings) -> None:
        self.rbmq_settings: RabbitSettings = rbmq_settings
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None

    async def connect(self) -> None:
        """Establish a connection to RabbitMQ and open a channel"""
        try:
            self._connection = await connect_robust(self.rbmq_settings.mq_uri)
            self._channel = await self._connection.channel()
        except AMQPConnectionError as e:
            raise ConnectionError("Failed to connect to RabbitMQ") from e

    @property
    def channel(self) -> AbstractChannel:
        """Get the open channel, raise an error if not initialized"""
        if self._channel is None or self._channel.is_closed:
            raise RuntimeError("RabbitMQ channel is not initialized or already closed")
        return self._channel

    @property
    def get_routing_key(self) -> str:
        return self.rbmq_settings.rabbit_rk

    @property
    def get_exchange_name(self) -> str:
        return self.rbmq_settings.rabbit_exchange

    async def close(self) -> None:
        """Close the channel and connection"""
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()

    async def __aenter__(self) -> "RabbitBase":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
