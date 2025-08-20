from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, Query
from fastapi.responses import ORJSONResponse
from starlette.requests import Request as StarletteRequest
import orjson

from src.async_queue.async_queue import AsyncQueue
from src.services.summary import summary_service
from src.setup import initialize_worker_pool_and_jobs, orjson_json

job_queue = AsyncQueue()


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    worker_pool = await initialize_worker_pool_and_jobs(job_queue, 8)
    yield
    await worker_pool.stop()

StarletteRequest.json = orjson_json
app = FastAPI(default_response_class=ORJSONResponse, lifespan=fastapi_lifespan)


@app.get("/payments-summary")
async def get_payments_summary(from_utc: str = Query(alias="from"),
                               to_utc: str = Query(alias="to")) -> Response:
    summary = await summary_service(from_utc, to_utc)
    return Response(orjson.dumps(summary), status_code=200)

@app.post("/payments")
async def process_payment(request: Request) -> Response:
    await job_queue.put(await request.json())
    return Response(status_code=200)

@app.get("/health")
async def health_check() -> Response:
    return Response(status_code=200)
