from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class TextStats:
    line_count: int = 0
    word_count: int = 0
    char_count: int = 0
    top_words: list = field(default_factory=list)



class Analyzer:
    """Analyze text in a single pass, without loading it into memory."""

    def __init__(self, lines: Iterable[str], top_n: int = 10):
        self.lines = lines
        self.top_n = top_n
    
    def analyze(self) -> TextStats:
        line_count = 0
        word_count = 0
        char_count = 0
        word_counter = Counter()

        for line in self.lines:
            line_count += 1
            char_count += len(line)
            words = line.split()
            word_count += len(words)
            word_counter.update(words)

        return TextStats(
            line_count=line_count,
            word_count=word_count,
            char_count=char_count,
            top_words=word_counter.most_common(self.top_n),
        )