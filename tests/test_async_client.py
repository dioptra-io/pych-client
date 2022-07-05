import pytest

from pych_client.exceptions import ClickHouseException


async def test_execute_bytes(async_client):
    assert await async_client.bytes("SELECT arrayJoin([1, 2, 3])") == b"1\n2\n3\n"


async def test_execute_bytes_iter(async_client):
    expected = [b"1\n2\n3\n", b""]
    actual = [x async for x in async_client.iter_bytes("SELECT arrayJoin([1, 2, 3])")]
    assert actual == expected


async def test_execute_text(async_client):
    assert await async_client.text("SELECT arrayJoin([1, 2, 3])") == "1\n2\n3"


async def test_execute_text_iter(async_client):
    expected = ["1\n", "2\n", "3\n"]
    actual = [x async for x in async_client.iter_text("SELECT arrayJoin([1, 2, 3])")]
    assert actual == expected


async def test_execute_json(async_client):
    expected = [{"x": 1}, {"x": 2}, {"x": 3}]
    actual = await async_client.json("SELECT arrayJoin([1, 2, 3]) AS x")
    assert actual == expected


async def test_execute_json_iter(async_client):
    expected = [{"x": 1}, {"x": 2}, {"x": 3}]
    actual = [
        x async for x in async_client.iter_json("SELECT arrayJoin([1, 2, 3]) AS x")
    ]
    assert actual == expected


async def test_execute_json_int64(async_client):
    assert await async_client.json("SELECT toInt64(1) AS x") == [{"x": 1}]


async def test_execute_json_params(async_client):
    assert await async_client.json("SELECT {val:Int64} AS x", {"val": 42}) == [
        {"x": 42}
    ]


async def test_execute_json_exception(async_client):
    with pytest.raises(ClickHouseException) as exc_info:
        await async_client.json("SELECT * FROM invalid_table")
    assert exc_info.value.code == 60
    assert "DB::Exception" in exc_info.value.error


async def test_execute_json_iter_exception(async_client):
    with pytest.raises(ClickHouseException) as exc_info:
        [x async for x in async_client.iter_json("SELECT * FROM invalid_table")]
    assert exc_info.value.code == 60
    assert "DB::Exception" in exc_info.value.error
