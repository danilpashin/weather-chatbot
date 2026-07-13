from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler

import telegram_bot.src.settings.config as cfg
from telegram_bot.src.context import CustomContext
from telegram_bot.src.handlers.settings_states import CHANGING_CITY, SAVE_CITY
from telegram_bot.src.services.location import get_city_timezone


async def start_change_city(update: Update, context: CustomContext) -> int:
    user_id = update.effective_user.id
    current_city = await context.cache.get(user_id)
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Да, сменить город", callback_data="confirm_change_yes"
                )
            ],
            [InlineKeyboardButton("⚙️Назад в меню", callback_data="confirm_change_no")],
        ]
    )

    await update.callback_query.edit_message_text(
        text=f"<i>Текущий город</i>: <b>{current_city}</b>. Хотите сменить его?",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )

    return CHANGING_CITY


async def confirm_change_city(update: Update, context: CustomContext) -> int:
    await update.callback_query.answer()

    if update.callback_query.data == "confirm_change_yes":
        city_buttons = [
            [InlineKeyboardButton(city, callback_data=f"set_city_{city}")]
            for city in cfg.CITIES
        ]
        reply_markup = InlineKeyboardMarkup(city_buttons)
        await update.callback_query.edit_message_text(
            text="Выберите город из списка:",
            reply_markup=reply_markup,
            parse_mode="HTML",
        )

        return SAVE_CITY
    else:
        await update.callback_query.edit_message_reply_markup(reply_markup=None)

        return ConversationHandler.END


async def save_new_city(update: Update, context: CustomContext) -> int:
    user_id = update.effective_user.id
    current_city = update.callback_query.data.replace("set_city_", "")
    if not current_city or current_city not in cfg.CITIES:
        await update.callback_query.edit_message_text(
            text=f"⚠️ Город <b>{current_city}</b> не поддерживается!\n\n",
            parse_mode="HTML",
        )
    else:
        timezone = await get_city_timezone(current_city)

        await context.cache.set(user_id, current_city, 300)
        await context.db.set_user_data(user_id, current_city, timezone)

        reply_text = (
            f"✨<b>Отлично, город сменён!</b>✨ "
            f"🌃 <i>Текущий город:</i> <b>{current_city}</b>"
        )

        await update.callback_query.edit_message_text(
            text=reply_text,
            parse_mode="HTML",
        )

    return ConversationHandler.END
