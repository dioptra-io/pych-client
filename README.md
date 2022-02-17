# pych-client

[![Coverage][coverage-badge]][coverage-url]
[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]
[![Tests Status][tests-workflow-badge]][tests-workflow-url]
[![PyPI][pypi-badge]][pypi-url]

pych-client is a [ClickHouse][clickhouse] client for Python. It targets the HTTP interface and offers the following
features:
- Sync (`ClickHouseClient`) and async (`AsyncClickHouseClient`) clients.
- Streaming requests and responses.
- Optionally load credentials from the environment variables, or from a configuration file.

## Installation

```bash
# Default Python JSON parser:
pip install pych-client
# Faster orjson parser:
pip install pych-client[orjson]
```

## Usage

```python
from pych_client import ClickHouseClient

params = {"table": "test_pych"}
with ClickHouseClient() as client:
    client.text('''
        CREATE TABLE {table:Identifier} (a Int64, b Int64)
        ENGINE MergeTree() ORDER BY (a, b)
    ''', params)
    client.text("INSERT INTO {table:Identifier} VALUES", params, "(1, 2), (3, 4)")
    client.text("INSERT INTO {table:Identifier} VALUES", params, [b"(5, 6)", b"(7, 8)"])
    client.json("SELECT * FROM {table:Identifier} ORDER BY a", params)
# [{'a': '1', 'b': '2'}, {'a': '3', 'b': '4'}, {'a': '5', 'b': '6'}, {'a': '7', 'b': '8'}]
```

### Command-line interface

```bash
pipx install pych-client
pych-client --help
```

### Credential provider chain

The client looks for credentials in a way similar to the [AWS SDK][aws-sdk]:

1. If one of `base_url`, `database`, `username` or `password` is specified, these values will be used.
2. If none of the previous values are specified, and one of `PYCH_BASE_URL`, `PYCH_DATABASE`, `PYCH_USERNAME`
   or `PYCH_PASSWORD` environment variables are present, these values will be used.
3. If none of the previous values are specified, and the file `~/.config/pych-client/credentials.json` exists, the
   fields `base_url`, `database` and `username` and `password` will be used.
4. If none of the previous values are specified, the values `http://localhost:8213`, `default` and `default`
   will be used.

[aws-sdk]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html

[clickhouse]: https://clickhouse.com

[coverage-badge]: https://img.shields.io/codecov/c/github/dioptra-io/pych-client?logo=codecov&logoColor=white

[coverage-url]: https://codecov.io/gh/dioptra-io/pych-client

[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/PyPI?logo=github&label=pypi

[pypi-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/pypi.yml

[tests-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/Tests?logo=github&label=tests

[tests-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/tests.yml

[pypi-badge]: https://img.shields.io/pypi/v/pych-client?logo=pypi&logoColor=white

[pypi-url]: https://pypi.org/project/pych-client/
