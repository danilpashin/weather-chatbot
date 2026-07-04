def get_handlers():
    from telegram_bot.src.handlers import (start, help, weather, city, unknown)

    handlers = (
        start.create_start_handler(),
        help.create_help_handler(),
        weather.create_weather_handler(),
        city.create_city_handler(),
        unknown.create_unknown_handler()
    )

    return handlers