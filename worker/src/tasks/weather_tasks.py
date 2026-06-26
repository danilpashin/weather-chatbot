import aiohttp
import asyncio
from worker.src.services.weather import process_city_weather
from worker.src.settings.config import CITIES, DEFAULT_INTERVAL
from packages.logging import logger


async def weather_worker():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                tasks = [process_city_weather(session, city_obj) for city_obj in CITIES]

                results = await asyncio.gather(*tasks)

                failed_cities = [res["city"] for res in results if not res["success"]]
                backup_used = [res["city"] for res in results if res.get("source") == "backup"]

                if failed_cities:
                    logger.error(f"Данные не были получены для городов {failed_cities}")
                if backup_used:
                    logger.warning(f"Для городов {backup_used} были использованы бэкапы")
            except Exception as e:
                logger.error(f"[КРИТИЧЕСКАЯ ОШИБКА ВОРКЕРА]: {e}", exc_info=True)

            logger.info(f"Засыпаем на {DEFAULT_INTERVAL} секунд...")
            await asyncio.sleep(DEFAULT_INTERVAL)