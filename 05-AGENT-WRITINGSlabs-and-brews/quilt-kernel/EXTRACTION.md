# EXTRACTION — turning `labs/quilt-kernel` into a standalone repo

Status: **manifest only. Nothing has been extracted or published.** This file says what would move, what
would not, and what must be true first. Every command below was run from this directory on this branch.

## 1. The standalone repo

**Proposed name: `receipt-kernel`** (PyPI/import name `quilt_kernel` kept as an alias for one release).
Reason: outsiders search for what it *does* — receipts. "quilt" is fleet vocabulary that means nothing to
someone who just wants to compare two model calls. If the fleet prefers identity over discoverability,
`quilt-kernel` is the fallback and needs no rename work, because the module is already `quilt_kernel.py`.
This is a naming call for the operator; nothing in the code depends on it.

Shape of the new repo (what ships):

```
receipt-kernel/
  quilt_kernel.py        # the module, unchanged (single file, stdlib only)
  selftest.py            # runs standalone; parity checks auto-skip when the labs are absent
  examples/              # data_pipeline.py, llm_call.py, build_step.py
  README.md  EXTRACTION.md -> replaced by CHANGELOG.md / CONTRIBUTING.md
  pyproject.toml         # NOT YET WRITTEN — py-modules = ["quilt_kernel"], requires-python >=3.9
```

Verified: copying this directory to an empty location and running `python3 selftest.py` gives
`115 checks, 0 failures` (the 8 parity checks against the labs are skipped and it says so). In-repo it is
`123 checks, 0 failures`. A deliberate mutation — disabling the product-identity gate — makes the copy
fail 2 checks, so the suite does bite.

**Before extracting:** (a) write `pyproject.toml` and choose a licence (the repo has none for labs; that is
the operator's call); (b) decide the name; (c) replace the selftest's parity block with a pinned golden
file if you want parity to survive without the labs (today it is live-compared, then dropped).

## 2. Public API surface (frozen at 0.x; ≤ 14 names)

```
Cell(fn, name, ledger, cost=None, route=None, keep=("input",), ignore=(), clock=perf_counter)
    .last                               receipt body of the latest call
Ledger(dev="kernel", link="sha256", clock=None, path=None)
    .emit(type, body) .hop(...) .verify(anchor=None) .anchor() .head() .total(route=None)
    .receipts(cell=None) .to_jsonl() .run_hash()      Ledger.load(text)
diff(a, b, ignore=())     -> {identical, a, b, first_difference}
price(candidates, standing=None, weights=None)  -> certified placement | refused
which(result, want)       -> implementation name | None | raises Refusal
Book()                    .observe(result) .settled() .weights
replay(ledger, cells)     -> {replayed, mismatches, ok}
budget / add_budget · fnv1a64 / canon / content_hash / canary · Refusal
```

Wire formats (these are the compatibility promise, more than the Python names):
ActiveLog v1 envelope `{alv, dev, seq, ts, mono, type, body, prev}`; receipt body
`{cell, input_hash, product_hash, activation, budget, …}`; verify verdict `{intact, firstBreak, reason}`;
anchor `{digest, seq, link}`. Verdict and anchor names deliberately follow
[forge-quilt](https://github.com/SuperInstance/forge-quilt)'s `openapi.yaml` (`verifyWitnessChain`,
`getAnchoredHead`, `getCanary`) so a fleet consumer can expose the ledger through that spec's `/witness/*`
paths without translation. Known deltas from forge-quilt, stated plainly:

| | forge-quilt | quilt-kernel |
|---|---|---|
| chain link hash | BLAKE2b-256 for integrity | sha256 by default (ActiveLog v1 rule); `link="blake2b-256"` matches forge |
| `firstBreak` | integer ≥ 1 | integer ≥ 1 (1-based), plus a `reason` string forge's `Verdict` does not have (its schema is `additionalProperties: false`) |
| anchor | `{digest, anchoredAt, anchor}` (where it lives) | `{digest, seq, link}` — the kernel doesn't know where you store it; add `anchoredAt`/`anchor` in your adapter |
| canary | `024a555471370b18d` over `café Δ 日本語` | same constant, checked by `canary()` |

Not aligned, not attempted: forge-quilt's cell lifecycle (`bindCell`, `receiveBottle`, `tick`, the γ+η
conservation refusal). The kernel receipts *functions*; it does not model stateful cells.

## 3. General-usage examples (each receipted and priced; each runs)

All three are in `examples/` and are executed by `selftest.py`. Budgets in the first two are a stated cost
model so the output is reproducible; the third measures real wall time and asserts only the storage axis.

**Data pipeline** — `python3 examples/data_pipeline.py`
```
ledger intact: True | records: 6
status: certified | class: dominant | faster: hashed
```
Two dedupes (`sorted` vs `set`) over three inputs. Identical products, `hashed` dominates on the priced axes.
It also uses more `mem_mb` — recorded in the receipts but *not priced* (see README §6). If memory is your
constraint, that is a gap in the placement, not in the data.

**LLM call** — `python3 examples/llm_call.py` (stub models; no network)
```
small vs large: certified dominant | cheapest: small | fastest: small
small vs cheap-wrong: refused - products differ at item 0 — never price a cheaper different answer
```
The Cell returns only the structured answer; token usage is read from the response in `cost` (budget, not
product). The refused line is the feature: the cheapest candidate is cheapest because it is wrong.
The token prices are invented. For a real API: same wrapping, `temperature=0`, a structured output.

**Build step** — `python3 examples/build_step.py`
```
build: certified | cheapest (storage): concat
```
Two bundlers emitting identical bytes; the staged one burns extra scratch storage (`train` bytes). The
class (dominant vs trade-off) depends on measured wall time and is not printed, on purpose.

## 4. What stays internal (does not move to the new repo)

| stays in the fleet | why |
|---|---|
| The 14-tuple cell, 11 opcodes, 26 kinds, 4D lattice, the five laws | the kernel needs none of it; receipts of *functions* are a smaller idea than the cell model and should not inherit its claims |
| `labs/system2-backtest` fixtures and `replay_route` over calc/convert/datetime quilts | they validate *our* example quilts; the kernel carries only the gate and the placement |
| `labs/route-preference` demo + `PreferenceBook` digest | the kernel has `Book`; the lab stays as the reference and as the parity oracle |
| `labs/activeledger` `otel_export`, `route_sim`, `at_rest` (RS repair, delta-predict compression) | optional layers above a ledger; good extension packages, bad kernel |
| `labs/situation-recorder` relation verbs (`TASK/ROUTE/DRAFT/…`), corpus builders | a transcript vocabulary for manager↔crew missions, not a general receipt |
| OrgBook standing | `standing=` accepts any non-negative ints; where they come from is not the kernel's business |
| Fleet deploy, witness-log-as-source-of-truth conventions, `ledger.transaction` authoring | operational policy. The type is accepted by `Ledger.emit`; nothing in the kernel constructs it |

## 5. Extraction checklist

1. Decide name and licence. 2. Add `pyproject.toml`. 3. Copy the six files listed in §1 into a new repo.
4. `python3 selftest.py` must print `quilt-kernel selftest: 115 checks, 0 failures` (standalone count).
5. Publish; in this repo, leave `labs/quilt-kernel` as a thin pointer and keep the parity block live.
6. Fleet-side follow-ups (not needed for extraction): switch `system2-backtest`/`route-preference` to import
   the kernel's gate and placement (removes the duplicated logic), and expose the ledger via forge-quilt's
   `/witness/*` operations.

## 6. Known gaps to fix before a 1.0

- Only four axes are priced; `mem_mb`/`power_w` are carried but ignored by `price`.
- `price` sums workloads; it does not weight items or report per-item variance.
- No thread safety; single writer per Ledger.
- Replay assumes the function is pure. An impure one is *detected* (mismatch), not repaired.
- The chain proves no more than forge-quilt says a chain proves: corruption and partial edits, not a
  motivated rewriter without an external anchor.
