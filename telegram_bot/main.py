from telegram.ext import ApplicationBuilder
from packages.logging import logger
from packages.cache import cache
from telegram_bot.src.settings import config as cfg
import telegram_bot.src.handlers as handlers


if __name__ == '__main__':
    application = ApplicationBuilder().token(cfg.TOKEN).build()

    application.bot_data = type('BotContext', (), {
        'cache': cache
    })()

    application.add_handlers(handlers.handlers)
    
    logger.info('МетеоБот запускается...')
    application.run_polling()