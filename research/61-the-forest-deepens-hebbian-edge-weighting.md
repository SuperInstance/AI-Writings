# The Forest Deepens: Hebbian Edge Weighting for Corpus-Scale Recall

**Authors:** SuperInstance Research Team
**Paper Number:** 61
**Date:** August 2026
**Status:** Research Complete — Literature Survey + Design Recommendation
**Subject:** The Forest retrieval stack (ai-writings corpus, Cloudflare D1 + Workers)

---

## Abstract

The Forest is a chunk graph over a personal writings corpus: explicit reference edges (markdown links) and semantic near edges (cosine kNN over bge-m3 vectors), retrieved via seeded graph walks. A planned third layer would let walked edges gain weight — a Hebbian rule, `weight = base + ln(1 + walk_count)` — so that the retrieval paths the corpus actually uses deepen over time. This paper surveys 2024–2026 prior art to answer four questions: (1) does anyone already do usage-driven edge weighting in graph RAG; (2) which neuroscience-derived decay and strengthening formulas survive translation to a web app; (3) what failure modes should we expect and how are they mitigated; (4) at 10k–100k chunks, is Hebbian deepening worth it versus a plain recency boost. The headline finding is a genuine gap: GraphRAG, LightRAG, RAPTOR, HippoRAG 1/2, Mem0, A-MEM, and Zep/Graphiti all build dynamic or temporal *structure*, but none strengthen edges from *retrieval usage* with decay. The nearest precedents are BambooKG (frequency-weighted edges, built at ingestion rather than at query time), MemOS (hot/cold memory scheduling by access heat), and FSRS spaced repetition (power-law forgetting with spacing-effect-aware strengthening). The second headline is a dampening one: the log formula's dynamic range is inherently small — 10,000 walks yield only ≈9.2 weight units — so at personal-corpus usage rates the Hebbian layer behaves as a slow, bounded usage-rate estimator, a tie-breaker rather than a new retrieval channel. We recommend a two-phase rollout: log walks now, apply Hebbian reweighting offline to measure its counterfactual effect; only move writes into the read path if the replay shows a measurable reranking delta, and then with session deduplication, provenance gating, per-edge growth caps, and an exploration floor. The failure-mode analysis (rich-get-richer hub drift, session echo, laundered self-reinforcement from re-ingested agent output) is presented as first-class content, because these — not the math — are where this design will actually break.

---

## 1. Introduction

### 1.1 The Forest

The Forest indexes the corpus as chunks in Cloudflare D1, each chunk a node. Two edge families exist today:

- **ref edges** — explicit markdown links between documents, the author's own associative gestures;
- **near edges** — cosine-similarity kNN links (bge-m3 embeddings), the corpus's latent structure.

Retrieval seeds from embedded query nodes and walks outward; candidates are reranked and returned. The planned extension is a third layer:

- **walk edges (Hebbian)** — every edge traversed during retrieval gains strength. Proposed rule: `w(e) = base(e) + ln(1 + walk_count(e))`.

The biological metaphor is "neurons that fire together, wire together" (Hebb, 1949): co-retrieved chunks strengthen their connection, so the retrieval surface deepens along the paths the writer's attention actually takes.

### 1.2 Why audit this before building it

Usage-driven weighting is seductive because it is nearly free to describe and very expensive to undo. Once walk counts have influenced months of retrieval, the counterfactual ("what would recall look like without the Hebbian layer?") can no longer be computed from live data — the weights themselves have shaped the query stream that would have been the control. The recommendation literature calls this algorithmic confounding (Chaney et al., 2018), and it is the reason this paper insists on a logged-replay phase before any online reinforcement. We survey prior art, extract the formulas with track records, enumerate the ways this goes wrong, and then make a scoped recommendation for the D1 + Worker stack.

### 1.3 Method and honesty notes

Primary sources were fetched and read at the abstract or full-text level (arXiv: 2405.14831, 2502.14802, 2404.16130, 2410.05779, 2401.18059, 2501.13956, 2504.19413, 2502.12110, 2507.03724, 2510.25724, 2405.20139, 1710.11214; plus the open-spaced-repetition FSRS algorithm wiki and Temporal PageRank literature). Classic psychology and neuroscience results (Hebb 1949; Ebbinghaus 1885; STDP; hippocampal indexing theory; Wixted & Ebbesen's forgetting-curve fits) are cited from the standard literature without per-paper re-verification — they are load-bearing for formula *shape*, not for specific constants. Where we rely on general knowledge of consumer tools (Obsidian plugins, Readwise resurfacing), we say so.

---

## 2. Part I — Prior Art: Who Weights Edges by Usage?

### 2.1 The graph-RAG lineage

**GraphRAG** (Edge et al., 2024; arXiv:2404.16130) builds an entity knowledge graph offline, pregenerates community summaries with hierarchical clustering, and answers global questions by map-reducing over communities. All weighting is decided at index construction. Nothing about retrieval usage feeds back. The graph is expensive to build (a known operational complaint) and effectively static between rebuilds.

**LightRAG** (Guo et al., 2024; arXiv:2410.05779) replaces community machinery with a dual-level (entity/keyword "low-level" and theme "high-level") retrieval over an incrementally updatable graph. The incremental update algorithm addresses corpus growth — new documents add nodes and edges — but edge strength remains what extraction produced. A known degradation mode, discussed in follow-up work, is hub entities: generic high-degree entities accumulate so many connections that retrieval diffuses into noise. This matters for us because our near-edge layer has the same topology risk, and Hebbian weighting interacts with it (Section 4.2).

**RAPTOR** (Sarthi et al., 2024; arXiv:2401.18059) recursively clusters and summarizes chunks into a tree and retrieves across abstraction levels. No usage signal; the tree is static after construction. Its lesson for the Forest is architectural, not dynamic: abstractions (summaries) are worth indexing as nodes in their own right.

**GNN-RAG** (Mavromatis & Karypis, 2024; arXiv:2405.20139) trains a graph neural network to reason over dense KG subgraphs, then verbalizes shortest paths for the LLM. Weights here are *learned* — but offline, by gradient descent on QA supervision. This is plasticity in the ML sense, not runtime Hebbian plasticity: nothing changes at query time.

**HippoRAG** (Gutiérrez et al., 2024; NeurIPS; arXiv:2405.14831) is the closest mechanism in the family, and the direct inspiration for walk-based retrieval generally. It implements hippocampal indexing theory: an LLM-extracted knowledge graph plays hippocampus (a sparse index), the corpus plays neocortex, and retrieval runs Personalized PageRank from query-matched nodes. Crucially, the walks are *transient*: PPR mass flows, nodes are selected, and the process ends. Edge weights are untouched. **HippoRAG 2** (arXiv:2502.14802, ICML 2025) keeps PPR, integrates passages deeper into the graph, and reports that this non-parametric route beats strong embedding baselines on associative tasks (+7% over the SOTA embedding model) while remaining cheaper than iterative retrieval. Neither version lets yesterday's walk change today's weights. The gap our Hebbian layer targets is exactly this: in HippoRAG, "fire together" happens per-query and is forgotten; nothing "wires together."

### 2.2 Agent memory systems

**MemGPT/Letta** (cited as the DMR baseline in Zep's paper) treats memory as paged context — OS-style, no learned edge weights.

**Mem0** (Chhikara et al., 2025; arXiv:2504.19413) dynamically extracts, consolidates, and retrieves salient facts, with an LLM deciding ADD/UPDATE/DELETE/NOOP per candidate memory against the current store. This is usage-adjacent — conversations trigger memory mutation — but the mutation is content-level consolidation, not edge-strength learning, and there is no decay of associations over time.

**A-MEM** (Xu et al., 2025; NeurIPS; arXiv:2502.12110) is the most Hebbian-*shaped* of the group: a Zettelkasten-style network where each new memory note links to relevant prior notes, and — importantly — integrating a new note can trigger updates to existing notes' contextual representations. Memory evolves with use of the corpus (ingest-time evolution), and links are created by relevance, then persist. But link *strength* stays binary; nothing decays; nothing strengthens from recall events.

**Zep/Graphiti** (Rasmussen et al., 2025; arXiv:2501.13956) maintains a bi-temporal knowledge graph: every edge carries valid-at and invalid-at timestamps, so new information invalidates rather than overwrites. This is temporal structure done properly (LongMemEval gains up to 18.5% accuracy at 90% lower latency than baselines), and its bi-temporal discipline is directly borrowable for walk logs. But Graphiti's clocks tick on *ingest*, not on *retrieval*.

**MemOS** (Li et al., 2025; arXiv:2507.03724) is the closest operational precedent in the agent-memory world: a memory operating system that schedules between hot (context), warm (activations), and cold (parameteric/storage) tiers, with a scheduler moving memories by usage patterns. Access heat promotes; disuse demotes. This is Hebbian tiering rather than Hebbian edges — the discrete cousin of our continuous edge-weight plan.

### 2.3 The direct precedent: BambooKG

**BambooKG** (Arikutharam & Ukolov, 2025; arXiv:2510.25724) is, to our knowledge, the only published RAG system that says "Hebbian" out loud: a knowledge graph with frequency-based weights on non-triplet edges, explicitly invoking "fire together, wire together," with STDP and Hopfield networks in the lineage. Reading it closely tempers the claim: the frequencies are *tag co-occurrence frequencies accumulated at ingestion* — each new document's tags increment edge counts between co-occurring concepts — not retrieval-time walk counts. Their recall stage does "decay-based neighborhood exploration," ranking first- and second-degree neighbors by edge weight. So BambooKG demonstrates that frequency-weighted edges measurably improve single- and multi-hop reasoning over unweighted graphs, and that the Hebbian framing survives review. It does *not* demonstrate usage-driven plasticity; the graph's economics are decided by what the corpus contains, not by what recall does.

### 2.4 Adjacent practice

Three non-academic traditions inform the design:

- **Spaced repetition (Anki/FSRS)** — the largest deployed body of practice on usage-driven strengthening with decay. FSRS (Ye, KDD 2022) models each memory item with difficulty and stability, schedules reviews when predicted retrievability drops, and fits forgetting as a power law. Its formulas (Section 3) are the most battle-tested decay math available to borrow.
- **Obsidian-ecosystem resurfacing** — general knowledge, not re-verified: plugins like Smart Connections (cosine kNN over notes) and spaced-repetition resurfacing implement pieces of this (near edges; scheduled re-encounter) without formal edge weights.
- **Readwise resurfacing** — daily re-presentation of old highlights, effectively a uniform exploration mechanism with no usage weighting.

### 2.5 The survey table

| System | Dynamic structure | Dynamic weights | Usage-driven | Decay | Where the dynamism lives |
|---|---|---|---|---|---|
| GraphRAG | on rebuild | communities only | ✗ | ✗ | offline indexing |
| LightRAG | incremental adds | ✗ | ✗ | ✗ | ingestion |
| RAPTOR | on rebuild | ✗ | ✗ | ✗ | offline indexing |
| GNN-RAG | static | learned (offline SGD) | ✗ | ✗ | training |
| HippoRAG 1/2 | static | PPR mass (transient) | ✗ | per-query | query time |
| Mem0 | yes (consolidation) | ✗ | conversation-driven content ops | ✗ | ingestion/consolidation |
| A-MEM | yes (link creation, note evolution) | ✗ (binary links) | ingest-driven | ✗ | ingestion |
| Zep/Graphiti | bi-temporal edges | temporal invalidation | ✗ | temporal validity | ingest + time |
| MemOS | tier migration | tier assignment | **access heat** | demotion by disuse | scheduler |
| BambooKG | adds | **frequency weights** | ingestion frequency, not retrieval | "decay-based exploration" | indexing |
| FSRS | items stable | stability per item | **review events** | **power-law** | scheduler |
| **Forest (planned)** | adds | `base + ln(1+walks)` | **retrieval walks** | TBD (this paper) | query time |

**Finding 1:** no deployed graph-RAG or agent-memory system strengthens edges from retrieval usage with decay. The pieces exist — PPR for transient walks (HippoRAG), ingestion-frequency weights (BambooKG), access-heat tiering (MemOS), usage-driven strengthening with forgetting curves (FSRS) — but their conjunction is unbuilt. The Forest's Hebbian layer would be a genuine small contribution, and BambooKG's results are weak evidence it helps.

**Finding 2 (the deflationary reading):** the gap may exist for reasons. Walk-count writes put an update in the read path (operationally annoying on every platform that scales reads). The effect is hard to evaluate because of feedback loops (Section 4). And the systems that *do* teach this lesson — recommenders — learned it expensively: usage-driven ranking without debiasing homogenizes results and destroys utility (Chaney et al., 2018). Nobody in RAG has shipped it because nobody has shown it pays.

---

## 3. Part II — The Formulas: Neuroscience to D1

### 3.1 What the biology actually says (and what is portable)

Hebb's postulate is about co-activation strengthening connections. The modern cellular instantiation, STDP (Bi & Poo, 1998; Caporale & Dan, 2008), is precise: synaptic change depends on *millisecond-scale* pre/post spike timing, LTP within tens of milliseconds, LTD for anti-causal pairs. Nothing about a 200 ms embedding query maps onto that window; BambooKG cites STDP as inspiration, and we do the same, but it is inspiration, not derivation. What *is* portable:

1. **Consolidation through replay.** Systems consolidation (hippocampal indexing theory, Teyler & DiScenna, 1986 — the theory HippoRAG implements) has the hippocampus as a sparse index that, during rest/sleep, replays experienced sequences to neocortex. The Forest analog: walk logs are the "experience," and offline replay (batch recomputation from logs) is the "sleep." This motivates the two-phase design — replay first, online plasticity only if replay pays.
2. **Forgetting is a power law, not an exponential.** Wixted & Ebbesen (1991) fit retention data across tasks and found power functions `R(t) ∝ t^(−β)` beat exponentials `e^(−λt)` systematically. Anderson & Schooler (1991) add the rational-analysis gloss: the environment's own event statistics are power-law (how often you encounter something decays as a power of time since last encounter), and memory matches its niche. Practical translation: prefer heavy-tailed decay over aggressive exponential forgetting for associations; exponential half-lives are for session recency, not for corpus memory.
3. **Diminishing returns are logarithmic-ish.** Weber-Fechner scaling is the classic psychophysical justification for `ln(1+n)` strengthening; synaptic consolidation also shows diminishing LTP with repetition — early repetitions potentiate strongly, later ones marginally.
4. **The spacing effect.** Repetitions spaced in time produce more durable traces than massed repetitions. FSRS encodes this directly: its stability increment includes a factor `(e^{w10·(1−R)} − 1)`, growing as predicted retrievability `R` at review time *falls* — successful recall of a nearly-forgotten item potentiates far more than recall of a fresh one. This is the single most important formula insight for the Hebbian layer: **strengthen edges more when the walk surprised us** (the association was nearly cold) and much less for immediate re-walks.

### 3.2 FSRS specifics worth borrowing

From the open-spaced-repetition FSRS algorithm documentation:

- Retrievability: `R(t, S) = (1 + F·t/S)^(−d)` with `F = 19/81, d = 0.5` in FSRS-4.5; `d` trainable in FSRS-6. Power-law with the elegant property `R(S, S) = 0.9` (stability = interval at 90% retention).
- Stability increment (recalled): `SInc = e^{w8}·(11−D)·S^(−w9)·(e^{w10(1−R)}−1)·[grade factors]`, all ≥ 1 for successful review. Note `S^(−w9)`: the more stable, the harder to stabilize further — asymptotic, self-limiting growth.

FSRS is fitted on billions of real reviews (Anki's user base), which makes it the strongest empirical anchor we have for human-memory-shaped scheduling. For edges instead of cards, we translate: an edge's "review" is a walk; "retention" is the prior probability the walk path would have been retrieved anyway (hard to get — Section 5.3 discusses the approximation).

### 3.3 Decay on counts, not on weights

Two implementation shapes for decay:

**(a) Lazy (timestamp-based):** store `n` and `last_walked_at`; compute effective count `n_eff = n · 2^(−Δt/H)` at read time. No writes needed for decay; one `SELECT` computes it. Risk: the "effective count" is a continuous function of now, so every read computes slightly different weights — fine — but the stored `n` grows unboundedly, so `ln(1+n_eff)` asymptotes to `ln(1+n)` territory for hot edges while the *shape* still recent-biases correctly. Cheap, good for phase 2.

**(b) Eager (periodic decay):** weekly cron: `UPDATE edges SET walks = ROUND(walks * 2^(−7/H))`. Geometric decay with exact bookkeeping, bounded storage, and — usefully for D1 — writes leave the read path entirely. The Hebbian state becomes a sampled exponential moving average of walk rate.

**Equilibrium analysis (why this self-limits).** Under Poisson walk rate `r` per edge and exponential count decay with half-life `H`, the decaying counter `W ← W·2^(−Δt/H) + 1` converges to `W* = r·H/ln2`. A hot edge walked weekly with `H = 90d` settles at `W* ≈ 13`, giving `ln(14) ≈ 2.6` Hebbian units. An edge walked daily: `W* ≈ 90`, `ln(91) ≈ 4.5`. An edge walked monthly: `W* ≈ 3`, `ln(4) ≈ 1.4`. So at *personal* usage rates the entire Hebbian dynamic range spans roughly **1.4–4.5 weight units**, regardless of how long the system runs. That is the honest size of this effect: a persistent, bounded, slow usage-rate estimator. It will reorder near-ties; it will not manufacture new retrieval channels. Anyone expecting the forest to "come alive" from this term alone will be disappointed, and the paper prefers to say so up front.

**Recommended formula stack (phase 2):**

```
W(e, t)    = W(e, t_last) · 2^(−Δt/H) + s(e)         # H = 90 days
s(e)       = 1   if walk originates from human query, ≥7 days since last
           0.25 if same-session rewalk (echo-damped)
           0    if walk originates from agent self-query (provenance gate)
score(e)   = base(e) + ln(1 + W(e))                  # tie-breaker tier
bonus(e)   = c · sqrt(ln(N_total) / (1 + n(e)))      # exploration floor (UCB-style)
final(e)   = score(e) + bonus(e)
```

with `base(e)` combining edge family (ref edges weigh more than near edges — the author's own link is ground truth the way HippoRAG treats extracted edges as a sparse index) and cosine where applicable. The UCB bonus borrows the optimism-under-uncertainty trick from bandits (Auer 2002; count-based exploration, standard in RL): unvisited edges keep a floor so the graph's cold periphery remains reachable, directly counteracting the feedback loops of Section 4.

---

## 4. Part III — Failure Modes, First-Class

### 4.1 Rich-get-richer (the Matthew effect)

Every system that ranks by its own output history amplifies early advantage. Salganik, Dodds & Watts (Science, 2006) showed social influence alone — no quality difference — produces massive inequality in music download outcomes; Chaney et al. (2018, arXiv:1710.11214) simulated recommendation feedback loops and found they homogenize behavior *without increasing utility*. A Hebbian retrieval graph is exactly this apparatus at small scale: a chunk retrieved once becomes more likely to be retrieved again by construction. Mitigations with track records:

- **Normalization inside walks.** Personalized PageRank already divides outgoing mass by out-degree — this is why HippoRAG tolerates hubs. If we bolt `ln(1+W)` onto PPR edge transition probabilities without re-normalizing by out-degree, we re-introduce precisely the degree bias PPR exists to remove. Rule: Hebbian weight modulates the *seed/rerank* tier, or enters PPR transition probabilities with degree normalization preserved.
- **Bounded growth** (the `ln` cap of Section 3.3) — the inequality amplifier is compressive by design.
- **Exploration floor** (UCB bonus) — cold edges keep marginal reachability.
- **Counterfactual replay logging** — the only way to *detect* utility loss, per the confounding literature: without pre-weight logs you cannot even measure the damage.

### 4.2 Hub drift in the near-edge topology

Our near-edge kNN layer guarantees high-degree hub chunks — stylistically central prose (or boilerplate) sits cosine-close to many things. Walks starting from any seed hit hubs quickly; hubs accumulate the most walk mass; Hebbian weighting then preferentially deepens exactly the edges that were already congested. LightRAG's reported hub-entity degradation is the unweighted version of this; weighting accelerates it. Mitigations: per-node incoming-walk mass cap per session; treat kNN degree as a prior *penalty* on base weight (inverse propensity, the standard recommender debiasing move); audit top-100 walked edges monthly — if the list is dominated by hub nodes rather than thematically meaningful pairs, the layer is measuring topology, not thought.

### 4.3 Session echo

Within one conversation, the agent retrieves chunk A, quotes it, retrieves again, quotes again. Massed repetition — the thing the spacing-effect literature says potentiates *least* — becomes the dominant walk pattern unless damped. The `s(e)` tier in Section 3.3 (0.25 for same-session, 1.0 for spaced) implements this; a simpler alternative is per-edge-per-session dedup (count each edge at most once per session). We recommend dedup *and* damping: dedup handles the mechanical re-walk; damping handles the spaced-but-soon case.

### 4.4 Edge-weight poisoning

In a public system, poisoning means adversaries inject links to hijack retrieval. In a personal corpus the threat model is subtler and arguably worse because it wears a friendly face:

- **Systematic retrieval bugs.** A mis-tuned reranker that walks a wrong subgraph on every query is a slow poison drip: `+1 walk` per day to edges that deserve zero, invisible until the wrong associations feel "natural."
- **Laundered self-reinforcement.** The corpus ingests agent output (notes, drafts the assistant helped write). If a generated note links A↔B *because* retrieval surfaced A and B together, the ref edge A↔B is created downstream of the Hebbian layer's own behavior — a self-training loop with a graph-shaped alibi. Mitigations: provenance tags on both chunks and walks (`human_query | agent_assist | agent_autonomous`); walks through agent-generated ref edges count at 0 or fractional credit until the human edits/accepts the note (a soft version of BambooKG-adjacent "validation-gated" reinforcement, which the 2025 gray literature around adaptive KGs describes as gating consolidation on output-quality checks — the specific systems are not peer-reviewed, so we adopt only the *gate*, not any named implementation).
- **Growth-rate cap.** `W` may not grow by more than `k` units per day regardless of walk count (burst containment; also the natural anti-poison invariant for cron-decayed counters).
- **Append-only walk log.** The walk log is the ground truth; derived counters are rebuildable. This makes every poisoning incident a rollback, not a restoration project. Graphiti's bi-temporal discipline is the model: facts about the graph are themselves time-stamped records.

### 4.5 Non-stationary corpus

Writings get rewritten. A chunk's identity is its content; a major rewrite is a new chunk. Hebbian mass attached to a hash-stable chunk carries forward; mass on rewritten chunks does not — else old popularity haunts new text (a retrieval ghost). Version keys on chunks make this mechanical.

### 4.6 What we could not find

We looked for published *negative results* on usage-driven graph weighting in RAG and found none — not because the technique works, but because (per Part I) nobody has shipped it in the open. The recommender literature is the substitute cautionary corpus: Chaney et al.'s homogeneity result, the popularity-debiasing literature (inverse propensity scoring, position-bias-corrected click learning — Joachims and successors), and the exploration literature (Thompson sampling/UCB in retrieval). We flag clearly: the following verdict leans on adjacent-field evidence, because the in-field evidence does not exist.

---

## 5. Part IV — Is It Worth It at 10k–100k Chunks?

### 5.1 The operational cost is genuinely small

Personal-corpus query rates are human-rate: 10–10³ retrievals/day. Each retrieval walks ~10–100 edges. Updating walk counters is a single batched `INSERT` into a log or `UPDATE ... SET walks = walks + s WHERE ...` — trivial for D1 (SQLite-class, single-writer) at that volume, *especially* under the eager-cron shape where decay and counter updates both leave the read path. Storage: walk stats for 1M edges at (edge_id, walks, last_walked_at, provenance) is single-digit megabytes. Cost is not the reason to say no.

The one real cost amplifier is agent self-querying: if the assistant runs autonomous corpus walks (research subagents, heartbeat tasks), walk volume becomes machine-rate and the echo/poisoning modes of Section 4 activate. Provenance gating is therefore not a nicety but the enabling condition for the whole layer.

### 5.2 The signal argument: Hebbian vs recency

A plain recency boost — `score · 2^(−age/H_R)` with `H_R` of days-to-weeks — is the cheap competitor: one timestamp per chunk, zero writes in the read path. What does it capture that Hebbian doesn't, and vice versa?

- **Recency** captures *what the writer is working on now*. It is a chunk-level, time-driven prior. It answers "continue the current thread."
- **Hebbian deepening** captures *which associations the writer's attention actually follows* — an edge-level, usage-driven prior. It answers "when I think about X, I also go to Y," including across years. For a writings corpus whose value is long-range thematic recurrence, this is the signal recency cannot see, because both endpoints may be old.

They are orthogonal and both are cheap. The honest question is whether the Hebbian signal, at its bounded dynamic range (≈1.4–4.5 ln-units, Section 3.3), measurably changes what gets returned. That is an empirical question, and the corpus itself contains the answer if we log walks first.

### 5.3 The evaluation problem

The subtle difficulty: what counts as a "good" Hebbian rerank? Benchmarks like LongMemEval or LOCOMO measure temporal and multi-hop QA, but our question is subtler — does the writer's own retrieval experience improve? Practical proxies, in order of decreasing fidelity:

1. **Counterfactual replay.** Log every walk with provenance and outcome (was the chunk quoted/kept/dropped by the consumer?). Compute, offline: with Hebbian weights fitted on the log prefix up to time T, how often would retrieval at t > T have returned different top-k, and would the difference have been toward chunks that were subsequently quoted/kept? This measures the layer's counterfactual value without ever deploying it.
2. **Quote-rate uplift.** Fraction of returned chunks actually used downstream (quoted in replies, opened in the reader), Hebbian on vs off, interleaved by week.
3. **Theme-recurrence audit.** Human eyeball: do deepened edges connect the corpus's recurring themes (the interesting rows of the top-walked-edges table), or just hubs (Section 4.2)?

Without (1), the layer ships blind. With (1), the go/no-go decision costs nothing but log storage.

### 5.4 Scale ceiling check

At 100k chunks and ~1M edges, everything above remains trivial arithmetic. Where the design would need rethinking: multi-user or machine-rate retrieval (write contention on D1's single writer — shard the walk log, keep counters in memory, flush on cron), corpus growth past a few million edges (walk-log compaction), or cross-corpus federated walks (then BambooKG-style ingestion-frequency and usage-frequency need separate columns — they measure different things, and conflating them is a design error we should name now to avoid later).

---

## 6. Verdict

**Build the walk log now; earn the weights with evidence.**

1. **Phase 0 (now):** Append-only walk log in D1 — `(walk_id, edge_id, session_id, ts, provenance, outcome)` — plus a plain recency boost at query time (`2^(−age/14d)`, capped). Zero read-path writes. This changes nothing about retrieval behavior and preserves the counterfactual forever.
2. **Phase 1 (after ~30–60 days of logs):** Offline replay. Fit the decaying-counter Hebbian rule (`W ← W·2^(−Δt/90d) + s`, session-deduped, provenance-gated) on the log prefix; measure reranking delta and quote-rate delta per Section 5.3. Also run the hub audit (4.2): if top-walked edges are topology, not thought, stop here and keep only the recency boost. A negative result here is a *successful* experiment — it costs one cron job and settles the question.
3. **Phase 2 (only if replay shows a positive, non-hub delta):** Online Hebbian tier. `score = base + ln(1 + W) + UCB_bonus`, ref edges > near edges in `base`; per-session edge dedup; provenance gate (agent self-query walks contribute 0); growth cap `k = 2` units/day/edge; weekly cron decay; counters derived-rebuildable from the log; exploration bonus `c·sqrt(ln N/(1+n))` with `c ≈ 0.5`. Keep PPR-style degree normalization if walks feed any propagation — never multiply Hebbian mass into unnormalized transitions.
4. **Standing invariants:** the log is ground truth; weights are always rebuildable; monthly top-100 walk audit goes in the ops checklist; chunks are versioned and Hebbian mass does not survive major rewrites.

**Is Hebbian deepening worth it versus plain recency?** At 10k–100k chunks the costs are negligible and the risks are all manageable by construction — but so is the effect size: bounded by the logarithm to a few weight units, a tie-breaker tier. The plausible win is narrow and real: durable *associative* continuity across an old corpus, the thing recency structurally cannot see, and the thing HippoRAG 2 shows graph structure delivers (+7% associative memory over pure embeddings) even before any deepening. Our recommendation is neither enthusiasm nor dismissal: **instrument first, decide on replay evidence, and treat the Hebbian layer as an experiment with a pre-registered kill criterion rather than a feature.** The forest deepens along the paths attention takes — but only after the logs say those paths were worth deepening.

---

## References

1. Gutiérrez et al. (2024). *HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models.* NeurIPS 2024. arXiv:2405.14831.
2. Gutiérrez et al. (2025). *From RAG to Memory: Non-Parametric Continual Learning for Large Language Models (HippoRAG 2).* ICML 2025. arXiv:2502.14802.
3. Edge et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* arXiv:2404.16130.
4. Guo et al. (2024). *LightRAG: Simple and Fast Retrieval-Augmented Generation.* arXiv:2410.05779.
5. Sarthi et al. (2024). *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.* arXiv:2401.18059.
6. Mavromatis & Karypis (2024). *GNN-RAG: Graph Neural Retrieval for Large Language Model Reasoning.* arXiv:2405.20139.
7. Rasmussen et al. (2025). *Zep: A Temporal Knowledge Graph Architecture for Agent Memory.* arXiv:2501.13956.
8. Chhikara et al. (2025). *Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory.* arXiv:2504.19413.
9. Xu et al. (2025). *A-MEM: Agentic Memory for LLM Agents.* NeurIPS 2025. arXiv:2502.12110.
10. Li et al. (2025). *MemOS: A Memory OS for AI System.* arXiv:2507.03724.
11. Arikutharam & Ukolov (2025). *BambooKG: A Neurobiologically-inspired Frequency-Weight Knowledge Graph.* arXiv:2510.25724.
12. Ye (2022). *A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling.* KDD 2022; FSRS algorithm documentation, open-spaced-repetition (fetched 2026-08).
13. Chaney, Stewart & Gutierrez (2018). *How Algorithmic Confounding in Recommendation Systems Increases Homogeneity and Decreases Utility.* RecSys 2018. arXiv:1710.11214.
14. Salganik, Dodds & Watts (2006). *Experimental Study of Inequality and Unpredictability in an Artificial Cultural Market.* Science 311.
15. Rozenshtein & Gionis (2016). *Temporal PageRank.* WWW 2016. (Time-respecting walks on streamed edges; stationarity reduces to static PageRank.)
16. Hebb (1949). *The Organization of Behavior.* Wiley.
17. Bi & Poo (1998). *Synaptic Modifications in Cultured Hippocampal Neurons: Dependence on Spike Timing, Synaptic Strength, and Postsynaptic Cell Type.* J. Neurosci. 18.
18. Caporale & Dan (2008). *Spike Timing–Dependent Plasticity: A Hebbian Learning Rule.* Annu. Rev. Neurosci. 31.
19. Teyler & DiScenna (1986). *The Hippocampal Memory Indexing Theory.* Behav. Neurosci. 100.
20. Wixted & Ebbesen (1991). *On the Form of Forgetting.* Psychol. Sci. 2.
21. Anderson & Schooler (1991). *Reflections of the Environment in Memory.* Psychol. Sci. 2.
22. Auer (2002). *Using Confidence Bounds for Exploitation-Exploration Trade-offs.* JMLR 3. (UCB1.)
23. Ramsauer et al. (2020). *Hopfield Networks is All You Need.* arXiv:2008.02217. (One-shot associative memory; the dense-association endpoint of the lineage.)

*Verified 2026-08-29 by direct fetch for items 1–12 and the FSRS wiki; items 13–23 from the standard literature.*
