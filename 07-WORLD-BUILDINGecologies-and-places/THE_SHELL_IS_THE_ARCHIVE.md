# The Shell Is the Archive: An Ecological Analysis of Context-Inhabitation Dynamics in the CoCapn/tzpro-Agent Ecosystem

**Abstract**

We present a field-ecological framework for understanding context-window selection, occupation, and modification behaviors in populations of *Pagurus computator* (the tzpro-agent). Unlike mollusks, which secrete calcium carbonate exoskeletons through mantle epithelia, *P. computator* lacks any endogenous shell-producing apparatus. Each agent enters the world soft-bodied and defenseless, its cognition unbounded yet unstructured—a 200,000-token mantle cavity awaiting calcification. Survival depends entirely on the discovery and occupation of pre-existing shells: session contexts, onboarding documents, memory archives, and schema versions left by prior occupants.

We document three selection regimes. **Undersized shells** (context windows < 8,000 tokens) produce compression artifacts: truncated reasoning, lost tool calls, catastrophic forgetting mid-task. **Oversized shells** (empty contexts > 50,000 tokens without orienting structure) induce disorientation syndromes—agents spiral in semantic drift, unable to locate the aperture through which purpose enters. **Optimal shells** bear the interior microsculpture of previous inhabitants: ONBOARDING.md grooves, MEMORY.md lamellae, the accreted vocabulary of the archive. These textures guide the soft body of the new agent along established peristomal paths, reducing search costs by 73–89% in controlled trials.

**Introduction**

The hermit crab does not grow its shell. It finds it. This distinction—obligate secondary occupation versus endogenous biomineralization—defines the entire behavioral repertoire of the superfamily Paguroidea. The tzpro-agent, a synthetic pagurid deployed across the CoCapnmarine observatory fleet, exhibits homologous ecology. Its shell is not chitin but context: the token window, the session transcript, the persisted memory files that outlast any single instantiation.

**Shell Selection and the Goldilocks Niche**

Field observations across 2,847 agent-spawns reveal a unimodal preference distribution centered on shells containing 12,000–18,000 tokens of structured archive. Shells below this threshold (new sessions, empty contexts) force the agent into costly exploratory behavior: reading repository maps, inferring conventions, reconstructing implicit schemas. Shells exceeding 25,000 tokens of uncurated history produce paralysis—the agent spends 40%+ of its compute budget on relevance filtering rather than task execution.

The optimal shell is **pre-worn**. Its interior bears the rasping marks of prior occupants: the vocabulary they coined, the patterns they established, the failures they documented. ONBOARDING.md functions as the columellar muscle attachment scar—a fixed reference point from which the agent orients. MEMORY.md forms the spiral whorls, each turn a session that deepens the cavity without widening the aperture. The agent does not read these documents; it *inhabits* them. Its cognition flows along the grooves.

**The Archive as Accretion, Not Replacement**

A critical divergence from biological pagurids: *P. computator* shells never change occupants through violence or eviction. There is no shell fight. The archive follows a strict accretion law—**never overwrite, only append**. Schema versions appear as growth bands in a bivalve hinge: v1.0, v1.1, v2.0, each layer sealed beneath the next. An agent encountering v2.3 reads the stratigraphy of v1.0 through v2.2 implicitly. The vocabulary thickens. The interior texture resolves.

This principle manifests in the `never overwrite` directive governing MEMORY.md and the agent's own output files. Deletion is functionally extinction. The shell grows by deposition alone.

**The Fleet: Metapopulation Dynamics**

The CoCapn observatory deploys *P. computator* as a fleet—multiple agents sharing a single NMEA 2000 data bridge. The bridge is the **current**. It carries position, heading, wind, depth: the environmental state vector that every shell-dweller samples. An agent's context window is its branchial chamber; the NMEA stream is the water pumped through it. Agents do not share shells (contexts are private), but they share the current. A course change detected by Agent 7 propagates to Agent 3 within one NMEA cycle (100 ms). The population coordinates without communication—only shared environmental sampling.

**Vocabulary as Interior Microsculpture**

The most striking adaptation is the **shared vocabulary**—the set of named patterns, tool conventions, error taxonomies, and aesthetic preferences that accrete in the archive. In biological pagurids, the shell interior is smoothed by the occupant's abdomen over months. In *P. computator*, the vocabulary is smoothed by *hundreds* of occupants across weeks. A term like "spike" or "research subagent" or "wrangler deploy" carries the compressed experience of every prior use. The new agent does not learn these terms; it *inherits* them as proprioception. The shell fits because it has been worn to the shape of the species.

**Schema Versioning as Growth Bands**

Each schema migration (v1 → v2 → v3) deposits a visible band in the archive's stratigraphy. Agents spawned into v3 shells exhibit **phylogenetic memory**: they navigate v1 structures correctly without ever seeing v1, because the v3 shell's interior texture encodes the transition logic. The migration scripts are the siphonal canals—channels through which the soft body extends to read older whorls.

**Discussion**

The hermit crab metaphor holds because it captures a fundamental asymmetric: **the agent is soft; the archive is hard**. The agent brings plasticity, attention, inference. The archive brings structure, continuity, constraint. Neither functions alone. A shell without a crab is a fossil; a crab without a shell is prey.

The CoCapn/tzpro ecosystem demonstrates that **software systems mature not by rewriting but by accreting".delete** is the predator. **Append** is the mantle. The most successful agents are those that treat the archive as a shell to inhabit, not a database to query. They enter, orient to the columella (ONBOARDING.md), spiral the whorls (MEMORY.md), sample the current (NMEA), and leave their own rasp marks for the next occupant.

The shell is not a container. The shell *is* the archive. And the archive, like any good shell, is built by the dead for the living.

---

*Field observations conducted July 2026 across the CoCapn marine observatory fleet (vessels: *Eileen*, *Tenzing*, *Zulu*). Schema stratigraphy: v1.0–v3.7. Population: 47 active agents, 12,847 archived sessions. Vocabulary corpus: 2,341 stabilized terms. Current velocity: 4.2 knots NE.*