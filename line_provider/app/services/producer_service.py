import asyncio
import json
from logging import getLogger

from aio_pika import ExchangeType, Message
from aio_pika.abc import AbstractChannel, AbstractExchange

from shared.configs import all_settings
from shared.configs.rabbitmq import RabbitBaseConnection
from shared.utils.json_coder import change_transfer_data

logger = getLogger(__name__)


class ProducerService:
    def __init__(self, rbmq_config: RabbitBaseConnection) -> None:
        self._rbmq_config = rbmq_config

    async def ensure_connection_initialized(self) -> None:
        """Ensure that the connection is initialized and open"""
        if not self._rbmq_config._connection or self._rbmq_config._connection.is_closed:
            logger.info("Connection is not initialized or closed, reconnecting...")
            try:
                await self._rbmq_config.connect()
                logger.info("Connection successfully reconnected")
            except Exception as e:
                logger.error(f"Failed to connect to RabbitMQ: {e}")
                raise RuntimeError("Failed to reconnect to RabbitMQ") from e

    async def _get_channel(self) -> AbstractChannel:
        """Get or create a RabbitMQ channel"""
        if not self._rbmq_config._connection or self._rbmq_config._connection.is_closed:
            await self.ensure_connection_initialized()

        try:
            assert self._rbmq_config._connection is not None
            return await self._rbmq_config._connection.channel()
        except Exception as e:
            logger.error(f"Failed to create channel: {e}")
            raise RuntimeError("Failed to create RabbitMQ channel") from e

    async def declare_exchange_and_queue(self) -> AbstractExchange:
        """Declare exchange and queue after ensuring connection is initialized"""
        channel = await self._get_channel()

        exchange = await channel.declare_exchange(
            name=all_settings.rabbit.rabbit_exchange, type=ExchangeType.DIRECT
        )
        queue = await channel.declare_queue(
            name=all_settings.rabbit.rabbit_rk, durable=True
        )
        await queue.bind(exchange=exchange, routing_key=all_settings.rabbit.rabbit_rk)
        return exchange

    async def produce_message(
        self, message_body: list, exchange: AbstractExchange
    ) -> None:
        """Produce a message and publish to the exchange"""
        message = Message(
            body=json.dumps(message_body).encode(),
        )
        try:
            await exchange.publish(
                message=message, routing_key=all_settings.rabbit.rabbit_rk
            )
            logger.info(f"Message successfully published: {message_body}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise RuntimeError("Failed to publish message to RabbitMQ") from e

    async def send_periodic_messages(
        self, message_body: dict, interval: int = 1
    ) -> None:
        """Send periodic messages with a specified interval"""
        exchange = await self.declare_exchange_and_queue()
        while True:
            try:
                new_message = await change_transfer_data(message_body)
                await self.produce_message(message_body=new_message, exchange=exchange)
                logger.info(f"Sent periodic message: {new_message}")
            except Exception as e:
                logger.error(f"Error in sending periodic message: {e}")
            await asyncio.sleep(interval)
