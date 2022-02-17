import pytest

from pych_client import AsyncClickHouseClient, ClickHouseClient
from pych_client.constants import (
    DEFAULT_BASE_URL,
    DEFAULT_DATABASE,
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
)


@pytest.fixture
async def async_client():
    async with AsyncClickHouseClient(
        base_url=DEFAULT_BASE_URL,
        database=DEFAULT_DATABASE,
        username=DEFAULT_USERNAME,
        password=DEFAULT_PASSWORD,
    ) as client:
        yield client


@pytest.fixture
def client():
    with ClickHouseClient(
        base_url=DEFAULT_BASE_URL,
        database=DEFAULT_DATABASE,
        username=DEFAULT_USERNAME,
        password=DEFAULT_PASSWORD,
    ) as client:
        yield client
