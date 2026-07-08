from telegram_bot.src.settings.config import CITIES_TIMEZONES


async def get_city_timezone(city: str) -> int:
    return CITIES_TIMEZONES[city]
