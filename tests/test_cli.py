import json
import subprocess
import sys


def run_cli(*args):
    """Run cli.py as a subprocess, return (stdout, stderr, returncode)."""
    result = subprocess.run(
        [sys.executable, "cli.py", *args],
        capture_output=True,
        text=True,
    )
    return result.stdout, result.stderr, result.returncode


def test_cli_basic(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello world\nhello again\n")
    stdout, stderr, code = run_cli(str(f), "--no-timing")
    assert code == 0
    assert "lines:  2" in stdout
    assert "hello" in stdout


def test_cli_json(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("a b a\n")
    stdout, stderr, code = run_cli(str(f), "--format", "json", "--no-timing")
    assert code == 0
    data = json.loads(stdout)
    assert data["line_count"] == 1
    assert data["top_words"][0] == {"word": "a", "count": 2}


def test_cli_missing_file():
    stdout, stderr, code = run_cli("does_not_exist.txt")
    assert code == 1
    assert "file not found" in stderr
    assert stdout == ""