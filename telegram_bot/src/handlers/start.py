import telegram_bot.src.settings.config as cfg

from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler
from telegram_bot.src.handlers.menu import menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_city = await context.bot_data.cache.get_current_city()
    await update.message.reply_text(
        "Привет! Меня зовут ☁️МетеоБот☁️. У меня ты можешь узнать погоду в своем городе!\n\n"
        "Отправь /cancel, чтобы закончить диалог.\n\n"
        f"По умолчанию установлен город {current_city}",
    )

    await menu(update, context)

start_handler = CommandHandler('start', start)