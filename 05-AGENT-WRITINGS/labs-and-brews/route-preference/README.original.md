# route-preference (B4) — record which of several same-answer routes to pick, and when

## 1. In one breath
Given two or more routes that reach the identical result, this tool records which route to choose when you care most about quality, speed, or cost (or two of the three), instead of collapsing them into one "best" score.

## 2. Why it exists
`system2-backtest` (B7) prices a *pair* of routes. Once System-2 keeps several elite routes per product, something has to hold the resulting map ("use A for a live turn, B for a batch backfill") and keep it steady as more backtests arrive. `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §14 states B4 as the join: `preferred_when = f(OrgBook standing[good], ActiveLedger budget[fast, cheap])`. Standing says who is correct; the budget vector says at what cost; B4 lays them side by side.

## 3. The mental model
- **Route** — a recorded ActiveLog run (B7's `replay_route`), with a name.
- **Gate** — every route must replay and share one product with the others. Any mismatch → `refused`; no budgets appear in the output.
- **Axes** — `good` = optional per-route **standing** (a non-negative int, higher is better; if it is missing for any route, `good` is a tie). `fast` = `wall_ms`. `cheap` = the vector (usd, tokens, storage_bytes): route X beats Y on cheap only if it is no worse on all three and better on one; otherwise they are *incomparable* and both stay in the running.
- **Frontier** — routes that no other route beats on every axis. **Dominated** routes list who beats them.
- **`preferred_when`** — one route per priority (`good`, `fast`, `cheap`) and per pair (`better-faster`, `better-cheaper`, `faster-cheaper`). A pair is `null` when no single route is best on both axes; that is a real trade-off, not a missing value.
- **Hebbian weights** — a `PreferenceBook` reinforces the route picked for each priority on every confirmed result and decays the others (integers in `[0, 1_000_000]`; +¼ of the gap up, −⅒ down). Weights only break ties the data leaves open and never override a strict win. `settled()` returns the route most consistently confirmed, so one odd backtest does not flip a long-standing preference.

## 4. Walkthrough
Demo over the five example quilts (each is a real cheap-vs-full route pair, certified cases only, workload sums):
```
$ cd labs/route-preference && python3 route_preference.py
== calculator  (simple vs full): 5 certified case(s)
   frontier=['simple']  class=dominant  good_source=tie
   preferred_when: {'good': 'tie', 'fast': 'simple', 'cheap': 'simple', 'better-faster': 'simple', 'better-cheaper': 'simple', 'faster-cheaper': 'simple'}
   settled: {'fast': 'simple@762694', 'cheap': 'simple@762694'}
== convert  (cheap vs full): 3 certified case(s)
   ...
```
All five quilts come out the same way: the cheap route is the only frontier member, so it takes every priority. With `good` tied, `better-faster` and `better-cheaper` reduce to the fast and cheap winners; they are not evidence of higher quality. These fixtures contain no trade-off, so the interesting case is synthetic. Three routes reaching `{"answer": 42}`: A = 10 ms / 900 B storage, B = 50 ms / 100 B, C = 60 ms / 950 B; standing A=1, B=5, C=5 (built as in `selftest.py`):
```
class          "trade-off"
frontier       ["A", "B"]
dominated      {"C": ["B"]}
preferred_when {"good": "B", "fast": "A", "cheap": "B", "better-faster": null,
                "better-cheaper": "B", "faster-cheaper": null}
result_hash    "0x0ee4739f410163a3"
```
Read it as: pick A when latency rules, B when cost or correctness does; nobody is both better and faster, so `better-faster` is null. C is out because B matches its standing and beats it on speed and storage. Without the `standing` argument, `good` is `"tie"` and A's speed is no longer offset, so C would still be dominated but `better-faster` would name A.

## 5. The contract
- `prefer(routes, standing=None, weights=None)` — `routes = [(name, records)]`. Returns a `certified` or `refused` result. Refuses: fewer than 2 routes, duplicate names, a route that fails B7's replay (bad chain, budget mismatch), differing products, standing that is not a non-negative int, or standing for an unknown route.
- `prefer_axes(named_axes, ...)` — same join over axis vectors you have already certified (used for workload sums).
- `PreferenceBook.observe(result)` / `.settled()` / `.weights` / `.digest()`; `reinforce_weights(weights, result)` is the pure step. Refused results and null picks change nothing.
- Invariants: pure and deterministic; independent of route order; weights are ints in `[0, SCALE]`; a strict win is never overridden; no budget is exposed on refusal.
- Receipt: `result_hash` = fnv1a-64 over canonical JSON of the result body (B7's idiom), recomputable from the body. `python3 selftest.py` → `route-preference selftest: 57 checks, 0 failures` (offline).

## 6. Failure modes / scars
- **Products differ** → refused by design. The gate is only as fine as the `ledger.transaction` fields (B7 §6): image-thumb records the size, not pixels.
- **`good` is a tie unless you supply standing for every route.** Partial standing is ignored on purpose; inventing a winner would misstate the evidence. Standing is passed in; this lab does not read an OrgBook.
- **Cheap is a vector, so incomparable routes both survive.** A route that saves dollars and one that saves storage are both `cheap` candidates (`tied.cheap`); the hebbian weight, then name order, picks which one `preferred_when.cheap` shows.
- **Weights lag on purpose.** After a real repricing, the raw `preferred_when` from fresh data changes at once, but `settled()` needs several confirmations to follow. There is no time-weighting yet (B7 §11.2 caveat carried in every result).
- **Case-level vs workload-level.** The demo feeds per-case results to the book and computes `preferred_when` on workload sums; the two can differ on mixed workloads.

## 7. How it composes
Consumes B7 (`labs/system2-backtest`: `replay_route`, `fixture_pairs`, `_sum_axes`) over B1 (`labs/activeledger`) records. Standing is the OrgBook half of §14; the budget vector is the ActiveLedger half. `labs/rubric-forge` yields a dense scalar reward that could be supplied as the `standing` integer (scaled) for a route; that wiring is not built here. B8 proposals reach this tool only after B7 certifies them.

## 8. Where to look next
- `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §11.1 (iron-triangle) and §14 (the join).
- `labs/system2-backtest/backtest.py` — the gate and the pairwise verdict this generalizes.
- `labs/route-preference/selftest.py` — every behavior above as an executable check; `situations/blueprints/README.md` — the doc standard.
