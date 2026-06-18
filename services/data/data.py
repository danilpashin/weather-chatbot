class Data:
    def __init__(self, lat: float, lon: float, name: str, temp: float, feels_like: float, weather_desc: str, wind: float, humidity: int):
        self.lat = lat
        self.lon = lon
        self.name = name
        self.temp = temp
        self.feels_like = feels_like
        self.weather_desc = weather_desc
        self.wind = wind
        self.humidity = humidity

    def set(self, temp: float, feels_like: float, weather_desc: str, wind: float, humidity: int):
        self.temp = temp
        self.feels_like = feels_like
        self.weather_desc = weather_desc
        self.wind = wind
        self.humidity = humidity
    