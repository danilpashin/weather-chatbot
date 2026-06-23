import logging
from fastapi import Query, APIRouter, Request, HTTPException
from packages.core.config import init_config
from weather_api.src.services import weather_service as service
from weather_api.src.limiter import limiter

init_config()

router = APIRouter()

@router.get("/weather")
@limiter.limit("10/minute")
async def root(request: Request, name: str):
    data = await service.get_weather_data(name)
    return data
