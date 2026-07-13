import string

import telegram_bot.src.text_analyzer.key_words as kw
from telegram_bot.src.domain.parsed_data import ParsedData
from telegram_bot.src.text_analyzer.analyzer import analyzer


def parse_intent(message) -> ParsedData:
    is_weather_request = False
    city = None

    for word in message.split():
        stripped_word = word.strip(string.punctuation)
        if not stripped_word:
            continue
        normal_form = analyzer.parse(stripped_word)[0].normal_form

        if not is_weather_request and normal_form in kw.WEATHER_KEYWORDS:
            is_weather_request = True
        else:
            for c in kw.CITIES:
                if c.lower() == normal_form:
                    city = c
                    break

            if city is None:
                for c in kw.CITIES_SHORT.keys():
                    if c == normal_form:
                        city = kw.CITIES_SHORT[c]
                        break

    return ParsedData(is_weather_request, city)
