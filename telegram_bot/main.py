import asyncio

from telegram.ext import ApplicationBuilder

from packages.cache import cache
from packages.db import db
from packages.logging import logger
from telegram_bot.src.context import context_types
from telegram_bot.src.services.user_limiter import init_limiter
from telegram_bot.src.settings.config import TOKEN


async def main():
    await init_limiter()

    application = ApplicationBuilder().token(TOKEN).context_types(context_types).build()

    application.bot_data["db"] = db
    application.bot_data["cache"] = cache

    from telegram_bot.src.handlers import get_handlers

    application.add_handlers(get_handlers())

    logger.info("МетеоБот запускается...")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
