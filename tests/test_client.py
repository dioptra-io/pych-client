import pytest

from pych_client.exceptions import ClickHouseException


def test_execute_bytes(client):
    assert client.bytes("SELECT arrayJoin([1, 2, 3])") == b"1\n2\n3\n"


def test_execute_bytes_iter(client):
    expected = [b"1\n2\n3\n", b""]
    actual = list(client.iter_bytes("SELECT arrayJoin([1, 2, 3])"))
    assert actual == expected


def test_execute_text(client):
    assert client.text("SELECT arrayJoin([1, 2, 3])") == "1\n2\n3"


def test_execute_text_iter(client):
    expected = ["1\n", "2\n", "3\n"]
    actual = list(client.iter_text("SELECT arrayJoin([1, 2, 3])"))
    assert actual == expected


def test_execute_json(client):
    expected = [{"x": 1}, {"x": 2}, {"x": 3}]
    actual = client.json("SELECT arrayJoin([1, 2, 3]) AS x")
    assert actual == expected


def test_execute_json_iter(client):
    expected = [{"x": 1}, {"x": 2}, {"x": 3}]
    actual = list(client.iter_json("SELECT arrayJoin([1, 2, 3]) AS x"))
    assert actual == expected


def test_execute_json_int64(client):
    assert client.json("SELECT toInt64(1) AS x") == [{"x": 1}]


def test_execute_json_params(client):
    assert client.json("SELECT {val:Int64} AS x", {"val": 42}) == [{"x": 42}]


def test_execute_json_exception(client):
    with pytest.raises(ClickHouseException) as exc_info:
        client.json("SELECT * FROM invalid_table")
    assert exc_info.value.code == 60
