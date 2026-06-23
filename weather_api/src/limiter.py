from slowapi import Limiter
from slowapi.util import get_remote_address
from packages.core.config import init_config
import os

init_config()

redis_url = os.getenv("REDIS_LIMITER_URL", "redis://localhost:6379/0")

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_url,
    default_limits=["10/minute"],
)