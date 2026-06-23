import logging
from fastapi import Query, APIRouter, Request, HTTPException
from packages.core.config import init_config
from weather_api.src.domain.exceptions import CityNotFoundError
from weather_api.src.services import weather_service as service
from weather_api.src.limiter import limiter

init_config()

router = APIRouter()

@router.get("/health")
@limiter.limit("1000/minute")
async def health(request: Request):
    return {"status": "ok"}

@router.get("/weather")
@limiter.limit("10/minute")
async def get_weather(
        request: Request, 
        name: str = Query(default="", description="Название города")
    ):
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="Город не указан")

    if not isinstance(name, str):
        raise HTTPException(status_code=400, detail="Имя города должно быть строкой")

    try:
        data = await service.get_weather_data(name.strip())
        return data
    except CityNotFoundError:
        raise HTTPException(status_code=404, detail=f"Город '{name}' не найден")
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
