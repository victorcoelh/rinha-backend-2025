from enum import StrEnum


class Processor(StrEnum):
    DEFAULT = "default"
    FALLBACK = "fallback"
    
    def get_processor(self) -> str:
        match self:
            case Processor.DEFAULT:
                return "http://localhost:8001/payments"
            case Processor.FALLBACK:
                return "http://localhost:8002/payments"
