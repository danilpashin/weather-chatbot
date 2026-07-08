from telegram import Update
from telegram.ext import MessageHandler, filters
from telegram_bot.src.context import CustomContext
from telegram_bot.src.services.user_limiter import rate_limit
from telegram_bot.src.text_analyzer.intent import parse_intent
from telegram_bot.src.handlers.weather import weather_all


@rate_limit(limit_seconds=0.5)
async def unknown(update: Update, context: CustomContext):
    data = parse_intent(update.message.text)
    if data.is_weather_request:
        if data.city is not None:
            await context.cache.set(update.message.from_user.id, data.city)
        await weather_all(update, context)
    else:
        text = (
            "Извини, я не понял твой запрос.\n"
            "Пожалуйста, введи запрос в виде: 'погода в москве' или воспользуйся кнопками меню ниже 👇"
        )
        await update.message.reply_text(
            text=text,
        )


def create_unknown_handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)
