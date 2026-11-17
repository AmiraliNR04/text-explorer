import argparse
import json
import sys
from contextlib import nullcontext

from reader import FileReader
from analyzer import Analyzer
from context import timed_block


def filtered_reader(path, keyword):
    """Yield only lines containing keyword. Still lazy."""
    for line in FileReader(path):
        if keyword in line:
            yield line


def run_analysis(args):
    """Build the pipeline and run it once."""
    if args.filter:
        lines = filtered_reader(args.path, args.filter)
    else:
        lines = FileReader(args.path)

    analyzer = Analyzer(lines, top_n=args.top)
    return analyzer.analyze()


def format_text(stats, args):
    out = []
    out.append(f"file:   {args.path}")
    out.append(f"lines:  {stats.line_count:,}")
    out.append(f"words:  {stats.word_count:,}")
    out.append(f"chars:  {stats.char_count:,}")
    out.append("")
    out.append(f"top {args.top} words:")
    for word, count in stats.top_words:
        out.append(f"  {count:>8}  {word}")
    return "\n".join(out)


def format_json(stats, args):
    data = {
        "path": args.path,
        "line_count": stats.line_count,
        "word_count": stats.word_count,
        "char_count": stats.char_count,
        "top_words": [{"word": w, "count": c} for w, c in stats.top_words],
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze text files in a single pass, lazily.",
    )
    parser.add_argument("path", help="path to the text file")
    parser.add_argument("--top", type=int, default=10,
                        help="show top N words (default: 10)")
    parser.add_argument("--filter", type=str, default=None,
                        help="only analyze lines containing this keyword")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="output format (default: text)")
    parser.add_argument("--no-timing", action="store_true",
                        help="disable timing output")
    args = parser.parse_args()

    timer = nullcontext() if args.no_timing else timed_block("total")

    try:
        with timer:
            stats = run_analysis(args)
    except FileNotFoundError:
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"error: permission denied: {args.path}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(format_json(stats, args))
    else:
        print(format_text(stats, args))
    return 0


if __name__ == "__main__":
    sys.exit(main())