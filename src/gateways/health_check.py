import asyncio
from src.gateways.processor import Processor
from src.gateways.redis import get_redis_client
from src.gateways.requests import get_request_client

LOCK_KEY = "healthcheck_scheduler_lock"
LOCK_TTL = 10  # seconds


async def _endpoint_health_check():
    while True:
        ##add to job queue
        await asyncio.sleep(5.5)
        
async def _redis_flush():
    redis_client = get_redis_client()
    await redis_client.flushdb(asynchronous=True) # type: ignore
    await redis_client.set("processor", "default") # type: ignore

async def startup_actor():
    loop = asyncio.get_running_loop()

    redis = get_redis_client()
    acquired = await redis.set(LOCK_KEY, "1", nx=True, ex=LOCK_TTL)  # type: ignore

    if not acquired:
        return

    loop.create_task(_endpoint_health_check())
    loop.create_task(_redis_flush())

async def check_endpoint_health() -> None:
    request_client = get_request_client()
    redis_client = get_redis_client()
    
    default_endpoint = Processor.DEFAULT.get_processor() + "/service-health"
    default_health = (await request_client.get(default_endpoint))
    
    if not default_health.is_success:
        return None
    
    default_health = default_health.json()
    if not default_health["failing"]:
        await redis_client.set("processor", Processor.DEFAULT)
