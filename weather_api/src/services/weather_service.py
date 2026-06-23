from weather_api.src.domain.data import Data
from weather_api.src.repositories.base import WeatherStorage
from weather_api.src.domain.exceptions import CityNotFoundError

def transform_weather_data(raw_data: dict) -> Data:
    return Data(
        temp=float(raw_data.get("temp", 0)),
        feels_like=float(raw_data.get("feels_like", 0)),
        weather_desc=str(raw_data.get("weather_desc", "")),
        wind=float(raw_data.get("wind", 0)),
        humidity=int(raw_data.get("humidity", 0))
    )

class WeatherService:
    def __init__(self, storage: WeatherStorage):
        self.storage = storage

    async def get_weather_data(self, city: str) -> Data:
        raw = await self.storage.get_weather(city)
        if not raw:
            raise CityNotFoundError(city)
        return transform_weather_data(raw)

    async def close(self):
        await self.storage.close()