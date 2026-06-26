import queue
import logging
import os
from packages.core.env import init_env
from logging.handlers import QueueHandler, QueueListener


_loggers_to_capture = [
    logging.getLogger("telegram.ext.Application"),
    logging.getLogger("telegram.ext"),
    logging.getLogger("telegram"),
    logging.getLogger("app")
]

init_env()
_service_name = os.getenv("SERVICE_NAME", "unknown")

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.service = _service_name
        return True    

def setup_logging() -> QueueListener:
    console = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(service)s] %(message)s"
    )
    console.setFormatter(formatter)

    log_queue = queue.Queue()
    async_handler = QueueHandler(log_queue)

    for lg in _loggers_to_capture:
        lg.setLevel(logging.INFO)
        lg.propagate = False
        lg.addHandler(async_handler)
        lg.addFilter(ContextFilter())

    listener = QueueListener(log_queue, console)
    listener.start()
    return listener


listener = setup_logging()
logger = logging.getLogger("app")