import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

broker = RedisBroker(host="localhost", port=6379)
broker.add_middleware(AsyncIO())
dramatiq.set_broker(broker)

from src.services import process_payment  # noqa: E402, F401
