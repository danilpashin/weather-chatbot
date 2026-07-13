import asyncio

from packages.logging import listener, logger
from worker.src.tasks.weather_tasks import weather_worker


async def main_worker():
    await weather_worker()


if __name__ == "__main__":
    try:
        asyncio.run(main_worker())
    finally:
        logger.warning("Воркер завершил работу!")
        listener.stop()
