import pytest

from reader import FileReader


@pytest.fixture
def sample_file(tmp_path):
    """Create a temp file with known content."""
    p = tmp_path / "sample.txt"
    p.write_text("hello world\nhello again\nerror: failed\n", encoding="utf-8")
    return p


def test_reads_all_lines(sample_file):
    reader = FileReader(str(sample_file))
    lines = list(reader)
    assert lines == ["hello world", "hello again", "error: failed"]


def test_strips_newlines(sample_file):
    reader = FileReader(str(sample_file))
    for line in reader:
        assert not line.endswith("\n")


def test_multiple_passes(sample_file):
    """FileReader must be re-iterable — each pass opens fresh."""
    reader = FileReader(str(sample_file))
    first = list(reader)
    second = list(reader)
    assert first == second


def test_is_lazy(sample_file):
    """Nothing should be read until we ask for the first line."""
    reader = FileReader(str(sample_file))
    it = iter(reader)
    assert next(it) == "hello world"


def test_missing_file_raises():
    reader = FileReader("does_not_exist.txt")
    with pytest.raises(FileNotFoundError):
        list(reader)