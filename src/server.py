from contextlib import asynccontextmanager
import json

from fastapi import FastAPI, Response, Query
from dramatiq.brokers.redis import RedisBroker
import dramatiq

from models.payment import Payment
from services.process_payment import payment_service
from services.summary import summary_service
from connections import redis_client, request_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis_client.flushdb(asynchronous=False) # pyright: ignore[reportUnknownMemberType]
    await redis_client.set("processor", "default")
    broker = RedisBroker(host="localhost", port=6379)
    dramatiq.set_broker(broker)

    yield

    # Shutdown
    await request_client.aclose()
    await redis_client.close()

app = FastAPI(lifespan=lifespan)


@app.get("/payments-summary")
async def get_payments_summary(from_utc: str = Query(alias="from"),
                               to_utc: str = Query(alias="to")) -> Response:
    summary = await summary_service(from_utc, to_utc)
    return Response(json.dumps(summary), status_code=200)

@app.post("/payments")
async def process_payment(payment: Payment) -> Response:
    payment_service.send(payment.model_dump())
    return Response(status_code=200)
