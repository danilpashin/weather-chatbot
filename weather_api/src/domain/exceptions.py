class CityNotFoundError(Exception):
    def __init__(self, city: str):
        super().__init__(f"Город '{city}' не найден")
        self.city = city