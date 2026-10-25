# unit-translation-audit (B2)

## 1. In one breath
An auditor that replays every unit conversion recorded in a run and tells you, hop by hop, whether converting forward and then back returns exactly what you started with — or, if not, says precisely what was lost.

## 2. Why it exists
Before this, a `route.hop` was only checked by `activeledger`'s zero-sum smoke test (`|credit*rate − debit| ≤ 1e-6`). That test can't see a rounding that is small in absolute terms but real (17 cents dropped), and it says nothing about *why*. The design doc (`situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §8, §14) calls the zero-sum-after-translation check "B2" and asks it to mirror OrgBook's exactness (exact identity, replay = live). This is that.

## 3. The mental model
- **hop** — a recorded `route.hop`: `credit` (source units, amount) → `debit` (dest units, amount), with `price.rate` (dest = source × rate).
- **Effect(forward, inverse)** — built from the rate: `forward(x)=x·rate`, `inverse(y)=y/rate`. The inverse *is* the round-trip auditor (quilt-studio's `EFFECT` contract; that repo was not read — only the contract as described in §8).
- **round trip** — push the *recorded debit* back through the inverse and compare to the recorded credit. Residual = |back − credit|.
- **class** — `EXACT` (zero residual in rational arithmetic; floats are read as the decimal they print as, so `0.01` = 1/100) · `WITHIN_TOL` (residual ≤ `rel_tol`, default 1e-9, of the credit) · `LOSSY` (beyond tolerance; a `reason` says why: integer-quantized debit, k-decimal-place rounded debit, zero rate).
- **replay** — the audit is a pure function of the recorded hops (no clock, no randomness), so a run audits to the same `audit_digest` every time.

## 4. Walkthrough
```
$ cd labs/unit-translation-audit && python3 audit.py     # audits calculator-quilt + convert-quilt workloads
calc/0:add   EXACT  USD->USD-cents  12.34 USD -> 1234 USD-cents  rate=100.0
calc/0:add   EXACT  USD-cents->USD  1800.0 USD-cents -> 18 USD   rate=0.01
calc/3:pct   LOSSY  USD-cents->USD  617.0 USD-cents -> 6 USD     rate=0.01
    why: debit is an integer but credit*rate = 6.17 has a fractional part; sub-unit remainder 0.17 dropped (integer-quantized debit)
convert/5:10lb->kg  EXACT       lb->g  10.0 lb -> 4535.9237 g  rate=453.59237
convert/5:10lb->kg  WITHIN_TOL  g->kg  4535.9237 g -> 4.535924 kg  rate=0.0010000000661386785
SUMMARY {... 'n_hops': 25, 'counts': {'EXACT': 16, 'WITHIN_TOL': 4, 'LOSSY': 5}, 'audit_digest': '0xddf7f4f5c220409c'}
```
In code: `import audit; a = audit.audit_run(log)` (an `ActiveLog`, a records list, or JSONL text) → `{"hops": [...per-hop records...], "receipt": {...}}`.

**What it found on the example quilts (real results, 25 hops):**
- **calculator-quilt (12 hops):** all 6 USD→cents hops are EXACT. **5 of 6 cents→USD hops are LOSSY** — `calc_quilt._hop` books the debit as `int(round(...))`, so 9999¢→`100` USD (true 99.99), 2997¢→`30`, 617¢→`6`, 250¢→`2`, 115762¢→`1158`. Only 1800¢→18 USD is whole-dollar and EXACT. The *product* is not wrong (the result `cell.tick` carries the correct string, e.g. "6.17"); the bookkeeping hop is what is lossy. An honest booking would carry the debit as `6.17`.
- **convert-quilt (13 hops):** 0 lossy. 9 EXACT (all identity hops, plus cm→m, km→m, lb→g and the m→in / m→ft hops, which are self-consistent because the recorded rate is derived as debit/credit), 4 WITHIN_TOL (rates that are float ratios like `0.0010000000661386785`, residuals ~1e-16).
- 3 of the convert hops (C→K, K→F, K→C) also carry an **affine caveat** (see scars).

## 5. The contract
- **Input:** an ActiveLog run (object, records, or JSONL); only `route.hop` records are read, others ignored.
- **Output:** per-hop `{seq, route, credit, debit, rate, translation, cls, reason, residual_abs, residual_rel, balanced_1e-6, caveats}` + receipt `{audit_v, rel_tol, n_hops, counts, round_trips, input_digest, audit_digest}`. `input_digest` = fnv1a-64 canonical-JSON hash of the hop bodies; `audit_digest` of the audit records (`activeledger.content_hash`).
- **Invariants:** deterministic; `round_trips` is true iff zero LOSSY hops; EXACT ⇒ residual exactly 0.
- **Receipt:** `python3 selftest.py` → `unit-translation-audit selftest: 34 checks, 0 failures` (offline; asserts exactness on exact-rate hops, lossy classification + reason on deliberately lossy fixtures, JSONL-replay == live, tamper changes the digest, and the real example-quilt counts 16/4/5).

## 6. Failure modes / scars
- **Self-consistent ≠ correct.** The auditor checks a hop against *its own recorded price*. convert-quilt records `rate = debit/credit`, so a wrong table would still audit EXACT. Guarding the law itself needs an independent oracle; not built.
- **Affine units (C/F).** A single multiplicative rate can't be the real translation (0 °C ≠ 0 K). The hop round-trips for that one amount; we flag it in `caveats` rather than classify it.
- **The emit gate can't catch this.** `activeledger.ActiveLog.emit` rejects unbalanced hops at 1e-6, but the calculator's inline stand-in `ActiveLog` (not the shared one) never runs that gate — which is how lossy hops got booked. Swapping EX1 onto `labs/activeledger` would now *raise* on those hops.
- **Tolerance is relative to the credit.** A hop whose credit is 0 is judged against 1; fine for our fixtures, revisit for zero-heavy data.
- Floats are interpreted through their shortest decimal repr (`Fraction(Decimal(repr(x)))`); a rate meant as a true binary float would be judged as its decimal spelling.

## 7. How it composes
Reads the `route.hop` shape from `labs/activeledger/activeledger.py` (imports its `content_hash`, `hop_balanced`). Audits any quilt in `labs/examples/`. The receipt digests are the same fnv1a-64 idiom as OrgBook-style replay pins, so a run's `audit_digest` can be booked alongside its `route_total`. Natural next composers: `run_all.py` (add an audit column), B4 preference (penalize routes with LOSSY hops).

## 8. Where to look next
- `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §8 (route.hop schema) and §14 (OrgBook reconciliation).
- `labs/activeledger/README.md` — the ledger this audits; its NEXT list names this lab.
- `labs/examples/calculator-quilt/calc_quilt.py` `_hop` — the source of the 5 lossy hops, if you want to fix it.
