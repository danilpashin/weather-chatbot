import json
from weather_api.src.domain.data import Data
from weather_api.src.repositories.base import WeatherCache
from weather_api.src.domain.exceptions import CityNotFoundError
from packages.logging import logger


def transform_weather_data(raw_data: dict) -> Data:
    return Data(
        temp=float(raw_data.get("temp", 0)),
        feels_like=float(raw_data.get("feels_like", 0)),
        weather_desc=str(raw_data.get("weather_desc", "")),
        wind=float(raw_data.get("wind", 0)),
        humidity=int(raw_data.get("humidity", 0)),
    )


class WeatherService:
    def __init__(self, cache: WeatherCache):
        self.cache = cache

    async def get_weather_data(self, city: str) -> Data:
        logger.info(f"Попытка получить данные для города {city}")
        data = await self.cache.get(city)
        if not data:
            logger.error(f"Город '{city}' не найден в кэше")
            raise CityNotFoundError(city)
        json_data = json.loads(data)
        return transform_weather_data(json_data)

    async def close(self):
        await self.cache.close()
