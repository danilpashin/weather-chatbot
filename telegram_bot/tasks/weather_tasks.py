import asyncio
import datetime
import json

from aiolimiter import AsyncLimiter
from telegram import Bot

from packages.cache import cache
from packages.db import db
from packages.logging import logger
from telegram_bot.src.settings.config import TOKEN

rate_limiter = AsyncLimiter(max_rate=25, time_period=1.0)


async def send_notifications(users: list[dict]):
    bot = Bot(token=TOKEN)

    unique_cities = {user["city"] for user in users}

    weather_data = {}
    for city in unique_cities:
        data = await cache.get(city)
        weather_data[city] = json.loads(data)

    await bot.initialize()

    try:
        for user in users:
            async with rate_limiter:
                try:
                    chat_id = user["chat_id"]
                    user_city = user["city"]
                    current_weather = weather_data[user_city]

                    temp = current_weather["temp"]
                    feels_like = current_weather["feels_like"]
                    wind = current_weather["wind"]
                    weather_desc = current_weather["weather_desc"]

                    weather_text = (
                        "✨<b>Уведомление</b>✨\n"
                        f"🌍<b>Погода в городе {user_city}</b>\n"
                        "\n"
                        f"🌡 <i>Текущая температура:</i> "
                        f"<b><code>{temp}°C</code></b>\n"
                        f"🤔 <i>По ощущениям как:</i> "
                        f"<b><code>{feels_like}°C</code></b>\n"
                        f"💨 <i>Скорость ветра:</i> "
                        f"<b><code>{wind}м/с</code></b>\n"
                        f"☁️ <i>За окном сейчас:</i> "
                        f"<b><code>{weather_desc}</code></b>\n\n"
                        "─────────────────────\n"
                        "✨ <i>Хорошего дня и отличного настроения!</i> ☀️"
                        "📌 Для настройки подписок используйте меню ниже."
                    )

                    await bot.send_message(
                        chat_id=chat_id,
                        text=weather_text,
                        parse_mode="HTML",
                    )
                except Exception:
                    logger.error(
                        f"Ошибке при отправке уведомлений для города {user['city']} в "
                    )
    finally:
        await bot.shutdown()


def check_and_send_notifications():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    current_utc_minute = (now_utc.hour * 60) + now_utc.minute

    users_list = asyncio.run(db.get_users_by_minute(current_utc_minute))

    if users_list:
        asyncio.run(send_notifications(users_list))
