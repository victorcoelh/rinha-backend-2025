from datetime import datetime
import json

from src.services.types import TransactionsSummary
from src.connections import redis_client


async def summary_service(from_utc: str, to_utc: str) -> TransactionsSummary:
    transactions: list[bytes] = await redis_client.lrange("transactions", 0, -1) # type: ignore
    summary = initialize_summary_dict()
    
    for transaction in transactions: # type: ignore
        transaction = json.loads(transaction.decode("utf-8")) # type: ignore

        if within_range(transaction["requestedAt"], from_utc, to_utc):
            summary[transaction["processor"]]["totalRequests"] += 1
            summary[transaction["processor"]]["totalAmount"] += transaction["amount"]

    return summary

def initialize_summary_dict() -> dict[str, dict[str, int | float]]:
    return {
        "default": {
            "totalRequests": 0,
            "totalAmount": 0
        },
        "fallback": {
            "totalRequests": 0,
            "totalAmount": 0
        }
    }

def within_range(time: str, from_utc: str, to_utc: str) -> bool:
    transaction_date = datetime.strptime(time[:-2], "%Y-%m-%dT%H:%M:%S.%f")
    start_date = datetime.strptime(from_utc[:-2], "%Y-%m-%dT%H:%M:%S.%f")
    end_date = datetime.strptime(to_utc[:-2], "%Y-%m-%dT%H:%M:%S.%f")

    return start_date <= transaction_date <= end_date
