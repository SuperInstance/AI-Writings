# system2-redesigner (B8) — propose new routes, let the judge refuse the wrong ones, promote the winners

## 1. In one breath
A crew of cheap models proposes cheaper or faster ways to compute the same answer. B7 rejects any proposal that changes the answer, even once. B4 ranks the survivors on {good, fast, cheap} and writes the winners into the preference map. This closes the System-2 loop (propose → backtest → promote).

## 2. Why it exists
B7 (`system2-backtest`) can judge two routes, and B4 (`route-preference`) can rank routes it is given. But until now nothing *came up with* new routes. §11 of `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` says System-2 must (1) propose alternative networks, (2) backtest them with product identity certified first, and (3) promote the winners and keep the losers as documented dead-ends. B8 does step 1 and runs steps 2 and 3. The proposer is deliberately cheap and fallible. Ideas are cheap to generate and cost nothing to refuse, because the judge cannot be gamed.

## 3. The mental model
- **Quilt under redesign:** text-normalize (EX4). Reference = `' '.join(NFKC(s).casefold().split())`. Incumbent = "if ASCII: byte ops, else reference".
- **Route DSL:** `{"name", "guard", "steps":[op…], "fallback": "full" | <nested network>}`. That is a guarded fast path with a fallback, nestable 3 deep. The vocabulary has 12 ops (NFKC/NFC/NFKD, casefold/lower, ws_collapse, strip, three ASCII byte ops that *crash* on non-ASCII, const_empty, identity) and 5 guards (always, ascii, latin1, blank, clean_ascii). A proposal that doesn't parse is refused before it runs.
- **Execute:** every (proposal, input) pair becomes a real ActiveLog v1 run: `cell.tick` per guard and op, `route.hop` per edge, and one `ledger.transaction` with the same product shape as the quilt (`{"out"}`).
- **Gate (B7, imported unmodified):** `backtest_pair(quilt FULL run, proposal run)` is called on each of **286 cases**. These are the quilt WORKLOAD, every ASCII code point in context, 28 unicode traps (ß/ẞ, ﬁ, Ⅷ, fullwidth, İ, ǅ, final-σ, NBSP/U+3000/U+2028, combining marks, …), every priced input, and 120 seeded fuzz strings. *One* refused case or one crash refuses the proposal, and the first counterexample is kept.
- **Promote (B4, imported unmodified):** each priced case runs `prefer()` over {full, incumbent, survivors}, which re-runs the gate and feeds a hebbian `PreferenceBook`. Then `prefer_axes()` runs over the workload sums. A proposal on the **frontier** in ≥1 traffic regime is **promoted**. One that passed the gate but is dominated everywhere is kept as a **satisfice** route.
- **Regimes:** pricing happens on traffic, not on the adversarial gate corpus. There are two regimes: `quilt-workload` (the quilt's recorded WORKLOAD) and `clean-heavy` (a declared regime of mostly already-normalized ASCII). "Preferred when" depends on the regime.
- **One cost model.** Every network B4 ranks is priced by `OP_COST`/`GUARD_COST`, and that includes the incumbent and full baselines, which are re-expressed in the DSL. The quilt's real run is used only as the product *oracle*. These are modeled costs (the same convention as the example quilts), not wall-clock measurements. The gate counts and verdicts are measured.

## 4. Walkthrough
Offline (stub proposals, no network):
```
$ cd labs/system2-redesigner && python3 system2_redesigner.py
  quilt-equiv   PASSED dup-of incumbent   ascii ? map_fs_controls>bytes_lower>bytes_ws_collapse : full
  early-exit    PASSED                    clean_ascii ? identity : ascii ? …bytes… : full
  blank-exit    PASSED                    blank ? const_empty : full
  latin1-lower  REFUSED(b7)    counterexample 'Straße' -> expected 'strasse' got 'straße'
  no-nfkc       REFUSED(b7)    counterexample '…Ⅷ  ＡＢＣ' -> expected '… viii abc' got '… ⅷ ａｂｃ'
  bytes-always  REFUSED(execute)  ValueError: bytes op on non-ASCII input
  bad-op        REFUSED(parse) unknown op(s) ['teleport']
  -- regime clean-heavy:    early-exit wall_ms=40 vs incumbent 56, storage 15,928 vs 17,152 → dominates, PROMOTED
  -- regime quilt-workload: incumbent keeps the frontier (47 ms / 26,192 B); early-exit 53 / 26,616 → satisfice
```
Live (`python3 system2_redesigner.py --live [--bold] [--moth] --out runs/x.json`): each DeepInfra crew model gets the DSL, the cost table and the reference, and replies with 2–3 JSON proposals. Moth optionally rotates the gating order with an un-gameable draw, which matters because the hebbian book depends on order. The full reports, including raw crew replies, are in `runs/`.

LIVE_RESULTS

## 5. The contract
- `parse(obj)` → canonical network | raises `Invalid`. `shape_hash(p)` content-addresses the *shape*, so crew duplicates are gated once and credited to every proposer. Rediscovering a baseline counts as a duplicate, not a win.
- `execute(p, text, label)` → ActiveLog records. B7's `replay_route` must audit them, and the selftest checks that it does.
- `gate(p, corpus)` → `passed` | `refused` with `stage` (execute/b7), `input`, `expected`, `got`, B7's reason. A refusal never exposes a budget.
- `redesign(items)` → report with per-proposal rows, per-regime promotion (frontier, dominated, preferred_when, settled hebbian picks, book digest), `promoted`, `satisfice`, `tally`, and `report_hash` (fnv1a-64). The function is pure and deterministic offline: the same proposals give the same report.
- Receipt: `python3 selftest.py` → `system2-redesigner selftest: 68 checks, 0 failures` (offline). It proves the propose→B7→B4 loop, that product-changing proposals are refused (wrong casing, dropped NFKC, NFC-for-NFKC), that a crash is refused, that B4 still refuses a smuggled wrong route, and that the promotion is regime-dependent.

## 6. Failure modes / scars
- **Cost-model mismatch (caught and fixed).** The first version priced the incumbent with the quilt's own `COST` table and priced proposals with `OP_COST`. Under that setup a plain re-expression of the incumbent came out "30% cheaper" and was promoted. Now every ranked network uses one cost model, and the quilt run is only the product oracle.
- **The gate is only as strong as its corpus.** NFC-for-NFKC passes an ASCII-only corpus and is refused on the full one (this is a selftest check). A wrong proposal that agrees on all 286 cases would pass. The defenses are the trap list and fuzz, and making the corpus wider is the remedy. B7's own scar applies too: the product is only what the transaction records.
- **Modeled, not measured, budgets.** usd/tokens are 0 for every route (all local), so "cheap" here means storage and memory. A real wall-clock or priced deployment needs re-backtesting (§11.2 stationarity caveat, carried in every B4 result).
- **Crew failure is logged, not hidden.** Timeouts, 429s and empty replies appear per model in `crew.models`. An unparseable reply contributes 0 proposals. A parseable but invalid proposal is refused at `parse`.
- **Safe crews find little.** When given the reference formula, the crew mostly proposes provably safe guarded fast paths. The `--bold` round pushes for drops, reorders and substitutions so that the gate gets exercised.

## 7. How it composes
It consumes B7 (`labs/system2-backtest/backtest.py`) and B4 (`labs/route-preference/route_preference.py`) unmodified, and EX4 (`labs/examples/text-normalize-quilt`) as the product oracle. It writes ActiveLog runs via B1 (`labs/activeledger`), and the crew goes through `labs/convo-quilt/providers.py`. Its output `preference_map` is B4's `preferred_when` per regime, ready for a router to read. The refused rows are §11's "documented dead-ends".

## 8. Where to look next
- `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §11 (System-2 loop, iron-triangle) and the B8 backlog row.
- `labs/system2-backtest/README.md` (the judge) and `labs/route-preference/README.md` (the ranker).
- `runs/*.json` — live crew reports with raw replies and counterexamples. `NOTE-B8.md` — the DONE-candidate note.
