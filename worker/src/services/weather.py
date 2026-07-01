import json
import aiohttp
from packages.logging import logger
from packages.core.env import init_env
from packages.cache import cache
from worker.src.clients.api import fetch_data
from worker.src.settings.config import CityTask

init_env()

async def process_city_weather(session: aiohttp.ClientSession, city_obj: CityTask) -> dict:
    city = city_obj.city

    payload = await fetch_data(session, city_obj.url)
    if payload is not None:
        value = json.dumps(payload)
        await cache.set(key=city, value=value, ex=900)
        logger.info(f"✅ {city} — данные получены и сохранены")
        return {"city": city, "success": True, "source": "api"}
    
    logger.warning(f"⚠️ {city} — API недоступно, ищу кэш...")
    cached = await cache.get(city)

    if not cached:
        logger.error(f"❌ {city} — API недоступно и кэш пуст!")
        return {"city": city, "success": False, "error": "no_data"}
    
    await cache.set(key=city, value=cached, ex=900)

    logger.info(f"💾 {city} — данные восстановлены из кэша (TTL обновлен)")
    return {"city": city, "success": True, "source": "backup"}
