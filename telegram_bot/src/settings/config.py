import os

from packages.core.env import init_env

init_env()

CITIES = ("Уфа", "Москва", "Санкт-Петербург")
URL = f"http://{os.getenv('API_HOST')}:{os.getenv('API_PORT')}/weather"
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CITIES_TIMEZONES = {
    "Уфа": 5,
    "Москва": 3,
    "Санкт-Петербург": 3,
}
