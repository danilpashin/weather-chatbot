from packages.cache.base import Cache
from packages.db.base import Database
from telegram.ext import CallbackContext, ExtBot
from telegram.ext import ContextTypes


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @property
    def db(self) -> Database:
        if self.bot_data is None:
            raise RuntimeError("bot_data is not initialized. Make sure application.bot_data is set before running.")
        return self.bot_data["db"]
    
    @property
    def cache(self) -> Cache:
        if self.bot_data is None:
            raise RuntimeError("bot_data is not initialized.")
        return self.bot_data["cache"]

context_types = ContextTypes(context=CustomContext)