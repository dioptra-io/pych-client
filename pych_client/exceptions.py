from httpx import Response

from pych_client.constants import CLICKHOUSE_EXCEPTION_CODE_HEADER


class ClickHouseException(Exception):
    def __init__(self, response: Response, query: str):
        self.code = int(response.headers[CLICKHOUSE_EXCEPTION_CODE_HEADER])
        self.error = response.text
        self.query = query
        msg = f"Query\n{self.query}\n\nError\n{self.error}"
        super().__init__(msg)
