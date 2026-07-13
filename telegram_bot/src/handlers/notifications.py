import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler

from telegram_bot.src.context import CustomContext
from telegram_bot.src.handlers.settings_states import (
    NOTIFICATIONS_SETTING,
    SETTING_NOTIFICATION_TIME,
    SETTING_TIME_ZONE,
)


async def show_notifications_menu(update: Update, context: CustomContext) -> int:
    user_id = update.effective_user.id

    current_city = await context.db.get_user_data(user_id)
    weather_data = await context.cache.get(current_city)

    notification_enabled = await context.db.get_notification_status(user_id)
    notification_time = await context.db.get_notification_time(user_id) or "09:00"
    time_zone = await context.db.get_user_timezone(user_id) or "UTC+3"

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Включено" if notification_enabled else "❌ Выключено",
                callback_data="toggle_notifications",
            )
        ],
        [
            InlineKeyboardButton(
                "⏰ Время уведомления", callback_data="set_notification_time"
            )
        ],
        [InlineKeyboardButton("🌍 Часовой пояс", callback_data="set_timezone")],
        [InlineKeyboardButton("⚙️ Назад", callback_data="back_to_settings")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = (
        f"✨ <b>Настройки уведомлений</b>\n\n"
        f"🏙️ Город: <b>{current_city}</b>\n"
        f"🌤️ Текущая погода: {'Доступна' if weather_data else 'Не определена'}\n"
        f"📅 Включены уведомления: {'Да' if notification_enabled else 'Нет'}\n"
        f"⏰ Время: {notification_time}\n"
        f"🌍 Часовой пояс: "
        f"{f'UTC+{time_zone}' if time_zone > 0 else f'UTC-{time_zone}'}\n"
    )

    query = update.callback_query

    if query:
        await query.answer()
        await update.callback_query.edit_message_text(
            text=message_text, reply_markup=reply_markup, parse_mode="HTML"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message_text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

    return NOTIFICATIONS_SETTING


async def toggle_notifications(update: Update, context: CustomContext) -> int:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    current_state = await context.db.get_notification_status(user_id)
    new_state = not current_state

    await context.db.set_chat_id(chat_id, user_id)
    await context.db.set_notification_status(user_id, new_state)
    await show_notifications_menu(update, context)

    return NOTIFICATIONS_SETTING


async def set_notification_time_prompt(update: Update, context: CustomContext) -> int:
    await update.callback_query.edit_message_text(
        text="⏰ Введите время уведомления в формате <b>ЧЧ:ММ</b> (например, 09:00):",
        parse_mode="HTML",
    )

    return SETTING_NOTIFICATION_TIME


async def set_notification_time_save(update: Update, context: CustomContext) -> int:
    user_id = update.effective_user.id
    user_input = update.message.text.strip() if update.message else ""
    user_tz_offset = await context.db.get_user_timezone(user_id)

    import re

    if not re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", user_input):
        await update.message.reply_text(
            "❌ Некорректный формат времени! Используйте HH:MM (например, 09:00).",
            parse_mode="HTML",
        )
        return SETTING_NOTIFICATION_TIME

    hours, minutes = map(int, user_input.split(":"))

    local_dt = datetime.datetime.combine(
        datetime.date.today(), datetime.time(hours, minutes)
    )
    utc_dt = local_dt - datetime.timedelta(hours=user_tz_offset)

    utc_minutes_value = (utc_dt.hour * 60) + utc_dt.minute

    await context.db.set_notification_time(user_id, user_input, utc_minutes_value)
    await show_notifications_menu(update, context)

    return NOTIFICATIONS_SETTING


async def set_timezone_prompt(update: Update, context: CustomContext) -> int:
    keyboard = [
        [InlineKeyboardButton("UTC+2", callback_data="tz_2")],
        [InlineKeyboardButton("UTC+3", callback_data="tz_3")],
        [InlineKeyboardButton("UTC+4", callback_data="tz_4")],
        [InlineKeyboardButton("UTC+5", callback_data="tz_5")],
        [InlineKeyboardButton("UTC", callback_data="tz_0")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_notifications")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        text="🌍 Выберите ваш часовой пояс:", reply_markup=reply_markup
    )

    return SETTING_TIME_ZONE


async def set_timezone_save(update: Update, context: CustomContext) -> int:
    user_id = update.effective_user.id
    tz_data = int(update.callback_query.data.replace("tz_", ""))

    await context.db.set_user_timezone(user_id, tz_data)

    await show_notifications_menu(update, context)

    return NOTIFICATIONS_SETTING


def create_notifications_handlers():
    return [
        CallbackQueryHandler(show_notifications_menu, pattern="^menu_notifications$"),
        CallbackQueryHandler(toggle_notifications, pattern="^toggle_notifications$"),
        CallbackQueryHandler(set_timezone_prompt, pattern="^set_timezone$"),
        CallbackQueryHandler(
            set_notification_time_prompt, pattern="^set_notification_time$"
        ),
        CallbackQueryHandler(
            show_notifications_menu, pattern="^back_to_notifications$"
        ),
    ]
