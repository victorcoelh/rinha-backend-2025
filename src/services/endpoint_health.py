import dramatiq

from src.connections import request_client, redis_client
from src.models.processor import Processor


@dramatiq.actor(max_retries=0)
async def check_endpoint_health() -> None:
    default_endpoint = Processor.DEFAULT.get_processor() + "/service-health"
    default_health = (await request_client.get(default_endpoint)).json()
    
    if not default_health["failing"]:
        await redis_client.set("processor", Processor.DEFAULT)
