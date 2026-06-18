from fastapi import FastAPI
import requests
from services.data.data import Data
import os
import sys
from pathlib import Path
from packages.core.config import init_config

init_config()

app = FastAPI()

is_mock = False

dataUfa = Data(54.73, 55.95, "Ufa", 24.66, 24.25, "облачно с прояснениями", 5.2, 48)
dataMoscow = Data(55.75, 37.62, "Moscow", 30.82, 26.85, "ясно", 2.5, 60)
dataSPB = Data(59.94, 30.32, "Saint Petersburg", 19.13, 18.45, "пасмурно", 12.4, 70)

@app.get("/storage")
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
        match name:
            case "Уфа":
                response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataUfa.lat}&lon={dataUfa.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")
            case "Москва":
                response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataMoscow.lat}&lon={dataMoscow.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")
            case "Санкт-Петербург":
                response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataSPB.lat}&lon={dataSPB.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")
            case _:
                response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={dataUfa.lat}&lon={dataUfa.lon}&units=metric&lang=ru&APPID={os.getenv("API_TOKEN")}")

        if response.status_code == 200:
            json_data = response.json()
            data = Data(json_data["coord"]["lat"], json_data["coord"]["lon"], name, json_data["main"]["temp"], json_data["main"]["feels_like"], json_data["weather"][0]["description"], json_data["wind"]["speed"], json_data["main"]["humidity"])
            return data
        else:
            return {"error": "failed to fetch data", "status_code": f"{response.status_code}"}
