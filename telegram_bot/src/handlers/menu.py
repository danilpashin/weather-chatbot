from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text="Выберите команду"):
    reply_keyboard = [["Погода", "Сменить город"]]
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )