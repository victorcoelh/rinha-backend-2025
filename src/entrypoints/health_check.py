import asyncio
from src.services.endpoint_health import check_endpoint_health

async def queue_health_check_every_5_seconds() -> None:
    while True:
        check_endpoint_health.send()
        await asyncio.sleep(5.5)
