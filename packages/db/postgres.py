import os
from typing import Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from packages.db.base import Database
from packages.core.env import init_env


init_env()

db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


class PostgresDB(Database):
    def __init__(self):
        self.engine = create_async_engine(
            url=db_url.replace("postgresql://", "postgresql+asyncpg://"),
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )

    async def connect(self):
        pass

    async def get_user_data(self, user_id: int) -> Any | None:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("SELECT city FROM users WHERE id = :id"), {"id": user_id}
            )
            if result.rowcount == 0:
                return None
            return result.fetchone()[0]

    async def set_user_data(self, user_id: int, city: str) -> None:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("SELECT city FROM users WHERE id = :id"), {"id": user_id}
            )
            data = result.fetchone()
            if data is None:
                await conn.execute(
                    text("INSERT INTO users (id, city) VALUES (:id, :city)"),
                    {"id": user_id, "city": city},
                )
            elif data[0] != city:
                await conn.execute(
                    text("UPDATE users SET city = :city WHERE id = :id"),
                    {"id": user_id, "city": city},
                )
            return None

    async def close(self):
        await self.engine.dispose()
