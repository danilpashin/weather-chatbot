import queue
import logging
import os
import json
from pathlib import Path
from packages.core.env import init_env
from logging.handlers import QueueHandler, QueueListener
from contextvars import ContextVar


init_env()

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="system")
user_id_var: ContextVar[str] = ContextVar("user_id", default="guest")
_service_name = os.getenv("SERVICE_NAME", "unknown")


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get()
        record.user_id = user_id_var.get()
        record.service = _service_name
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "service": getattr(record, "service", "weather-chatbot"),
            "trace_id": getattr(record, "trace_id", "N/A"),
            "user_id": getattr(record, "user_id", "N/A"),
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> QueueListener:
    text_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(service)s] [Trace:%(trace_id)s] [User:%(user_id)s] %(message)s"
    )

    log_dir = Path(os.getenv("LOG_DIR", "/app/logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "all_services.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())

    console = logging.StreamHandler()
    console.setFormatter(text_formatter)

    log_queue = queue.Queue()
    async_handler = QueueHandler(log_queue)

    loggers_to_capture = [
        logging.getLogger("telegram.ext.Application"),
        logging.getLogger("telegram.ext"),
        logging.getLogger("telegram"),
        logging.getLogger("app"),
    ]

    for lg in loggers_to_capture:
        lg.setLevel(logging.INFO)
        lg.propagate = False
        lg.addHandler(async_handler)
        lg.addFilter(ContextFilter())

    listener = QueueListener(log_queue, console, file_handler)
    listener.start()
    return listener


listener = setup_logging()
logger = logging.getLogger("app")
