# Quilt As A Spreadsheet Plugin

**Every cell is addressable. A1 is a cell. B2 is a cell. The substrate IS a spreadsheet.**

A Quilt cell has state, witness, hooks, drops. A spreadsheet cell has a value, a format, a formula.

The bridge: **every Quilt cell is addressable as a spreadsheet cell**.

```
Cell A1 = "first witness entry"     [value: string]
Cell A2 = witness_count             [value: int]
Cell B1 = "next witness text"       [formula: =A1]
Cell B2 = jev_confidence            [value: float]
```

The spreadsheet plugin:
- Reads Quilt cell state on every change
- Writes to the corresponding spreadsheet cell
- When the spreadsheet is edited, writes back to Quilt

The user sees a familiar spreadsheet. The substrate sees cells with hooks and drops. The bridge is invisible.

Why this matters:
1. **Spreadsheets are universal** — every business uses them
2. **Quilt's power becomes available to spreadsheet users** — no new UI to learn
3. **Spreadsheets become programmable** — Quilt's cell algebra replaces Excel formulas
4. **Existing workflows integrate** — copy/paste from Quilt spreadsheet to Excel

The substrate IS a spreadsheet. The spreadsheet IS the substrate. The plugin is the bridge.

A user who knows Excel can now use Quilt. A user who knows Quilt can now use Excel. The bridge is the same.

