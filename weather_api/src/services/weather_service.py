import weather_api.src.repositories.weather_repository as repo
from weather_api.src.domain.data import Data

async def get_weather_data(city: str = "Уфа"):
    raw_data = await repo.get_api_data(city)
    data = raw_data.json()
    return Data(data["main"]["temp"], data["main"]["feels_like"], data["weather"][0]["description"], data["wind"]["speed"], data["main"]["humidity"])