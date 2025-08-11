import os

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
import dramatiq


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
broker = RedisBroker(url=REDIS_URL)
asyncio_middleware = AsyncIO()
broker.add_middleware(asyncio_middleware)
broker.flush_all()
dramatiq.set_broker(broker)
