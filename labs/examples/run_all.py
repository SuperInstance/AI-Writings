#!/usr/bin/env python3
"""run_all — the example-collection interop harness.

The example quilts are meant to be testable *between one another*, not in isolation:
each reaches product-identical results through different routes, books its run to the
SAME shared ledger (labs/activeledger), and picks the cheap route when it can. This
harness runs every example's offline selftest and reports which examples sit on the
one shared ledger — so the collection reads as one body, not a pile of scripts.

    python3 run_all.py        # -> runs every example selftest + the shared-ledger report
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
examples = sorted(d for d in HERE.iterdir() if d.is_dir() and (d / "selftest.py").exists())

passed, failed, shared, standalone = [], [], [], []

print("== example-collection interop harness ==")
for d in examples:
    r = subprocess.run([sys.executable, "selftest.py"], cwd=d, capture_output=True, text=True)
    line = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    print(f"  {line}")
    (passed if r.returncode == 0 else failed).append(d.name)
    src = " ".join(p.read_text(errors="ignore") for p in d.glob("*.py"))
    (shared if "activeledger" in src else standalone).append(d.name)

print()
print(f"selftests: {len(passed)}/{len(examples)} green"
      + (f"  FAILED: {', '.join(failed)}" if failed else ""))
print(f"on the shared labs/activeledger: {len(shared)}/{len(examples)}"
      + (f"  (standalone stand-in: {', '.join(standalone)})" if standalone else "  (all one ledger)"))
if standalone:
    print("  note: a standalone example uses an inline ActiveLog stand-in; swapping it to import"
          " labs/activeledger folds it onto the one shared ledger (a clean follow-up).")

sys.exit(1 if failed else 0)
