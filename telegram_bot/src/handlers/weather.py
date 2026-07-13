import aiohttp
import telegram_bot.src.settings.config as cfg

from telegram import Update
from telegram.ext import MessageHandler, filters
from telegram_bot.src.utils.telegram_helpers import clear_active_inline_menu
from telegram_bot.src.context import CustomContext
from telegram_bot.src.services.user_limiter import rate_limit
from packages.logging import logger
from packages.logging.logger import trace_id_var, user_id_var
from telegram_bot.src.services.user_limiter import limiter


@limiter.as_decorator(name=lambda **kwargs: kwargs.get('user_id'))
async def weather_all(update: Update, context: CustomContext):
    current_city = await context.cache.get(update.effective_user.id)
    if current_city is None:
        current_city = await context.db.get_user_data(update.effective_user.id)
        await context.cache.set(update.effective_user.id, current_city, 300)

    current_url = f"{cfg.URL}?name={current_city}"

    user_id = user_id_var.get()
    trace_id = trace_id_var.get()

    headers = {
        "X-Trace-ID": trace_id,
        "X-User-ID": user_id,
    }

    await clear_active_inline_menu(update, context)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(current_url, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"❌ Ошибка API {response.status}: {error_text}")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="❌ Ошибка сервера, попробуйте ещё раз позже!",
                    )
                    return None

                data = await response.json()
                logger.info(f"✅ {current_city} - Данные успешно получены")

                weather_text = (
                    f"🌍<b>Погода в городе {current_city}</b>\n"
                    "\n"
                    f"🌡 <i>Текущая температура:</i> <b><code>{data['temp']}°C</code></b>\n"
                    f"🤔 <i>По ощущениям как:</i> <b><code>{data['feels_like']}°C</code></b>\n"
                    f"💨 <i>Скорость ветра:</i> <b><code>{data['wind']}м/с</code></b>\n"
                    f"☁️ <i>За окном сейчас:</i> <b>{data['weather_desc']}</b>\n\n"
                    f"─────────────────────\n"
                    f"✨ <i>Хорошего дня и отличного настроения!</i> ☀️"
                )

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=weather_text,
                    parse_mode="HTML",
                )
        except Exception as e:
            logger.error(f"❌ Ошибка при запросе к {current_url}: {e}", exc_info=True)
            return None


def create_weather_handler():
    return MessageHandler(filters.Text(["Погода", "☁️Погода"]), weather_all)
