from telegram import Update
from telegram.ext import MessageHandler, filters

from telegram_bot.src.context import CustomContext
from telegram_bot.src.handlers.weather import weather_all
from telegram_bot.src.services.user_limiter import limiter
from telegram_bot.src.text_analyzer.intent import parse_intent


@limiter.as_decorator(name=lambda **kwargs: kwargs.get("user_id"))
async def unknown(update: Update, context: CustomContext):
    data = parse_intent(update.message.text)
    if data.is_weather_request:
        if data.city is not None:
            await context.cache.set(update.message.from_user.id, data.city, 300)
        await weather_all(update, context)
    else:
        text = (
            "Извини, я не понял твой запрос.\n"
            "Пожалуйста, введи запрос в виде: 'погода в москве' "
            "или воспользуйся кнопками меню ниже 👇"
        )
        await update.message.reply_text(
            text=text,
        )


def create_unknown_handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)
