from uuid import uuid4
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram_bot.src.context import CustomContext
from telegram_bot.src.services.user_limiter import rate_limit
from packages.logging.logger import trace_id_var, user_id_var


@rate_limit(limit_seconds=1)
async def start(update: Update, context: CustomContext):
    user_id = update.message.from_user.id
    trace_id = str(uuid4())

    trace_id_var.set(trace_id)
    user_id_var.set(str(user_id))

    current_city = await context.db.get_user_data(user_id)
    if current_city is None:
        await context.db.set_user_data(
            user_id=user_id,
            city="Москва",
            tz=3,
        )
        current_city = "Москва"
    await context.cache.set(user_id, current_city, 300)

    await menu(update)


async def menu(update: Update):
    welcome_text = (
        "Привет! Меня зовут ☁️<b>МетеоБот</b>☁️. У меня ты можешь узнать погоду в своем городе!\n\n"
        "<i>Отправь <b><code>/help</code></b>, чтобы просмотреть доступные команды.</i>"
    )

    reply_keyboard = [["☁️Погода", "⚙️Настройки"]]
    await update.effective_message.reply_text(
        text=welcome_text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            resize_keyboard=True,
            input_field_placeholder="Выберите кнопку ниже или введите текстом...",
        ),
        parse_mode="HTML",
    )


def create_start_handler():
    return CommandHandler("start", start)
