"""Entry point. Reads app-ads.txt content on stdin, prints one record per line."""

import sys

from adstxt.parser import InventoryPartnerDomain, Record, parse_line


def main() -> int:
    lines = []
    for raw in sys.stdin:
        result = parse_line(raw)
        if isinstance(result, InventoryPartnerDomain):
            lines.append(f"inventorypartnerdomain={result.domain}")
        elif isinstance(result, Record):
            line = f"{result.domain}|{result.publisher_id}|{result.relationship}"
            if result.inventory_partner_domain:
                line += f"|inventorypartnerdomain={result.inventory_partner_domain}"
            lines.append(line)
    if lines:
        print("\n".join(lines), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
