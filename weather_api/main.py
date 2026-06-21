import asyncio
import uvicorn
import os
from packages.core.config import init_config
from weather_api.src.routers.weather import router, limiter
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
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

init_config()

async def main_application():
    app = FastAPI()

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.include_router(router, tags=["weather"])

    config = uvicorn.Config(app=app, host=os.getenv("API_HOST"), port=int(os.getenv("API_PORT")))
    server = uvicorn.Server(config)
    
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main_application())
    finally:
        listener.stop()