from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from telegram_bot.src.text_analyzer.intent import parse_intent
from telegram_bot.src.handlers.weather import weather_all
from telegram_bot.src.handlers.menu import menu


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = parse_intent(update.message.text)
    if data.is_weather_request:
        if data.city is not None:
            await context.bot_data.cache.set_current_city(data.city)
        await weather_all(update, context)
    else:
        await update.message.reply_text("Извините, я не понимаю вашу команду.")
        await menu(update, context)


unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)