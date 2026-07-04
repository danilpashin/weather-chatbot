from packages.cache.base import Cache
from packages.db.base import Database
from telegram.ext import CallbackContext, ExtBot
from telegram.ext import ContextTypes


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @property
    def db(self) -> Database:
        return self.bot_data["db"]

    @property
    def cache(self) -> Cache:
        return self.bot_data["cache"]


context_types = ContextTypes(context=CustomContext)
