import requests
import os
from packages.core.config import init_config
from weather_api.src.domain.coord import Coord

init_config()

dataUfa = Coord(54.73, 55.95)
dataMoscow = Coord(55.75, 37.62)
dataSPB = Coord(59.94, 30.32)

async def get_api_data(city):
    match city:
        case "Уфа":
            data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataUfa.lat}&lon={dataUfa.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")
        case "Москва":
            data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataMoscow.lat}&lon={dataMoscow.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")
        case "Санкт-Петербург":
            data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataSPB.lat}&lon={dataSPB.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")
        case _:
            data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataUfa.lat}&lon={dataUfa.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")
    
    return data