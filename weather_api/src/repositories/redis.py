from weather_api.src.repositories.base import WeatherStorage
from typing import Any
import os
import json
import redis
import logging

class RedisStorage(WeatherStorage):
    def __init__(self, host: str = None, port: int = 6379):
        self.host = host or os.getenv("REDIS_HOST", "localhost")
        self.port = port
        self._client = None

    async def _get_client(self):
        if self._client is None:
            self._client = redis.asyncio.Redis(
                host=self.host, port=self.port, decode_responses=True
            )
        return self._client

    async def get_weather(self, city: str) -> dict[str, Any] | None:
        try:
            client = await self._get_client()
            raw = await client.get(city)
            if raw is None:
                logging.info(f"Данные для города {city} не найдены.")
            return json.loads(raw) if raw else None
        except Exception as e:
            logging.error(f"Ошибка Redis при получении данных для города '{city}': {e}")
            return None

    async def close(self):
        if self._client:
            await self._client.close()
            self._client = None