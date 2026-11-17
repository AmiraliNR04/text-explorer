import pytest

from context import timed_block, AnalysisSession


def test_timed_block_runs(capsys):
    with timed_block("test"):
        pass
    captured = capsys.readouterr()
    assert "[timed] test" in captured.err   


def test_timed_block_logs_on_error(capsys):
    with pytest.raises(ValueError):
        with timed_block("crash"):
            raise ValueError("boom")
    captured = capsys.readouterr()
    assert "[timed] crash" in captured.err   

def test_session_success(capsys):
    with AnalysisSession("fake.txt") as session:
        session.stats = "ok"
    assert session.success is True
    assert session.stats == "ok"


def test_session_failure(capsys):
    with pytest.raises(ValueError):
        with AnalysisSession("fake.txt"):
            raise ValueError("boom")
    captured = capsys.readouterr()
    assert "[session] failed: ValueError" in captured.out