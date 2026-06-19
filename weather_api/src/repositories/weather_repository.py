import os
import redis
import json
import logging
from packages.core.config import init_config

init_config()

async def get_redis_data(city):
    r = redis.asyncio.Redis(host=os.getenv("REDIS_WEATHER_HOST"), port=os.getenv("REDIS_WEATHER_PORT"), decode_responses=True)
    try:
        raw_data = await r.get(city)

        if raw_data is None:
            logging.info(f"Данные для города {city} не найдены (ключ не существует).")
            return None

        data = json.loads(raw_data)
        return data
    except Exception as e:
        logging.error(f"Ошибка при чтении из Redis: {e}")
        return None