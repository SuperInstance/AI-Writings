# invariance-miner — the receipt log is a free dataset of your program's symmetries

**One line:** read a cell's receipts (input → output digest) backwards to discover which input
transforms leave its product unchanged. Compose the ones the receipts actually pay for into a cache
canonicalizer, and let the differ veto the rest.

Every quilt cell already writes `(input, digest)`. Two different inputs with one digest, both mapped
to one key by a candidate transform `t`, are *collision evidence* for `f(t(x)) == f(x)`. One bucket
holding two digests *refutes* `t`. **Mining costs zero cell calls**: the evidence was already paid
for by the audit trail.

```
python3 invariance_miner.py     # report (~8 s)  -> report.txt
python3 selftest.py             # invariance-miner selftest: 25 checks, 0 failures
```

The cells under study are unmodified example-quilt code: `text-normalize-quilt` `full_route` and
`convert-quilt` `full_route`. The transform library includes planted traps (`strip_punct`,
`sort_words`, `trunc16`, `round3`, `unit_lower`, `swap_units`). Traffic is Zipf over intents with
real surface variation (case, spacing, padding, `+1.50` vs `1.5`). It **shifts** between the 600-
receipt mining window and the 3000-request serving window, and the shift adds intents that spring
the traps.

## Measured (20 seeds, mean per run)

| cell | cache key | hit rate | cell calls | **false hits** |
|---|---|---|---|---|
| text | exact key | 0.761 | 717.2 | 0 |
| text | log-only canonicalizer | 0.992 | 23.0 | **90.8** |
| text | + active differ check (k=8) | 0.993 | 20.0 | 0 |
| text | **guarded** (Occam + active) | **0.993** | **20.0** | **0** |
| convert | exact key | 0.982 | 54.0 | 0 |
| convert | log-only | 0.997 | 10.0 | **241.95** |
| convert | + active differ check | 0.997 | 10.0 | **241.95** |
| convert | **guarded** | **0.996** | **11.0** | **0** |

Trap adoption across 20 runs: log-only 20/20 (text) and 20/20 (convert). After active checks: 0/20
(text) and **20/20** (convert). Guarded: 0/20 for both.

Text, guarded: **36× fewer cell calls** than exact-key caching, with 0 wrong products. It mined
`collapse_ws ∘ casefold` for 16 active calls.

## The three findings

1. **Receipts are a symmetry detector.** The log alone finds the real invariances (`casefold`,
   `collapse_ws`, `strip`, `canon_number`, `strip_plus`) and refutes nothing true, at zero cost.
2. **Log-only acceptance is dangerous under shift.** `trunc16` and `sort_words` are *consistent with
   every receipt*, because the log never held two inputs that separate them. Once traffic shifts,
   they serve wrong products (90.8 per run).
3. **Active checks sampled from the log cannot refute an off-support trap** (the honest negative).
   `round3` gives the right product on *every* logged input, because no logged value has more than
   3 decimal places. Drawing more checks from the same distribution never catches it. What does
   catch it is the **Occam guard**: adopt a transform only if it *merges* at least `min_gain` more
   logged inputs than the chain already does. `round3`'s extra coarsening is unevidenced (every merge
   it makes, `canon_number` already made), so it is pure off-support risk and is never adopted.
   *Never adopt a symmetry the receipts don't pay for.*

## Honest limits

- There are 0 false hits on *this* traffic. A guarded transform is still only verified on the log's
  support plus k checks. `casefold` before NFKC is not a theorem for all of Unicode, only for what
  was seen. Pair it with `labs/audit-lottery` to keep auditing the canonical cache in production.
- The transform library is hand-written. Discovering transforms (for example, from a DSL of string
  ops) is the next lane.
- Convert traffic has low cardinality, so exact-key caching already hits 0.98 there. The win is a 5×
  cut in calls, not the hit rate.

**Extraction target:** `quilt-invariance-cache` — **general-use** (any deterministic function behind
a cache: API gateways, LLM prompt caches with normalization, build caches, feature stores).
