from redis.asyncio import Redis

_redis_client = None


def get_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis(
            host="redis",
            port=6379,
            db=0,
            max_connections=50,
            decode_responses=False
        )

    return _redis_client
