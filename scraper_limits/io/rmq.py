from typing import TYPE_CHECKING, Optional

import aio_pika

if TYPE_CHECKING:
    from aio_pika.abc import (
        AbstractChannel,
        AbstractQueue,
        AbstractRobustConnection,
    )

import logging

from scraper_limits.io import InputMessage


class InputClass:
    _connection: Optional["AbstractRobustConnection"]
    _channel: Optional["AbstractChannel"]
    _queue: Optional["AbstractQueue"]
    _is_queue_empty: bool = False

    def __init__(self) -> None:
        self._connection = None
        self._channel = None
        self._queue = None

    async def async_initialize(self) -> None:
        if not self._connection:
            self._connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1:5672/")

        if not self._channel:
            self._channel = await self._connection.channel()

        if not self._queue:
            self._queue = await self._channel.declare_queue(name="urls", durable=True)

    async def get(self) -> InputMessage:
        logging.info("Getting message")

        if not self._queue:
            raise ValueError("Queue is not initialized")

        if self._queue.declaration_result.message_count == 0:
            self._is_queue_empty = True

        incoming_message = await self._queue.get(timeout=1)

        if not incoming_message:
            raise NotImplementedError("Queue is Empty")

        message = InputMessage(
            message_source=incoming_message,
            url=incoming_message.body.decode(),
            headers=incoming_message.headers,
        )
        logging.info(f"Consuming message: {message.url}")
        return message

    async def success(self, message: InputMessage) -> None:
        logging.info(f"Acking message: {message.url}")
        await message.message_source.ack()

    async def failure(self, message: InputMessage) -> None:
        logging.info(f"Republishing message: {message.url}")
        await message.message_source.nack(requeue=True)

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()
        if self._channel:
            await self._channel.close()
