from packages.logging import logger
from fastapi import Query, APIRouter, Request, HTTPException, Depends
from pyrate_limiter import Duration, Limiter, Rate
from weather_api.src.domain.exceptions import CityNotFoundError
from weather_api.src.services.weather_service import WeatherService
from fastapi_limiter.depends import RateLimiter

router = APIRouter()

def get_weather_service() -> WeatherService:
    raise NotImplementedError("Use app.dependency_overrides in tests")

@router.get(
    "/health",
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(1000, Duration.MINUTE * 1))))]
)
async def health(request: Request):
    return {"status": "ok"}

@router.get(
    "/weather",
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(10, Duration.MINUTE * 1))))]
)
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