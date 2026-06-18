import weather_api.src.repositories.weather_repository as repo
from weather_api.src.domain.data import Data

async def get_weather_data(city: str = "Уфа"):
    data = await repo.get_redis_data(city)
    return Data(data["temp"], data["feels_like"], data["weather_desc"], data["wind"], data["humidity"])