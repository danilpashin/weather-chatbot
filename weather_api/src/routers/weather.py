from fastapi import FastAPI
from weather_api.src.services import weather_service as service

app = FastAPI()

is_mock = False

class MockData:
    def __init__(self, name: str, temp: float, feels_like: float, weather_desc: str, wind: float, humidity: int):
        self.name = name
        self.temp = temp
        self.feels_like = feels_like
        self.weather_desc = weather_desc
        self.wind = wind
        self.humidity = humidity

dataUfa = MockData("Уфа", 24.66, 24.25, "облачно с прояснениями", 5.2, 48)
dataMoscow = MockData("Москва", 30.82, 26.85, "ясно", 2.5, 60)
dataSPB = MockData("Санкт-Петербург", 19.13, 18.45, "пасмурно", 12.4, 70)

@app.get("/weather")
async def root(name: str):
    if is_mock:
        match name:
            case "Уфа":
                return dataUfa
            case "Москва":
                return dataMoscow
            case "Санкт-Петербург":
                return dataSPB
            case _:
                return dataUfa
    else:
        data = await service.get_weather_data(name)
        return data
