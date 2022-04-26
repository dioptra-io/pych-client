import sys
from contextlib import contextmanager
from io import StringIO

from pych_client.cli import main


@contextmanager
def replace_stdin(text):
    # https://stackoverflow.com/a/36491341
    prev = sys.stdin
    sys.stdin = StringIO(text)
    yield
    sys.stdin = prev


def test_main(capsys):
    with replace_stdin("SELECT [1, 2, 3] FORMAT CSV"):
        main([])
    out, err = capsys.readouterr()
    assert '"[1,2,3]"' in out
    assert not err


def test_main_exception(capsys):
    with replace_stdin("SELECT * FROM invalid_table"):
        main([])
    out, err = capsys.readouterr()
    assert "DB::Exception" in out
    assert not err
