from telegram import Update

from telegram_bot.src.context import CustomContext


async def clear_active_inline_menu(update: Update, context: CustomContext) -> None:
    active_menu_id = context.user_data.get("active_inline_menu_id")

    if active_menu_id:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=active_menu_id,
            )
        except Exception:
            pass
        finally:
            context.user_data["active_inline_menu_id"] = None
