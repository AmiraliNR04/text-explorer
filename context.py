import time
from contextlib import contextmanager


@contextmanager
def timed_block(label):
    """Time any block of code. Logs even on error (try/finally)."""
    start = time.perf_counter()
    try:
        yield
    finally:
        duration = time.perf_counter() - start
        print(f"[timed] {label}: {duration:.3f}s")


class AnalysisSession:
    """Class-based context manager for analysis tracking.

    Demonstrates __enter__ / __exit__ explicitly.
    """

    def __init__(self, path, top_n=10):
        self.path = path
        self.top_n = top_n
        self.stats = None
        self.duration = 0.0
        self.success = False

    def __enter__(self):
        self._start = time.perf_counter()
        print(f"[session] starting: {self.path}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.duration = time.perf_counter() - self._start
        self.success = exc_type is None
        if not self.success:
            print(f"[session] failed: {exc_type.__name__}")
        else:
            print(f"[session] done in {self.duration:.3f}s")
        return False  # don't swallow exceptions