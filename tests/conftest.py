import pytest

from pych import ClickHouseClient


@pytest.fixture
def client():
    with ClickHouseClient() as client:
        yield client
