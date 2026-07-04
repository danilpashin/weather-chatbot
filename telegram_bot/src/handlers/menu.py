from telegram import Update, ReplyKeyboardMarkup
from telegram_bot.src.context import CustomContext


async def menu(update: Update, context: CustomContext, text="Выберите команду"):
    reply_keyboard = [["Погода", "Сменить город"]]
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )