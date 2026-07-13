from rq import Queue, Worker

from packages.logging import logger
from packages.redis.redis_client import RedisConnManager

master = RedisConnManager(decode_responses=False).get_master()

queue = Queue("notifications", master)

if __name__ == "__main__":
    logger.info("RQ Воркер запущен!")
    w = Worker([queue], connection=master)
    w.work()
