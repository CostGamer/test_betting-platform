import asyncio
import json

from aio_pika import ExchangeType, Message
from aio_pika.abc import AbstractExchange

from shared.configs.rabbitmq import RabbitBase
from shared.utils.json_coder import change_transfer_data


class ProducerService:
    def __init__(self, rbmq_config: RabbitBase) -> None:
        self._rbmq_config = rbmq_config

    async def declare_exchange_and_queue(self) -> AbstractExchange:
        channel = self._rbmq_config.channel
        exchange = await channel.declare_exchange(
            name=self._rbmq_config.get_exchange_name, type=ExchangeType.DIRECT
        )
        queue = await channel.declare_queue(
            name=self._rbmq_config.get_routing_key, durable=True
        )
        await queue.bind(
            exchange=exchange, routing_key=self._rbmq_config.get_routing_key
        )
        return exchange

    async def produce_message(
        self, message_body: list, exchange: AbstractExchange
    ) -> None:
        message = Message(
            body=json.dumps(message_body).encode(),
        )
        await exchange.publish(
            message=message, routing_key=self._rbmq_config.get_routing_key
        )

    async def send_periodic_messages(
        self, message_body: dict, interval: int = 10
    ) -> None:
        exchange = await self.declare_exchange_and_queue()
        while True:
            new_message = await change_transfer_data(message_body)
            await self.produce_message(message_body=new_message, exchange=exchange)
            await asyncio.sleep(interval)
