from types import TracebackType
from typing import Optional

from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection
from aio_pika.exceptions import AMQPConnectionError

from .settings import RabbitSettings


class RabbitBaseConnection:
    def __init__(self, rbmq_settings: "RabbitSettings") -> None:
        self.rbmq_settings = rbmq_settings
        self._connection: Optional[AbstractRobustConnection] = None

    async def connect(self) -> None:
        """Establish a connection to RabbitMQ."""
        if not self._connection or self._connection.is_closed:
            try:
                self._connection = await connect_robust(self.rbmq_settings.mq_uri)
            except AMQPConnectionError as e:
                raise ConnectionError("Failed to connect to RabbitMQ") from e

    @property
    def connection(self) -> AbstractRobustConnection:
        """Get the connection, raise an error if not initialized."""
        if not self._connection or self._connection.is_closed:
            raise RuntimeError(
                "RabbitMQ connection is not initialized or already closed."
            )
        return self._connection

    async def close(self) -> None:
        """Close the connection."""
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None

    async def __aenter__(self) -> "RabbitBaseConnection":
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type] = None,
        exc_val: Optional[Exception] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        await self.close()
