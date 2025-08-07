from enum import StrEnum


class Processor(StrEnum):
    DEFAULT = "default"
    FALLBACK = "fallback"
    
    def get_processor(self) -> str:
        match self:
            case Processor.DEFAULT:
                return "http://payment-processor-default:8080/payments"
            case Processor.FALLBACK:
                return "http://payment-processor-fallback:8080/payments"
