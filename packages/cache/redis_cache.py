import json
from typing import Any

from packages.cache.base import Cache
from packages.core.env import init_env
from packages.logging import logger
from packages.redis.redis_client import AsyncRedisConnManager

init_env()


class RedisCache(Cache):
    def __init__(self):
        self._client = None
        self._decode_responses = True
        self.client = AsyncRedisConnManager().get_master()

    async def set(self, key, value, ex: int | None = None):
        try:
            client = self.client
            if ex:
                await client.set(key, value, ex=ex)
            else:
                await client.set(key, value)
        except Exception as e:
            logger.error(f"Ошибка при записи данных: {e}")

    async def hset_user(self, user_id: int, **kwargs):
        try:
            client = self.client
            await client.hset(f"user:{user_id}", mapping=kwargs)
            await client.hexpire(f"user:{user_id}", 300)
        except Exception as e:
            logger.error(f"Ошибка при записи данных: {e}")

    async def hget_user(self, user_id: int, field: str):
        try:
            client = self.client
            await client.hget(f"user:{user_id}", field)
        except Exception as e:
            logger.error(f"Ошибка при получении данных: {e}")

    async def get(self, key) -> Any | None:
        try:
            client = self.client
            data = await client.get(key)
            if data is None or data == "":
                logger.debug(f"Ключ '{key}' не найден или пуст!")
                return None

            return data
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга в JSON при ключе '{key}': {e}")
            return None
        except Exception as e:
            logger.error(f"Ошибка при получении данных по ключу '{key}': {e}")
            return None

    async def close(self):
        client = self.client
        if client is not None:
            logger.warning("Redis-кэш закрывается...")
            await self.client.close()
            self.client = None
