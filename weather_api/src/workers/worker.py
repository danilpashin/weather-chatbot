import aiohttp
import asyncio
import os
from packages.core.config import init_config
from weather_api.src.domain.coord import Coord
from .services import process_city_weather
import logging

init_config()

dataUfa = Coord(54.73, 55.95)
dataMoscow = Coord(55.75, 37.62)
dataSPB = Coord(59.94, 30.32)

cities_tasks = [
    {"city": "Уфа", "url": f"https://api.openweathermap.org/data/2.5/weather?lat={dataUfa.lat}&lon={dataUfa.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}"},
    {"city": "Москва", "url": f"https://api.openweathermap.org/data/2.5/weather?lat={dataMoscow.lat}&lon={dataMoscow.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}"},
    {"city": "Санкт-Петербург", "url": f"https://api.openweathermap.org/data/2.5/weather?lat={dataSPB.lat}&lon={dataSPB.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}"}
]

interval_seconds = 10

async def weather_worker():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                tasks = [process_city_weather(session, task["city"], task["url"]) for task in cities_tasks]

                results = await asyncio.gather(*tasks)

                failed_cities = [res["city"] for res in results if not res["success"]]
                backup_used = [res["city"] for res in results if res.get("source") == "backup"]

                if failed_cities:
                    logging.error(f"Данные не были получены для городов {failed_cities}.")
                if backup_used:
                    logging.warning(f"Для городов {backup_used} были использованы бэкапы.")
        except Exception as e:
            logging.error(f"[КРИТИЧЕСКАЯ ОШИБКА ВОРКЕРА]: {e}")

        logging.info(f"[Воркер] Засыпаем на {interval_seconds} секунд...")
        await asyncio.sleep(interval_seconds)