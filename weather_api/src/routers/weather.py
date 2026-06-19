from fastapi import APIRouter, Request
import os
from packages.core.config import init_config
from weather_api.src.services import weather_service as service
from slowapi import Limiter
from slowapi.util import get_remote_address

init_config()

limiter = Limiter(key_func=get_remote_address, storage_uri=f"redis://{os.getenv("REDIS_LIMITER_HOST")}:{os.getenv("REDIS_LIMITER_PORT")}/0")

router = APIRouter()

@router.get("/weather")
@limiter.limit("10/minute")
async def root(request: Request, name: str):
    data = await service.get_weather_data(name)
    return data
