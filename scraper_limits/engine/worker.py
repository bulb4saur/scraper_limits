from typing import TYPE_CHECKING

import aiohttp

if TYPE_CHECKING:
    from scraper_limits.io import InputClass

from scraper_limits.engine.models import WorkerStatus


class Worker:
    status = WorkerStatus.FREE
    _session = None

    async def work(self, input_class: "InputClass") -> None:
        self.status = WorkerStatus.BUSY

        # reuse session if exists
        if not self._session:
            self._session = aiohttp.ClientSession()

        # get message
        message = await input_class.get()

        async with self._session.get(message.url) as response:
            if not response:
                await input_class.failure(message)

            await input_class.success(message)
            self.status = WorkerStatus.FREE
