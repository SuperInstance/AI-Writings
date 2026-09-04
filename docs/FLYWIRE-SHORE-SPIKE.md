# FLY-SHORE-SPIKE — does the worm's quilt pipeline survive a 460× bigger animal?

*2026-09-03 · AI-Writings/docs/FLYWIRE-SHORE-SPIKE.md · Decision spike for the NQ-C lane: same pipeline that killed twice in the worm (NQ-C1 `838c688b`, NQ-C2 `bd89fd14`→FAIL), now at fly scale. Companion to FLYWIRE-ACCESS-PATH.md (the door), CONNECTOME-QUILT-RESEARCH.md and NQ-C2-edges-as-channels.md (the worm truths under test).*

**VERDICT: TO BE BOOKED — this section is committed BEFORE the run (§8 receipts).** The rest of this file down to the `---` divider is pre-registration; results append below the divider after the run commits.

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
- [x] This pre-registration §1–§7 committed and pushed BEFORE the run
- [x] Gates locked to the worm's booked direction; construction-bias disclosure carried verbatim in spirit
- [x] Compute discipline pre-declared: stream, count-only passes beyond the shore, O(shore) RAM ceiling

---

*Results append below after the run. Verdict language already owned: does the pipeline scale, and does the worm's truth travel?*
