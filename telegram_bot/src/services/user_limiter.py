import time
from functools import wraps
from telegram import Update
from telegram_bot.src.context import CustomContext
from packages.cache import cache


def rate_limit(limit_seconds: float = 0.5):
    def decorator(handler_func):
        @wraps(handler_func)
        async def wrapper(update: Update, context: CustomContext):
            user_id = update.effective_user.id
            current_time = time.time()

            last_time = await cache.get(user_id)
            if last_time:
                if (current_time - last_time) < limit_seconds:
                    if update.callback_query:
                        await update.callback_query.answer(
                            text="Слишком частые запросы! Подождите.",
                            show_alert=True,
                        )
                    return

            await cache.set(user_id, current_time)

            return await handler_func(update, context)

        return wrapper

    return decorator
