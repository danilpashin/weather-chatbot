from telegram_bot.src.handlers import (start, weather, city, unknown)

handlers = [
    start.start_handler, 
    weather.weather_handler, 
    city.change_city_conv,
    unknown.unknown_handler
]