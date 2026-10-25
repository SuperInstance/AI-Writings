# EDGES AS CHANNELS: NQ-C2 — Are Inter-Cluster Synapses Stronger Than Intra-Cluster Ones?

**NQ-C lane, second shore-spike. Casey nodded: go (2026-09-03).**
Spawned directly from NQ-C1's corpse (CONNECTOME-QUILT-RESEARCH.md §7.3, finding #1): the worm's escape reflex executes *across* cluster boundaries through strong convergent edges — PVC lives in the command module, its strongest targets (DB-class motor neurons) live in the cord module. That was an observation from one dead partition. This spike asks whether it is *systematic*.

**Verdict up front: FAIL, as pre-registered — and the worm answered with the *opposite* gradient.** Inter-cluster synapses are not heavier than intra-cluster ones; they are *lighter* — median 1 vs median 2 synapses (R = 0.500), rank-biserial −0.310, and the reverse direction (intra ≥ inter) posts permutation p = 0.0001, the strongest statement 10,000 shuffles can make. All 20/20 bootstrap re-clusterings agree; the effect survives hub exclusion; and every one of the 12 heaviest directed connections in the animal (VB03→DD02 at 37 synapses on down) is *intra*-cluster. The pre-registered gates for "edges are channels" (inter median ≥ 2× intra, p < 0.001) were never in reach: p came out **1.000** in the hypothesis direction. As pre-booked in §4: **the connectome thread closes with two kills, which is still a result.** NQ-C1 killed partitions-as-law; NQ-C2 kills boundaries-as-heavy-wire. The one honest post-hoc nuance the corpse keeps: boundaries are *numerically* busy (43.5% of all directed chemical pairs cross one) but featherweight — the worm spends its heavy wire *inside* clusters, on locomotor crossover giants like VB→DD, and keeps boundary crossings cheap. Boundaries are many thin doors, not few thick gates.

Pre-registration discipline note: §1–§4 below are unchanged from the pre-registration commit `bd89fd14`, which precedes the run (verified: pushed before the spike executed — see git history). Results were appended after, in the second commit. One execution scar is booked honestly in §5.1: the *first* run of the script contained a label-alignment bug that produced a spuriously perfect null; the post-hoc cross-check caught it (same-cluster pairs printing as INTER), the fix is one alignment line, the corrected run is the one booked here, and the buggy receipt is preserved for the record. Reading your own receipts is load-bearing — the bug produced the most plausible-looking FAIL imaginable.

**Why this question survives the NQ-C1 kill:** the C1 kill murdered *partition stability* (cluster identity as byte-exact law). It did not touch the edge-weight question. "Are boundary-crossing synapses systematically heavier?" is a statistic on the raw graph that needs only *a* partition, not a stable one — and it is exactly the quilt thesis wearing measurable clothes: **if boundaries are where the truth lives, the truth should be carried by heavier wire.** The elephant question (§4 of the C1 doc — boundary-edge surprise) inherits whatever this spike finds.

**Pre-registered circularity disclosure (booked before the run, because it cuts):** Louvain maximizes modularity, which *rewards* placing heavy edges inside communities. The construction bias therefore inflates intra-cluster weights. Our hypothesis runs *against* the grain of that bias: if inter-cluster edges still come out stronger, the result overcame the algorithm's own preference and is meaningful. Conversely, a FAIL is partly expected from construction alone and will be booked with that caveat — it will NOT be booked as "boundaries don't matter," only as "under modularity partitions, edges do not lean outward." Both directions of the asymmetry are stated now, before the data.

---

## 1. Provenance Chain (locked before run)

| Link | Value | Status |
|---|---|---|
| Raw source | WormAtlas `NeuronConnect.xls` (White et al. hermaphrodite, somatic) | cached from NQ-C1, **no re-download** |
| Raw file | `/tmp/NeuronConnect.xls`, 518,144 bytes | ✅ present |
| sha256 | `120c2c6332050a2d1494c19c687f447ed65620ad0db5f8b732189aa10e5162f1` | ✅ verified this session, matches NQ-C1's booked hash |
| Ingest | identical to `docs/nq_c1_spike.py` (xlrd; UA-header fetch only if cache hash ever fails) | reused verbatim |
| Partition | **NQ-C1's τ=3 partition**: Louvain on symmetrized `max(w_ij,w_ji)` chemical pairs with `w≥3`, plus EJ gap pairs as weight-1 undirected edges; `networkx.community.louvain_communities(weight='weight', seed=42, resolution=1.0)` | rebuilt deterministically; **must reproduce the cluster sets in `/tmp/nq_c1_constraint_table.json` exactly or the run aborts** (provenance check is load-bearing) |
| Partition fragility | **booked: this partition is seed-dependent** (C1 §7.1: seed-ARI min 0.522, mean 0.715 at fixed τ) | that is why §3.4 exists |
| Node universe | the 277 neurons surviving τ=3 pruning | edges touching the other 25 neurons have no cluster home and are excluded entirely — booked |

The partition is a *lens*, not a law (C1 killed the law version). Every statistic below is therefore run through the lens, then through 20 fresh lenses (§3.4) to bound how much of the answer is the lens.

## 2. The Statistic (locked before run)

**Edge universe (primary):** every directed chemical pair (u, v) from the raw XLS — types S/Sp summed per ordered pair, u ≠ v — where both endpoints sit in the 277-node partition. Weight = summed synapse count, all weights ≥ 1 (weak edges the clustering never saw are included on purpose; the sensitivity run in §3.3 covers the alternative).

**Classification:** pair is *inter* if `P[u] ≠ P[v]`, *intra* otherwise.

**Reported numbers:**
- `m_inter`, `m_intra` (medians; synapse counts are small integers, medians are the honest center), and the primary effect **R = m_inter / m_intra**.
- Mann-Whitney U, one-sided (`inter > intra`), scipy asymptotic with tie correction; rank-biserial correlation `2U/(n₁n₂) − 1` as the distributional effect size.
- **Permutation p:** 10,000 shuffles of the cluster-label vector across the 277 nodes (cluster sizes preserved — the null is "this partition's sizes, randomly assigned"), statistic `T = m_inter − m_intra`, one-sided `p = (1 + #{T_perm ≥ T_obs}) / 10001`. RNG booked: `numpy.random.default_rng(20260903)`, re-seeded per named sub-run with `+1` increments so every number is replayable.

## 3. Gates and Robustness (locked before run)

### 3.1 Verdict gates on the C1 τ=3 partition (seed 42)

- **PASS:** permutation p < 0.001 **and** R ≥ 2.0 — *inter-cluster synapses are at least twice as heavy: edges are channels.*
- **PARTIAL:** p < 0.001 but R < 2.0 — *edges lean outward, weakly.* Reframe: **gradient, not channel.** Booked in exactly those words if it happens.
- **FAIL:** p ≥ 0.001 — book honestly; the connectome thread closes with two kills, which is still a result.

### 3.2 Hub-blind rerun (a result carried only by AVA-class hubs is a weaker claim)

Exclude the top-5 nodes by degree in the τ=3 build graph (unweighted degree; ties broken by `(-degree, name)` for determinism — names booked at runtime), drop every edge touching them, re-run §2 in full.
- A candidate **PASS** survives only if hub-blind p < 0.001 **and** hub-blind R ≥ 2.0; else downgrade to PARTIAL, annotated *hub-driven*.
- A candidate **PARTIAL** survives only if hub-blind p < 0.001; else downgrade to FAIL.

### 3.3 Sensitivity (reported, non-gating — booked so it can't be quietly dropped)

Re-run §2 on the *clustering-seen* universe only: directed pairs with raw pair weight ≥ 3 (the weak w=1,2 edges the partition never saw are removed). If the primary contrast lives only in the weak-edge regime, this says so. Directional inversion here (R < 1 at p < 0.001) is flagged in the interpretation as evidence the primary effect was weak-edge asymmetry, not strong-wire truth — it annotates, it does not gate.

### 3.4 Bootstrap churn bound (the seed-dependence tax)

20 fresh Louvain re-clusterings of the **same** τ=3 graph, seeds 1–20. Each gets its own R, MWU p, permutation p, and ARI vs the C1 partition. Booked robustness rule: **if ≥ 5 of 20 bootstrap partitions yield R < 1 (direction inversion), the verdict drops one notch** and the finding is booked as *signal-under-lucky-seeds* — per the directive, that outcome IS the finding, not an embarrassment to launder.

### 3.5 Bonus cell — gap junctions (exploratory, clearly separated, NO pass/fail)

Same WormAtlas file, EJ rows, deduped to unordered pairs (frozenset), pair weight = sum of the rows' `Nbr` values; both endpoints in the 277-node partition; identical statistic (R, one-sided MWU, 10k label-shuffle permutation). Framing that rides on it: gap junctions are the worm's wired broadcast. **If gap junctions come out intra-heavy while chemical synapses come out inter-heavy, the C1 doc's story sharpens: chemical edges are channel traffic, electrical edges are cell interior.** If gap junctions also lean inter, the story dampens instead. Either way this cell annotates and never gates. Caveat booked before the run: the τ=3 partition's build graph included weight-1 EJ edges, so the lens already swallowed some gap-junction structure — exploratory means exploratory.

## 4. Interpretation boundaries (locked before run)

- This is one animal, one reconstruction (White/hermaphrodite/somatic), one lens family (modularity at τ=3). Nothing here generalizes to flies, male worms, or developing animals without Witvliet-class replication — which this spike does not attempt.
- Per-edge weight ≠ information flow. Heavier synapse counts mean *more anatomical commitment*, not proven traffic. The channel claim being tested is anatomical: evolution spent more wire on boundary crossings.
- If FAIL: the lane closes with two kills (partition not law; edges not channels) and the honest sentence is *the worm's boundaries are real but its truth is not edge-weighted* — the quilt thesis takes the hit, books it, moves on.

## 5. Run Receipt

- **Pre-registration commit:** `bd89fd14` (pushed before the run; git history is the witness — NQ-C1's results booking `838c688b` also precedes it, keeping both spikes' ordering stories clean).
- **Run:** 2026-09-03, evening shift, this laptop, ~90 s wall clock. Script: `docs/nq_c2_spike.py` (committed with this results commit).
- **Provenance receipts (verbatim):**

```
raw sha256 OK = 120c2c6332050a2d1494c19c687f447ed65620ad0db5f8b732189aa10e5162f1 (matches NQ-C1 booking; no re-download)
tau=3 rebuild: 277 nodes, 1155 edges, 8 clusters (seed=42)
partition reproduces /tmp/nq_c1_constraint_table.json cluster sets EXACTLY — lens verified
cluster sizes: [71, 63, 59, 27, 18, 17, 16, 6]
```

- **Statistic receipts (verbatim):**

```
[PRIMARY all-weights] inter n=949 median=1 | intra n=1231 median=2 | R=0.500 | MWU U=403084 p=1.000e+00 rank-biserial=-0.310 | perm T=-1.0 p=1.00000
[SENSITIVITY w>=3] inter n=183 median=4 | intra n=562 median=5 | R=0.800 | MWU U=34761 p=1.000e+00 rank-biserial=-0.324 | perm T=-1.0 p=0.99850
top-5 hubs (degree, build graph): [('AVAL', 68), ('AVAR', 65), ('AVBR', 49), ('AVBL', 40), ('PVCR', 29)]
[HUB-BLIND minus top-5] inter n=779 median=1 | intra n=1059 median=2 | R=0.500 | MWU U=284392 p=1.000e+00 rank-biserial=-0.311 | perm T=-1.0 p=1.00000
```

Bootstrap churn bound (20 re-clusterings, seeds 1–20 — every single line, verbatim pattern):

```
[BOOT seed=01 ARI=0.74] inter n=991 median=1 | intra n=1189 median=2 | R=0.500 | ... rank-biserial=-0.323 | perm T=-1.0 p=1.00000
[BOOT seed=03 ARI=0.52] inter n=1169 median=1 | intra n=1011 median=3 | R=0.333 | ... rank-biserial=-0.362 | perm T=-2.0 p=1.00000
  (all 20 boots: R ∈ {0.333, 0.500}, rank-biserial −0.302…−0.362, perm p = 1.00000)
bootstrap R: min=0.333 median=0.500 max=0.500 | inversions R<1: 20/20 | perm p<0.001 in 0/20

== VERDICT: FAIL ==
== connectome thread closes with two kills — still a result ==

[BONUS EJ gap junctions] inter n=254 median=2 | intra n=260 median=2 | R=1.000 | MWU U=32802 p=5.625e-01 rank-biserial=-0.007 | perm T=+0.0 p=0.99990
```

(Full untrimmed stdout lives in the run log; the 18 unquoted boot lines are line-for-line identical in shape — ARI 0.52–0.88, R = 0.500 in 19/20, p = 1.00000 throughout.)

### 5.1 Scar — the first run was a beautifully wrong FAIL (booked, not buried)

The script's first execution passed `list(part.values())` — dict insertion order — as the label vector, while edge indices were built against `sorted(part)`. A silently permuted classification: the "observed" inter/intra split *was itself a random draw*, so every cell came back dead flat (medians 2 vs 2, R = 1.000, perm p ≈ 1.000, rank-biserial ≈ 0) — the most convincing null a bug can print. It was caught not by a test but by a post-hoc cross-check printing cluster names next to classifications: `VB03 -> DD02 INTER (C3|C3)` — same cluster, impossible label. Fix: one alignment function (`labvec`), no gate, threshold, or statistic touched — §1–§4 are byte-identical across both runs. Corrected run = the booked run. Buggy receipt preserved at `/tmp/nq_c2_receipt.txt` (and in this paragraph's existence). Lesson, worth the ink: **a perfectly clean null from real messy data is a smell, not a result** — the correct run, like the truth, has texture (R = 0.500, not 1.000).

## 6. Results — What the Worm Actually Said

### 6.1 The pre-registered question: answered NO, with the gradient pointing the other way

| Cell (pre-registered) | inter median | intra median | R | rank-biserial | perm p (inter>intra) |
|---|---|---|---|---|---|
| PRIMARY, all weights | 1 (n=949) | 2 (n=1231) | **0.500** | −0.310 | 1.000 |
| SENSITIVITY, w ≥ 3 | 4 (n=183) | 5 (n=562) | 0.800 | −0.324 | 0.999 |
| HUB-BLIND (−AVAL/R, AVB/L/R, PVCR) | 1 (n=779) | 2 (n=1059) | 0.500 | −0.311 | 1.000 |
| BOOTSTRAP 20× (seeds 1–20) | 1 | 2–3 | 0.333–0.500 | −0.30…−0.36 | 1.000 (all) |

Gates (§3.1): perm p < 0.001 in the hypothesis direction was required for PASS or PARTIAL; the run returned **p = 1.000**. Not PARTIAL ("edges lean outward, weakly") — edges lean *inward*, at every robustness cell the design owned. Downgrade rules never even engaged; FAIL is the floor. **Booked FAIL.**

The pre-registered circularity disclosure (§ preamble) predicted this direction as the construction-bias outcome: Louvain's modularity objective rewards placing heavy edges inside communities, and the data obliges — this FAIL was booked *in advance* as partly-expected-from-construction, and is therefore booked now as "under modularity partitions, edges do not lean outward," **not** as "boundaries don't matter." The two confounds (construction bias, τ=3 lens) are exactly why §3.4 existed — and even across 20 fresh lenses (ARI 0.52–0.88 vs the C1 partition), not one run moved the direction.

### 6.2 POST-HOC cells (not pre-registered, never gate — labeled as such)

1. **Means, same direction:** inter mean 1.90 vs intra mean 3.71 synapses — the inward lean is not a median artifact.
2. **Reverse-direction permutation p (intra ≥ inter): 0.0001** — the floor of what 10,000 shuffles can express. The worm's per-edge weights *do* separate by cluster side; they just separate the wrong way for the channels thesis.
3. **The heaviest wire in the animal is interior wire.** All 12 heaviest directed pairs are intra-cluster: `VB03→DD02 (37)`, `PDER→DVA (35)`, `VB06→DD04 (30)`, `VB08→DD05 (30)`, `VB05→DD03 (27)`, `DB03→VD05 (26)`, `DA03→VD03 (25)`, `VA06→DD03 (24)`, `PDEL→DVA (24)`, `DB02→VD03 (23)`, `OLLL→AVER (21)`, `VA04→DD02 (21)`. This is locomotor architecture — the A/B-class excitors driving the D-class inhibitory crossovers that switch body-bend direction — and evolution built it as *dense local machinery inside modules*. The C1 corpse's famous boundary edges (PVC→DB-class, ~10–15 synapses) are real but mid-table: the escape reflex's cross-boundary wiring is heavy *for a boundary*, not heavy for the worm.
4. **Boundaries are numerically busy:** 949 of 2,180 directed pairs (43.5%) cross a cluster boundary — but at median weight 1. Many thin doors, no thick gates.

### 6.3 Bonus cell — gap junctions (exploratory, never gated): flat on weight, rich on density

Weights: dead flat (inter median 2, intra median 2, R = 1.000, rank-biserial −0.007, perm p = 0.9999 in the greater direction). The "wired broadcast" does not buy heavier electrical coupling across boundaries — or within them. But the post-hoc density count: **260 of 514 gap-junction pairs (50.6%) are intra-cluster vs ~18% expected under random labels** — gap junctions concentrate inside modules, twice the random rate. Caveat (booked in §3.5 *before* the run): EJ edges were in the lens's build graph at weight 1, so some of that concentration is construction. What the bonus cell honestly says: the "chemical = channel traffic, electrical = cell interior" story survives only in its density half and dies in its weight half — the worm's electrical interior is *more connected within* modules but not *more strongly coupled* per junction, and its chemical traffic is not channel-shaped at all.

### 6.4 What closes, what survives

- **CLOSED: the connectome→quilt lane, two kills deep.** NQ-C1: partitions aren't stable enough to be law. NQ-C2: boundaries don't carry heavier wire. Together they close the specific thesis that the worm's modular decomposition is a *channel architecture* — boundaries as the thick, meaningful interfaces of quilt doctrine. The honest sentence pre-registered in §4 stands: *the worm's boundaries are real but its truth is not edge-weighted.*
- **SURVIVES: the ingest + provenance discipline** (both spikes replayable, hash-verified, lens-verified — §5's reproduction check is the template); **the C1 command-module finding** (AVM→PVC/AVB/AVA co-clustering was correct anatomy); and one genuinely new, pre-registration-clean negative: **the worm's strongest wiring is local recurrent motor machinery, and its inter-module signaling is done with many cheap synapses, not few expensive ones.** If that pattern generalizes (fly, male worm, Witvliet developmental series), it is a real constraint on any graph→agent decomposition, not just ours: *decompose where the wire is thick, and expect the interfaces to be the thin part.*
- **If anyone ever reopens this lane** (not recommended without new data): the entry fee is now higher — Witvliet's 8 developmental connectomes as the stability instrument *and* a construction-bias-corrected statistic (e.g., configuration-model nulls rather than label shuffles) before any channel claim gets words put in its mouth.

## 7. Receipt

- [x] Pre-registration §1–§4 committed and pushed BEFORE the run (`bd89fd14`; NQ-C1's own results booking `838c688b` precedes it)
- [x] Raw provenance hash-verified against NQ-C1's booking — no re-download (receipt verbatim in §5)
- [x] Partition lens reproduced byte-exactly vs C1's cached constraint table — run aborts on mismatch (it didn't)
- [x] All four pre-registered cells executed: primary, sensitivity, hub-blind, 20-bootstrap — plus the EJ bonus, kept exploratory and ungated
- [x] Verdict booked exactly per §3.1 gates: **FAIL** (p = 1.000 in hypothesis direction; effect points opposite, R = 0.500)
- [x] Post-hoc cells labeled POST-HOC and quarantined from the gates (§6.2, §6.3)
- [x] First-run label-alignment bug booked as scar, not buried (§5.1); corrected run is the booked run
- [x] Lane closes with two kills, honestly: partitions not law (NQ-C1), boundaries not channels (NQ-C2)
