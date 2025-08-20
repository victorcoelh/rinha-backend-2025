import asyncio
from asyncio.tasks import Task
from src.async_queue.async_queue import AsyncQueue

from src.services.payment import process_payment


class WorkerPool:
    def __init__(self, queue: AsyncQueue, num_workers: int) -> None:
        self._queue = queue
        self._workers: list[Task] = []
        self.num_workers = num_workers
    
    async def start(self) -> None:
        loop = asyncio.get_running_loop()

        for _ in range(self.num_workers):
            self._workers.append(loop.create_task(self._worker()))

    async def stop(self) -> None:
        for worker in self._workers:
            worker.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)

    async def _worker(self) -> None:
        while True:
            payment = await self._queue.get()

            if await process_payment(payment):
                await self._queue.put(payment)
