from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from telegram_bot.src.context import CustomContext
from telegram_bot.src.handlers.city import (
    confirm_change_city,
    save_new_city,
    start_change_city,
)
from telegram_bot.src.handlers.notifications import (
    create_notifications_handlers,
    set_notification_time_save,
    set_timezone_save,
    show_notifications_menu,
)
from telegram_bot.src.handlers.settings_states import (
    CHANGING_CITY,
    NOTIFICATIONS_SETTING,
    SAVE_CITY,
    SELECTING_SETTING,
    SETTING_NOTIFICATION_TIME,
    SETTING_TIME_ZONE,
)
from telegram_bot.src.services.user_limiter import limiter


@limiter.as_decorator(name=lambda **kwargs: kwargs.get("user_id"))
async def start_settings(update: Update, context: CustomContext) -> int:
    keyboard = [
        [InlineKeyboardButton("🏙️ Сменить город", callback_data="menu_change_city")],
        [InlineKeyboardButton("🔔 Уведомления", callback_data="menu_notifications")],
        [InlineKeyboardButton("🏠 Назад в меню", callback_data="back_to_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Выберите настройки:"

    query = update.callback_query

    if query:
        await query.answer()
        msg = await query.edit_message_text(
            text=text, reply_markup=reply_markup, parse_mode="HTML"
        )
        context.user_data["active_inline_menu_id"] = msg.message_id
    else:
        msg = await update.effective_message.reply_text(
            text=text,
            reply_markup=reply_markup,
        )
        context.user_data["active_inline_menu_id"] = msg.message_id

    return SELECTING_SETTING


async def back_to_settings_menu(update: Update, context: CustomContext) -> int:
    await start_settings(update, context)
    return SELECTING_SETTING


async def back_to_menu(update: Update, context: CustomContext) -> int:
    await update.callback_query.answer()
    await update.callback_query.delete_message()

    return ConversationHandler.END


def create_settings_handler():
    return ConversationHandler(
        entry_points=[
            CommandHandler("settings", start_settings),
            MessageHandler(filters.Text(["Настройки", "⚙️Настройки"]), start_settings),
        ],
        states={
            SELECTING_SETTING: [
                CallbackQueryHandler(start_change_city, pattern="^menu_change_city$"),
                CallbackQueryHandler(
                    show_notifications_menu, pattern="^menu_notifications$"
                ),
            ],
            CHANGING_CITY: [
                CallbackQueryHandler(confirm_change_city, pattern="^confirm_change_"),
            ],
            SAVE_CITY: [
                CallbackQueryHandler(save_new_city, pattern="^set_city_"),
            ],
            NOTIFICATIONS_SETTING: create_notifications_handlers(),
            SETTING_NOTIFICATION_TIME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, set_notification_time_save
                )
            ],
            SETTING_TIME_ZONE: [
                CallbackQueryHandler(set_timezone_save, pattern="^tz_"),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(back_to_settings_menu, pattern="^back_to_settings$"),
            CallbackQueryHandler(back_to_menu, pattern="^back_to_menu$"),
        ],
    )
