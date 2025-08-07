import os

from dramatiq.brokers.redis import RedisBroker
import dramatiq
from dramatiq.middleware.asyncio import AsyncIO


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
broker = RedisBroker(url=REDIS_URL)
broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)
