from telegram_bot.tasks.weather_tasks import check_and_send_notifications
from packages.redis.redis_client import RedisConnManager
from packages.logging import logger
from rq.cron import CronScheduler


master = RedisConnManager(decode_responses=False).get_master()

cron = CronScheduler(
    connection=master,
    logging_level="INFO",
)

cron.register(
    check_and_send_notifications,
    "notifications",
    cron="*/1 * * * *",
)

try:
    cron.start()
except KeyboardInterrupt:
    logger.info("Завершение cron планировщика...")
