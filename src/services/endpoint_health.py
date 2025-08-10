import dramatiq

from src.connections import get_redis_client, get_request_client
from src.models.processor import Processor


@dramatiq.actor(max_retries=0)
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
