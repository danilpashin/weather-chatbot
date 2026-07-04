import aiohttp
from packages.logging import logger


async def fetch_data(session: aiohttp.ClientSession, url):
    try:
        async with session.get(url) as response:
            data = await response.json()

            if response.status != 200:
                logger.error("Ошибка при запросе к API.")
                return None

            payload = {
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "weather_desc": data["weather"][0]["description"],
                "wind": data["wind"]["speed"],
                "humidity": data["main"]["humidity"],
            }

            return payload
    except Exception as e:
        logger.error(f"Ошибка при запросе к {url}: {e}", exc_info=True)
        return None
