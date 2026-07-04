import telegram_bot.src.settings.config as cfg

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import filters, MessageHandler, ConversationHandler
from telegram_bot.src.handlers.menu import menu
from telegram_bot.src.context import CustomContext


WAITING_CITY, CONFIRM_CITY = range(2)


async def change_city_start(update: Update, context: CustomContext) -> int:
    user_id = update.message.from_user.id
    current_city = await context.cache.get(user_id)
    reply_keyboard = [["Да", "Нет"]]
    await update.message.reply_text(
        f"Текущий город: {current_city}. Хотите сменить его?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            resize_keyboard=True,
        ),
    )

    return CONFIRM_CITY


async def change_city_confirm(update: Update, context: CustomContext) -> int:
    reply = update.message.text

    if reply == "Да":
        reply_keyboard = [cfg.CITIES]
        await update.message.reply_text(
            "Выберите город из списка:\n\n"
            "Уфа, Москва, Санкт-Петербург",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, 
                one_time_keyboard=True, 
                resize_keyboard=True,
            ),
        )

        return WAITING_CITY
    else:
        await menu(update, context)

        return ConversationHandler.END


async def save_new_city(update: Update, context: CustomContext) -> int:
    user_id = update.message.from_user.id
    current_city = update.message.text
    if not current_city or current_city not in cfg.CITIES:
        await update.message.reply_text(f"⚠️ Город {current_city} не найден. Попробуйте снова.\n\n")
    else:
        await context.cache.set(user_id, current_city)
        await context.db.set_user_data(user_id, current_city)
        await update.message.reply_text(f"Отлично, город сменён! Текущий город: {current_city}\n\n")

    await menu(update, context)

    return ConversationHandler.END


async def cancel(update: Update, context: CustomContext) -> int:
    await update.message.reply_text(
        "Действие отменено", reply_markup=ReplyKeyboardRemove()
    )

    await menu(update, context)

    return ConversationHandler.END


def create_city_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Сменить город"), change_city_start)],
        states={
            CONFIRM_CITY: [MessageHandler(filters.Text(["Да", "Нет"]), change_city_confirm)],
            WAITING_CITY: [MessageHandler(filters.Text(cfg.CITIES), save_new_city)],
        },
        fallbacks=[MessageHandler(filters.Text(["❌ Отмена", "Отмена"]), cancel)],
    )