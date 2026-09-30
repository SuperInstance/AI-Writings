# Priced training — which training steps System-2 can price, and which it can only bound

*Architecture mark, 2026-09-30. This answers the open question from
[FLEET-CONVERGENCE-CELL-NATIVE-ML.md](FLEET-CONVERGENCE-CELL-NATIVE-ML.md): **can a training step be
made product-identical enough to be priced like a forward route, or only bounded?** The runnable half
is [`labs/priced-training/`](../../labs/priced-training/), whose selftest reports 80 checks and 0
failures. Every number here comes from that lab (full output in `labs/priced-training/REPORT.txt`)
unless it is marked **(speculative)**. The tolerances and nulls were committed in `prereg.py` before
the first run. A second relation (quality) was registered in a separate commit before it was run.
The doc follows the dual-audience standard in
[`situations/blueprints/README.md`](../blueprints/README.md).*

---

## 1. In one breath

**Only a canonical step can be priced.** A training step can be priced exactly when every reduction
in it is correctly rounded (fsum). That makes its whole trajectory byte-identical under
reordering. Every other cheaper step either produces the same *decisions* (priceable at the product
boundary) or is only *bounded* by an anytime-valid witness that can retract. bf16 is neither.

## 2. Why it exists

- **The problem.** The forward pass can be priced because its product, the token, is exact
  ([ML-IN-QUILT-ARCHITECTURE.md](ML-IN-QUILT-ARCHITECTURE.md) §3.3). Training has no obvious
  exact product. xruntime-conformance saw the loss digest disagree across runtimes while 23/23
  forward digests agreed. B7's first law is *never price a cheaper different answer*, so an
  unstable loss digest seems to put every cheaper optimizer step (lower precision, fused,
  reordered, distributed) beyond pricing.
- **Before this.** "fp32 / bf16 / stochastic rounding trains just as well" was an assertion. No gate
  said *how* well, and no bound said how often it fails.
- **What we studied.**
  - **quilt-nn**, for the training cells and receipts. We mirrored its LCG init and shuffle, its
    `f64|8|hex` scalar preimages and its per-epoch sha256 chain. Cited, not merged.
  - **quilt-attention**, for backprop cells, receipt format v2 and the dtype-in-preimage rule.
  - **cellgraph**, whose float32 hashing scar is why dtype goes into the digest.
  - **quilt-ewitness**, for anytime-valid honesty. We took its Ville bar, its retraction rule and
    its refusal to run without pre-registered parameters. Its README was fetched read-only.
  - **xruntime-conformance**: `raw.githubusercontent.com` returned 404 on `main` and `master`, so
    only the scout's summary of it was available.

## 3. The mental model

### 3.1 The nouns

- **Update route.** One implementation of the `tick` cell (`w ← w − lr·ḡ`). There are seven:
  - `fp64`: the reference.
  - `fp64-rev`: the batch sum in reversed order.
  - `fp32`: float32 weight storage.
  - `bf16-rn`: bfloat16 storage, round to nearest.
  - `bf16-sr`: bfloat16 storage, stochastic rounding.
  - `fsum`: the batch sum and the loss sum are correctly rounded (`math.fsum`, Shewchuk).
  - `fsum-rev`: fsum with the reversed order.

  All routes share init, shuffle, data and the forward/backward arithmetic, so only the step differs.
- **Product ladder.** What B7 must see identical, from strongest to weakest:
  1. `step`: the full trajectory, every epoch's loss digest and weight root.
  2. `preds`: exact held-out float predictions.
  3. `labels`: held-out decisions (classifier only).
- **Two relations, never merged.**
  - *Identity* is B7's gate at some level of the ladder.
  - *Tolerance/quality* is explicit and pre-registered: |Δf| ≤ EPS = 0.02 per point, and accuracy
    drop ≤ 0.01 or MSE ratio ≤ 1.10 per seed. It may *bound* a route, but it never certifies one.
- **Witness.** A betting e-process for H0 "misses on ≥ p0". It runs at two grains: per function
  over streamed held-out points (p0 = 1%), and per route over independent seeds (p0 = 10%). The
  claim is live only while E ≥ 1/δ = 20.

### 3.2 Why fsum works and the rest cannot

A float sum depends on its order. The naive batch sum in `fp64-rev` changes the last bit in epoch
0. SGD then carries that bit forward, so no later weight root can match (0/40 seeds). A correctly
rounded sum is a *function of the multiset* of its terms, so its result cannot depend on order.
With every cross-sample reduction made that way, the step becomes a pure function of (weights,
batch-as-set). Its trajectory is then byte-identical under reordering: 40/40 seeds, every epoch,
on both tasks. Lower-precision storage is different in kind. It changes the arithmetic itself
(fp32, bf16), not just the order, so no reduction discipline can make it identical to fp64.

## 4. Walkthrough — what the lab measured

```
$ cd labs/priced-training && python3 selftest.py        # 80 checks, 0 failures, ~2.5 min
$ python3 priced_training.py                             # the report (REPORT.txt)
```

The tasks are `sine` (1-8-1, regression, 25 params, 300 epochs) and `circle` (2-8-1, classifier, 33
params, 200 epochs). Each route runs 40 seeds and is compared against its reference.

**E1: the honest negative, reproduced.**
- `fp64-rev`, `fp32`, `bf16-sr` and `bf16-rn` never share a trajectory with fp64. Weight roots are
  equal 0/40 and trajectories 0/40, with the first divergence in **epoch 0** for every route.
- B7 refuses the `step` product on every seed, on both devices.
- The loss digest alone is a weak witness. On `circle`, `fp64-rev`'s *final* loss digest happened
  to equal fp64's on 4/40 seeds while the weights still differed. This matches cellgraph's
  "the digest can lie by coarseness" scar.

**E1′: the constructive result.**
- `fsum-rev` vs `fsum`: loss digests 40/40, weight roots 40/40, full trajectories 40/40, no divergence epoch.
- B7 certifies the `step` product 40/40 on both devices (class `equivalent`).
- The price of byte-stability is **1.64× declared flops** per step (2,050 vs 1,250 on sine; 2,706
  vs 1,650 on circle). Both declared rooflines are bytes-bound at this size, so the modeled wall
  time is **unchanged** (32.17 ms vs 32.17 ms over 40 circle runs on edge). In Python the cost is
  +14% on sine and +19% on circle (86.9 vs 76.5 ms, 138.3 vs 116.6 ms, best of 3 in REPORT.txt).
  Wall time is a sidecar and varies by roughly 10% between runs; it is never logged.
- fsum's trajectory never equals plain fp64's (0/40). **The canon is a choice**: you adopt fsum as
  the reference. You do not certify it against legacy fp64.

**E2: is the learned function identical even when the step is not?**

| route | sine max \|Δf\| (all seeds) | circle max \|Δf\| | circle label flips (40×256) | circle seeds label-identical |
|---|---|---|---|---|
| fp64-rev | 1.8e-15 | 6.6e-14 | 0 | 40/40 |
| fp32 | 7.6e-7 | 1.3e-4 | 0 | 40/40 |
| bf16-sr | 6.5e-2 (24/40 seeds ≤ EPS) | 7.4e-1 (0/40 ≤ EPS) | 224 | 6/40 |
| bf16-rn | 6.5e-2 (24/40 ≤ EPS) | 4.9e-1 (0/40 ≤ EPS) | 237 | 4/40 |

- Exact float predictions (`preds`) are refused for every non-canonical route. Even 1.8e-15 is not identity.
- Decisions (`labels`) survive where the function error is far below the decision margin: fp32 and
  fp64-rev on 40/40 seeds.
- bf16 learns a *different function* of similar quality:
  - final training loss is within 3% of fp64 (circle 3.75e-2 / 3.83e-2 vs 3.88e-2);
  - held-out accuracy is 0.872 / 0.881 vs 0.875;
  - 16–20% of its updates are swallowed by the storage precision, even with stochastic rounding
    (fp32: 4e-6 to 9e-6).

**E3: the anytime-valid bound.**
- Per function (2048 streamed points, p0 = 1%): fp64-rev, fp32 and fsum-rev are witnessed on
  40/40 seeds. The worst anytime upper bound on the miss rate is **0.0022**. A clean stream needs
  421 points to cross the bar. bf16 is witnessed on 24/40 (sine) and 0/40 (circle).
- Per route (40 seeds, p0 = 10%):
  - fp64-rev, fp32 and fsum-rev are WITNESSED at stop_t = 40 (E = 20.4). The anytime upper bound
    on "a training run produces a function off by > EPS" is **0.10**.
  - This is the *price of evidence*: 40 clean training runs buy "< 10% at 95%", and no fewer can.
  - bf16-sr and bf16-rn are NOT_WITNESSED. They miss on 16/40 seeds (sine) and 40/40 (circle), with E ≈ 5e-3 and 3e-6.
- Quality relation (amendment 1):
  - fp32, fp64-rev and fsum-rev are witnessed (0 seeds failing).
  - bf16-sr fails on 7 seeds (sine) and 8 (circle); bf16-rn on 11 and 5. Neither is witnessed.
  - bf16-rn's circle *mean* accuracy is higher than fp64's. A per-seed bound still refuses it,
    because 5/40 runs drop more than 1 point.
- Retraction control: 40 clean fp32 runs are followed by 40 bf16-sr runs on the same witness. The
  claim is WITNESSED at the switch and **RETRACTED** by the end (E 20.4 → 8e-6).
- Validity control: under exact nulls, the false-witness rate is 0.028 (2000 Bernoulli(0.1)
  streams × 200) and 0.0175 (400 Bernoulli(0.01) streams × 2048), both below δ = 0.05.

**E4: System-2.**
- **B7 on `circle` at `labels`:**
  - fp32 is certified 40/40 and `dominates-faster-cheaper` fp64 on both devices. Over 40 runs it
    costs 16.96 vs 32.17 modeled ms on edge (16.90 vs 32.10 on accel) and 5,280 vs 10,560
    checkpoint bytes.
  - bf16 is certified only on its 6 (sr) or 4 (rn) label-identical seeds. There it also dominates.
- **B4 on `circle`** (fp64, fp32, fp64-rev): frontier `[fp32]` on both devices.
- **B4 on `sine`:** refused. No non-canonical route has an exact product to price.

### The verdict

| update route | at the step | at the learned function | System-2 status |
|---|---|---|---|
| **fsum-rev** (vs canonical fsum) | **identical, 40/40** | identical | **PRICEABLE at the step.** B7-certified trajectory; costs 1.64× flops, free on bytes-bound rooflines |
| fp32 | never | labels identical 40/40; floats within 1.3e-4 | **PRICEABLE at a decision boundary** (dominates fp64). **Only BOUNDED** for regression (upper bound 0.10 per run, 0.0022 per point) |
| fp64-rev (naive reorder) | never | labels identical; floats within 7e-14 | Same as fp32. The fix is to make the reference canonical (fsum), after which it is priceable at the step |
| bf16-sr / bf16-rn | never | a different function of similar quality | **FLAGGED.** Neither identity nor the pre-registered quality relation is witnessed. Priceable only on the minority of seeds B7 certifies, which is not a route-level claim |

**In plain words:** a training step is priceable like a forward route only when it is made canonical
(correctly rounded reductions, on one substrate). Cheaper *precision* is never priceable at the
step. It is priceable where the task has a coarse product boundary (decisions) and the precision
loss stays well inside the margin (fp32). Everywhere else it is **bounded, and only if the witness
says so**. bf16 at this scale is not.

## 5. The contract

**A training route run:**
1. One ActiveLog v1 slice: one `train.step` tick per epoch, one `eval` tick, one `checkpoint` tick
   (storage at rest), and one `ledger.transaction`. `total_budget` equals the sum of tick budgets
   (B7's `replay_route` re-derives it).
2. Every epoch has a receipt `{loss_sha, w_in, weight_root_sha, prev, sha}`. The weight root
   carries the storage dtype in every preimage. `verify_chain` rejects an edited loss or a dropped
   epoch.
3. Product levels are `step` (label-free trajectory digest), `preds` or `labels`. The product must
   never include the route name.

**Pricing a training route:**
1. B7 gates at the strongest level the route can meet. Pricing at `step` needs a canonical reference.
2. A route that fails identity may be *bounded* only by a pre-registered witness (EPS, p0, δ
   committed before the data). The bound is reported as `{state, stop_t, E, upper bound}`. It is
   never passed to B4 as if it were certification.
3. A bounded route stays bounded only while its witness is live. On retraction it drops to flagged.

**Receipt:** `python3 labs/priced-training/selftest.py` → `priced-training selftest: 80 checks, 0 failures`.

## 6. Failure modes / scars

1. **The tip trap.** The receipt chain includes `impl`, so two routes' tips never match. The first
   order-invariance test reported "different" for exactly that reason. Compare the label-free
   `step_trace` instead.
2. **fsum is order-invariant, not substrate-invariant.** `tanh` and `exp` come from the platform
   libm. Cross-runtime identity also needs a correctly rounded libm (CORE-MATH / crlibm-class)
   or transcendental cells built from correctly rounded primitives. **(speculative: one substrate
   was run.)** This is the exact gap between our result and xruntime-conformance's.
3. **GPU reality (speculative).** Atomics and split-K make reduction order nondeterministic, which
   is precisely the order problem fsum removes. At scale, a correctly rounded or fixed-point
   (integer superaccumulator) reduction costs real bandwidth, not only flops. The "free on
   bytes-bound rooflines" result is a property of our declared model and this tiny size.
4. **The loss digest lies by coarseness.** Equal final loss digests on 4/40 seeds did not mean
   equal weights. Never gate training on the loss digest alone.
5. **bf16-rn did not stall.** The textbook stall (Gupta et al. 2015) did not appear at these
   learning rates. What appeared instead was a *different* function of similar quality, which
   identity refuses and quality does not clear per seed. This is the training analog of ML-IN-QUILT's
   "the rat" scar.
6. **The price of evidence is steep.** With p0 = 10%, a witness needs 40 clean independent training
   runs, and one failure costs roughly another 40 (the betting factor 1 − 0.9 on the largest bet).
   At real scale, "bounded across seeds" is a budget line, not a free check.
7. **B4 naming scar.** Two identically priced routes (fsum, fsum-rev) come out as class
   `trade-off` with both on the frontier.
8. **Toy scale.** 25–33 parameters. What transfers is *which comparisons are possible*, not the values.

## 7. How it composes — and the EXTRACTION note

| piece | reusable? | where it should live |
|---|---|---|
| **`route_witness.py`**: an anytime-valid miss-rate witness with retraction, a confidence-sequence upper bound, the price of evidence (`clean_needed`) and a null-validity control. It has no training code | **General tool. Extract it.** It bounds *any* non-identical route: q8/q4 kernels in `ml-in-quilt` (per-token miss vs fp), fused kernels (ML-4), cached or approximate routes in the example quilts, and cross-runtime ports | A sibling to B7, e.g. `labs/route-witness/` (B7b). B7 says *certified or refused*. The witness says *bounded, flagged or retracted* for the refused ones. B4 should display bounded routes separately and never mix them into the certified frontier |
| **The canonical-step discipline**: correctly rounded reductions make a step's trajectory a B7 product | **General rule, small code.** It is one line per reduction (`math.fsum` or a superaccumulator) | A cell contract clause: "a training cell's reductions must be correctly rounded if its trajectory is to be priced". It belongs in quilt-nn / quilt-attention as an optional canonical mode |
| **The product ladder** (`step` → `preds` → `labels`) | General pattern; ML-IN-QUILT uses the same idea at the token | Already in B7 practice. Name it in ACTIVELEDGER-CELL-GRAPH §11 |
| `nettrain.py` (the toy net, bf16 emulation, cost model) | **Specific.** It is a fixture | Stays in the lab |
| `prereg.py` | The *practice* is general; the values are specific | Every witness user commits its own prereg before running |

It composes with:
- B1 (records);
- B7, unmodified (`backtest_pair` at three levels);
- B4, unmodified (`prefer` / `prefer_axes`);
- quilt-nn's receipt format;
- quilt-ewitness's honesty rules.

## 8. Where to look next

- [`labs/priced-training/README.md`](../../labs/priced-training/README.md) and `REPORT.txt`: the lab and the full measured output.
- [ML-IN-QUILT-ARCHITECTURE.md](ML-IN-QUILT-ARCHITECTURE.md) §3.3 and §7.4: the forward-pass
  version of the same question, and the "second relation must be explicit" rule this doc applies.
- [FLEET-CONVERGENCE-CELL-NATIVE-ML.md](FLEET-CONVERGENCE-CELL-NATIVE-ML.md): the siblings
  (quilt-nn, quilt-attention, quilt-ewitness, xruntime-conformance) this answers.

### Next (dependency-ordered)

| # | item | receipt |
|---|---|---|
| PT-1 | Extract `route_witness` to `labs/route-witness/` and run it on ml-in-quilt's q8/q4 per-token misses | q8 bounded or flagged, with an upper bound per device |
| PT-2 | Port `fsum` mode to quilt-nn (Node) and compare `step_trace` across Node and Python | same trajectory digest, or a named libm divergence epoch |
| PT-3 | Correctly rounded `tanh`/`exp` cells (or polynomial cells over correctly rounded ops) | a cross-runtime step certified by B7 |
| PT-4 | Witness-aware B4: show bounded routes beside the certified frontier, never inside it | B4 selftest plus a bounded fp32 sine route displayed, not ranked |

### The spine (five lines)

1. **A training step is priceable only when it is canonical.** With correctly rounded reductions, the trajectory is a product.
2. **Precision changes the function, and order changes only the bits.** fsum fixes order. Nothing fixes precision at the step.
3. **Decisions can survive what floats cannot.** Price at the coarsest honest boundary (labels), where the error sits inside the margin.
4. **Everything else is bounded, not priced.** It needs a pre-registered, anytime-valid witness that retracts.
5. **Evidence has a price.** 40 clean runs buy "< 10% at 95%". Budget for it.
