from redis.asyncio import Redis

import httpx

_redis_client = None
_request_client = None


def get_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis(host="redis", port=6379, db=0)
    return _redis_client

def get_request_client() -> httpx.AsyncClient:
    global _request_client
    if _request_client is None:
        _request_client = httpx.AsyncClient(timeout=None)
    return _request_client
