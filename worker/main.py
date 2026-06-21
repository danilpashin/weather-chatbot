import asyncio
import queue
import logging
from logging.handlers import QueueHandler, QueueListener

console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console_handler.setFormatter(formatter)

log_queue = queue.Queue()
async_handler = QueueHandler(log_queue)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(async_handler)

listener = QueueListener(log_queue, console_handler)
listener.start()

from .src.tasks.weather_tasks import weather_worker

async def main_worker():
    await weather_worker()

if __name__ == "__main__":
    try:
        asyncio.run(main_worker())
    finally:
        listener.stop()
        logging.warning("Воркер завершил работу!")