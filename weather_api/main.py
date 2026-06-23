import asyncio
import uvicorn
import os
from packages.core.config import init_config
from weather_api.src.routers.weather import router
from fastapi import FastAPI, Depends
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import queue
import logging
from logging.handlers import QueueHandler, QueueListener
from weather_api.src.limiter import limiter
from weather_api.src.repositories.redis import RedisStorage
from weather_api.src.services.weather_service import WeatherService

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

def create_weather_service() -> WeatherService:
    storage = RedisStorage()
    return WeatherService(storage)

def factory() -> FastAPI:
    app = FastAPI()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    from weather_api.src.routers.weather import get_weather_service

    async def weather_service_dependency():
        service = create_weather_service()
        try:
            yield service
        finally:
            await service.close()

    app.dependency_overrides[get_weather_service] = weather_service_dependency
    app.include_router(router, tags=["weather"])

    return app

async def main_application():
    app = factory()

    config = uvicorn.Config(
        app=app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8080))
    )
    server = uvicorn.Server(config)

    try:
        await server.serve()
    finally:
        listener.stop()

if __name__ == "__main__":
    asyncio.run(main_application())