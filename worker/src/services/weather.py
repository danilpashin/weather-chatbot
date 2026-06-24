import logging
import redis
import json
import aiohttp
import os
from packages.core.config import init_config
from worker.src.clients.api import fetch_data

init_config()

r = redis.asyncio.Redis(host=os.getenv("REDIS_HOST"), decode_responses=True)

async def process_city_weather(session: aiohttp.ClientSession, city: str, url: str) -> dict:
    payload = await fetch_data(session, url)

    if payload is not None:
        value = json.dumps(payload)
        await r.set(name=city, value=value)
        logging.info(f"Данные по городу {city} успешно сохранены в Redis.")
        return {"city": city, "success": True, "source": "api"}
    
    logging.warning(f"API недоступно для {city}. Попытка получить запасные данные...")
    backup_data = await r.get(city)

    if backup_data is None:
        logging.error(f"Данные по городу {city} в бэкапе не найдены!")
        return {"city": city, "success": False, "error": "no_data"}
    
    await r.set(name=city, value=backup_data)
    logging.info(f"Найдена резервная копия данных для {city}.")
    return {"city": city, "success": True, "source": "backup"}
