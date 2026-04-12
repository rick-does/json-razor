import argparse
import os
import sys

from .core import collapse
from .formats import dump, dump_ndjson, load, load_ndjson


def detect_format(path):
    if path is None:
        return "json"
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        return "json"
    if ext in (".yaml", ".yml"):
        return "yaml"
    if ext == ".ndjson":
        return "ndjson"
    return "json"


def main():
    parser = argparse.ArgumentParser(
        prog="json-razor",
        description="Cut the fat. Collapse repeated structures in JSON, YAML, and NDJSON.",
    )
    parser.add_argument("input", nargs="?", help="Input file (default: stdin)")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument(
        "--keep",
        type=int,
        default=1,
        metavar="N",
        help="Examples to keep per repeated structure (default: 1)",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=None,
        metavar="N",
        help="Stop collapsing below this nesting depth",
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml", "ndjson"],
        help="Input format (default: auto-detect from extension)",
    )
    parser.add_argument(
        "--truncate",
        type=int,
        default=100,
        metavar="N",
        help="Max string length before truncating (default: 100)",
    )
    args = parser.parse_args()

    if args.input is None and sys.stdin.isatty():
        parser.print_help()
        sys.exit(0)

    fmt = args.format or detect_format(args.input)

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if fmt == "ndjson":
        records = load_ndjson(text)
        collapsed = collapse(records, keep=args.keep, depth=args.depth, truncate=args.truncate)
        result = dump_ndjson(collapsed)
    else:
        data = load(text, fmt)
        collapsed = collapse(data, keep=args.keep, depth=args.depth, truncate=args.truncate)
        result = dump(collapsed, fmt)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
            if not result.endswith("\n"):
                f.write("\n")
    else:
        print(result)


if __name__ == "__main__":
    main()
