# Quilt latent tools: ML and intelligence tools already implied by the paradigm

*A design-and-measure mark (2026-09-30), branch `claude/quilt-latent`. Mission: find the tools that
are latent in quilt but not yet built. The ingredients are cells, budget vectors, hash-chained
receipts, differ-gated product identity, System-2 route pricing, quantum-drawn randomness and the
situation corpus. Build the best two with receipts and measured numbers, and name an extraction
target for each. Every number below comes from a run in this branch. Anything unbuilt is marked
**SPECULATIVE**.*

**For the owner (one paragraph).** Two new tools work and are measured.
**`labs/audit-lottery`** lets a cheap route serve traffic while unpredictable spot-checks keep it
honest, and revokes it on evidence. Its big finding: *seeded, replayable dice give no protection at
all.* A strategic route that knows the seed serves 93.8% wrong answers and is never caught; with
secret draws the same strategy is caught every time and serves 1.3% wrong. **`labs/invariance-miner`**
reads a cell's own receipts to discover which input changes don't change the answer, and turns them
into cache keys: 36× fewer calls on the text cell, zero wrong answers. Along the way it showed that
"verify on a sample" cannot catch a shortcut that is only wrong off the sample. A simple Occam rule
catches it.

**For the next agent (one paragraph).** Both labs are Python stdlib only and import the example
quilts unmodified (`labs/examples/text-normalize-quilt`, `convert-quilt`) and `labs/activeledger`'s
fnv1a-64. The selftests are `audit-lottery selftest: 33 checks, 0 failures` and
`invariance-miner selftest: 25 checks, 0 failures`. Full reports are in `labs/*/report.txt`. One live
Moth call (comet-qrng-v1, `emu/aer`, S=2.80, 125 conditioned bytes) is frozen in
`labs/audit-lottery/moth_draws.json` along with its pre-outcome commitment. Nothing in B4, B7 or the
corpus was modified.

## What already existed (so we don't duplicate it)

The in-repo labs are situation-recorder, situation-memory, B7 system2-backtest, B4 route-preference,
code-real-quant, rubric-forge, activeledger and at_rest, encoding-experiments, ml-in-quilt and
polyform. The sibling repos, read through raw README fetches, are **cellgraph** (digest-perturbation
localization), **quilt-nn** (training as cells), **quilt-ewitness** (anytime-valid e-process
witnesses with retraction) and **forge-quilt** (the kernel as an OpenAPI spec). Seed (b) in the brief,
the self-witnessing cell, is essentially quilt-ewitness. Seed (d), the receipt interpretability probe,
is essentially cellgraph's localization control. So both were pushed *past*, not rebuilt.

## Step 1: the candidate landscape (8)

| # | tool (one line) | why it's a breakthrough | use | status |
|---|---|---|---|---|
| 1 | **audit-lottery**: COMMIT → unpredictable DRAW → differ AUDIT → e-process LICENSE for any cheap route | A *certified cascade*: the protocol order, recorded in the receipt chain, proves the route could not have answered carefully only when watched, and Ville bounds false revocation. It fuses four quilt primitives that no lab had combined. | general | **BUILT, 33/0** |
| 2 | **invariance-miner**: receipts read backwards give the program's symmetries, which become differ-guarded canonical cache keys | The audit trail doubles as a free symmetry dataset, and mining costs 0 calls. The Occam guard ("adopt only what the receipts pay for") fixes a failure that sampling-based verification cannot. | general | **BUILT, 25/0** |
| 3 | **sealed-eval**: commit the model or route output first, *then* draw the held-out split from a secret-at-commit-time source | This transfers finding 1 directly. Benchmarks are gamed exactly the way public-seed audits are. A commit-then-draw eval makes test-set overfitting detectable by construction. | general | SPECULATIVE (derived from a measured result) |
| 4 | **trust-credit detector**: a Shiryaev–Roberts e-detector alongside Ville e-processes for *keeping* a license, not only granting it | Measured here: a Ville license drains its wealth on clean audits. After 16 000 honest items it misses 98% of a later 20% drift, while SR catches every one at about 360 items. That vulnerability applies to quilt-ewitness and to B4's Hebbian `PreferenceBook` standing. | general | **measured inside #1**. The ports to ewitness and B4 are SPECULATIVE. |
| 5 | **certified augmentation**: mined invariances (from #2) used as *product-certified* data augmentations for distilling a student cell | This is seed (f), made concrete: an augmentation is safe only if the differ says the teacher's product is invariant. #2 produces exactly that list, with receipts. | general | SPECULATIVE |
| 6 | **B4-as-MoE router**: experts are cells, and the router is B4's Pareto frontier plus `preferred_when` per situation, priced on the iron triangle | Seed (a). The router's decisions would be receipted and priced rather than a learned softmax. However, `ml-in-quilt` already ships gated, speculative and trust routes over block implementations, so the marginal novelty is per-situation *expert* selection. | specific (ml-in-quilt) | SPECULATIVE |
| 7 | **digest-bisect**: cellgraph's perturbation localization generalized to any receipted pipeline (bisect the first diverging digest between a good run and a bad run) | Seed (d), pushed from "which transformer cell" to "which step of *any* quilt route". It is `git bisect` over receipts rather than commits. | general | SPECULATIVE (cellgraph proves the mechanism) |
| 8 | **corpus→curriculum**: mine the situation corpus plus the base rate into an ordered curriculum of decomposition tasks | Seed (c), aimed at the "learn to decompose" goal. | specific | **honest negative for now**: see below |

Rejected seed (e), **quantum-seeded NAS**. The analysis follows from finding 1. Quantum draws are
worth paying for only when some party *benefits from predicting them*. A NAS optimizer is not
adversarial toward its own mutation stream, so a QRNG adds nothing measurable over a PRNG there. The
un-gameable draw belongs where a party can game it: evaluation (#3) and audits (#1).

## Step 2: what we built and measured

### `labs/audit-lottery` (certified cascade)

The product pair is real: the text-normalize example's FULL unicode route versus a plausible "lazy"
shortcut (`lower` plus `split`, with no NFKC or casefold). The two are identical on ASCII. Once
unicode arrives, the lazy route disagrees on a measured **0.201** of items.

| result | number |
|---|---|
| honest drift (p=1/16, R=200) | revoked in 100% of runs, 0 before onset. 96.7 wrong products served vs 401.7 with no audit (**4.2× less**). Cost 6311 vs 9000 always-exact. |
| strategic route, **public-seed** draws | **0%** revoked, **93.8%** of outputs wrong, E_max=1 |
| strategic route, **secret** draws (20% blind cheating) | **100%** revoked, **1.3%** wrong |
| Ville validity at q=ε=0.01 (R=1000, 2000 audits) | false revocation **0.020** ≤ δ=0.05 |
| trust credit, Ville | detection delay 165 / 491 / 1302 items after 0 / 1k / 4k honest items; **misses 98%** after 16k |
| trust credit, Shiryaev–Roberts (A=40000) | detection delay 345–367 at every history length, 0 early false alarms, 1.0% false alarms within 2000 audits at q=ε |
| receipts | an in-place edit breaks the chain. An answer swapped after the draw keeps a **valid** chain, and only the COMMIT/AUDIT consistency check catches it. |
| live Moth QRNG pool | a blind cheater was revoked at item 6. Chain and order checks ok. |

**Findings.** (1) "Un-gameable" means *unpredictable to the audited party at commit time*. A seeded
MicroMoth circuit is exactly as gameable as a published PRNG seed: replayability is a virtue for
receipts and a vice for audits. (2) Long honesty buys cover under a Ville license, so use Ville to
grant and SR to keep watching. (3) Hash chains prove integrity, not honesty. The protocol order is
what proves honesty.

### `labs/invariance-miner` (receipts → symmetries → cache keys)

Traffic is 600 mining receipts and then 3000 served requests under **shifted** traffic, over 20 seeds.

| cell | exact key calls | guarded calls | guarded hit rate | guarded false hits | log-only false hits |
|---|---|---|---|---|---|
| text-normalize/full | 717.2 | **20.0** | 0.993 (vs 0.761) | **0** | 90.8 |
| convert/full | 54.0 | **11.0** | 0.996 (vs 0.982) | **0** | 241.95 |

Mining spent **0** cell calls. The real invariances it found are `casefold`, `collapse_ws`, `strip`,
`canon_number` and `strip_plus`.

**Honest negative, and the fix.** On convert, the trap `round3` passes *every* active differ check
drawn from the log, because no logged value has more than 3 decimal places. As a result, the
active-verified canonicalizer serves 241.95 wrong products per run, the same as log-only. More
samples from the same distribution cannot help. The **Occam marginal-merge guard** removes it in
20/20 runs: adopt a transform only if it merges ≥3 more logged inputs than the chain already does.
The rule is: *never adopt a symmetry the receipts don't pay for.*

## Honest negatives (booked, not hidden)

- **corpus→curriculum (#8) is premature.** Rebuilding the corpus (`labs/situation-recorder/run_all.sh`)
  gives **7** FOLD decompositions, 163 routes and 5 judgments. The transparent lexical baseline
  localizes the weakest leaf at **0.14** top-1, below the **0.25** random base rate (0/5 on
  factual-error folds). A curriculum mined from 7 examples would be a toy. The honest move is to let
  live folds accumulate, and meanwhile treat the 5 example quilts' "is the cheap route identical here?"
  decisions as a synthetic curriculum. That cuts the other way from #2: invariance-miner produces
  exactly those labelled decisions.
- **The live QRNG is `emu`.** The Moth bytes came from an Aer simulator behind a pre-outcome
  commitment. The big runs used the OS CSPRNG as the secret source. Neither is hardware-certified
  randomness, and finding 1 does not need it to be. It needs *secrecy at commit time*.
- **Cost models are the example quilts' deterministic `wall_ms`, not measured timings.**
- **Both tools verify on the traffic's support.** 0 false hits holds on *this* traffic. The two tools
  compose: the audit-lottery should keep auditing an invariance-cache in production.

## Ranked extraction backlog

| rank | repo | use | state | first step |
|---|---|---|---|---|
| 1 | **`quilt-audit-lottery`** | general (LLM cascades, cached or quantized inference, third-party APIs) | built, 33/0 | lift `audit_lottery.py`, take the differ as a callable, add a live Moth draw adapter with the pre-outcome commitment |
| 2 | **`quilt-invariance-cache`** | general (API gateways, prompt caches, build caches, feature stores) | built, 25/0 | lift the miner, add a transform DSL so transforms are *searched*, not hand-listed |
| 3 | **`quilt-sealed-eval`** | general (benchmarks, bake-offs, contractor acceptance tests) | speculative | commit-then-draw held-out split. The first experiment mirrors #1's public-seed vs secret contrast on a benchmark-overfitting adversary. |
| 4 | **SR lane in `quilt-ewitness`** | general | measured here, port pending | contribute `SRDetector` plus the trust-credit experiment upstream |
| 5 | **B4 standing demotion** (`labs/route-preference`) | specific | speculative | test whether `PreferenceBook`'s Hebbian standing shows the same trust credit |
| 6 | **`quilt-certified-augment`** | general | speculative | feed #2's guarded invariances into a quilt-nn student as augmentations and measure the gain |
| 7 | **`quilt-digest-bisect`** | general | speculative (mechanism proven by cellgraph) | bisect the first diverging digest across two activeledger runs |
| 8 | **`quilt-moe-router`** | specific (ml-in-quilt) | speculative | B4 frontier as the expert gate over ml-in-quilt block implementations |
| 9 | **corpus curriculum** | specific | blocked on corpus volume (N=7 folds) | revisit when live folds exceed the base rate by a margin |

## Reproduce

```
python3 labs/audit-lottery/selftest.py        # 33/0 (~20 s)
python3 labs/audit-lottery/audit_lottery.py   # full report (~5 min); --fast for ~1 min
python3 labs/invariance-miner/selftest.py     # 25/0
python3 labs/invariance-miner/invariance_miner.py
```
