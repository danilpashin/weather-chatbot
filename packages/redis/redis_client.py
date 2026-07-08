import os
from packages.core.env import init_env
from redis.asyncio.sentinel import Sentinel as AsyncSentinel
from redis.sentinel import Sentinel as SyncSentinel


init_env()


class AsyncRedisConnManager:
    def __init__(self, db=0, decode_responses=True):
        self.sentinels_env = os.getenv(
            "REDIS_SENTINELS",
            "redis-sentinel-1:26379,redis-sentinel-2:26380,redis-sentinel-3:26381",
        )
        self.master_name = os.getenv("REDIS_MASTER_NAME", "mymaster")
        self.password = os.getenv("REDIS_PASSWORD", None)
        self.db = db

        self.sentinel_hosts = []
        for s in self.sentinels_env.split(","):
            host, port = s.split(":")
            self.sentinel_hosts.append((host, int(port)))

        self.sentinel_manager = AsyncSentinel(self.sentinel_hosts, socket_timeout=0.1)
        self.master_client = self.sentinel_manager.master_for(
            self.master_name, decode_responses=decode_responses
        )

    def get_master(self):
        return self.master_client


class RedisConnManager:
    def __init__(self, db=0, decode_responses=True):
        self.sentinels_env = os.getenv(
            "REDIS_SENTINELS",
            "redis-sentinel-1:26379,redis-sentinel-2:26380,redis-sentinel-3:26381",
        )
        self.master_name = os.getenv("REDIS_MASTER_NAME", "mymaster")
        self.password = os.getenv("REDIS_PASSWORD", None)
        self.db = db

        self.sentinel_hosts = []
        for s in self.sentinels_env.split(","):
            host, port = s.split(":")
            self.sentinel_hosts.append((host, int(port)))

        self.sentinel_manager = SyncSentinel(self.sentinel_hosts, socket_timeout=0.1)
        self.master_client = self.sentinel_manager.master_for(
            self.master_name, decode_responses=decode_responses
        )

    def get_master(self):
        return self.master_client
