import asyncio
import time

import aiohttp

from packages.logging import logger
from worker.src.services.weather_service import process_city_weather
from worker.src.settings.city_tasks import CITY_TASKS
from worker.src.settings.config import DEFAULT_INTERVAL

HEALTH_FILE = "/tmp/worker_status/health.txt"


async def weather_worker():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                tasks = [
                    process_city_weather(session, city_obj) for city_obj in CITY_TASKS
                ]

                results = await asyncio.gather(*tasks)

                failed_cities = [res["city"] for res in results if not res["success"]]
                backup_used = [
                    res["city"] for res in results if res.get("source") == "backup"
                ]

                if failed_cities:
                    logger.error(f"Данные не были получены для городов {failed_cities}")
                if backup_used:
                    logger.warning(
                        f"Для городов {backup_used} были использованы бэкапы"
                    )

                with open(HEALTH_FILE, "w") as f:
                    f.write(str(time.time()))
                    f.flush()
            except Exception as e:
                logger.error(f"[КРИТИЧЕСКАЯ ОШИБКА ВОРКЕРА]: {e}", exc_info=True)

            logger.info(f"Засыпаем на {DEFAULT_INTERVAL} секунд...")
            await asyncio.sleep(DEFAULT_INTERVAL)
