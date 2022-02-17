import pytest

from pych_client import AsyncClickHouseClient, ClickHouseClient


@pytest.fixture
async def async_client():
    async with AsyncClickHouseClient() as client:
        yield client


@pytest.fixture
def client():
    with ClickHouseClient() as client:
        yield client
