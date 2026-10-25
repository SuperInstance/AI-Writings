# system2-backtest (B7) — price alternative routes without ever pricing a different answer

## 1. In one breath
Given two recorded routes that claim to reach the same result, this tool first proves the results are identical, and only then says which route is faster, which is cheaper, and when you'd pick each.

## 2. Why it exists
Before this, "route B is cheaper" was a claim, and a cheaper route that quietly returns a *different* answer looks great on a spreadsheet. System-2 (`situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §11) proposes many alternative cell-networks; something must judge them against history at zero live cost, and it must refuse to compare budgets unless the product is certified identical.

## 3. The mental model
- **Route run** — one slice of an ActiveLog: `cell.tick`/`route.hop` records (each with a budget vector) closed by one `ledger.transaction` (product + declared total).
- **Gate (good)** — product identity. Runs first. Different product → `refused`, and no budgets appear in the verdict.
- **fast** = `wall_ms`. **cheap** = two separate measurements: *compute* (usd, tokens) and *storage* (`train+prod` bytes). A route can win one cheapness and lose the other; the verdict says `split`.
- **Verdict** — per axis winner, plus a class: `dominates-faster-cheaper` (wins both, loses none — the other route merely *satisfices*), `dominates-better-faster` / `-better-cheaper` (needs an oracle `quality` score), `dominates-one-axis`, `trade-off` ("preferred when fast: A; when cheap: B"), or `equivalent`.
- **Corpus** — many cases per quilt. A route that *can't* handle a case is `inapplicable` (a coverage fact, not a comparison); totals sum only certified cases.

## 4. Walkthrough
```
$ cd labs/system2-backtest && python3 backtest.py
== calculator  (simple vs full): certified 5, refused 0, inapplicable 1
   simple      wall_ms=25   usd=0.0   tokens=0   storage_bytes=6400
   full        wall_ms=80   usd=0.0   tokens=0   storage_bytes=102400
   verdict: dominates-faster-cheaper ...   preferred-when: fast=simple, cheap=simple, good=tie
```
Real iron-triangle placements on the example quilts (cheap route vs full route, certified cases only):

| quilt | cheap route | certified / inapplicable | wall_ms cheap vs full | storage bytes cheap vs full | placement |
|---|---|---|---|---|---|
| calculator | simple | 5 / 1 (compound) | 25 vs 80 | 6,400 vs 102,400 | faster-cheaper |
| convert | identity | 3 / 5 (src≠dst) | 9 vs 39 | 1,200 vs 46,080 | faster-cheaper |
| datetime | utc | 5 / 3 (tz/DST) | 25 vs 95 | 3,440 vs 179,200 | faster-cheaper |
| text-normalize | ascii | 7 / 2 (non-ASCII) | 35 vs 91 | 4,816 vs 250,880 | faster-cheaper |
| image-thumb | passthrough | 3 / 2 (needs resample) | 15 vs 72 | 1,584 vs 122,880 | faster-cheaper |

usd and tokens are 0 on both routes in every quilt (local compute), so the compute cheapness ties and the whole "cheap" win is storage. Read this as: the cheap route dominates *where it applies*; the full route is the durable satisfice that covers the inapplicable cases (§11.1).

## 5. The contract
- `replay_route(records)` — verifies the chain, re-sums every tick/hop budget, and requires it to equal the declared `total_budget`; else `Refusal`.
- `backtest_pair(a, b, quality=None)` → `certified` verdict or `refused` verdict. Pure: same records in, same verdict (and `verdict_hash`, fnv1a-64) out.
- `backtest_corpus(cases, labels)` → per-case statuses + workload verdict over certified totals.
- Receipt: `python3 selftest.py` → `system2-backtest selftest: 38 checks, 0 failures` (offline; covers the refusal gate, dominance detection, split cheapness, tamper refusal, determinism).

## 6. Failure modes / scars
- **Products differ** → refused by design; fix the route, don't loosen the gate.
- **Product is what the transaction records.** Identity is only as strong as the `ledger.transaction` fields (e.g. image-thumb records the thumbnail *size*, not pixels). A coarse product field means a coarse gate.
- **Stationarity (§11.2).** Every verdict carries the as-of window (record/mono range) and a caveat; re-backtest after repricing or a hardware change. There's no time-weighting yet.
- **Forced routes** in the fixtures use each quilt's own `force`/`choose` hook; the calculator has none, so the fixture temporarily patches `choose`.
- `good` is a tie whenever products match; better-* classes only appear if you pass an oracle `quality` score.

## 7. How it composes
Reads `labs/activeledger` records (B1), so any quilt on the shared ledger is backtestable. Feeds B4 (route-preference: `preferred_when` is its input alongside OrgBook standing) and B8 (`system2-redesigner` proposals get scored here). Shares the `route_total` audit idea with OrgBook's replay≡live pin.

## 8. Where to look next
- `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §11 (System-2, iron-triangle) and §14 (OrgBook × budget join).
- `labs/activeledger/activeledger.py` — the budget vector and chain.
- `labs/examples/*/` — the route pairs used as fixtures; `situations/blueprints/README.md` — this doc's standard.
