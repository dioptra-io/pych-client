# pych-client

[![Coverage][coverage-badge]][coverage-url]
[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]
[![Tests Status][tests-workflow-badge]][tests-workflow-url]
[![PyPI][pypi-badge]][pypi-url]

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

## Command-line interface

```bash
pipx install pych-client
pych-client --help
```

[coverage-badge]: https://img.shields.io/codecov/c/github/dioptra-io/pych-client?logo=codecov&logoColor=white

[coverage-url]: https://codecov.io/gh/dioptra-io/pych-client

[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/PyPI?logo=github&label=pypi

[pypi-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/pypi.yml

[tests-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych-client/Tests?logo=github&label=tests

[tests-workflow-url]: https://github.com/dioptra-io/pych-client/actions/workflows/tests.yml

[pypi-badge]: https://img.shields.io/pypi/v/pych-client?logo=pypi&logoColor=white

[pypi-url]: https://pypi.org/project/pych-client/
