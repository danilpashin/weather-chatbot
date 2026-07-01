import abc

class Database:
    def __init__(self):
        pass

    @abc.abstractmethod
    async def get_user_data(self, user_id: int) -> dict | None:
        pass

    @abc.abstractmethod
    async def set_user_data(self, user_id: int, data: dict) -> None:
        pass