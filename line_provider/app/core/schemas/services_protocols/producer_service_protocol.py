from typing import Protocol

from aio_pika.abc import AbstractChannel, AbstractExchange


class ProducerServiceProtocol(Protocol):
    async def ensure_connection_initialized(self) -> None:
        """Ensure that the connection is initialized and open"""
        pass

    async def _get_channel(self) -> AbstractChannel:
        """Get or create a RabbitMQ channel"""
        pass

    async def declare_exchange_and_queue(self) -> AbstractExchange:
        """Declare exchange and queue after ensuring connection is initialized"""
        pass

    async def produce_message(
        self, message_body: list, exchange: AbstractExchange
    ) -> None:
        """Produce a message and publish to the exchange"""
        pass

    async def send_periodic_messages(
        self, message_body: dict, interval: int = 1
    ) -> None:
        """Send periodic messages with a specified interval"""
        pass
