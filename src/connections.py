from redis.asyncio import Redis

import httpx

request_client = httpx.AsyncClient(timeout=None)
redis_client = Redis(host="redis", port=6379, db=0)
