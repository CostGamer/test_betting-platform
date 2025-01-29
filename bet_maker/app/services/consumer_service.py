import asyncio
from logging import getLogger

from aio_pika.abc import AbstractChannel, AbstractIncomingMessage, AbstractQueue

from bet_maker.app.core.schemas.repo_protocols.redis_repo_protocols import (
    RedisRepoProtocol,
)
from shared.configs.rabbitmq import RabbitBaseConnection
from shared.configs.settings import Settings

logger = getLogger(__name__)


class ConsumerService:
    def __init__(
        self,
        rbmq_config: RabbitBaseConnection,
        redis: RedisRepoProtocol,
        settings: Settings,
    ) -> None:
        self._rbmq_config = rbmq_config
        self._redis_service = redis
        self.queue_name = settings.rabbit.rabbit_rk

    async def _reconnect_rabbitmq(self) -> None:
        if not self._rbmq_config._connection or self._rbmq_config._connection.is_closed:
            logger.info("Connection is not initialized or closed, reconnecting...")
            try:
                await self._rbmq_config.connect()
                logger.info("Connection successfully reconnected")
            except Exception as e:
                logger.error(f"Failed to connect to RabbitMQ: {e}")
                raise RuntimeError("Failed to reconnect to RabbitMQ") from e

    async def _create_channel(self) -> AbstractChannel:
        if not self._rbmq_config._connection or self._rbmq_config._connection.is_closed:
            logger.error("RabbitMQ connection is closed or not initialized")
            await self._reconnect_rabbitmq()

        try:
            assert self._rbmq_config._connection is not None
            return await self._rbmq_config._connection.channel()
        except Exception as e:
            logger.error(f"Failed to create channel: {e}")
            raise RuntimeError("Failed to create RabbitMQ channel") from e

    async def _declare_queue(
        self, channel: AbstractChannel, queue_name: str
    ) -> AbstractQueue:
        try:
            return await channel.declare_queue(queue_name, durable=True)
        except Exception as e:
            logger.error(f"Failed to declare queue {queue_name}: {e}")
            raise RuntimeError(f"Failed to declare queue {queue_name}") from e

    async def consume_message(self, queue_name: str) -> None:
        await self._reconnect_rabbitmq()

        try:
            channel = await self._create_channel()
            queue = await self._declare_queue(channel, queue_name)
        except Exception as e:
            logger.error(f"Error setting up RabbitMQ: {e}")
            return

        logger.info("Starting to listen for messages")
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self._process_message(message)

    async def _process_message(self, message: AbstractIncomingMessage) -> None:
        logger.info(f"Received message: {message.body.decode()}")
        try:
            await self._redis_service.send_message(message.body.decode())
            logger.info("Message processed successfully")
            await message.ack()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await message.nack(requeue=True)

    async def consume_forever(self, interval: int = 5) -> None:
        logger.info(f"Starting consumer for queue: {self.queue_name}")
        while True:
            try:
                await self.consume_message(self.queue_name)
            except Exception as e:
                logger.error(f"Error in consumer loop: {e}")
            await asyncio.sleep(interval)
