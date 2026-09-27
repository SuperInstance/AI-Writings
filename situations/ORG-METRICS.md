# Org metrics — the dispatch org as a measured learning system

*Baseline snapshot, 2026-09-27, computed directly from
[`dispatch-ledger.csv`](dispatch-ledger.csv). This is the instrument the
[`arch/INTELLIGENCE-CLUSTERS.md`](arch/INTELLIGENCE-CLUSTERS.md) study of "the cluster's
own O1–O12 as a learning system" reads. Replay ≡ live: every number here re-derives from
the booked WAL, so this file is a reading, never a source of truth.*

## Snapshot (42 well-formed dispatches)

| metric | value | reads on |
|---|---|---|
| booked dispatches | 42 | O5 (everything booked) |
| resolved (DONE+FOLDED) | 31 | — |
| passed w/ earned standing | 16 | R2 |
| total cost-units | 185 | O7 metabolism |
| **expensive-tier wakes (cost ≥ 8, Opus/Fable)** | **11 = 26%** | **O1 deadband** |
| cost per passed-with-standing | 5.69 | O7 |
| verdict mix | ACT 25 · ESCALATE 12 · CONFIRM 2 · INDUCE 2 · ANSWER 1 | routing |
| model mix | sonnet-5 20 · opus-5.5 9 · opus-4.8 8 (dispatcher) · haiku 3 · fable 2 | tiering |

## Trend by thirds (booking order)

| third | dispatches | resolved | passed | cost-units | cost/passed |
|---|---|---|---|---|---|
| early | 14 | 13 | 5 | 48 | 3.20 |
| mid | 14 | 7 | 1 | 48 | 3.00 |
| recent | 14 | 11 | 10 | 89 | **7.20** |

## Honest reading (what the numbers do and don't say)

- **O1 (deadband) is holding.** The expensive tier is woken 26% of the time; the cheaper
  tiers (Sonnet build + Haiku runner + dispatcher) carry ~74%. ACT is 60% of verdicts —
  the build tier is the default, as designed. Fable fired twice (apex, rare).
- **O7 (cost-per-passed *falling*) is NOT yet demonstrated — and the doc will not pretend
  it is.** Cost/passed rose in the recent third (3.0 → 7.2), but that rise is an
  *investment*, not decay: the recent third contains the deliberate Fable apex call
  (cost 20) and the Opus arch keystone (cost 8) of the cargo-line sprint. The window is 42
  dispatches over one day — far too small, and dominated by a chosen high-leverage spend,
  to claim a metabolism trend either way. Stated plainly so nobody Goodharts the number.
- **The real O7 test comes later.** The prediction to falsify: once the commons of solved
  architectures (O3) starts letting the dispatcher *reuse* an architecture instead of
  re-waking Opus, and once runners earn standing (O2) and run unsupervised, cost-per-passed
  should fall on the *routine* task-classes even as apex spend stays lumpy. Re-measure at
  ~d080 and ~d120 and compare like-for-like task-classes, not the blended average.

## Method

Parse `dispatch-ledger.csv`; a dispatch "passed" iff `status ∈ {DONE, FOLDED}` and
`standing == 1` (an acceptance-bearing dispatch that earned it — SESSION/NOTE/dispatcher
rows carry standing 0 by design and are excluded from the pass-rate). "Cost-units" sum the
integer `cost_class` (8 Opus/Fable · 3 Sonnet · 1 Haiku/dispatcher). Trend splits the rows
in booking order into thirds. No sampling, no estimation — it is a full scan of the WAL.

*The org optimizes itself the way the software does — but only if it measures itself
honestly. This is the first reading; the trend is the artifact, not the snapshot.*
