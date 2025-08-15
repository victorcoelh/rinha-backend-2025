import json
from datetime import datetime, timezone

from src.models.processor import Processor
from src.connections import get_redis_client, get_request_client
from src.types import Payment


async def process_payment(payment: Payment) -> None:
    redis_client = get_redis_client()
    request_client = get_request_client()
    
    processor_type: bytes = await redis_client.get("processor")
    processor = Processor(processor_type.decode("utf-8"))

    payment["processor"] = processor
    payment["requestedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    response = await request_client.post(processor.get_processor(), json=payment)

    if not response.is_success:
        await invert_redis_processor()
        response.raise_for_status()

    await redis_client.rpush("transactions", json.dumps(payment)) # type: ignore

async def invert_redis_processor() -> str:
    redis_client = get_redis_client()
    
    processor_type: bytes = await redis_client.get("processor")
    current_processor = processor_type.decode("utf-8") # type: ignore

    if current_processor == Processor.DEFAULT:
        await redis_client.set("processor", Processor.FALLBACK)
        return Processor.FALLBACK
    else:
        await redis_client.set("processor", Processor.DEFAULT)
        return Processor.DEFAULT
