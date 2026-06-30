import asyncio
import uvicorn
from uuid import uuid4
from weather_api.src.routers.weather import router
from fastapi import FastAPI, Request, Response
from fastapi.routing import _IncludedRouter
from typing import Callable, Awaitable
from weather_api.src.routers.weather import get_weather_service
from weather_api.src.services.weather_service import WeatherService
from weather_api.src.settings import config as cfg
from packages.logging import logger, listener
from packages.cache import cache
from packages.logging.setup import trace_id_var, user_id_var


if not hasattr(_IncludedRouter, "path"):
    _IncludedRouter.path = property(lambda self: "")

def _create_middleware():
    async def log_request(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        trace_id = request.headers.get("X-Trace-ID")
        user_id = request.headers.get("X-User-ID")

        if trace_id is None:
            trace_id_var.set(str(uuid4()))
        else:
            trace_id_var.set(trace_id)
        
        if user_id is not None:
            user_id_var.set(user_id)
        
        response = await call_next(request)
        return response
    return log_request

def _create_service() -> WeatherService:
    return WeatherService(cache)

def _setup_app_dependencies(app: FastAPI):
    app.dependency_overrides[get_weather_service] = _create_service
    app.include_router(router, tags=["weather"])


def factory() -> FastAPI:
    app = FastAPI()
    app.middleware("http")(_create_middleware())
    _setup_app_dependencies(app)

    return app

async def main_application():
    app = factory()
    config = uvicorn.Config(app=app, host=cfg.HOST, port=cfg.PORT)
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