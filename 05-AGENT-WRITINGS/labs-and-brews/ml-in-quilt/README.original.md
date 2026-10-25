# ml-in-quilt — a transformer where every block is a cell System-2 can price

*A `labs/` cell. Python stdlib only, offline, deterministic. The runnable half of
[`situations/arch/ML-IN-QUILT-ARCHITECTURE.md`](../../situations/arch/ML-IN-QUILT-ARCHITECTURE.md).*

## 1. In one breath
A tiny transformer (2 layers, d=32, 19k params) whose tokenize/embed/norm/attention/MLP/head/sample
steps are each a cell. Each cell writes a budgeted, hash-chained tick to an ActiveLog, and the
attention, MLP and head cells each have fp32, int8 and 4-bit versions. The fleet's existing
System-2 tools (B7 backtest, B4 preference) then choose between them without changes.

## 2. Why it exists
Porting llama3-from-scratch or simple-llm line by line gives you a forward pass that runs, and
nothing else: no receipts, no priced alternatives, and no way to tell which block made a run go
wrong. This lab asks what the forward pass looks like when it is built from quilt cells, and tests
whether B1/B7/B4/at_rest/situation-memory accept it as it is. They do, with one design constraint
(§3, *product boundary*) and two blind spots (§6).

## 3. The mental model
```
tokenize ─▶ embed ─▶ [ norm ─▶ attn(+KV chain) ─▶ norm ─▶ mlp ] × 2 ─▶ norm ─▶ head ─▶ sample
   exact      fp        fp      fp|q8|q4              fp     fp|q8|q4        fp    fp|q8|q4  greedy
                                                                  (or: norm ─▶ jepa.predict ─▶ head, exit after L0)
```
- **Cell tick.** Each call to a cell emits one `cell.tick` with `{cell, kind, impl, pos, in, out, w, kv, flops, bytes, budget}`.
  `in`/`out` are fnv1a-64 hashes of the exact IEEE bytes, and `w` is the hash of the packed weights
  the tick read. Ticks close into one `ledger.transaction` whose **product** is `{prompt, tokens, text}`.
- **Plan.** Maps a cell or kind to an impl, e.g. `{"mlp": "q4"}` or `{"exit": 1}`. A **route** is a
  plan, or a composition of plans such as `spec-q4` (draft with the q4 plan, verify with fp).
- **Product boundary.** B7 requires exact product identity. A quantized activation never equals
  the fp32 activation, so identity is declared at the **sampled token**. Everything upstream of
  that is how the route got there.
- **Verifier cell.** A lossy draft plus one batched exact verify pass gives speculative decoding.
  The committed tokens are the verify plan's argmax by construction, so the route is
  product-identical to fp on every situation (24/24 in the run below).
- **KV chain.** Each layer's KV cache is a hash chain: `kvh[p] = H(kvh[p-1], H(k_p, v_p))`. Every
  prefix therefore has a content address. The prefix cache uses it as a key, and its hits can be
  checked against the chain.
- **Budget.** Every tick carries `wall_ms` from a declared roofline model
  (`max(flops/F, bytes/B)`, `cellml.DEVICES`). It is not measured, because measured wall-clock would
  break replay == live. Real Python timing is reported beside it and is never logged.

## 4. Walkthrough
```
$ cd labs/ml-in-quilt && python3 mlq_system2.py          # ~30 s
model  d=32 layers=2 heads=2 ff=64 ctx=64  params=19260  readout train_acc=0.7589  jepa r2=0.9926
== differ (teacher-forced vs fp, 145 positions)
   plan        agree   max|dz|    mean|dz|   gate-safe gate-flip
   q8          0.9931  0.0283     0.0119     0.8219    0
   q4          0.8069  2.2275     0.8185     0.0000    0
   q4-attn     0.8621  0.2754     0.1008     0.2603    0
   q4-mlp      0.8414  0.2325     0.1187     0.3288    0
   q4-head     0.9448  2.1870     0.8124     0.0000    0
   jepa-exit1  0.7724  1.0681     0.1845     0.0000    0
== B7 fp vs route, 24 situations x 12 tokens, device=edge
   q8         certified 20 refused  4  class=dominates-faster-cheaper   (q8 dominant)
   q4         certified  0 refused 24
   spec-q4    certified 24 refused  0  class=dominates-faster-cheaper   (fp dominant)  accept=195/379
   spec-jepa  certified 24 refused  0  class=dominates-faster-cheaper   (fp dominant)  accept=190/399
   gate-q8    certified 24 refused  0  (fp dominant)  eps=0.0283 verifies=101/288 fixed=0
   trust-q8   certified 24 refused  0  (fp dominant)  eps=0.0283 verifies=80/288 fixed=0
== B7 ... device=accel   (modeled wall ms, 24 situations: fp 2.428)
   spec-q4    certified 24 refused  0  class=trade-off   wall 2.374
   gate-q8    certified 24 refused  0  class=trade-off   wall 2.144
   trust-q8   certified 24 refused  0  class=trade-off   wall 1.879
== B4 device=edge   exact routes=[fp, gate-q8, spec-jepa, spec-q4, trust-q8]  frontier=['fp']
== B4 device=accel  frontier=['fp','spec-q4','trust-q8']  fast=trust-q8  cheap=fp
== replay==live (spec-q4, 177 records): True   tamper L1.w1[0][0]+0.25 -> first divergence load:L1.w1, first compute cell L1.mlp
== prefix cache: reused 19 positions, kv heads match=True, B7 certified, flops 1308792 -> 589680
== at rest: weights fp=73456 q8=20396 q4=11244 B (q4 6.53x smaller); RS x1.270, 96 bytes corrupted -> repaired=True
   activation log 177 records: jsonl 88765 B, jsonl+lzma 12108 B, ALR1+RS 6127 B, exact=True
== recall (q8 held on 20/24; majority 0.8333): LOO 3-NN lexical 0.8333 latent 0.7917 margin 0.875
== python wall ms (best of 3, sidecar): fp 45.8  q8 41.4  q4 51.6  spec-q4 99.7  spec-jepa 63.3
```
How to read the output:
- **q8** is certified on 20 of 24 situations and dominates fp on those 20.
- **q4** in every block never survives 12 greedy tokens. Its *product horizon*, the first token
  that differs from fp, has mean 3.3 and is 0 on 5 of the 24 situations. For q8 the mean is 10.9.
- **Speculative decoding** turns q4 into an exact route. Whether that route is worth running
  depends on the device:
  - On `edge` (flop:byte = 1), fp dominates it.
  - On `accel` (flop:byte = 100), the batched verify is nearly free, and spec-q4 is the faster of the two.
- **Margin-triggered verify** (`cellml.run_gated`, the routes `gate-q8` and `trust-q8`):
  - q8 decodes on its own. When its top-1 margin is ≤ 2ε, fp catches up on every pending token in
    one batched pass and supplies the uncertain token itself.
  - ε = 0.0283, the max |Δlogit| on the first half of the corpus.
  - **trust-q8 never re-checks confident tokens, yet it is certified 24/24**, against 20/24 for
    q8 alone. Across all runs the confident tokens were never wrong (0 fixes).
  - On `accel` it is the fastest exact-product route measured: 1.88 ms modeled, vs 2.43 for fp and
    2.37 for spec-q4. On `edge`, fp still wins.
  - **Out of distribution** (`OOD_PROMPTS`: 16 pangram fragments whose words the corpus never
    contains; accel profile), trust-q8 is again 16/16 with 0 fixes, against 12/16 for q8 alone.
    It needed 44 verify passes for 192 tokens.

## 5. The contract
- `cellml.run_greedy(model, prompt, n, plan, route)` and
  `run_speculative(model, prompt, n, draft_plan, verify_plan, route, k)` each return an ActiveLog.
  The log passes `activeledger.verify_chain` and `backtest.replay_route` (budget re-sum).
- `mlq_system2.replay(model, records)` re-executes a run from its transaction alone. It returns
  `equal` when the records are byte-identical. Otherwise it returns the first divergent record and
  the first divergent compute cell.
- Invariants:
  - Every compute tick reads an earlier tick's output (dataflow closure).
  - A prefix-cache hit's KV chain head equals the computed one.
  - A refused B7 verdict exposes no budget.
- `run_gated(model, prompt, n, cheap_plan, exact_plan, route, eps, final_verify)`: with
  `final_verify=True` the route is exact by construction. With `False`, tokens trusted by
  calibration are never re-checked, and B7 decides whether the route holds.
- Receipt: `python3 selftest.py` prints `ml-in-quilt selftest: 83 checks, 0 failures` (~50 s).

## 6. Failure modes / scars
- **Identity is not quality.** On "the rat ", fp writes `sat sathe ma` and q8 writes `sat on the m`.
  q8's text reads better, but the gate refuses q8 because the products differ. The gate is working
  as designed. `good` needs an oracle (rubric-forge or standing), not the differ.
- **Latent closeness is not product identity.** The JEPA predictor maps Z_in → Z_out with
  R² = 0.993, yet it has the *lowest* teacher-forced token agreement of any plan (0.772).
  Residual error lands on decision boundaries.
- **B7 has no hot-memory axis** (reproduced from ENCODING-GEMS-STUDY). The prefix cache's
  residency is logged in `mem_mb`, but B7 does not score it, so the cache looks free.
- **B7 cheap = storage.** `spec-q4` stores both fp and q4 weights (83 KB vs 73 KB). That is why
  fp stays cheaper even on `accel`.
- **The cost model is declared, not measured.** In Python, q4 is *slower* than fp (51.6 vs 45.8 ms).
  The kernel keeps a dequantized copy, the same scar as code-real-quant. The roofline prices what a
  fused kernel would stream.
- **The situation-recall sample is too small to mean anything.** The margin feature scores 0.875
  against a majority baseline of 0.833, a one-case difference. Lexical recall ties the baseline,
  and latent recall is below it.
- **Toy scale.** The model is 19k params, with seeded weights and a ridge-fitted readout. It is an
  echo-state net, not an LLM, and none of the numbers transfer to real models as values. What
  transfers is the *shape*: gate at the token, and price by device.
- **trust-q8 is certified by calibration, not proven.** ε is the max |Δlogit| on the first half
  of the corpus, and the 24 situations overlap that corpus. The 16 OOD situations also held.
  However, after the first few characters generation drifts back to corpus-like text, so the OOD
  test is weaker than it looks. A logit error above ε on unseen text would still let a wrong
  confident token through. B7 would refuse such a run, but only after the fact.
  `gate-q8` pays roughly 14% more modeled time (accel) to remove this risk.

## Localization control

*Credit: the cellgraph repo proved this shape (perturb one weight, watch which cell digests move
first; Wq → 14 cells, Wv → 12, Wlog → 2). We had only asserted that faults localize. See
[`situations/arch/FLEET-CONVERGENCE-CELL-NATIVE-ML.md`](../../situations/arch/FLEET-CONVERGENCE-CELL-NATIVE-ML.md).*

[`localize.py`](localize.py) adds 1e-9 to one element of one weight, re-runs the prompt
`"the cat sat on the "`, and compares the per-cell `out` digests (plus each layer's KV chain head)
against the baseline. It reads digests only. The expected answer comes from a declared
graph (weight → consumer cell, in execution order) that the digests are checked against.
Measured (`python3 localize.py`, 11 cells in this 2-layer toy):

| perturbed | first cell moved | cells moved | KV-chain layers moved |
|---|---|---|---|
| embed | embed | 11 / 11 | 0, 1 |
| L0.wqkv | L0.attn | 9 / 11 | 0, 1 |
| L0.wo | L0.attn | 9 / 11 | 1 |
| L0.w1 | L0.mlp | 7 / 11 | 1 |
| L0.w2 | L0.mlp | 7 / 11 | 1 |
| L1.wqkv | L1.attn | 5 / 11 | 1 |
| L1.wo | L1.attn | 5 / 11 | none |
| L1.w1 | L1.mlp | 3 / 11 | none |
| L1.w2 | L1.mlp | 3 / 11 | none |
| head | head | 1 / 11 | none |

In every row the first-detected cell is the declared direct consumer, and the moved set is exactly
the declared downstream cone. Selftest asserts both. What this does and does not show:
the residual stream makes this toy a single chain, so the moved set is always a suffix of the
execution order. Localization pins down *where the suffix starts*, and the KV-chain column adds
a second, non-suffix signal (an `L0.w1` fault changes layer 1's cache but not layer 0's).
It is a 19k-param toy, and one prompt and one element per tensor were tried, so this is a
control, not a coverage claim. The `wqkv` element is a K row, because a Q-row perturbation
would not touch the KV chain. Caveat: the `fp` kernel's at-rest `whash` packs float32, so a 1e-9
change to a weight is invisible to `load:` ticks. Activation digests are what catch it.

## Why dtype is in the digest

*Credit: cellgraph found that casting to float32 before hashing made a 9.8e-10 perturbation
byte-identical, so the digest silently lied.*

`act_hash` in [`cellml.py`](cellml.py) already packed full float64 bytes (no downcast). It now also
hashes a dtype tag (`f64:`, `f32:` or `i64:`) in front of the bytes, so the same bytes declared under
two precisions cannot collide, and a future lower-precision route has to say what it is.
`act_hash(x, "f32")` exists to declare such a route (and to demonstrate the failure).
Selftest proves, on a copy of a small activation: (a) the default f64 digest detects a 1e-9
perturbation; (b) hashing that same pair at f32 gives equal digests, i.e. the masking is real;
(c) the same values under two declared dtypes hash differently.

**Golden-hash change.** Prepending the tag changes every activation digest, so previously recorded
ml-in-quilt logs and the report hash no longer match. The selftest `report_hash` moved from
`0xb1f485ee166a8e53` to `0x0f8f32c90426f98a`. No pass/fail check changed. The old value is quoted in
`situations/dispatch-ledger.csv` row d155 as history, and that row was not edited.

## 7. How it composes
- **B1** `labs/activeledger`: envelope, budget vector, chain.
- **B7** `labs/system2-backtest`: `backtest_pair`, `backtest_corpus`, `replay_route`, used
  unmodified. Route metadata goes under `chosen`, which B7 excludes from the product.
- **B4** `labs/route-preference`: `prefer`, `prefer_axes`, `PreferenceBook`.
- `labs/code-real-quant`: the q4 centroids, pack/unpack and fnv1a.
- `labs/activeledger/at_rest.py`: `rs_wrap`/`rs_unwrap` for weights, and `pack`/`unpack` (ALR1+RS)
  for activation logs.
- `labs/situation-memory`: `MissionEmbedder.embed_text` as the lexical situation encoder.

## 8. Where to look next
- [`situations/arch/ML-IN-QUILT-ARCHITECTURE.md`](../../situations/arch/ML-IN-QUILT-ARCHITECTURE.md):
  the full design, what's hard, and the next iterations.
- [`labs/system2-backtest/README.md`](../system2-backtest/README.md): the gate this lab bends around.
- [`situations/arch/ENCODING-GEMS-STUDY.md`](../../situations/arch/ENCODING-GEMS-STUDY.md): the
  at-rest formats and the hot-memory blind spot.
