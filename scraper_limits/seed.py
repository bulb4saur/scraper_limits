import asyncio
from typing import TYPE_CHECKING

import aio_pika
import aio_pika.abc

if TYPE_CHECKING:
    from aio_pika.abc import AbstractChannel, AbstractRobustConnection


async def main() -> None:
    connection: "AbstractRobustConnection" = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")
    channel: "AbstractChannel" = await connection.channel()
    routing_key = "urls"

    for _ in range(1_000_000):
        await channel.default_exchange.publish(
            aio_pika.Message(body="http://127.0.0.1:8080".encode()), routing_key=routing_key
        )

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
