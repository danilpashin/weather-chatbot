from abc import ABC, abstractmethod
from typing import Any

class WeatherStorage(ABC):
    @abstractmethod
    async def get_weather(self, city: str) -> dict[str, Any] | None:
        pass

    async def close(self) -> None:
        pass