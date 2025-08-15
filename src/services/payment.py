import json
from datetime import datetime, timezone

from redis.asyncio import Redis

from src.gateways.processor import Processor
from src.gateways.requests import get_request_client
from src.gateways.redis import get_redis_client
from src.types import Payment


async def process_payment(payment: Payment) -> Payment | None:
    redis_client = get_redis_client()
    request_client = get_request_client()
    
    processor_type: bytes = await redis_client.get("processor")
    processor = Processor(processor_type.decode("utf-8"))

    payment["processor"] = processor
    payment["requestedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    response = await request_client.post(processor.get_processor(), json=payment)

    if not response.is_success:
        await invert_redis_processor(redis_client, processor.value)
        return payment

    await redis_client.rpush("transactions", json.dumps(payment)) # type: ignore
    return None

async def invert_redis_processor(redis_client: Redis, current_processor: str) -> str:
    redis_client = get_redis_client()

    if current_processor == Processor.DEFAULT:
        await redis_client.set("processor", Processor.FALLBACK)
        return Processor.FALLBACK
    else:
        await redis_client.set("processor", Processor.DEFAULT)
        return Processor.DEFAULT
