from worker.src.settings.config import API_TOKEN


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
            f"&APPID={API_TOKEN}"
        )
