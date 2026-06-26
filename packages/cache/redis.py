import redis
import json
import os
from typing import Any
from packages.cache.base import Cache
from packages.logging import logger
from packages.core.env import init_env

init_env()

class RedisCache(Cache):
    def __init__(self):
        self._client = None
        self._host = os.getenv("REDIS_HOST", "localhost")
        self._port = int(os.getenv("REDIS_PORT", 6379))
        self._decode_responses = True

    async def set(self, key: str, value: str | bytes, ex: int | None = None):
        client = await self._get_client()
        if ex:
            await client.set(key, value, ex=ex)
        else:
            await client.set(key, value)

    async def get(self, key: str) -> str | None:
        client = await self._get_client()
        return await client.get(key)

    async def _get_client(self):
        if self._client is None:
            self._client = redis.asyncio.Redis(
                host=self._host,
                port=self._port,
                decode_responses=self._decode_responses
            )
        return self._client

    async def get_weather(self, city: str) -> dict[str, Any] | None:
        try:
            client = await self._get_client()
            raw = await client.get(city)
            if not raw:
                return None
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, TypeError) as e:
                logger.error(f"Ошибка при декодировании данных для города {city}: {e}")
                return None
        except Exception as e:
            logger.error(f"Ошибка при получении данных о погоде для города {city}: {e}")
            return None
        
    async def set_weather(self, city: str, value):
        try:
            client = await self._get_client()
            await client.set(city, value)
        except Exception as e:
            logger.error(f"Ошибка при записи данных о погоде для города {city}: {e}")

    async def get_current_city(self) -> str | None:
        client = await self._get_client()
        current_city = await client.get('current_city')
        if current_city:
            return current_city
        
        return None

    async def set_current_city(self, city):
        try:
            client = await self._get_client()
            await client.set("current_city", city)
        except Exception as e:
            logger.error(f"Ошибка при установке текущего города: {e}")
    
    async def close(self):
        client = await self._get_client()
        if client is not None:
            logger.warning("Redis-кэш закрывается...")
            await self._client.close()
            self._client = None