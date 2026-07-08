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

    async def set_user_data(self, user_id: int, city: str, tz: int) -> None:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("SELECT city FROM users WHERE id = :id"), {"id": user_id}
            )
            data = result.fetchone()
            if data is None:
                await conn.execute(
                    text(
                        "INSERT INTO users (id, city, timezone) VALUES (:id, :city, :timezone)"
                    ),
                    {"id": user_id, "city": city, "timezone": tz},
                )
            elif data[0] != city:
                await conn.execute(
                    text(
                        "UPDATE users SET city = :city, timezone = :timezone WHERE id = :id"
                    ),
                    {"id": user_id, "city": city, "timezone": tz},
                )
            return None

    async def get_users_by_minute(self, utc_minutes: int) -> list[dict]:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text(
                    "SELECT chat_id, city FROM users WHERE utc_minutes = :utc_minutes"
                ),
                {"utc_minutes": utc_minutes},
            )
            rows = result.fetchall()
            return [{"chat_id": row[0], "city": row[1]} for row in rows]

    async def set_chat_id(self, chat_id: int, user_id: int) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(
                text("UPDATE users SET chat_id = :chat_id WHERE id = :user_id"),
                {"chat_id": chat_id, "user_id": user_id},
            )
            return None

    async def get_notification_status(self, user_id: int) -> bool:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("SELECT notification_status FROM users WHERE id = :id"),
                {"id": user_id},
            )
            row = result.fetchone()
            return row[0] if row else False

    async def set_notification_status(self, user_id: int, status: bool) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(
                text("""
                    INSERT INTO users (id, notification_status)
                    VALUES (:id, :status)
                    ON CONFLICT (id) 
                    DO UPDATE SET notification_status = :status
                """),
                {"id": user_id, "status": status},
            )

    async def get_notification_time(self, user_id: int) -> str | None:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("SELECT local_time FROM users WHERE id = :id"), {"id": user_id}
            )
            row = result.fetchone()
            return row[0] if row and row[0] else None

    async def set_notification_time(
        self, user_id: int, time_str: str, utc_minutes: int
    ) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(
                text("""
                    INSERT INTO users (id, local_time, utc_minutes)
                    VALUES (:id, :local_time, :utc_minutes)
                    ON CONFLICT (id) 
                    DO UPDATE SET local_time = :local_time, utc_minutes=:utc_minutes
                """),
                {"id": user_id, "local_time": time_str, "utc_minutes": utc_minutes},
            )

    async def get_user_timezone(self, user_id: int) -> int | None:
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("SELECT timezone FROM users WHERE id = :id"), {"id": user_id}
            )
            row = result.fetchone()
            return row[0] if row and row[0] else None

    async def set_user_timezone(self, user_id: int, tz: int) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(
                text("""
                    INSERT INTO users (id, timezone)
                    VALUES (:id, :tz)
                    ON CONFLICT (id) 
                    DO UPDATE SET timezone = :tz
                """),
                {"id": user_id, "tz": tz},
            )

    async def close(self):
        await self.engine.dispose()
