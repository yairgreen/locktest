"""Entry point. Reads app-ads.txt content on stdin, prints one record per line."""

import sys

from .parser import parse_line


def main() -> int:
    for raw in sys.stdin:
        record = parse_line(raw)
        if record:
            print(f"{record.domain}|{record.publisher_id}|{record.relationship}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
