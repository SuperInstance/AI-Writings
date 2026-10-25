# 000 — The Plugin Is the Portal

The genre of spreadsheet plugins: the kernel projected into every grid
program on earth.

**Seed thesis.** Spreadsheets are the most-installed programming environment
in history — Excel, Google Sheets, LibreOffice, Zoho, Airtable, Notion
tables. A plugin formula is a portal: `=JEV.CHOICE(state, options)` evaluates
in the jev-quilt kernel and returns a typed decision into a cell that any
program can then treat as data. The spreadsheet is not the substrate; it is
one of the substrate's faces. Backend logic runs in a model-sense —
percentages are decision distributions, not unexplained numbers.

**What a plugin must never do.** It must never train, never fetch at
runtime without a cached fallback, and never leave a cell holding a value
whose type the cell didn't declare. The plugin renders; the kernel decides;
the bookkeeper remembers. (The fleet's deckboss proved formula-native fleet
ops in May — this is that, productized for any program.)

**Open threads:**
- Formula surface design: `JEV.CHOICE`, `JEV.SCORE`, `JEV.NOUL`,
  `JEV.COMMENSURATE(a, b)` — what else deserves first-class syntax?
- Recalculation semantics: hooks eat deltas — but spreadsheet engines recalc
  whole sheets. Bridging deadband-silence into recalc-on-change is the
  integration crux.
- Offline honesty: a decision made offline must be labeled with its
  backend's receipt, or the percentage wears a costume.
