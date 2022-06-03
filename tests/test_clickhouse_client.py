from pych_client.clickhouse_client import get_clickhouse_client_args


def test_get_clickhouse_client_args(client):
    args = get_clickhouse_client_args(
        client.config,
        "SELECT {val:UInt64}",
        {"val": 1},
        {"default_format": "JSONEachRow"},
    )
    assert args == [
        "--query=SELECT {val:UInt64}",
        "--database=default",
        "--user=default",
        "--param_val=1",
        "--format=JSONEachRow",
    ]
