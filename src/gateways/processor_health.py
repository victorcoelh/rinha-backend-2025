import asyncio

from redis.asyncio import Redis
from src.gateways.processor import Processor
from src.gateways.redis import get_redis_client
from src.gateways.requests import get_request_client


async def health_check_scheduler():
    redis_client = get_redis_client()

    while True:
        await asyncio.sleep(1.5)

        processor_type: bytes = await redis_client.get("processor")
        current_processor = processor_type.decode("utf-8") # type: ignore
        
        if current_processor == Processor.FALLBACK:
            await check_processor_health(redis_client)

async def check_processor_health(redis_client: Redis) -> None:
    request_client = get_request_client()
    
    default_endpoint = Processor.DEFAULT.get_processor() + "/service-health"
    default_health = (await request_client.get(default_endpoint))
    
    if not default_health.is_success:
        return None
    
    default_health = default_health.json()
    if not default_health["failing"]:
        await redis_client.set("processor", Processor.DEFAULT)
