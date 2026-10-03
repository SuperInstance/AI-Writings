# pincher (B3) — answer from a cheap guess when it has earned the right, else run the full route

## 1. In one breath
A learned early-exit: for each kind of input it counts how often a cheap guess matched the full route's answer, returns the guess once that record is good enough, and otherwise runs the full route and keeps learning. Whether the guess is allowed to stand is never taken on trust: B7 replays both routes and refuses to price any pair whose answers differ.

## 2. Why it exists
`situations/arch/ACTIVELEDGER-CELL-GRAPH.md` row B3: B4 ("preferred when") needs at least two real routes to the same product, and the pincher is the cheapest way to get a genuinely different second one. This lab is self-contained (it mirrors the quilt-pincher idea, imports no external repo). The testbed is `labs/examples/text-normalize-quilt`; the pincher is its second route, priced by `labs/system2-backtest` (B7) and ranked by `labs/route-preference` (B4).

## 3. The mental model
- **Full route** — textnorm's unicode path (NFKC, casefold, whitespace collapse). Always right.
- **Guess** — `" ".join(t.lower().split())`. Right on ASCII, Cyrillic, most Latin; wrong on `ß`, `ﬁ`, `Ⅷ`, fullwidth, decomposed accents, final sigma `ς`, `µ`, `ŉ`.
- **Class** — which codepoint ranges appear in the text (`A`, `AE`, `AY`, `AL`, `AG`, `AK`, `AC`, …); a range scan, no `unicodedata`. Coarse on purpose: some classes are only partly reliable and the pincher must learn to decline them.
- **Confidence** — `conf = agree / (n + K)`, K=3 phantom disagreements, exact `Fraction`. Pinch iff `conf >= 9/10`.
- **Grows with evidence** — under all-agree evidence `conf = n/(n+3)` strictly increases and a class flips to "pinch" at exactly `n* = 27` (closed form `n_star()`). A disagreement leaves `agree` flat while `n` grows, so confidence shrinks.
- **Audit slice** — every 10th pinch in a class still runs the full route, so a drifting class is noticed (its confidence drops, the full answer is returned).
- **Fallback** — below the bar it runs the full route and compares its own guess to the answer, so evidence accrues even while declining.

## 4. Walkthrough
`cd labs/pincher && python3 pincher.py` — 600 seeded texts per mix, the pincher learning as it goes, each run replayed by B7 against the full route:
```
== ascii-heavy: n=600  paths={'pinch': 466, 'audited': 50, 'fallback': 84}  full-route calls=134/600
   B7: certified 600, refused 0
   pinch  wall_ms=4474  storage_bytes=5341327     full  wall_ms=7800  storage_bytes=21504000
   iron-triangle: dominates-faster-cheaper  axes={'good': 'tie', 'fast': 'pinch', 'cheap': 'pinch'}
== balanced:    paths={'pinch': 312, 'audited': 33, 'fallback': 255}  full-route calls=288/600
   pinch  wall_ms=6168  storage_bytes=11210281    full  wall_ms=7800  storage_bytes=21504000
   iron-triangle: dominates-faster-cheaper  axes={'good': 'tie', 'fast': 'pinch', 'cheap': 'pinch'}
== adversarial: paths={'pinch': 0, 'audited': 0, 'fallback': 600}  full-route calls=600/600
   pinch  wall_ms=9600  storage_bytes=23100920    full  wall_ms=7800  storage_bytes=21504000
   iron-triangle: dominates-faster-cheaper  axes={'good': 'tie', 'fast': 'full', 'cheap': 'full'}
   B4 preferred_when: fast=full, cheap=full  (pinch is a pure loss when nothing is pinchable)
```
**Iron-triangle placement (modeled budgets, product-identical on all 1,800 cases):** `good` is a tie by construction (identical products); on the ascii-heavy and balanced mixes the pincher takes `fast` and `cheap` (B7 class `dominates-faster-cheaper`, B4 `preferred_when` = pinch for fast, cheap, better-faster, better-cheaper, faster-cheaper); on the adversarial mix the same verdict flips to `full`. `cheap` splits into compute vs storage (B7 §11.1): `usd` and `tokens` are 0 locally, so compute ties and **storage alone** decides cheap. What it learned on the balanced mix: `A` 57/57 and `AY` 30/30 agreements → pinchable; `AE` (3% `ŉ` drift) 50/53 → conf 25/28, just under the bar, never pinched; `AL`, `AG` mixed, `AK`, `AC` always wrong → never pinched. Modeled break-even: a pinched call costs 5 wall_ms, a fallback 16, full 13, so the pincher wins when more than 3/11 ≈ 27% of calls pinch (balanced: 52%).

## 5. The contract
- `Pincher(guess, full, classify, tol=0, target=9/10, k=3, audit_every=10).answer(x) -> (out, info)`; `info.path` ∈ `pinch | audited | fallback`; `info.guess_ok` is `None` only for an unaudited pinch. `close(a, b, tol)`: numbers within `tol`, everything else exact (text uses tol 0).
- `run(text, pincher)` books an ActiveLog v1 run (`cell.tick` kind `PINCHER`, `route.hop`, `ledger.transaction` with product `{out}`, same shape as textnorm's). A pinched call costs a cheap-route-sized call plus the class scan and its table row; a fallback pays the full route's own steps **plus** the gate. `train` bytes = the measured size of the table row consulted.
- `price(texts)` → B7 `backtest_corpus` + B4 `prefer`/`prefer_axes` over the pincher and full records.
- Invariants: no float on the decision path; state is a pure function of the observation sequence (`digest()`); a pinched answer that differs from full makes B7 and B4 **refuse**, exposing no budget.
- Receipt: `python3 selftest.py` → `pincher selftest: 73 checks, 0 failures` (offline, seeded).

## 6. Failure modes / scars
- **The win is modeled, not wall-clock.** The budget vector uses the example quilts' declared cost model (full route = heavy unicode tables). Measured in CPython on this testbed the full route is already ~0.3–0.8 µs, and the whole pincher (class scan + bookkeeping) is slower: `real ns/call end-to-end` — ascii-heavy 1,955 vs 267, balanced 4,220 vs 424, adversarial 8,354 vs 782 (one run; timings vary by machine and are not asserted). The pincher pays off only where the full route is genuinely expensive (model/API calls); here it is a correctness/plumbing demonstration.
- **Class granularity limits the win.** A range class that mixes safe and unsafe inputs (`AL`: `é` vs `ß`) is never pinched even though most of its texts are safe. A finer class would pinch more and cost more to compute.
- **Mispinches are possible.** Unaudited pinches (9 of 10) are not checked. In the 1,800 measured cases none slipped through, but a reckless pincher (target 0) does mispinch, and the selftest shows B7 refusing 3 of 4 such cases. B7 is the backstop, not the pincher's own check.
- **Storage is the only separating cheap axis here** (`usd`/`tokens` are 0); with a paid full route, compute would dominate the cheap verdict.
- **Stationary budget** (B7 §11.2): re-backtest on repricing. Workload mixes are synthetic and seeded (seed 20260929), not production traffic.

## 7. How it composes
Reads B1 records (`labs/activeledger`); the testbed is `labs/examples/text-normalize-quilt` (its `full_route`, `COST`, `run`). B7 (`labs/system2-backtest`) gates and prices; B4 (`labs/route-preference`) records `preferred_when` and a `PreferenceBook` (settles on pinch for `fast` under the balanced mix). B8 could propose pincher thresholds as alternative networks.

## 8. Where to look next
- `labs/pincher/selftest.py` — 73 checks: premise (guess right/wrong where claimed), n* closed form and monotone growth, cold fallback, audit slice, drift, numeric tolerance, B7 certification and refusal, regime flips.
- `ACTIVELEDGER-CELL-GRAPH.md` B3, B4, B7 rows and §11.1; `labs/system2-backtest/README.md`, `labs/route-preference/README.md`.
