import dramatiq
from dramatiq.middleware import Middleware

import src.broker # noqa: F401
import logging

from src.services import process_payment  # noqa: E402, F401
from src.services import endpoint_health  # noqa: E402, F401
from src.health_check import startup_actor

logging.getLogger("dramatiq").setLevel(logging.CRITICAL)


class StartupMiddleware(Middleware):
    def after_worker_boot(self, broker, worker) -> None:
        startup_actor.send()


dramatiq.get_broker().add_middleware(StartupMiddleware())
dramatiq.get_broker().flush_all()
