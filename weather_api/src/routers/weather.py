from packages.logging import logger
from fastapi import Query, APIRouter, Request, HTTPException, Depends
from weather_api.src.domain.exceptions import CityNotFoundError
from weather_api.src.services.weather_service import WeatherService
from weather_api.src.settings.config import limiter

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

    raw_name = request.url.query
    city = name.strip()

    try:
        data = await service.get_weather_data(city)
        return {
            "temp": data.temp,
            "feels_like": data.feels_like,
            "weather_desc": data.weather_desc,
            "wind": data.wind,
            "humidity": data.humidity
        }
    except CityNotFoundError as e:
        logger.warning(f"⚠️ Город не найден | город={city} | original_query={raw_name}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(f"❌ Ошибка при получении погоды | город={city} | query={raw_name} | ip={request.client.host} | error={type(e).__name__}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")