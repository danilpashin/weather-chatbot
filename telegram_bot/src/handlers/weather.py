import aiohttp
import telegram_bot.src.settings.config as cfg

from uuid import uuid4
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram_bot.src.handlers.menu import menu
from packages.logging import logger
from packages.logging.setup import trace_id_var, user_id_var


async def weather_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_city = await context.bot_data.cache.get(update.message.from_user.id)
    current_url = f"{cfg.URL}?name={current_city}"

    user_id = user_id_var.get()
    trace_id = trace_id_var.get()

    headers = {
        "X-Trace-ID": trace_id,
        "X-User-ID": user_id
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(current_url, headers=headers) as response:
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