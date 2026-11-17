import pytest

from analyzer import Analyzer


def test_basic_counts():
    lines = ["hello world", "hello again", "error: failed"]
    stats = Analyzer(lines, top_n=3).analyze()

    assert stats.line_count == 3
    assert stats.word_count == 6
    assert stats.char_count == sum(len(l) for l in lines)


def test_top_words_order():
    lines = ["a b a c a", "b b"]
    stats = Analyzer(lines, top_n=2).analyze()

    assert stats.top_words[0] == ("a", 3)
    assert stats.top_words[1] == ("b", 3)


def test_empty_input():
    stats = Analyzer([], top_n=5).analyze()
    assert stats.line_count == 0
    assert stats.word_count == 0
    assert stats.char_count == 0
    assert stats.top_words == []


def test_top_n_respected():
    lines = ["a b c d e"]
    stats = Analyzer(lines, top_n=2).analyze()
    assert len(stats.top_words) == 2


def test_is_single_pass():
    """Analyzer must consume the iterable exactly once."""
    calls = {"count": 0}

    def counting_lines():
        for line in ["x y", "x z"]:
            calls["count"] += 1
            yield line

    Analyzer(counting_lines(), top_n=5).analyze()
    assert calls["count"] == 2  # exactly two lines, not four