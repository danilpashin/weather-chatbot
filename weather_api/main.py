import asyncio
import uvicorn
from weather_api.src.routers.weather import router
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from weather_api.src.settings.config import limiter
from weather_api.src.routers.weather import get_weather_service
from weather_api.src.services.weather_service import WeatherService
from weather_api.src.settings import config as cfg
from packages.logging import logger, listener
from packages.cache import cache


def create_weather_service() -> WeatherService:
    return WeatherService(cache)

def factory() -> FastAPI:
    app = FastAPI()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.dependency_overrides[get_weather_service] = create_weather_service
    app.include_router(router, tags=["weather"])

    return app


async def main_application():
    app = factory()

    config = uvicorn.Config(
        app=app,
        host=cfg.HOST,
        port=cfg.PORT
    )
    server = uvicorn.Server(config)

    try:
        logger.info("WeatherAPI запущен!")
        await server.serve()
    finally:
        logger.warning("WeatherAPI завершил работу!")
        listener.stop()
        await cache.close()


if __name__ == "__main__":
    asyncio.run(main_application())