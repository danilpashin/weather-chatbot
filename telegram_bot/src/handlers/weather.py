import aiohttp
import telegram_bot.src.settings.config as cfg

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram_bot.src.handlers.menu import menu
from packages.logging import logger


async def weather_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_city = await context.bot_data.cache.get_current_city()
    current_url = f"{cfg.URL}?name={current_city}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(current_url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"❌ Ошибка API {response.status}: {error_text}")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"❌ Ошибка API: {response.status}. Подробности в логах."
                    )
                    return None
                
                data = await response.json()
                logger.info(f"✅ {current_city} - Данные успешно получены")
                lines = [
                    f"🌍 Прогноз погоды в городе {current_city}:",
                    "",
                    f"🌡 Текущая температура: {data["temp"]}°C",
                    f"🤔 По ощущениям: {data["feels_like"]}°C",
                    f"💨 Ветер: {data["wind"]} м/с",
                    f"☁️ На улице: {data["weather_desc"]}"
                ]

                ans = "\n".join(lines)

                await context.bot.send_message(chat_id=update.effective_chat.id, text=ans)
        except Exception as e:
            logger.error(f"❌ Ошибка при запросе к {current_url}: {e}", exc_info=True)
            return None
        
    await menu(update, context)


weather_handler = MessageHandler(filters.Text("Погода"), weather_all)