def get_handlers():
    from telegram_bot.src.handlers import start, help, weather, settings, unknown

    handlers = (
        start.create_start_handler(),
        help.create_help_handler(),
        weather.create_weather_handler(),
        settings.create_settings_handler(),
        unknown.create_unknown_handler(),
    )

    return handlers
