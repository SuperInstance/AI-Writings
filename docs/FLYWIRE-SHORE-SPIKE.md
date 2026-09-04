# FLY-SHORE-SPIKE — does the worm's quilt pipeline survive a 460× bigger animal?

*2026-09-03 · AI-Writings/docs/FLYWIRE-SHORE-SPIKE.md · Decision spike for the NQ-C lane: same pipeline that killed twice in the worm (NQ-C1 `838c688b`, NQ-C2 `bd89fd14`→FAIL), now at fly scale. Companion to FLYWIRE-ACCESS-PATH.md (the door), CONNECTOME-QUILT-RESEARCH.md and NQ-C2-edges-as-channels.md (the worm truths under test).*

**VERDICT (booked 2026-09-03 22:10 AKDT, run `fly_shore_spike.py` @ commit `0cfb9e65`): INCONCLUSIVE on the pre-registered gates — the worm's *direction* travels (inter-cluster edges lighter, 14/14 cells, 10/10 bootstraps), the worm's *strength* does not (R = 0.889 vs worm 0.500; rank-biserial 0.083 vs 0.31), and the biggest-wire audit FAILED (6/12 intra vs worm 12/12 — the fly shore's heaviest wires are boundary wires). NO-GO for a full-animal science lane; pipeline mechanics themselves scale easily (§R4: ~1.1 GB, ~15 min wall, this box). The worm teaches mostly worm truths; the piece that travels is a sign, not a law.**

**Data:** FlyWire public release v783 (Oct 2023 snapshot), CC BY-NC 4.0. Data: Dorkenwald et al. 2024 (doi:10.1038/s41586-024-07558-y); Schlegel et al. 2024 (doi:10.1038/s41586-024-07686-5); synapse detection per Buhmann et al. 2021 (doi:10.1038/s41592-021-01183-7); neurotransmitter predictions per Eckstein et al. 2024 (doi:10.1016/j.cell.2024.03.016). Retrieved from gs://flywire-data (codex/data/fafb/783).

---

## 1. The question, one sentence

The worm booked: *inter-cluster edges are LIGHTER than intra-cluster edges (R = m_inter/m_intra = 0.500, reverse-perm at the 10k floor), boundaries are many thin doors at median weight 1 (43.5% of pairs cross), and the 12 heaviest wires in the animal are all interior local machinery (VB03→DD02 et al.)* — does that truth survive a 460× bigger animal, and does the *pipeline* (τ-prune → Louvain → inter/intra statistic) even run there without choking?

This is NOT a full-animal ingest. One neuropil = the shore. The whole animal stays un-ingested; it is only counted (§7).

## 2. The shore: right antennal lobe (token `AL_R`) — booked with reason

**Picked: `AL_R`.** Booked reason, three legs:

1. **Scale fits the shore budget.** `AL_R` = 36,826 rows (0.95% of 3,869,878 edges); endpoints ≈ low thousands of neurons ≈ ~2% of the 139,255-neuron animal. The medulla alternative (`ME_R`+`ME_L`) is 909,990 rows touching 71,656 neurons — **51% of the animal**. That is not a shore, that is a continent; it violates the spike's own scope clause (~1–5%).
2. **Cleaner spatial anatomy.** The antennal lobe is a compact first-order olfactory relay: ~60 discrete glomeruli, each a chemotopic unit, synapses confined inside the glomerular neuropil. The medulla's "cleanliness" is a tiling illusion — ~750 repeated columns graded into layers with wide-field tangential cells crossing them all; "one neuropil" there is a tiled farm, not one module. If Louvain can find structure anywhere with a honest prior, it is glomeruli.
3. **One token, no aggregation ambiguity.** `AL_R` is a single neuropil field value; no hemisphere-combining judgment call (both-hemisphere `AL` stays un-run, bookable later).

Differences from the worm lens, booked in advance: the fly file is **chemical synapses only** (no EJ/gap-junction column — worm's weight-1 EJ build edges don't exist here); `nt_type` column present but **unused**; weights are `syn_count` per (pre, post) pair per neuropil.

**Shore-graph definition (two cells):**
- **PRIMARY (gating): piece-of-tissue reading.** The `AL_R` subgraph = rows with `neuropil == "AL_R"` only, endpoints of those rows, deduplicated per (pre, post), self-loops dropped. This is the spatially-delimited piece of the animal — the AL's own synaptic machinery.
- **SECONDARY (non-gating, labeled): whole-wiring reading.** Full induced subgraph on PRIMARY's neuron set: all edges among those neurons from *any* neuropil (captures AL neurons' outputs to lateral horn/calyx/etc.). Tests whether the AL community's position in the whole-animal graph is also thin-doored.

## 3. The pipeline — verbatim NQ-C1/C2 lens, no re-tuning

- **Prune:** `syn_count >= 3` (τ = 3, the worm's booked lens) for the Louvain build graph.
- **Build:** undirected symmetrization `w = max(w_ij, w_ji)` over pruned directed pairs (worm-exact; no EJ term — file has none).
- **Cluster:** `networkx.community.louvain_communities(weight="weight", seed=42, resolution=1.0)`, clusters ordered by size descending — the exact C1 lens ("NQ-C1 lens").
- **Statistic (worm C2-exact):** over the directed pair list (all weights, both endpoints in the partition): inter = weights crossing cluster boundary, intra = same-cluster; **R = median(inter)/median(intra)**; Mann-Whitney U one-sided; **permutation test, 10,000 label shuffles**, T = m_intra − m_inter (replication direction — the worm booked the reverse-direction floor), RNG_BASE = 20260903, one booked child stream per stat cell.
- **Robustness cells (pre-registered):** τ=5 build (sensitivity, non-gating); hub-blind = drop top-5 build-graph-degree hubs from the statistic (downgrades replication one notch if it dies); bootstrap = 10 fresh Louvain seeds (1–10), each re-running the primary statistic.

## 4. Pre-registered gates — the worm prediction, on trial at scale

**Prediction (pre-registered, from NQ-C2 §6.1–6.2): REPLICATE — inter-cluster edges LIGHTER.**

| Gate | Condition | Meaning |
|---|---|---|
| G1 sign | R < 1 | inter lighter, point estimate |
| G2 rank | MWU one-sided (intra > inter) p < 0.001 | the worm's separation, rank-level |
| G3 shuffle | perm T = m_intra − m_inter, one-sided p < 0.001 | not label-luck |
| G4 seed | ≥ 8/10 bootstrap re-clusterings hold R < 1 | not one-lens luck |

**REPLICATED** = G1∧G2∧G3∧G4. **WEAKLY REPLICATED** = all but hub-blind died (drop one notch). **FALSIFIED** = R > 1 with MWU (inter > intra) p < 0.001 and ≥ 8/10 bootstraps R > 1 — the worm taught only worm truths. Anything mushier: **INCONCLUSIVE**, booked as such, no words put in its mouth.

**Known construction-bias disclosure (carried from C2 §preamble):** Louvain's modularity objective rewards heavy edges *inside* clusters — an R < 1 outcome is partly expected-from-construction. A REPLICATE verdict therefore books as *"under modularity partitions at 460× scale, edges still do not lean outward"* — NOT as "boundaries don't matter" — exactly the worm's booking language.

## 5. Pre-registered audits

- **Biggest-wire audit (gating-lite):** top-12 heaviest directed pairs of the shore (τ≥3), intra vs inter. Worm: 12/12 intra (VB→DD locomotor giants). Replicate if **≥ 10/12 intra**; also name the giants and ask the fly-analogue question: are they local recurrent machinery?
- **Degree distribution (descriptive, no gate):** in/out degree on the shore, log-log least-squares slope booked; compared qualitatively to worm (N≈302, gently skewed, no scale-free claim ever made there). This is bookkeeping for the full-lane RAM model, not science.

## 6. Compute/memory honesty — pre-registered discipline

- Stream the 3.87M-row CSV with `gzip+csv` chunkwise; the full edge table is **never materialized**. RAM-resident beyond constants: (a) AL neuron id set, (b) AL_R pair dict (~37k), (c) secondary induced dict (bounded by S², expected ≪), (d) the pruned build graph + numpy stat arrays. Whole-file passes (max 3) touch every row but keep nothing.
- Book via `resource.getrusage` max RSS and wall-clock per phase. Extrapolation to the full animal uses **measured** per-edge costs (networkx bytes/edge via `tracemalloc`, Louvain wall time, per-shuffle permutation cost), scaled to the τ≥3 whole-animal row count (3,161,243 rows — counted, not stored), with the shore's measured row→unique-pair dedup factor applied. No hand-waving: every number in §7-results extrapolation traces to a measured quantity.
- **GO/NO-GO for a full-animal lane** (the deliverable): GO requires (i) pipeline mechanics survived the shore without choking, (ii) extrapolated full-animal RAM ≤ 8 GB and honest time estimate on this 24-core/15 GB box, (iii) the science is *decisive either way* (a clean replicate or a clean falsify both justify the lane; mush does not).

## 7. Provenance

- `connections.csv.gz` sha256 `d49dd692e59e153aa3c83f5257bfc0eff51247b86d7bb183386c6d1622c70fc9` (50,289,304 bytes), `neurons.csv.gz` sha256 `6a6b3759e635f0f35a677d169052362131ec61d95f55919298b55c43fce4e719` (1,679,884 bytes) — downloaded 2026-09-03 21:58 AKDT from the FLYWIRE-ACCESS-PATH route 1 bucket, anonymous.
- Whole-animal counts (from streaming passes, no storage): 3,869,878 rows; 3,161,243 rows with syn_count ≥ 3; 79 neuropil tokens; 139,255 neurons.
- Spike script: `docs/fly_shore_spike.py`, committed with this pre-registration, before its own execution.

## 8. Receipt (pre-run)

- [x] Shore chosen and reason booked (§2) BEFORE any weight statistic ran (only row/endpoint *counts* were touched, to verify scale)
- [x] This pre-registration §1–§7 committed and pushed BEFORE the run (`0cfb9e65`, 2026-09-03 22:03 AKDT — run started 22:04:12, receipt below)
- [x] Gates locked to the worm's booked direction; construction-bias disclosure carried verbatim in spirit
- [x] Compute discipline pre-declared: stream, count-only passes beyond the shore, O(shore) RAM ceiling
- [x] All pre-registered cells executed; verdict booked per gates (INCONCLUSIVE — G3 failed at primary) with post-hoc cells labeled POST-HOC and quarantined below the divider

---

# RESULTS — booked after the run, per the divider contract

Run: 2026-09-03 22:04:12 AKDT, wall ≈ 4 min, peak RSS 305 MB (§R4). Raw receipt: `/tmp/fly_shore_run.log`, summary `/tmp/fly_shore_summary.json`. Script: `docs/fly_shore_spike.py` (committed pre-run).

## R1. The gates, cell by cell

Shore `AL_R`: 36,826 rows → 36,826 unique directed pairs (dedup 1.000, zero self-loops), 3,392 neurons ≈ 2.4% of the animal. τ=3 build graph: 3,151 nodes, 28,203 edges. Louvain (seed 42, NQ-C1 lens): **32 clusters**, sizes [482, 413, 329, 282, 271, 212, 143, …] — finer-grained than the worm's 8, as expected at 10× the neurons.

| Cell | inter med (n) | intra med (n) | R | rank-biserial (replication dir) | MWU(intra>) p | perm(T=i−m) p |
|---|---|---|---|---|---|---|
| **PRIMARY all-w** | 8 (20,367) | 9 (15,997) | **0.889** | +0.083 | 2.0e-42 | **0.350** ✗G3 |
| SENS w≥5 subset | 8 (19,402) | 11 (13,730) | 0.727 | +0.216 | 1.5e-249 | 0.0001 |
| SENS τ=5 rebuild | 8 (20,729) | 10 (15,127) | 0.800 | +0.104 | 8.2e-64 | 0.0002 |
| HUB-BLIND −top5 | 8 (16,108) | 9 (14,487) | 0.889 | +0.072 | 7.3e-28 | 0.166 |
| BOOT seeds 1–10 | 8 | 9 | 0.889 (all ten) | +0.04…+0.08 | ≤1.3e-9 (all) | 0.35–0.37 (all) |
| SECONDARY whole-wiring | 8 (23,231) | 12 (19,727) | 0.667 | +0.239 | ~0 | 0.0001 |

**Gate tally: G1 ✓ (R<1 everywhere, 14/14 cells, 10/10 bootstraps) · G2 ✓ (p=2e-42) · G3 ✗ at primary (p=0.350; passed at both sensitivity cells and the secondary) · G4 ✓ (10/10).** → **INCONCLUSIVE** per §4's booking language, no words put in its mouth. Direction universal, primary-lens magnitude mushy.

**POST-HOC diagnosis (labeled, never gates):** the pre-registered T = m_inter − m_intra was calibrated on worm weight scales (medians 1 vs 2 — a 2× gap). At fly scale the primary gap is 8 vs 9 — one integer unit — and a median-difference statistic on integer weights cannot resolve that against label noise (shuffles hit −1 easily: p=0.35). The same statistic at w≥5 (8 vs 11) hits the 10k floor. The rank level (MWU) is decisive at every cell in the replication direction. This is a statistic-resolution miss, not an effect miss — but the gates were locked before the run, so INCONCLUSIVE stands, and the *magnitude* story below is the real finding.

**What travels and what doesn't:**
- **Travels (sign):** inter-cluster edges are lighter than intra-cluster edges — every cell, every bootstrap, both shore readings. The worm's inward lean exists at 460×.
- **Doesn't travel (strength):** worm R = 0.500, rb = 0.31 — a 2× separation. Fly shore R = 0.889, rb = 0.083 at primary — a ~1.1× lean, 4× weaker in rank terms. The fly's doors are thin only *relatively* (8 vs 9–12); absolutely they are fat (worm's heaviest edge anywhere: 37 synapses; fly AL_R's median boundary edge: 8; its top wires: 700+).
- **Doesn't travel (giants):** see R2 — the audit gate failed.

Thin-door density: 56.0% of directed pairs cross a boundary (worm 43.5%) — boundaries are, if anything, *busier* per pair at fly scale.

## R2. Biggest-wire audit — FAILED against the worm's signature (6/12 vs 12/12)

Worm: all 12 heaviest wires intra-cluster locomotor machinery (VB→DD giants). Fly shore `AL_R` (τ≥3):

```
AL.3  -> AL.13   w=729  INTER (C1->C5)
AL.3  -> AL.14   w=668  INTER (C1->C5)
AL.4  -> AL.13   w=639  INTER (C1->C5)
AL.4  -> AL.14   w=611  INTER (C1->C5)
AL.102-> AL.LAL.1 w=577 INTRA (C3)
AL.36 -> AL.17   w=524  INTER (C1->C0)
AL.3  -> AL.32   w=495  INTRA (C1)
AL.4  -> AL.32   w=463  INTRA (C1)
AL.3  -> AL.36   w=462  INTRA (C1)
AL.32 -> AL.17   w=439  INTER (C1->C0)
LAL.145->LAL.41  w=424  INTRA (C4)
AL.4  -> AL.36   w=417  INTRA (C1)
```

Gate (≥10/12 intra): **6/12 — FAILED.** And the failure is structured, not noisy: the four heaviest wires in the shore — 600–729 synapses each, ~20× the worm's heaviest wire — all cross the *same* boundary (C1→C5), from two giant senders (AL.3, AL.4; out-degrees ~1,000) into two giant receivers (AL.13, AL.14; in-degree max 640). POST-HOC, labeled: this is the shape of olfactory convergence — few massive fan-in wires feeding module-scale targets — versus the worm's evenly-distributed interior giants. Where the worm spread its thickness *inside* modules, the fly shore concentrates thickness on *one* boundary. **For quilt doctrine this is the opposite pole: at 460×, thick gates exist** (four of them, heavier than everything the worm ever built), embedded in a boundary population that is otherwise thin (median 8 vs intra 9–12). Biology not verified against `labels.csv`/`classification.csv.gz` — booked as future cell, names are FlyWire auto-types only.

## R3. Degree distribution (descriptive, no gate, as pre-registered)

In-degree: n=2,306, median 3, max 640, log-log slope −1.03. Out-degree: n=2,797, median 4, max 1,033, slope −1.20. Heavy-tailed on a 3.4k-neuron shore — hubs an order of magnitude above the worm's (worm max degree ≈ 50-ish on 302 neurons). No scale-free claim made or needed; the slopes are inputs to the extrapolation below, not findings.

## R4. Compute/memory honesty — measured, then extrapolated

| Quantity | Measured (shore) | Extrapolated (full animal) |
|---|---|---|
| Stream pass (3.87M rows) | 2.0 s, nothing retained | 2 more passes ≈ free |
| τ=3 build graph | 28,203 edges, 8.1 MB (288 B/edge), 0.1 s | ≤3.16M unique pairs → **~1.1 GB** (20% headroom, upper bound) |
| Louvain (seed 42) | 0.24 s | ~1 min (power-law 1.1 on E; measured at 1/100 scale — order-of-magnitude only) |
| 10k-perm stat cell | 102 µs/shuffle @ 2k edges | ~27 min single-core; 13 cells ÷ 24 cores → **~15 min wall** |
| Peak RSS whole run | **305 MB** | ≲2 GB all-in on a 15 GB box (8 GB available) |

E_full upper bound = 3,161,243 τ≥3 rows × dedup 1.000 (cross-neuropil pair merging only shrinks it). The O(shore) RAM ceiling held: the only whole-animal object ever resident was a row counter.

## R5. GO/NO-GO for a full-animal lane

**NO-GO for the full-animal science lane, per the pre-registered §6 criteria.** Mechanics: GO, trivially — everything fits in ≲2 GB and ~an hour wall on this box, no new engineering needed. But §6(iii) required the science to be *decisive either way*, and the shore returned mush at the primary gate (G3 ✗, audit ✗): a clean replicate or a clean falsify would have justified the lane; a weak-and-structured maybe does not. The informative numbers are already in hand at 2.4% of the cost:

1. The inter-lighter *sign* is near-certain to hold animal-wide (14/14 here, 20/20 worm) — a full run would spend an hour confirming a foregone conclusion.
2. The *strength* question (does anything approach the worm's 2× separation anywhere in the animal?) is the only live science, and it does not need the whole animal — it needs *targeted* shores chosen for contrast (medulla's tiled columns vs AL's glomeruli vs CX's nested rings), not a 460× bulk re-run.
3. The thick-gate finding (R2) points where the real structure is: per-boundary heterogeneity. That is a different statistic (boundary-weight distributions, not a single inter/intra ratio), pre-registerable, and runnable on shores.

**Booked sentence for the lane: the pipeline scales; the worm's truth doesn't.** Worm-scale quilt law (thin doors everywhere, giants interior, 2× separation) is a small-animal truth. At 460× the same lens finds the sign intact, the strength diluted 4×, and the giants redistributed onto a few very thick boundary wires — architecture the worm literally cannot express with 37-synapse wires. If anyone reopens this, the entry is per-boundary analysis on contrast shores, not the full-animal re-run.

## R6. Post-run receipt

- [x] Pre-reg committed & pushed (`0cfb9e65`) at 22:03 AKDT; run started 22:04:12; results committed after (this commit)
- [x] Raw sha re-verified at run start (d49dd692…, matches §7); no re-download
- [x] All six pre-registered cells + 10 bootstraps + audit + degree booked; gates scored exactly as §4 wrote them — INCONCLUSIVE stands despite the POST-HOC diagnosis that the primary T was resolution-starved (diagnosis quarantined, never gates)
- [x] Audit failure booked at face value (6/12), with the structured C1→C5 concentration labeled POST-HOC
- [x] Compute table all-measured; extrapolation flagged where it outruns the measurement (Louvain power law)
- [x] NO-GO booked against pre-registered §6(iii), with the cheaper targeted-shore alternative named
- [x] Spike wall: ~14 min start-to-push (cap 40) — the discipline is the expensive part, not the compute

*Spike closed 2026-09-03. The pipeline scales; the worm's truth mostly stays home.*
