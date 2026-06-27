from uuid import uuid4
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler
from telegram_bot.src.handlers.menu import menu
from packages.logging.setup import trace_id_var, user_id_var


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    trace_id = str(uuid4())

    trace_id_var.set(trace_id)
    user_id_var.set(user_id)

    current_city = await context.bot_data.cache.get_current_city()
    await update.message.reply_text(
        "Привет! Меня зовут ☁️МетеоБот☁️. У меня ты можешь узнать погоду в своем городе!\n\n"
        "Отправь /cancel, чтобы закончить диалог.\n\n"
        f"По умолчанию установлен город {current_city}",
    )

    await menu(update, context)

start_handler = CommandHandler('start', start)