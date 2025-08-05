from redis.asyncio import Redis
import httpx

request_client = httpx.AsyncClient()
redis_client = Redis(host="localhost", port=6379, db=0)
