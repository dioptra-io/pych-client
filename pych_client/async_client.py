import builtins
from types import TracebackType
from typing import Any, AsyncIterator, List, Optional, Type

import httpx
from httpx import Response

from pych_client.base import get_client_args, get_credentials, get_http_params
from pych_client.constants import (
    CLICKHOUSE_EXCEPTION_CODE_HEADER,
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_READ_WRITE_TIMEOUT,
)
from pych_client.exceptions import ClickHouseException
from pych_client.line_decoder import LineDecoder
from pych_client.typing import Data, Params, Settings

try:
    import orjson as json
except ModuleNotFoundError:
    import json  # type: ignore


class AsyncClickHouseClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        database: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        settings: Settings = None,
        connect_timeout: Optional[float] = DEFAULT_CONNECT_TIMEOUT,
        read_write_timeout: Optional[float] = DEFAULT_READ_WRITE_TIMEOUT,
    ):
        base_url, database, username, password = get_credentials(
            base_url, database, username, password
        )
        self.config = {
            "base_url": base_url,
            "database": database,
            "username": username,
            "password": password,
            "settings": settings,
            "connect_timeout": connect_timeout,
            "read_write_timeout": read_write_timeout,
        }
        self.client = httpx.AsyncClient(**get_client_args(**self.config))  # type: ignore

    async def __aenter__(self) -> "AsyncClickHouseClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self.client.aclose()

    async def execute(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> httpx.Response:
        r = await self.client.post(
            "/",
            content=data,
            params=get_http_params(query, params, settings),
        )
        await raise_for_status(r, query)
        return r

    async def stream(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> Any:
        return self.client.stream(
            "POST", "/", content=data, params=get_http_params(query, params, settings)
        )

    async def bytes(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> builtins.bytes:
        r = await self.execute(query, params, data, settings)
        return r.content

    async def iter_bytes(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> AsyncIterator[builtins.bytes]:
        stream = await self.stream(query, params, data, settings)
        async with stream as r:
            await raise_for_status(r, query)
            async for chunk in r.aiter_bytes():
                yield chunk

    async def text(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> str:
        r = await self.execute(query, params, data, settings)
        return r.text.strip()

    async def iter_text(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> AsyncIterator[str]:
        stream = await self.stream(query, params, data, settings)
        async with stream as r:
            await raise_for_status(r, query)
            # Faster implementation of httpx.Response.iter_text()
            # based on a custom version of LineDecoder.
            decoder = LineDecoder()
            async for text in r.aiter_text():
                for line in decoder.decode(text):
                    yield line
            for line in decoder.flush():
                yield line

    async def json(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> List[dict]:
        settings = settings or {}
        settings = {
            **settings,
            "default_format": "JSONEachRow",
            "output_format_json_quote_64bit_integers": 0,
        }
        result = await self.text(query, params, data, settings)
        return [json.loads(line) for line in result.split("\n") if line]

    async def iter_json(
        self,
        query: str,
        params: Params = None,
        data: Data = None,
        settings: Settings = None,
    ) -> AsyncIterator[dict]:
        settings = settings or {}
        settings = {
            **settings,
            "default_format": "JSONEachRow",
            "output_format_json_quote_64bit_integers": 0,
        }
        async for line in self.iter_text(query, params, data, settings):
            if line:
                yield json.loads(line)


async def raise_for_status(response: Response, query: str) -> None:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        code = int(response.headers[CLICKHOUSE_EXCEPTION_CODE_HEADER])
        error = (await response.aread()).decode()
        raise ClickHouseException(code, error, query) from e
