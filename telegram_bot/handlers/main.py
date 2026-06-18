import logging
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler
import os
from packages.core.config import init_config

init_config()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

url = "http://127.0.0.1:8080/weather"
current_city = "Уфа"

WAITING_CITY, CONFIRM_CITY = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Меня зовут ☁️МетеоБот☁️. У меня ты можешь узнать погоду в своем городе!\n\n"
        "Отправь /cancel, чтобы закончить диалог.\n\n"
        f"По умолчанию установлен город {current_city}",
    )

    await menu(update, context)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text="Выберите команду"):
    reply_keyboard = [["Погода", "Сменить город"]]
    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

async def change_city_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global city

    reply_keyboard = [["Да", "Нет"]]
    await update.message.reply_text(
        f"Текущий город: {current_city}. Хотите сменить его?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return CONFIRM_CITY

async def change_city_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply = update.message.text

    if reply == "Да":
        reply_keyboard = [["Уфа", "Москва", "Санкт-Петербург"]]
        await update.message.reply_text(
            "Выберите город из списка:\n\n"
            "Уфа, Москва, Санкт-Петербург",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )

        return WAITING_CITY
    else:
        await menu(update, context)

async def save_new_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global current_city
    current_city = update.message.text
    await update.message.reply_text(f"Отлично, город сменён! Текущий город: {current_city}\n\n")

    await menu(update, context)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Пока! Пиши в любое время!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def weather_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(url + f"?name={current_city}")

    if response.status_code == 200:
        data = response.json()
        lines = [
            f"🌍 Прогноз погоды в городе {current_city}:",
            "",
            f"🌡 Текущая температура: {data["temp"]}°C",
            f"🤔 По ощущениям: {data["feels_like"]}°C",
            f"💨 Ветер: {data["wind"]} м/с",
            f"☁️ На улице: {data["weather_desc"]}"
        ]

        ans = "\n".join(lines)
    else:
        data = "Не удалось получить данные!\n\nПопробуйте ещё раз через некоторое время"
        ans = data
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ans)

    await menu(update, context)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, я не понимаю вашу команду")
    await menu(update, context)


if __name__ == '__main__':
    application = ApplicationBuilder().token(f'{os.getenv("TELEGRAM_BOT_TOKEN")}').build()

    start_handler = CommandHandler('start', start)
    weather_handler = MessageHandler(filters.Text("Погода"), weather_all)

    change_city_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Сменить город"), change_city_start)],
        states={
            CONFIRM_CITY: [MessageHandler(filters.Text(["Да", "Нет"]), change_city_confirm)],
            WAITING_CITY: [MessageHandler(filters.Text(["Уфа", "Москва", "Санкт-Петербург"]), save_new_city)],
        },
        fallbacks=[],
    )
    cancel_handler = CommandHandler('cancel', cancel)
    unknown_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(weather_handler)
    application.add_handler(change_city_conv)
    application.add_handler(cancel_handler)
    application.add_handler(unknown_handler)
    
    application.run_polling()