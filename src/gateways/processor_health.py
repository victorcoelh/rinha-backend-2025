import asyncio
from src.gateways.processor import Processor
from src.gateways.redis import get_redis_client
from src.gateways.requests import get_request_client

LOCK_KEY = "healthcheck_scheduler_lock"
LOCK_TTL = 10  # seconds


async def health_check_scheduler():
    while True:
        await check_processor_health()
        await asyncio.sleep(5.5)

async def check_processor_health() -> None:
    request_client = get_request_client()
    redis_client = get_redis_client()
    
    default_endpoint = Processor.DEFAULT.get_processor() + "/service-health"
    default_health = (await request_client.get(default_endpoint))
    
    if not default_health.is_success:
        return None
    
    default_health = default_health.json()
    if not default_health["failing"]:
        await redis_client.set("processor", Processor.DEFAULT)
