import aiohttp
import asyncio
import json
import os
import redis
from packages.core.config import init_config
from weather_api.src.domain.coord import Coord

init_config()

dataUfa = Coord(54.73, 55.95)
dataMoscow = Coord(55.75, 37.62)
dataSPB = Coord(59.94, 30.32)

API_URLS={
    "Уфа":f"https://api.openweathermap.org/data/2.5/weather?lat={dataUfa.lat}&lon={dataUfa.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}",
    "Москва": f"https://api.openweathermap.org/data/2.5/weather?lat={dataMoscow.lat}&lon={dataMoscow.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}",
    "Санкт-Петербург": f"https://api.openweathermap.org/data/2.5/weather?lat={dataSPB.lat}&lon={dataSPB.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}"
}

r = redis.asyncio.Redis(host=os.getenv("REDIS_WEATHER_HOST"), port=os.getenv("REDIS_WEATHER_PORT"), decode_responses=True)
interval_seconds = 10

async def fetch_data(session, city, url):
    try:
        async with session.get(url) as response:
            data = await response.json()

            payload = {
                "temp": data["main"]["temp"], 
                "feels_like": data["main"]["feels_like"], 
                "weather_desc": data["weather"][0]["description"], 
                "wind": data["wind"]["speed"], 
                "humidity": data["main"]["humidity"]
            }

            value = json.dumps(payload)

            await r.set(name=city, value=value)
            print(f"Данные по городу {city} успешно сохранены в Redis.")
            return None
    except Exception as e:
        print(f"Ошибка при запросе к {url}: {e}")
        return None         

async def background_api_worker():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_data(session, city, url) for city, url in API_URLS.items()]

                results = await asyncio.gather(*tasks)

                print(f"[Воркер] Успешно обработано запросов: {len(results)}")
        except Exception as e:
            print(f"[КРИТИЧЕСКАЯ ОШИБКА ВОРКЕРА]: {e}")

        print(f"[Воркер] Засыпаем на {interval_seconds} секунд...")
        await asyncio.sleep(interval_seconds)