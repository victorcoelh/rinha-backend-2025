import asyncio
import dramatiq
from src.services.endpoint_health import check_endpoint_health
from src.connections import get_redis_client

LOCK_KEY = "healthcheck_scheduler_lock"
LOCK_TTL = 10  # seconds


async def _endpoint_health_check():
    while True:
        check_endpoint_health.send()
        await asyncio.sleep(5.5)
        
async def _redis_flush():
    redis_client = get_redis_client()
    await redis_client.flushdb(asynchronous=True) # type: ignore
    await redis_client.set("processor", "default") # type: ignore

@dramatiq.actor
async def startup_actor():
    loop = asyncio.get_running_loop()

    redis = get_redis_client()
    acquired = await redis.set(LOCK_KEY, "1", nx=True, ex=LOCK_TTL)  # type: ignore

    if not acquired:
        return

    loop.create_task(_endpoint_health_check())
    loop.create_task(_redis_flush())
