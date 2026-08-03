"""Parse app-ads.txt lines into structured records."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    domain: str
    publisher_id: str
    relationship: str
    cert_id: str | None = None
    inventory_partner_domain: str | None = None


@dataclass(frozen=True)
class InventoryPartnerDomain:
    domain: str


def parse_line(line: str) -> Record | InventoryPartnerDomain | None:
    """Parse one app-ads.txt line. Returns None for blanks and comments."""
    line = line.split("#", 1)[0].strip()
    if not line:
        return None

    if "," not in line and "=" in line:
        key, _, value = line.partition("=")
        if key.strip().lower() == "inventorypartnerdomain":
            return InventoryPartnerDomain(domain=value.strip().lower())
        return None

    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 3:
        return None

    domain, publisher_id, relationship = parts[0], parts[1], parts[2].upper()
    if relationship not in ("DIRECT", "RESELLER"):
        return None

    cert_id = None
    inventory_partner_domain = None
    for part in parts[3:]:
        ext_key, sep, ext_value = part.partition("=")
        if sep and ext_key.strip().lower() == "inventorypartnerdomain":
            if inventory_partner_domain is None:
                inventory_partner_domain = ext_value.strip().lower()
        elif cert_id is None and part:
            cert_id = part

    return Record(
        domain=domain.lower(),
        publisher_id=publisher_id,
        relationship=relationship,
        cert_id=cert_id,
        inventory_partner_domain=inventory_partner_domain,
    )
