# priced-training — can a training step be priced like a forward route, or only bounded?

*A `labs/` cell. Python stdlib only, offline, deterministic. The runnable half of
[`situations/arch/PRICED-TRAINING.md`](../../situations/arch/PRICED-TRAINING.md).*

## 1. In one breath
This lab trains a tiny network with seven interchangeable update steps and receipts every epoch.
It then asks System-2 which cheaper steps can be *priced*, meaning certified identical and then
compared on cost, and which can only be *bounded* by a witness that keeps checking and can take its
claim back.

## 2. Why it exists
`xruntime-conformance` found that forward-pass digests agree across runtimes (23/23) but the loss
digest does not. B7 (`system2-backtest`) only prices routes whose products are identical, so a
training step with an unstable loss digest looks unpriceable. The scout note
([FLEET-CONVERGENCE-CELL-NATIVE-ML.md](../../situations/arch/FLEET-CONVERGENCE-CELL-NATIVE-ML.md))
left this open as a question to prototype rather than assert. This lab is that prototype.

## 3. The mental model
```
seed ─▶ LCG ─▶ init ─▶ [ shuffle ─▶ batch grads (fp64) ─▶ Σ over batch ─▶ tick: w ← store(w − lr·ḡ) ] × epochs
                                                            │                    │
                                        order: listed | reversed      store: f64 | f32 | bf16-rn | bf16-sr
                                        sum:  naive  | fsum (correctly rounded)
each epoch ─▶ receipt {loss_sha, w_in, weight_root_sha, prev, sha}  (quilt-nn v2 preimages + dtype tag)
run ─▶ ActiveLog slice (train.step ticks, eval tick, checkpoint tick) ─▶ ledger.transaction(product)
```
- **Route**: one update implementation. `fp64` is the reference. `fp64-rev` reverses the batch
  sum order. `fp32` stores weights as float32. `bf16-rn` and `bf16-sr` store them as bfloat16 with
  nearest or stochastic rounding. `fsum` uses correctly rounded sums, and `fsum-rev` is `fsum` with
  the reversed order. Init, shuffle, data and forward/backward arithmetic are shared by all routes,
  so only the update step differs.
- **Product level**: what B7 must see identical before it compares cost.
  - `step`: the whole trajectory digest (every epoch's loss digest and weight root) plus the final weights.
  - `preds`: the exact float64 predictions on 256 held-out points.
  - `labels`: the classifier's decisions on those points.
- **Witness** (`route_witness.py`): an anytime-valid betting e-process for H0 "the cheap route
  misses tolerance EPS on ≥ p0 of cases". It is live only while E ≥ 1/δ and retracts when evidence
  decays. p0, δ and EPS are fixed in `prereg.py`, which was committed before any run (`git log
  prereg.py`).

## 4. Walkthrough
```
$ cd labs/priced-training && python3 priced_training.py      # ~2.5 min; full output in REPORT.txt
$ python3 selftest.py                                          # priced-training selftest: 80 checks, 0 failures
```
The verdict lines, with 40 seeds per route on both tasks (all numbers measured; see REPORT.txt):

| route (vs ref) | step identical | sine: max \|Δf\| / verdict | circle: labels certified / verdict |
|---|---|---|---|
| fp64-rev (vs fp64) | 0/40 (diverges in epoch 0) | 1.8e-15 · **bounded** | 40/40 · **priceable at labels** (equivalent) |
| fp32 (vs fp64) | 0/40 | 7.6e-7 · **bounded** | 40/40 · **priceable at labels**, dominates fp64 faster-cheaper |
| bf16-sr (vs fp64) | 0/40 | 6.5e-2, only 24/40 seeds within EPS · **flagged** | 6/40 · priceable where certified, **route flagged** |
| bf16-rn (vs fp64) | 0/40 | 6.5e-2, only 24/40 seeds within EPS · **flagged** | 4/40 · priceable where certified, **route flagged** |
| **fsum-rev (vs fsum)** | **40/40, every epoch, byte-identical** | 0 · **priceable at the step** | 40/40 · priceable at the step |

On the witness side, fp64-rev, fp32 and fsum-rev are WITNESSED within EPS=0.02 at the route level
(40/40 clean runs; anytime upper bound on the miss rate 0.10) and per function (2048 streamed points
each; upper bound 0.0022). bf16 is NOT witnessed on either task, under either the identity relation
or the quality relation. In the retraction control, a route that ran clean for 40 runs and then
switched to bf16-sr went from WITNESSED to **RETRACTED** (E fell from 20.4 to 8e-6).

## 5. The contract
- `nettrain.train(task, impl, seed)` returns weights, a per-epoch receipt chain, and the swallowed-update share.
  `verify_chain` recomputes every link and loss commitment.
- `nettrain.to_activelog(run, level, xs, device)` produces an ActiveLog v1 slice. B7's
  `replay_route` accepts it unmodified.
- `route_witness.witness(xs, p0, delta)` returns `WITNESSED`, `NOT_WITNESSED` or `RETRACTED`, plus
  `stop_t`, `E`, `upper_bound(xs, delta)` and `clean_needed(p0, delta)`. It refuses to run without p0 and δ.
- The receipt is `python3 selftest.py` → `priced-training selftest: 80 checks, 0 failures`.

## 6. Failure modes / scars
- **The chain tip never matches across routes.** The receipt carries `impl`, so the tip differs by
  design. The `step` product uses `step_trace`, which is label-free. The first fsum comparison
  "failed" on this until we compared the right field.
- **fsum makes the step order-invariant but does not make it runtime-invariant.** It removes
  reduction-order divergence only. `tanh` and `exp` come from the platform libm, which is not
  correctly rounded across platforms. Cross-runtime identity would also need a correctly rounded
  libm. **Not tested: this lab ran on one substrate.**
- **The canon is a choice.** fsum's trajectory never equals plain fp64's (0/40). Pricing a step
  means choosing fsum as the reference, not certifying fsum against legacy fp64 (B7 refuses that pair).
- **bf16-rn did not stall here.** At these learning rates the update is usually larger than half an
  ulp. Both bf16 routes swallow 16–20% of updates, and SR does not prevent this per step. Both
  still train (final loss within 5% of fp64), but they learn *different* functions.
- **B4 labels two identically priced routes "trade-off"** (fsum vs fsum-rev: frontier of both).
  That is a naming scar in B4, not a real trade-off.
- **B4 over all five routes on circle has only 1 seed** where every route is certified, which is
  too thin to read.
- The cost model is declared (the rooflines from `labs/ml-in-quilt`), not measured. In Python, the
  cheap routes are *slower* (bf16 emulation). See the python-wall sidecar in REPORT.txt.

## 7. How it composes
- It mirrors quilt-nn's training cells and receipts (LCG init and shuffle, `f64|8|hex` preimages,
  sha256 chain) and cellgraph's dtype-in-digest rule.
- It emits B1 ActiveLog records that B7 `backtest_pair` and B4 `prefer`/`prefer_axes` consume
  unmodified.
- `route_witness.py` borrows quilt-ewitness's Ville honesty and retraction rule, with a
  betting construction for miss rates in place of Gaussian increments.

## 8. Where to look next
- [`situations/arch/PRICED-TRAINING.md`](../../situations/arch/PRICED-TRAINING.md): the verdict and the extraction note.
- [`labs/ml-in-quilt`](../ml-in-quilt/): the forward pass priced at the token (the sibling question).
- [`labs/system2-backtest`](../system2-backtest/) and [`labs/route-preference`](../route-preference/): the gate and the frontier used here.
