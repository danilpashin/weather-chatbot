from uuid import uuid4
from telegram import Update
from telegram.ext import CommandHandler
from telegram_bot.src.handlers.menu import menu
from telegram_bot.src.context import CustomContext
from packages.logging.logger import trace_id_var, user_id_var


async def start(update: Update, context: CustomContext):
    user_id = update.message.from_user.id
    trace_id = str(uuid4())

    trace_id_var.set(trace_id)
    user_id_var.set(str(user_id))

    current_city = await context.db.get_user_data(user_id)
    if current_city is None:
        await context.db.set_user_data(user_id, "Москва")
        current_city = "Москва"
    await context.cache.set(user_id, current_city, 300)
    await update.message.reply_text(
        "Привет! Меня зовут ☁️МетеоБот☁️. У меня ты можешь узнать погоду в своем городе!\n\n"
        "Отправь /help, чтобы просмотреть доступные команды.\n\n"
        f"По умолчанию установлен город {current_city}",
    )

    await menu(update, context)


def create_start_handler():
    return CommandHandler("start", start)
