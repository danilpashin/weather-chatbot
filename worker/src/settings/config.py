import os

from packages.core.env import init_env

init_env()

API_TOKEN = os.getenv("API_TOKEN")

DEFAULT_INTERVAL = int(os.getenv("INTERVAL_SECONDS", 60))
