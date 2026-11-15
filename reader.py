class FileReader:
    """Read a text file line by line, lazily."""

    def __init__(self, path: str):
        self.path = path

    def __iter__(self):
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.rstrip("\n")