import abc
from typing import Any


class Cache:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def get_weather(self, city: str) -> dict[str, Any] | None:
        pass

    @abc.abstractmethod
    async def set_weather(self, city: str, value):
        pass

    @abc.abstractmethod
    async def get_current_city(self) -> str | None:
        pass

    @abc.abstractmethod
    async def set_current_city(self, city):
        pass