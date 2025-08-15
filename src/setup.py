import asyncio
import logging
import orjson
import uvloop

from src.gateways.processor_health import health_check_scheduler
from src.async_queue.async_queue import AsyncQueue
from src.async_queue.worker_pool import WorkerPool
from src.gateways.redis import get_redis_client

uvloop.install()
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)
    

async def initialize_worker_pool_and_jobs(queue: AsyncQueue, num_workers: int) -> WorkerPool:
    pool = WorkerPool(queue, num_workers)
    await pool.start()
    
    loop = asyncio.get_running_loop()
    loop.create_task(flush_redis_db())
    loop.create_task(health_check_scheduler())
    
    logging.info("Initialized worker pool")
    return pool

async def flush_redis_db():
    redis_client = get_redis_client()
    await redis_client.flushdb(asynchronous=True) # type: ignore
    await redis_client.set("processor", "default") # type: ignore
    
async def orjson_json(self):
    return orjson.loads(await self.body())
