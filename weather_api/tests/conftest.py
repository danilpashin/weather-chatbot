import os
import pytest

os.environ["REDIS_URL"] = "memory://"

from httpx import ASGITransport, AsyncClient
from weather_api.main import factory

@pytest.fixture(scope="function")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def client():
    transport = ASGITransport(app=factory())
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
