import logging
import json
from datetime import datetime, timezone
from typing import Any

import dramatiq

from src.models.processor import Processor
from src.connections import redis_client, request_client

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)


@dramatiq.actor(min_backoff=500, max_backoff=2000, max_retries=3)
async def payment_service(payment_body: dict[str, Any]) -> None:
    payment_body["requestedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
    processor_type: bytes = await redis_client.get("processor")
    processor = Processor(processor_type.decode("utf-8"))

    response = await request_client.post(processor.get_processor(), json=payment_body)

    if not response.is_success:
        await invert_redis_client_processor()
        response.raise_for_status()

    payment_body["processor"] = processor
    await redis_client.rpush("transactions", json.dumps(payment_body)) # type: ignore

async def invert_redis_client_processor() -> str:
    processor_type: bytes = await redis_client.get("processor")
    current_redis_client = processor_type.decode("utf-8")

    if current_redis_client == Processor.DEFAULT:
        await redis_client.set("processor", Processor.FALLBACK)
        return Processor.FALLBACK
    else:
        await redis_client.set("processor", Processor.DEFAULT)
        return Processor.DEFAULT
