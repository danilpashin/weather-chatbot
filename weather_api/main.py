import asyncio
import uvicorn
import os
from packages.core.config import init_config
import weather_api.src.workers.scheduler as scheduler
from weather_api.src.routers.weather import router, limiter
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

init_config()

async def main_application():
    worker_task = asyncio.create_task(scheduler.background_api_worker())

    app = FastAPI()

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.include_router(router, tags=["weather"])

    config = uvicorn.Config(app=app, host=os.getenv("API_HOST"), port=int(os.getenv("API_PORT")))
    server = uvicorn.Server(config)
    
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main_application())