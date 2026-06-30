import os

from packages.core.env import init_env

init_env()

HOST = os.getenv("API_HOST", "0.0.0.0")
PORT = int(os.getenv("API_PORT", 8080))