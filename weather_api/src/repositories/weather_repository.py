import requests
import os
import redis
import json
from packages.core.config import init_config
from weather_api.src.domain.coord import Coord

init_config()

dataUfa = Coord(54.73, 55.95)
dataMoscow = Coord(55.75, 37.62)
dataSPB = Coord(59.94, 30.32)

async def get_redis_data(city):
    r = redis.asyncio.Redis(host=os.getenv("REDIS_WEATHER_HOST"), port=os.getenv("REDIS_WEATHER_PORT"), decode_responses=True)
    try:
        raw_data = await r.get(city)

        if raw_data is None:
            print(f"Данные для города {city} не найдены (ключ не существует).")
            return None

        data = json.loads(raw_data)
        return data
    except Exception as e:
        print(f"Ошибка при чтении из Redis: {e}")
        return None