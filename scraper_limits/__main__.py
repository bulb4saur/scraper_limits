import asyncio
import logging

from scraper_limits.engine.worker import Worker, WorkerStatus
from scraper_limits.io.rmq import InputClass


async def crawl() -> None:
    worker_pool = [Worker() for _ in range(10)]
    input_class = InputClass()
    await input_class.async_initialize()

    while True:
        if input_class._is_queue_empty:
            break

        for worker in worker_pool:
            if worker.status == WorkerStatus.BUSY:
                continue

            await worker.work(input_class=input_class)

        # await asyncio.sleep(0.01)

    await input_class.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawl())
