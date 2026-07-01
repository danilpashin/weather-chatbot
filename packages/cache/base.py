import abc
from typing import Any


class Cache:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def get(self, key) -> Any | None:
        pass

    @abc.abstractmethod
    async def set(self, key, value):
        pass