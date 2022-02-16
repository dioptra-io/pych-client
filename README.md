# dioptra-pych

[![Coverage][coverage-badge]][coverage-url]
[![PyPI Status][pypi-workflow-badge]][pypi-workflow-url]
[![Tests Status][tests-workflow-badge]][tests-workflow-url]
[![PyPI][pypi-badge]][pypi-url]

## Installation

```bash
# Default Python JSON parser:
pip install dioptra-pych
# Faster orjson parser:
pip install dioptra-pych[orjson]
```

## Usage

```python
from pych import ClickHouseClient
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

[coverage-badge]: https://img.shields.io/codecov/c/github/dioptra-io/pych?logo=codecov&logoColor=white

[coverage-url]: https://codecov.io/gh/dioptra-io/pych

[pypi-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych/PyPI?logo=github&label=pypi

[pypi-workflow-url]: https://github.com/dioptra-io/pych/actions/workflows/pypi.yml

[tests-workflow-badge]: https://img.shields.io/github/workflow/status/dioptra-io/pych/Tests?logo=github&label=tests

[tests-workflow-url]: https://github.com/dioptra-io/pych/actions/workflows/tests.yml

[pypi-badge]: https://img.shields.io/pypi/v/dioptra-pych?logo=pypi&logoColor=white

[pypi-url]: https://pypi.org/project/dioptra-pych/
