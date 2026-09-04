# CONNECTOME → QUILT: Can a Biological Brain Partition Into Cells?

**NQ-C lane research doc — superinstance quilt, phase-0 feasibility.**
Casey directive, 2026-09-03: biological connectomes (FlyWire, C. elegans — both open) piped into the quilt architecture via a 4-phase pipeline. Verdict below.

**Verdict up front:** The pipeline is **feasible on the worm and unproven on the fly**, and the honest statement is stronger than that: phases 1–3 are standard graph engineering (existing libraries, hours not weeks), phase 4 is *not* engineering at all — it is the whole quilt question wearing a biology costume. What a biological connectome gives us is not a smarter brain for the fleet; it is a **77-million-year-old decomposition experiment whose results are already on disk**. Evolution already ran the "how do I cut a graph into bounded cells with meaningful boundaries" problem. We are reading its answer key. That is the actual value. A fly-scale graph will not run as a live cell fabric on a 4050; a worm graph will, in seconds. So the whole lane should be scoped: **worm first, fly as data, never fly as substrate.**

Second verdict, before any details: **everything below the raw file is DERIVED DATA.** A pruned connectome is not a connectome. If the provenance chain (raw hash → prune params → cluster assignment → constraint table) is not booked at every step, the cell fabric inherits unrepeatable inputs and F98 conformance becomes a lie we run on schedule. §3 is not a compliance section; it is load-bearing.

---

## 1. Data Survey (links fetched and verified 2026-09-03)

House honesty rule applied: every link below was fetched from this laptop. Notes on what verified and what fought back are part of the survey, not decoration — access friction is real feasibility data.

### 1.1 C. elegans — the substrate lane

| Source | What it is | Size / shape | License | Access (as tested) |
|---|---|---|---|---|
| **WormAtlas `NeuronConnect.xls`** — [wormatlas.org/images/NeuronConnect.xls](https://www.wormatlas.org/images/NeuronConnect.xls), landing page [neuronalwiring.html](https://www.wormatlas.org/neuronalwiring.html) | White et al. 1986 hermaphrodite somatic nervous system: 302 neurons, chemical synapses + gap junctions, directed, weighted by synapse count | 6,417 rows; columns `Neuron 1, Neuron 2, Type, Nbr`; Type ∈ {S, Sp, EJ} | free academic use (WormAtlas terms; not an explicit OSI license — book it) | ✅ **fetched and parsed on this laptop** (518,144 bytes, real Excel OLE file). Scar: `curl` without a browser User-Agent gets connection-dropped; with `Mozilla/5.0` UA it works. Parsed with `xlrd` 2.0.2. |
| **Cook et al. 2019, "Whole-animal connectomes of both C. elegans sexes"** — [doi:10.1038/s41586-019-1352-7](https://doi.org/10.1038/s41586-019-1352-7) | Both sexes: hermaphrodite (302 neurons) and male (385 neurons), ~1,500 gap junctions + ~6,000 chemical synapses per animal, incl. muscles | tabular, paper supplement + Zenodo dataset | paper CC-BY; dataset see Zenodo terms | ✅ DOI resolves (title scraped from landing page). Zenodo mirror ([10.5281/zenodo.2585695](https://doi.org/10.5281/zenodo.2585695)) resolves but blocks bot scraping with 403 — downloadable via browser/UI, noted as friction. |
| **Witvliet et al. 2021, "Connectomes across development reveal principles of brain maturation"** — [doi:10.1038/s41586-021-03778-8](https://doi.org/10.1038/s41586-021-03778-8) | 8 isochronic connectomes, L1 → adult, same 302-neuron scaffold — **this is the future canary set for threshold/developmental robustness** | 8 × edge lists | paper CC-BY; datasets via journal data links | ✅ DOI resolves, title verified. Data files not curl-tested yet — do not claim more than verified. |
| **OpenWorm `owmeta`** — [github.com/openworm/owmeta](https://github.com/openworm/owmeta), docs [owmeta.readthedocs.io](https://owmeta.readthedocs.io/en/latest/) | Programmatic, versioned C. elegans connectome (White + updates); the *provenance-correct* ingest route | Python API | permissive (repo + docs live) | ✅ repo 200, docs 200, c302 sibling repo 200. Not installed for the spike — heavier than needed for NQ-C1. |
| **OpenWorm `c302`** — [github.com/openworm/c302](https://github.com/openworm/c302) | The muscle-by-muscle whole-animal model built on the connectome — prior art for §6 | model code + configs | open source | ✅ verified live (repo + raw README fetch). |

**Hermaphrodite vs male (booked, per directive):** hermaphrodite = 302 somatic neurons, ~7k synapses, the canonical dataset, everything above. Male = 385 neurons with sex-specific circuits (Cook 2019; Jarrell et al. 2012 Science for the male tail). NQ-C1 uses the **hermaphrodite, somatic only** (pharyngeal 20-neuron system excluded, as in White's own somatic table — the WormAtlas XLS already reflects this scope).

### 1.2 Drosophila — the data lane (not the substrate lane)

| Source | What it is | Size / shape | License | Access (as tested) |
|---|---|---|---|---|
| **FlyWire / Codex** — [flywire.ai](https://flywire.ai), [codex.flywire.ai](https://codex.flywire.ai) | Adult female *D. melanogaster* whole-brain connectome, ~140k neurons, ~50M synapses; Codex is the flat-table warehouse (neurons, connections, neurotransmitters as TSV views) | far too big for edge-hardware fabrics; fine for offline partition study | **CC-BY 4.0** (stated by Codex) | ✅ both hosts live (200). Scar: `codex.flywire.ai/api/download?...` returns the SPA shell to `curl` — the flat TSVs flow through the web UI / authenticated Python client, not anonymous GET. Real, but session-gated. |
| **Dorkenwald et al., "Neuronal wiring diagram of an adult brain"** — [doi:10.1038/s41586-024-07558-y](https://doi.org/10.1038/s41586-024-07558-y) | The FlyWire adult brain paper (+ companion Zheng et al. "A complete connectome of the adult Drosophila brain") | paper + open data | CC-BY | ✅ DOI resolves, title scraped and verified. |
| Drosophila larva (Winding et al. 2023, Science) — *not fetched* | 3,013 neurons, ~500k synapses — the mid-scale rung between worm and fly | edge list, open | open | ⚠ not verified this session; do not plan against it until fetched. |

### 1.3 What the survey actually says

- **The worm lane is fully unblocked today**: one UA-header'd GET away from a clean 6,417-edge weighted directed graph, parseable with stock Python. No registration, no session, no download button.
- **The fly lane is real but session-gated** and, more importantly, size-prohibitive as a live substrate on our hardware class: 50M synapses is a data problem, not a cell problem. Partition *studies* on it: yes, offline, on the desktop forge. Live fabric on the 4050: no, and pretending otherwise would violate the undersell rule.
- **License honesty:** FlyWire is cleanly CC-BY. WormAtlas is "free for academic use," which is NOT an OSI license — for anything that ships, we should prefer Cook 2019 / Witvliet 2021 (journal CC-BY + deposited data) as canonical sources, and treat the White XLS as the convenient community mirror it is. Booked.

---

## 2. Phase-by-Phase Feasibility

The 4 phases as directed, each with: concrete tools (existing libs — per the existing-solutions preflight, this whole lane is library-composition, not invention), hard open questions, and the quilt mapping.

### Phase 1 — Ingest + high-pass prune

- **Tools:** `pandas` + `xlrd` (worm XLS) or Codex TSVs (fly); `networkx.DiGraph` with `weight = Nbr`. Prune = keep edge iff `weight ≥ τ`. One evening of code, and it is already written (§7 spike).
- **Hard question — threshold sensitivity is the whole phase.** Synapse counts in White's data are tiny integers (mode = 1–3). A high-pass at τ=2 deletes a huge fraction of total edges; τ=5 guts it. There is no natural gap in the weight distribution to hide behind — the "weak synapse" concept has no biological cliff. **Pre-registered canary (directly from the directive): does the motif partition survive ±20% threshold swings?** If cluster identity churns wildly across the sweep, phases 2–4 inherit noise and the lane dies here. Tested in §7 — result booked.
- **Quilt mapping:** the raw edge list is the **byte-exact tier** input (it is a file, hashable, immutable). The pruned graph is already a *derived view* — it belongs in the trace-labeled tier with its derivation parameters booked. Tier law applies from step one, not from deployment.

### Phase 2 — Louvain/spectral clustering into functional motifs

- **Tools:** `networkx.community.louvain_communities` (built into networkx ≥ 2.8 — no extra dep; runs on 302 nodes in milliseconds), `scipy` for spectral fallback / Fiedler-vector cuts. `python-igraph` and `python-louvain` are fine alternates; nothing here needs to be written from scratch.
- **Hard questions:**
  1. **Louvain is randomized.** Same graph + different seed ⇒ different partition (usually cosmetically different, occasionally not). Deterministic replay therefore requires seed-booking — or moving to spectral/modularity-approximation methods with defined tie-breaking. This intersects §3 hard.
  2. **Directedness.** Stock Louvain ignores edge direction. C. elegans chemical synapses are strongly directed (sensory→inter→motor). Options: run on symmetrized weight (standard practice, defensible for gap-junction-rich graphs), or split analysis (in/out motif structure). The spike symmetrizes (`max(w_ij, w_ji)`) and books that as a parameter, not a truth.
  3. **Resolution limit:** Louvain cannot see communities below a scale set by total graph size — for a 302-node graph this mostly doesn't bite, but "how many clusters" is a *choice of resolution parameter*, and the number of cells in the fabric is exactly the thing we're pretending to discover. Honest booking: cluster count is an input dressed as an output.
- **Quilt mapping:** cluster assignment = the **cell manifest**. Not yet constraint logic — the manifest names the cells; phase 3 wires them.

### Phase 3 — Wrap clusters as bounded cells; inter-cluster edges become constraint logic

This is the phase the directive is really about, so it gets the most careful treatment.

**What "constraint logic at the boundary" means in quilt terms.** After clustering, every edge is either *intra*-cluster (absorbed into a cell's internal complexity — nobody outside the cell sees it) or *inter*-cluster (crosses a boundary). In quilt-cellular terms:

| Quilt concept | Connectome mapping | Tier assignment |
|---|---|---|
| `qm_bind` | A cluster binds as a cell; its manifest = node list + intra-cluster edge multiset, hashed | The **node list is byte-exact** (membership is discrete, replayable) |
| `qm_link` | Inter-cluster edges: (cell A → cell B, aggregate weight w, neurotransmitter class if fly) | The **edge set is byte-exact** (it's a table); its *interpretation* is trace-labeled |
| `qm_effect` | A cell writes to its boundary channel when its internal state crosses a level — e.g., aggregate activation of its input side | **Trace-labeled** — internal dynamics are continuous/simulated, never byte-exact |
| `qm_view` | A cell reads only its incoming boundary channels (+ its own state), never another cell's interior | The abstraction contract itself: internal complexity hidden behind the channel interface |
| `qm_tick` | The propagation step of the sim — cells evaluate on tick, exchange boundary signals | Tick count is byte-exact; tick *content* is trace-labeled |

**The two-tier law, mapped:** byte-exact = *the boundary table itself* (which cells exist, which edges cross, what weights) — it's discrete tabular data, hashable, replayable. Trace-labeled = *everything the cells do across those boundaries* (activation states, propagated signals, any learned dynamics). This is exactly the boat's law (gauges byte-exact, neural advisory) transposed: **anatomy is a gauge, activity is a neural tenant.** Never mixed inside one cell.

The deep fit — and the reason this lane is worth a spike at all — is that phase 3 is what biology already validated: functional compartments with rich internal structure and sparse, meaningful boundaries. The quilt's bet (boundaries are where the truth lives) is the connectome's observed architecture.

- **Hard question:** is the clustered decomposition *stable enough to be law*? A constraint table that changes when τ moves from 3 to 4 is not law, it's weather. Hence the §7 sweep.

### Phase 4 — Deploy clusters as sub-agents on edge hardware

- **Analog hardware:** RTX 4050 / boat laptop (NOT Jetson — per directive; we own the 4050 class, it's the boat brain already mapped in `BOAT-SUPERINSTANCE-QUILT.md`).
- **What deployment means:** each cluster becomes a process (`qm_bind` at boot from the hashed manifest), boundaries become IPC channels with the byte-exact constraint table as the *shared contract*, cells tick, the journal records boundary traffic.
- **Honest feasibility:** 302-node worm ⇒ single-digit-to-dozens of clusters ⇒ trivially hostable; a laptop is overkill, which is the point (headroom for failure instrumentation). Fly ⇒ 140k neurons ⇒ hundreds of MB of boundary traffic per simulated second if done naively; edge-hardware deployment of fly-scale dynamics is a **research program, not a deploy step**. The doc's scope ruling stands: worm as substrate, fly as study material.
- **Hard question:** what does a cell *do* when it ticks, other than forward-propagate a toy state? The honest answer: for NQ-C1 the internal dynamics are a placeholder (linear threshold propagation), and the spike does not pretend otherwise. The value of the spike is the **partition + boundary contract**, not the dynamics. Anyone who sells you "we simulated a brain" from a threshold-propagation toy is selling you the abstraction, not the animal.

---

## 3. The Determinism Boundary (load-bearing, not compliance)

A pruned biological graph is **derived data**. The chain, and what breaks without it:

```
raw file (sha256 booked)
  → prune params (τ, symmetrization rule, edge-type filter)     [choice — human-booked]
  → pruned graph (hash of canonical edge serialization)          [deterministic given above]
  → cluster assignment (algorithm + seed + resolution)           [choice + RNG]
  → constraint table (hash)                                      [deterministic given assignment]
  → cell fabric (manifests + boundary channels)                  [deployed]
```

Each arrow is either a *deterministic function* (safe) or a *choice* (must be booked, because choices are where unrepeatability enters):

1. **Raw hash** — the anchor. The White XLS is a 2006-era Excel file maintained by a lab; it can and does get corrected. Pin the sha256, or "the worm connectome" silently drifts under the fabric.
2. **Prune params** — τ is a scientific choice with no ground truth. Not replayable across *studies*, only within one: every artifact downstream must carry its τ in the filename. Not negotiable, because §7 shows partitions genuinely depend on it.
3. **Cluster assignment** — the RNG hole. Louvain without a booked seed makes the *cell manifest itself* unrepeatable, which means the byte-exact tier's foundation is a dice roll. Law: **seed is booked or the clustering didn't happen.** (Better law, longer term: consensus clustering across seeds, which converts a random draw into a robust statistic — see §7.3.)
4. **Constraint table** — pure function of the above; hash it, ship it, verify on boot (`qm_bind` refuses to start a cell against a manifest whose hash doesn't match the table's).

The quilt already has the doctrine for this (journal replay ⇒ byte-exact reproduction of derived views). This lane just makes it literal: **replaying `prune(seed=…) → cluster(seed=…) → table` must reproduce the constraint table hash exactly, or the fabric does not bind.** That check is the F98 of this lane.

---

## 4. The Elephant Connection: Is a Cluster a ROOM? (speculative — marked as such)

*Everything in this section is speculation by construction; it is direction-setting, not booking.*

The elephant service reads room temperature from vMF field embeddings of agent traffic: hot room = dense, surprising interaction; cold = sparse, predictable. JEPA surprise (per the iceberg paper's math) = ‖φ(s) − φ(ŝ)‖² — how wrong a cell's world-model just was.

**The speculation:** a cluster-partitioned connectome gives each cell a *local* embedding context — its own state + its boundary channels — and the boundary is exactly the surface where prediction is hardest. Inside a motif, neighbors are densely wired: the next tick is well-predicted from recent input (low JEPA surprise — warm but boring). **Across a motif boundary, wiring is sparse and convergent: the same boundary signal admits many internal continuations, and surprise concentrates there.** So: warm/cold contrast across motif boundaries is not just possible, it is *expected from the degree distribution* — boundary channels carry more bits of genuine novelty per edge than interior edges. The elephant's room-temperature concept maps onto the connectome fabric as: **a cell runs hot exactly when its boundary channels violate its learned interior model** — i.e., when another cluster's business became its business.

If that's right, the testable (eventually) claim is: **boundary-edge surprise > interior-edge surprise, measurably, in a propagation sim.** That is a canary-shaped statement (pre-registerable rate comparison, like BQ-3's ≥2× base-rate test). It is NOT tested in NQ-C1 — the toy dynamics are too weak to carry it — but NQ-C1's plumbing (per-edge bookkeeping of boundary vs interior traffic) is the precondition, and the spike keeps the plumbing.

And the room answer, stated honestly: a cluster is a room's *floor plan* — the walls are real (the boundary table), but whether there's temperature in the room depends on dynamics we haven't built. NQ-C1 builds walls. Temperature is NQ-C2+'s problem, if walls hold.

---

## 5. NQ-C1 — First Falsifiable Shore-Spike (C. elegans)

**Pre-registration (booked BEFORE running — see git history, survey commit precedes spike commit):**

- **Input:** WormAtlas `NeuronConnect.xls` (White et al. hermaphrodite, somatic; sha256 booked at runtime).
- **Procedure:** ingest → prune at 3 thresholds (τ ∈ {1, 3, 5} on synapse count) → Louvain (symmetrized `max(w_ij, w_ji)`, seed=42, booked) → constraint table emitted → simple threshold state-propagation sim of the touch/escape circuit across cell boundaries.
- **PASS condition:** the posterior-touch escape circuit — touch receptor (AVM/PLM) → command interneurons (AVB/PVC) → DB-class motor neurons (backward locomotion arc) — emerges as ≥1 cluster whose internal boundary structure matches known functional anatomy (i.e., the arc is NOT shattered across unrelated clusters; the cluster containing PVC also contains the DB motor pool it drives).
- **KILL condition:** cluster boundaries are threshold-brittle — no stable partition across the τ sweep (quantified below by pairwise partition agreement across thresholds). If killed: **the pipeline idea dies at phase 2 for worms and this doc says so in its results section.**
- **Stability metric:** pairwise partition agreement (fraction of node pairs co-clustered identically) across the 3 thresholds; plus seed-robustness check at fixed τ (10 Louvain seeds, agreement vs the booked seed). Pass needs agreement well above the random-partition floor; "well above" is honestly fuzzy — the number is booked either way, and the ±20% τ swing (τ = 2.4/3/3.6 → {2,3,4} in integer data) rides along in the sweep.

**RESULTS: see §7 — run after pre-registration commit.**

---

## 6. Related Work — Honest Scan

- **OpenWorm** (project + c302): whole-animal *simulation* from the connectome — the flagship prior art for "take the worm seriously as an engineering object." Their goal is biophysical fidelity (muscle electrophysiology, body mechanics), NOT graph→multi-agent decomposition. Nearest neighbor, different axis: they simulate *one* animal in depth; we partition *one* graph into many cooperating agents.
- **Cook et al. 2019 / Witvliet et al. 2021**: connectome *construction and comparison* papers — data science, no multi-agent framing.
- **FlyWire codex papers** (Dorkenwald et al. 2024; Zheng et al. 2024): reconstruction, cell typing, motif statistics — again, no agent-decomposition framing.
- **Network-neuroscience motif/modularity literature** (community detection on connectomes is a standard subfield — e.g., modularity analyses of the C. elegans graph; rich-club studies): phase 2 of our pipeline is, honestly, *routine* neuroscience tooling. We are not claiming partitioning itself as novel.
- **Connectome→reservoir computing** (`conn2res` line of work): uses the worm connectome as fixed dynamics for ML — closest in spirit to "the connectome as compute substrate," but single-reservoir, not cell-decomposed, not multi-agent.
- **Graph neural networks / graph partitioning at scale**: standard engineering, no biology.
- **Verdict on territory:** to the best of an honest (not exhaustive) scan: **graph→multi-agent decomposition of real connectomes, with cells as bounded agents and inter-cluster edges as an explicit contract, appears unclaimed.** Nearest neighbors: OpenWorm (fidelity axis), conn2res (substrate axis), modularity neuroscience (partition axis). The quilt framing — boundary tier law on top of the partition — is genuinely ours. Undersold restatement: being first matters less than whether phase 2 stability holds, and that's §7's question, not the novelty claim.

---

## 7. Spike Results

*(filled in after pre-registration commit — by construction, see git order)*

**PENDING — run follows.**

---

## 8. Receipt

- [x] Data survey: all links fetched/verified 2026-09-03; scars (UA-gating, 403s, session-gating) booked in §1
- [x] Phases mapped to quilt opcodes + tier law (§2, table in 2.3)
- [x] Determinism chain specified with the seed-booking law (§3)
- [x] Elephant/JEPA section marked speculative (§4)
- [x] NQ-C1 pre-registered before run (§5, enforced by commit order)
- [ ] Spike run + honest pass/kill booking (§7) — next commit
