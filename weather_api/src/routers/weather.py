import logging
from fastapi import Query, APIRouter, Request, HTTPException, Depends
from weather_api.src.domain.exceptions import CityNotFoundError
from weather_api.src.services.weather_service import WeatherService
from weather_api.src.limiter import limiter

router = APIRouter()

def get_weather_service() -> WeatherService:
    raise NotImplementedError("Use app.dependency_overrides in tests")

@router.get("/health")
@limiter.limit("1000/minute")
async def health(request: Request):
    return {"status": "ok"}

@router.get("/weather")
@limiter.limit("100/minute")
async def get_weather(
    request: Request,
    name: str = Query(default="", description="Название города"),
    service: WeatherService = Depends(get_weather_service)
):
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="Город не указан")

    try:
        data = await service.get_weather_data(name.strip())
        return {
            "temp": data.temp,
            "feels_like": data.feels_like,
            "weather_desc": data.weather_desc,
            "wind": data.wind,
            "humidity": data.humidity
        }
    except CityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")