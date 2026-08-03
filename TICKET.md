# Ticket: support inventorypartnerdomain (IPD)

app-ads.txt files may carry an `inventorypartnerdomain=` declaration, which
tells buyers that inventory on this app may be sourced from another party's
supply chain. We currently drop those lines on the floor, so a demand partner
checking for a partner domain sees nothing and will not bid.

Two forms appear in the wild:

    inventorypartnerdomain=partner.com

and as a trailing field on a seller line:

    example.com, 1234, DIRECT, abc123, inventorypartnerdomain=partner.com

Both should be recognised. A standalone declaration applies to the file, not
to a single record.

Out of scope: validating that the partner domain resolves, and anything to do
with sellers.json.
