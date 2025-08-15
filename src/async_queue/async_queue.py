import asyncio
from collections import deque

from src.types import Payment


class AsyncQueue:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._queue = deque()
        self._not_empty = asyncio.Condition()
    
    async def put(self, payment: Payment) -> None:
        self._queue.append(payment)
        async with self._not_empty:
            self._not_empty.notify()
    
    async def get(self) -> Payment:
        async with self._not_empty:
            while not self._queue:
                await self._not_empty.wait()
        
        async with self._lock:
            return self._queue.popleft()
