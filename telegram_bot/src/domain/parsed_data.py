class ParsedData:
    def __init__(self, is_weather_request: bool, city: str | None):
        self.is_weather_request = is_weather_request
        self.city = city
