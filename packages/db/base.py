import abc


class Database:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def get_user_data(self, user_id: int) -> dict | None:
        pass

    @abc.abstractmethod
    async def set_user_data(self, user_id: int, city: str, tz: int) -> None:
        pass

    @abc.abstractmethod
    async def get_users_by_minute(self, utc_minutes: int) -> list[dict]:
        pass

    @abc.abstractmethod
    async def set_chat_id(self, chat_id: int, user_id: int) -> None:
        pass

    @abc.abstractmethod
    async def get_notification_status(self, user_id: int) -> bool:
        pass

    @abc.abstractmethod
    async def set_notification_status(self, user_id: int, status: bool) -> None:
        pass

    @abc.abstractmethod
    async def get_notification_time(self, user_id: int) -> str | None:
        pass

    @abc.abstractmethod
    async def set_notification_time(
        self, user_id: int, local_time: str, utc_minutes: int
    ) -> None:
        pass

    @abc.abstractmethod
    async def get_user_timezone(self, user_id: int) -> int | None:
        pass

    @abc.abstractmethod
    async def set_user_timezone(self, user_id: int, tz: int) -> None:
        pass
