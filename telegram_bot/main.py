from telegram.ext import ApplicationBuilder
from packages.logging import logger
from packages.cache import cache
from packages.db import db
from telegram_bot.src.settings.config import TOKEN
from telegram_bot.src.context import context_types


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).context_types(context_types).build()

    application.bot_data["db"] = db
    application.bot_data["cache"] = cache

    from telegram_bot.src.handlers import get_handlers

    application.add_handlers(get_handlers())

    logger.info("МетеоБот запускается...")
    application.run_polling()
