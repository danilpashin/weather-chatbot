from fastapi import APIRouter, Request
import os
from packages.core.config import init_config
from weather_api.src.services import weather_service as service
from slowapi import Limiter
from slowapi.util import get_remote_address

init_config()

limiter = Limiter(key_func=get_remote_address, storage_uri=f"redis://{os.getenv("REDIS_LIMITER_HOST")}:{os.getenv("REDIS_LIMITER_PORT")}/0")

router = APIRouter()

is_mock = False

class MockData:
    def __init__(self, name: str, temp: float, feels_like: float, weather_desc: str, wind: float, humidity: int):
        self.name = name
        self.temp = temp
        self.feels_like = feels_like
        self.weather_desc = weather_desc
        self.wind = wind
        self.humidity = humidity

dataUfa = MockData("Уфа", 24.66, 24.25, "облачно с прояснениями", 5.2, 48)
dataMoscow = MockData("Москва", 30.82, 26.85, "ясно", 2.5, 60)
dataSPB = MockData("Санкт-Петербург", 19.13, 18.45, "пасмурно", 12.4, 70)

@router.get("/weather")
@limiter.limit("10/minute")
async def root(request: Request, name: str):
    if is_mock:
        match name:
            case "Уфа":
                return dataUfa
            case "Москва":
                return dataMoscow
            case "Санкт-Петербург":
                return dataSPB
            case _:
                return dataUfa
    else:
        data = await service.get_weather_data(name)
        return data
