import pytest

from pych_client import ClickHouseClient


@pytest.fixture
def client():
    with ClickHouseClient() as client:
        yield client
