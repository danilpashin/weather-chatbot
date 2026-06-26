from slowapi import Limiter
from slowapi.util import get_remote_address
import os
from packages.core.env import init_env

init_env()

HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", 8080))

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL,
    default_limits=["10/minute"],
)