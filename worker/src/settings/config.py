import os
from packages.core.env import init_env

init_env()

class CityTask:
    def __init__(self, city: str, lat: float, lon: float):
        self.city = city
        self.lat = lat
        self.lon = lon

    @property
    def url(self) -> str:
        return (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={self.lat}&lon={self.lon}"
            f"&units=metric&lang=ru"
            f"&APPID={os.getenv('API_TOKEN')}"
        )

CITIES = [
    CityTask("Уфа", 54.73, 55.95),
    CityTask("Москва", 55.75, 37.62),
    CityTask("Санкт-Петербург", 59.94, 30.32),
]

DEFAULT_INTERVAL = int(os.getenv("INTERVAL_SECONDS", 3600))