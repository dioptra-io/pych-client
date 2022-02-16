from argparse import ArgumentParser

from pych_client.client import (
    DEFAULT_BASE_URL,
    DEFAULT_DATABASE,
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    ClickHouseClient,
    ClickHouseException,
)


def main():
    parser = ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--database", default=DEFAULT_DATABASE)
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    args = parser.parse_args()
    with ClickHouseClient(
        base_url=args.base_url,
        database=args.database,
        username=args.username,
        password=args.password,
    ) as client:
        hostname = client.text("SELECT hostname()")
        while True:
            try:
                inp = input(f"{hostname} :) ").strip()
                if inp:
                    out = client.text(inp, settings={"default_format": "PrettyCompact"})
                    print(out)
            except ClickHouseException as e:
                print(f"\033[91m{e}\033[0m")
            except (EOFError, KeyboardInterrupt):
                break
