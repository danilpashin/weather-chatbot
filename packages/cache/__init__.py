from packages.cache.redis_cache import RedisCache
from packages.core.env import init_env


init_env()

cache = RedisCache()
