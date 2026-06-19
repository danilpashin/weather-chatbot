import aiohttp
import asyncio
import json
import os
import redis
from packages.core.config import init_config
from weather_api.src.domain.coord import Coord
import logging

init_config()

dataUfa = Coord(54.73, 55.95)
dataMoscow = Coord(55.75, 37.62)
dataSPB = Coord(59.94, 30.32)

API_URLS={
    "Уфа":f"https://api.openweathermap.org/data/2.5/weather?lat={dataUfa.lat}&lon={dataUfa.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}",
    "Москва": f"https://api.openweathermap.org/data/2.5/weather?lat={dataMoscow.lat}&lon={dataMoscow.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}",
    "Санкт-Петербург": f"https://api.openweathermap.org/data/2.5/weather?lat={dataSPB.lat}&lon={dataSPB.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}"
}

r_main = redis.asyncio.Redis(host=os.getenv("REDIS_WEATHER_HOST"), port=os.getenv("REDIS_WEATHER_PORT"), decode_responses=True)
r_backup = redis.asyncio.Redis(host=os.getenv("REDIS_BACKUP_WEATHER_HOST"), port=os.getenv("REDIS_BACKUP_WEATHER_PORT"), decode_responses=True)

interval_seconds = 10

async def fetch_data(session: aiohttp.ClientSession, city, url):
    try:
        async with session.get(url) as response:
            data = await response.json()

            if response.status != 200:
                logging.error("Ошибка при запросе к API.")
                logging.info("Попытка получить запасные данные...")
                data = await r_backup.get(city)
                if data is None:
                    logging.error(f"Данные по городу {city} не найдены.")
                    return False
                await r_main.set(name=city, value=data)
                return True

            payload = {
                "temp": data["main"]["temp"], 
                "feels_like": data["main"]["feels_like"], 
                "weather_desc": data["weather"][0]["description"], 
                "wind": data["wind"]["speed"], 
                "humidity": data["main"]["humidity"]
            }

            value = json.dumps(payload)

            await r_main.set(name=city, value=value)
            await r_backup.set(name=city, value=value)

            logging.info(f"Данные по городу {city} успешно сохранены в Redis.")
            return True
    except Exception as e:
        logging.error(f"Ошибка при запросе к {url}: {e}", exc_info=True)
        return False

async def weather_worker():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_data(session, city, url) for city, url in API_URLS.items()]

                results = await asyncio.gather(*tasks)

                successful_count = sum(results)

                logging.info(f"[Воркер] Всего задач запущено: {len(results)}")
                logging.info(f"[Воркер] Успешно обработано запросов: {successful_count}")
                logging.info(f"[Воркер] Ошибок: {len(results) - successful_count}")
        except Exception as e:
            logging.error(f"[КРИТИЧЕСКАЯ ОШИБКА ВОРКЕРА]: {e}")

        logging.info(f"[Воркер] Засыпаем на {interval_seconds} секунд...")
        await asyncio.sleep(interval_seconds)