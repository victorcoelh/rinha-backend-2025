import json

from fastapi import FastAPI, Request, Response, Query
from fastapi.responses import ORJSONResponse
from starlette.requests import Request as StarletteRequest
import orjson

import src.broker  # noqa: F401
from src.services.process_payment import payment_service
from src.services.summary import summary_service

async def orjson_json(self):
    return orjson.loads(await self.body())
StarletteRequest.json = orjson_json

app = FastAPI(default_response_class=ORJSONResponse)


@app.get("/payments-summary")
async def get_payments_summary(from_utc: str = Query(alias="from"),
                               to_utc: str = Query(alias="to")) -> Response:
    summary = await summary_service(from_utc, to_utc)
    return Response(json.dumps(summary), status_code=200)

@app.post("/payments")
async def process_payment(request: Request) -> Response:
    payment_service.send(await request.json())
    return Response(status_code=200)
