import telegram_bot.src.settings.config as cfg

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import filters, MessageHandler, ContextTypes, ConversationHandler
from telegram_bot.src.handlers.menu import menu


WAITING_CITY, CONFIRM_CITY = range(2)


async def change_city_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    current_city = await context.bot_data.cache.get_current_city()
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


async def change_city_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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


async def save_new_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    current_city = update.message.text
    if not current_city or current_city not in cfg.CITIES:
        await update.message.reply_text(f"⚠️ Город {current_city} не найден. Попробуйте снова.\n\n")
    else:
        await context.bot_data.cache.set_current_city(current_city)
        await update.message.reply_text(f"Отлично, город сменён! Текущий город: {current_city}\n\n")

    await menu(update, context)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Действие отменено", reply_markup=ReplyKeyboardRemove()
    )

    await menu(update, context)

    return ConversationHandler.END


change_city_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Сменить город"), change_city_start)],
        states={
            CONFIRM_CITY: [MessageHandler(filters.Text(["Да", "Нет"]), change_city_confirm)],
            WAITING_CITY: [MessageHandler(filters.Text(cfg.CITIES), save_new_city)],
        },
        fallbacks=[MessageHandler(filters.Text(["❌ Отмена", "Отмена"]), cancel)],
    )