from typing import Protocol

from aio_pika.abc import AbstractExchange


class ProducerServiceProtocol(Protocol):
    async def declare_exchange_and_queue(self) -> AbstractExchange:
        """Method that declares an exchange and a queue"""
        pass

    async def produce_message(
        self, message_body: list, exchange: AbstractExchange
    ) -> None:
        """Compose and publish the message"""
        pass

    async def send_periodic_messages(
        self, message_body: dict, interval: int = 10
    ) -> None:
        """Periodicly send messages to MQ"""
        pass
