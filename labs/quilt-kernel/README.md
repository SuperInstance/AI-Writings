# quilt-kernel

*Receipt, differ and price your own cells. One file, stdlib only, Python 3.9+.*

Status: **extraction-ready, not yet extracted.** Lives at `labs/quilt-kernel/` so it can be tested against
the labs it came from; [`EXTRACTION.md`](EXTRACTION.md) is the plan for making it its own repo.

## 1. What it is (plain version)

You have several ways to do the same job — two models, two algorithms, two build strategies. Which one
should you use? You can't say until you know (a) they really give the *same answer*, and (b) what each
one *costs*. `quilt_kernel` does both, and keeps a tamper-evident log of what it saw:

- **Cell** — wrap a function; every call leaves a *receipt* (answer hash + cost) in a log.
- **Ledger** — the log: append-only, each record hash-linked to the one before.
- **diff** — are two answers the same? Says where they first differ.
- **price** — given two or more implementations, say which wins on *fast* / *cheap*, and when.
  If their answers differ it **refuses** and shows no costs: a cheaper wrong answer is not a bargain.

## 2. Quickstart (10 lines, copy-paste)

<!-- quickstart -->
```python
from quilt_kernel import Cell, Ledger, price, which
led = Ledger()
fast = Cell(lambda xs: sorted(set(xs)), "fast", led, cost=lambda o, xs: {"wall_ms": 1, "usd": 0.002})
slow = Cell(lambda xs: sorted(dict.fromkeys(xs)), "slow", led, cost=lambda o, xs: {"wall_ms": 5, "usd": 0.001})
data = [3, 1, 3, 2]
fast(data); slow(data)
res = price({"fast": fast.last, "slow": slow.last})
print(res["status"], res["class"], "-> fastest:", which(res, "fast"), "| cheapest:", which(res, "cheap"))
print("ledger intact:", led.verify()["intact"], "| records:", len(led.records))
```

Expected output:

```
certified trade-off -> fastest: fast | cheapest: slow
ledger intact: True | records: 2
```

(`cost=` here states the numbers so the output is reproducible. Leave it off and `wall_ms` is measured.)

## 3. API (the whole thing)

| name | does |
|---|---|
| `Cell(fn, name, ledger, cost=None, route=None, keep=("input",), ignore=(), clock=perf_counter)` | call it like `fn`; `.last` is the receipt body of the latest call |
| `Ledger(dev, link="sha256", clock=None, path=None)` | `.emit(type, body)` `.hop(...)` `.verify(anchor=None)` `.anchor()` `.head()` `.total(route=None)` `.receipts(cell=None)` `.to_jsonl()` `Ledger.load(text)` |
| `diff(a, b, ignore=())` | `{identical, a, b, first_difference}`; a, b are raw outputs or receipts (`ignore` applies to raw dicts; for cells use `Cell(ignore=)`) |
| `price(candidates, standing=None, weights=None)` | `{name: receipt \| [receipts]}` → placement, or a refusal |
| `which(result, want="cheap")` | the implementation for `want` ∈ good, fast, cheap, better-faster, better-cheaper, faster-cheaper |
| `Book()` | Hebbian tie-break memory: `.observe(result)`, `.settled()`, `.weights` → feed to `price(weights=)` |
| `replay(ledger, cells)` | re-run stored inputs; `{ok, mismatches}` — replay == live or it says where not |
| `budget`, `add_budget`, `fnv1a64`, `canon`, `content_hash`, `canary` | the primitives, exported |

A receipt body: `{cell, input_hash, product_hash, activation, budget, [input], [product], [route]}`.
`activation = fnv1a64(canon({cell, input, product}))`. The budget vector is ActiveLog v1's:
`{wall_ms, tokens:{api}, usd, power_w, mem_mb, storage_bytes:{train,prod}, reqs}`.
The envelope is ActiveLog v1's: `{alv, dev, seq, ts, mono, type, body, prev}`; types `cell.tick`,
`route.hop`, `ledger.transaction`. Cells emit `cell.tick`; `Ledger.hop` emits balanced double-entry.

## 4. How it decides

1. **Gate first.** Every receipt must be self-consistent (its activation recomputes), and for every
   workload item the products must hash identically across implementations. Otherwise: `refused`, reason
   given, **no budgets in the result**.
2. **Then place** on the iron triangle. *fast* = `wall_ms`. *cheap* = the vector (usd, tokens, storage
   bytes): one implementation beats another only if no worse on all three and better on one; otherwise
   they're incomparable and both stay candidates. *good* = optional `standing` (non-negative ints); if not
   given for every name it is a **tie** — the kernel never invents quality.
3. **Frontier, not a scalar.** You get the undominated set and `preferred_when` per priority. A
   contractor pair (`better-faster`, …) is `None` when no single implementation wins both — a real trade-off.
4. **Weights break ties only.** `Book` (integer Hebbian weights) can choose between implementations the
   data leaves tied; it never overrides a strict win.

## 5. What the log does and doesn't prove

- **Does:** editing or deleting a record is detected, and `verify()` reports the *first* bad record
  (`firstBreak`, 1-based), as in forge-quilt's `verifyWitnessChain`. A receipt whose hash fields disagree
  with its own activation is caught even if it is the last record.
- **Doesn't:** an editor who rewrites *the whole chain* consistently. Store `ledger.anchor()` somewhere you
  don't control the writer of (and pass it to `verify(anchor=)`). Editing *only the last record's budget*
  is likewise invisible to the chain alone; the anchor catches it.
- **fnv1a-64 is a conformance hash.** It proves two ports/runs agree on a product; it is not
  collision-resistant against an adversary. The chain links use sha256 (ActiveLog v1) or
  `link="blake2b-256"` (forge-quilt's integrity rule). The selftest checks the fleet canary.
- **A budget is a claim.** wall time is measured, but `usd`/`tokens` come from your `cost` function; the
  kernel records them, it does not audit them. Receipts don't prove a cost was *real*.

## 6. Limits (honest)

- Products must be JSON-shaped and deterministic. Non-canonicalisable values raise (no `repr()` hashing);
  floats compare exactly, so round them yourself if you need tolerance. LLM calls need a structured or
  temperature-0 answer, and even then a provider can change a model under you — that shows up as a
  refusal or a `replay` mismatch, which is the point.
- Only `wall_ms`, `usd`, `tokens` and `storage_bytes` are priced. `mem_mb` and `power_w` are recorded and
  summed but do not move the placement. Costs are assumed stationary: re-price when prices or hardware change.
- Per-record `ts` is a deterministic counter unless you pass `clock=`. Not thread-safe; one Ledger, one writer.
- The placement logic is copied from `labs/route-preference` (Pareto + Hebbian) and gated like
  `labs/system2-backtest`; `selftest.py` cross-checks parity with those labs when they sit next to it.

## 7. For contributors (technical)

```
python3 selftest.py        # prints: quilt-kernel selftest: N checks, 0 failures
python3 examples/data_pipeline.py   # dedupe: sorted vs hashed
python3 examples/llm_call.py        # two stub models + one cheaper-but-wrong model (refused)
python3 examples/build_step.py      # bundle: concat vs staged
```

The selftest includes the README quickstart (extracted from the block above and executed), every
example, tamper/anchor/first-break cases, replay of pure and impure functions, and parity with the
source labs. Design rule: a new primitive must be reducible to "one more receipt field, one more gate,
or one more axis" — otherwise it belongs in a layer above, not here.

## 8. Lineage

`labs/activeledger` (envelope, budget, double-entry, prev-chain) · `labs/system2-backtest` (identity
gate, iron triangle) · `labs/route-preference` (Pareto frontier, Hebbian book) · `labs/situation-recorder`
(fnv1a-64 canonical-JSON, tamper-evident chain) · API shape follows
[SuperInstance/forge-quilt](https://github.com/SuperInstance/forge-quilt) `openapi.yaml`
(`verifyWitnessChain` → `{intact, firstBreak}`, `getAnchoredHead`, `getCanary`; FNV-1a is conformance-only).
See [`EXTRACTION.md`](EXTRACTION.md).
