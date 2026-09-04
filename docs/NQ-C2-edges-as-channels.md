# EDGES AS CHANNELS: NQ-C2 — Are Inter-Cluster Synapses Stronger Than Intra-Cluster Ones?

**NQ-C lane, second shore-spike. Casey nodded: go (2026-09-03).**
Spawned directly from NQ-C1's corpse (CONNECTOME-QUILT-RESEARCH.md §7.3, finding #1): the worm's escape reflex executes *across* cluster boundaries through strong convergent edges — PVC lives in the command module, its strongest targets (DB-class motor neurons) live in the cord module. That was an observation from one dead partition. This spike asks whether it is *systematic*.

**Verdict up front: PRE-REGISTERED — NOT YET RUN.** This document's §1–§4 are the pre-registration, committed **before** the spike runs (commit hash booked in §5 at runtime). Results, receipts, and the verdict get appended only after, in a second commit. Nobody renames the gates after seeing the data — that is the whole house law, and NQ-C1 just demonstrated it by killing its own pipeline on schedule.

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

**RESULTS NOT YET RUN.** This section, §6 (results + verdict), and the verbatim stdout land in the second commit only. Pre-registration commit: booked below at run time.

- pre-registration commit: *(booked post-push — see git log; this line edited only to paste the hash)*
