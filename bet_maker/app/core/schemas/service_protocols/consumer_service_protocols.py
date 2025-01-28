from typing import Protocol

from aio_pika.abc import AbstractChannel, AbstractIncomingMessage, AbstractQueue


class ConsumerServiceProtocol(Protocol):
    async def _reconnect_rabbitmq(self) -> None:
        """Re-establish connection to RabbitMQ if necessary"""
        pass

    async def _create_channel(self) -> AbstractChannel:
        """Create and return a new RabbitMQ channel"""
        pass

    async def _declare_queue(
        self, channel: AbstractChannel, queue_name: str
    ) -> AbstractQueue:
        """Declare a RabbitMQ queue"""
        pass

    async def consume_message(self, queue_name: str) -> None:
        """Consume messages from RabbitMQ and process them"""
        pass

    async def _process_message(self, message: AbstractIncomingMessage) -> None:
        """Process an individual message"""
        pass

    async def consume_forever(self, queue_name: str) -> None:
        """Continuously consume messages from RabbitMQ"""
        pass
