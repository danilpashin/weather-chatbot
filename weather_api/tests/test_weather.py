import pytest
from unittest.mock import AsyncMock, patch
from weather_api.src.domain.data import Data
from weather_api.src.domain.exceptions import CityNotFoundError


@pytest.mark.anyio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_get_weather_success(client):
    with patch("weather_api.src.routers.weather.service.get_weather_data", new_callable=AsyncMock) as mock_get_weather:
        mock_get_weather.return_value = Data(22.5, 21.9, "облачно с прояснениями", 3.5, 52)

        response = await client.get("/weather?name=Уфа")

        assert response.status_code == 200
        assert response.json() == {
            "temp": 22.5,
            "feels_like": 21.9,
            "weather_desc": "облачно с прояснениями",
            "wind": 3.5,
            "humidity": 52
        }
        mock_get_weather.assert_awaited_once_with("Уфа")


@pytest.mark.anyio
async def test_get_weather_empty_name(client):
    response = await client.get("/weather?name=")
    assert response.status_code == 400
    assert response.json()["detail"] == "Город не указан"


@pytest.mark.anyio
async def test_get_weather_missing_name(client):
    response = await client.get("/weather")
    assert response.status_code == 400
    assert response.json()["detail"] == "Город не указан"


@pytest.mark.anyio
async def test_get_weather_city_not_found(client):
    with patch("weather_api.src.routers.weather.service.get_weather_data", new_callable=AsyncMock) as mock_get_weather:
        mock_get_weather.side_effect = CityNotFoundError("Город не найден")

        response = await client.get("/weather?name=Москва")

        assert response.status_code == 404
        assert response.json()["detail"] == "Город 'Москва' не найден"
        mock_get_weather.assert_awaited_once_with("Москва")


@pytest.mark.anyio
async def test_get_weather_internal_error(client):
    with patch("weather_api.src.routers.weather.service.get_weather_data", new_callable=AsyncMock) as mock_get_weather:
        mock_get_weather.side_effect = Exception("База данных не отвечает")

        response = await client.get("/weather?name=Уфа")

        assert response.status_code == 500
        assert response.json()["detail"] == "Внутренняя ошибка сервера"
        mock_get_weather.assert_awaited_once_with("Уфа")


@pytest.mark.anyio
async def test_get_weather_with_whitespace(client):
    with patch("weather_api.src.routers.weather.service.get_weather_data", new_callable=AsyncMock) as mock_get_weather:
        mock_get_weather.return_value = Data(10.0, 9.5, "ясно", 2.0, 60)

        response = await client.get("/weather?name=%20%20%20%20%20")
        assert response.status_code == 400

        response = await client.get("/weather?name=%20Уфа%20")
        assert response.status_code == 200
        mock_get_weather.assert_awaited_once_with("Уфа")