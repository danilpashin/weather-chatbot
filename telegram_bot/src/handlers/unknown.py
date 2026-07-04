from telegram import Update
from telegram.ext import MessageHandler, filters
from telegram_bot.src.context import CustomContext
from telegram_bot.src.text_analyzer.intent import parse_intent
from telegram_bot.src.handlers.weather import weather_all
from telegram_bot.src.handlers.menu import menu


async def unknown(update: Update, context: CustomContext):
    data = parse_intent(update.message.text)
    if data.is_weather_request:
        if data.city is not None:
            await context.cache.set(update.message.from_user.id, data.city)
        await weather_all(update, context)
    else:
        await update.message.reply_text("Извините, я не понимаю вашу команду.")
        await menu(update, context)


def create_unknown_handler():
    return MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)