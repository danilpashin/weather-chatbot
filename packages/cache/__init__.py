from packages.cache.redis import RedisCache
from packages.core.env import init_env
import os

init_env()

cache = RedisCache()