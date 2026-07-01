from abc import ABC, abstractmethod
from typing import Any

class WeatherCache(ABC):
    @abstractmethod
    async def get_weather(self, city: str) -> dict[str, Any] | None:
        pass

    async def close(self) -> None:
        pass


class UserRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def get_user(self, user_id: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def set_user(self, user_id: str, city: str) -> None:
        pass

    async def close(self) -> None:
        pass