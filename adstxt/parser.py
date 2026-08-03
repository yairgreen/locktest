"""Parse app-ads.txt lines into structured records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    domain: str
    publisher_id: str
    relationship: str
    cert_id: str | None = None


def parse_line(line: str) -> Record | None:
    """Parse one app-ads.txt line. Returns None for blanks and comments."""
    line = line.split("#", 1)[0].strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 3:
        return None

    domain, publisher_id, relationship = parts[0], parts[1], parts[2].upper()
    if relationship not in ("DIRECT", "RESELLER"):
        return None

    return Record(
        domain=domain.lower(),
        publisher_id=publisher_id,
        relationship=relationship,
        cert_id=parts[3] if len(parts) > 3 and parts[3] else None,
    )
