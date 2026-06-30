import json
from typing import Any
from packages.redis.redis_client import RedisConnManager
from packages.cache.base import Cache
from packages.logging import logger
from packages.core.env import init_env

init_env()

class RedisCache(Cache):
    def __init__(self):
        self._client = None
        self._decode_responses = True
        self.client = RedisConnManager().get_master()

    async def set(self, key: str, value: str | bytes, ex: int | None = None):
        client = self.client
        if ex:
            await client.set(key, value, ex=ex)
        else:
            await client.set(key, value)

    async def get(self, key: str) -> str | None:
        client = self.client
        return await client.get(key)

    async def get_weather(self, city: str) -> dict[str, Any] | None:
        try:
            client = self.client
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
            client = self.client
            await client.set(city, value)
        except Exception as e:
            logger.error(f"Ошибка при записи данных о погоде для города {city}: {e}")

    async def get_current_city(self) -> str | None:
        client = self.client
        current_city = await client.get('current_city')
        if current_city:
            return current_city
        
        return None

    async def set_current_city(self, city):
        try:
            client = self.client
            await client.set("current_city", city)
        except Exception as e:
            logger.error(f"Ошибка при установке текущего города: {e}")
    
    async def close(self):
        client = self.client
        if client is not None:
            logger.warning("Redis-кэш закрывается...")
            await self.client.close()
            self.client = None