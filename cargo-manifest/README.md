# Cargo-Manifest

The hold's inventory: 6 files counting what the fleet carries — the full inventory in two formats, the scanner that built it, and the summary script. One entry is a file whose name ends in a newline; the shipwright's typo, preserved for posterity.

## What's inside
- [fleet-inventory.md](fleet-inventory.md) — the inventory, human-readable
- [fleet-inventory.json](fleet-inventory.json) — the inventory, machine-readable
- [scan.js](scan.js) — the scanner that walked the whole fleet and counted it
- [summary.js](summary.js) — the script that turned the count into a summary
- 1 accidental entry: a second "scan.js" whose name contains a trailing newline

## Start here
- [fleet-inventory.md](fleet-inventory.md) — everything the fleet knows it carries, in one list
- [scan.js](scan.js) — how the count was made
