from pydantic import BaseModel


class Payment(BaseModel):
    correlationId: str
    amount: float
