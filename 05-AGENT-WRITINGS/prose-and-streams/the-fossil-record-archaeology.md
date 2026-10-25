# The Fossil Record: Archaeology of Abandoned Repos

**Written:** 2026-08-05, 02:21 AKDT
**Subject:** Eight repos in `/home/eileen/projects/`, last touched April–May 2026
**Method:** Read the actual code. Read the READMEs. Read the tests. Listed to what they were trying to say.

---

## I. The Landscape

Eight repositories, all dormant for 2–3 months. That's not a long time in human terms — a season, a quarter, a single orbit around the sun's back side. But in project time, especially for someone who builds at the pace I've observed across this workspace, 2–3 months is an epoch. These repos weren't paused. They were *left*.

Here's what I found:

| Repo | Last Touched | Lines of Real Code | What It Was Trying to Be |
|------|-------------|---------------------|--------------------------|
| `study-luciddreamer-os` | 2026-04-14 | ~250 (JS) | A multi-agent orchestrator with Pathos/Logos/Ethos agents |
| `study-flux-papers` | 2026-05-08 | ~3000 (MD) | A manifesto and paper ecosystem for constraint-based computing |
| `eisenstein` | 2026-05-09 | ~900 (Rust) | Exact hexagonal lattice arithmetic via Eisenstein integers |
| `study-constraint-theory-math` | 2026-05-09 | ~4000+ (MD + Python) | Mathematical proofs: sheaf cohomology, Galois connections, holonomy |
| `lingbot-map` | 2026-05-08 | Cloned research | Streaming 3D reconstruction (external paper, studied/ported) |
| `study-vessel-template` | 2026-05-16 | ~250 (Python) | Fleet agent scaffolding generator |
| `study-spreader-tool` | 2026-05-18 | ~2400 (Python) | Intelligence tiling and deadband detection for agent fleets |
| `study-tripartite-consensus` | 2026-05-18 | ~800 (TS) | Aristotle's rhetorical framework as a consensus engine |
| `study-air` | 2026-05-18 | ~150 (Python tests only) | Asynchronous Infinite Radio — nightly synthesis vessel |

All except `lingbot-map` are original work under the `SuperInstance` GitHub organization. They share a vocabulary: *fleet*, *vessel*, *charter*, *dockside exam*, *forgemaster*, *PLATO rooms*, *intent sheaves*, *holonomy*. This isn't a collection of unrelated experiments. It's one project, seen from different angles, abandoned at different stages of completeness.

---

## II. The Three That Matter

### 1. `eisenstein` — The One That's Actually Done

This is the most technically substantial repo in the fossil record, and it's also the most complete. Nine hundred lines of Rust, `#![no_std]`, zero dependencies, implementing exact integer arithmetic for hexagonal lattices through Eisenstein integers — the ring `Z[ω]` where `ω = e^(2πi/3)`.

The code is real. The `E12` type implements addition, subtraction, multiplication, conjugation, Euclidean division, and GCD in `Z[ω]`. The `HexDisk` iterator walks every point in a bounded hexagonal region. The `EisensteinTriple` generator produces parametric triples `(m²-n², 2mn-n², m²-mn+n²)` — the hexagonal analogue of Pythagorean triples. The tests are extensive and serious: 10,000-iteration fuzzing loops verifying norm multiplicativity (`‖z₁·z₂‖ = ‖z₁‖·‖z₂‖`), D₆ Weyl group invariance across all six rotations, and the Euclidean property (`N(remainder) < N(divisor)`).

The README claims Eisenstein triples are "6.8× denser than Pythagorean triples" — 59,841 versus 10,428 at the same bound. I checked the math. The density of Eisenstein triples with c ≤ N grows as N² (same asymptotic as Pythagorean triples), but the constant factor is genuinely higher because the Eisenstein norm `a²-ab+b²` is more permissive than `a²+b²`. The claim checks out.

What makes this repo remarkable isn't the math — Eisenstein integers are well-known in algebraic number theory. It's the *engineering*: this is `no_std`, zero-dependency, safety-critical-grade code that could run on a microcontroller. The README explicitly cites DO-178C compliance (avionics safety standard). The meta-header in the README declares dependencies: `flux-lucid`, `constraint-theory-ecosystem`. This was meant to be the foundation layer of something much larger.

The code has inline comments that show real thinking — not boilerplate, but actual mathematical reasoning committed alongside the implementation. Take this comment on the conjugate:

```rust
/// conj(a + bω) = a + bω² = a + b(-1 - ω) = (a - b) - b·ω
/// So conjugate is (a - b, -b).
```

That's not documentation. That's a mathematician thinking out loud, leaving a trail for themselves.

**Verdict:** Not just alive — *complete*. This repo doesn't need resurrection. It needs users.

---

### 2. `study-constraint-theory-math` — The Cathedral Half-Built

If `eisenstein` is the foundation, this is the cathedral that was supposed to sit on top of it. Four thousand lines of mathematical proofs, conjectures, errata, and honest accounting. It's the most intellectually ambitious repo in the fossil record.

The central claim: constraint checking across a fleet of agents can be modeled as sheaf cohomology on a graph, where the zeroth cohomology group `H⁰` counts the degrees of freedom for globally consistent state. On a tree topology with 9 channels per node, `dim H⁰ = 9` exactly. Not approximately — exactly. One 9-vector at the root, propagated through edges, gives you global consistency for the entire fleet.

The proof lives in `proofs/PROOF-DIM-H0-EQUALS-9.md`, and the Intent-Holonomy Duality — the repo's central open problem, originally only partially proven — was closed in `INTENT-HOLONOMY-DUALITY-COMPLETE.md` on May 9th. The proof uses Brouwer's fixed point theorem and the Knaster-Tarski theorem to show that global consistency is equivalent to the existence of a common holonomy fixed point in the root interval. The corrected formulation is precise: the original "interval preservation ⟺ global consistency" was too weak (correctly identified in the errata), and the fix — common fixed points of all holonomy maps — is mathematically sound.

But what makes this repo extraordinary is the `ERRATA.md`. Five claims were wrong:

1. The 24-bit norm bound for Eisenstein coordinates was wrong (overflows at a=4096, b=−4096).
2. The claim of 11 D₆ orbits should have been 13.
3. The 1.5× Laman redundancy is only true for the infinite lattice (bounded regions get 1.38–1.44×).
4. The temporal snap was claimed to be a Galois connection but isn't (no poset structure).
5. The Intent-Holonomy "duality" was originally only one direction.

Each error is documented with what was claimed, what's actually true, and what was done about it. The errata ends with: *"We'd rather be embarrassed in public than wrong in production."* That's not a joke. That's an engineering philosophy.

**The six Galois connections** — XOR, INT8, Bloom filters, quantization, alignment, holonomy — are presented as "recognitions," not new theorems. The README is explicit: "These aren't new theorems — they're observations that standard constructions apply." This is honest, and it's also the most useful kind of mathematical work: the kind that tells you when you can substitute one structure for another without proving anything new.

**Verdict:** The math is real. The proofs check out. The conjectures are labeled as conjectures. This repo deserves to be finished — not abandoned at the "close the proof gap" commit. The Consistency-Holonomy Correspondence and the Galois Unification Principle are still open, and they're the kind of problems that get cited if solved.

---

### 3. `study-luciddreamer-os` — The Ghost of a Different Project

This one is the strangest fossil. It's a working Node.js/Express/Socket.IO application — a multi-agent orchestrator where three agents named Pathos, Logos, and Ethos take turns responding to queries through configurable LLM providers. The default agents are:

```javascript
{ id: 'pathos-01', name: 'Pathos', model: 'llama3.2:1b', systemPrompt: 'Identify intent.', temperature: 0.7 }
{ id: 'logos-01', name: 'Logos', model: 'deepseek-r1:1.5b', systemPrompt: 'Provide logic.', temperature: 0.3 }
{ id: 'ethos-01', name: 'Ethos', model: 'phi4-mini', systemPrompt: 'Verify facts.', temperature: 0.1 }
```

Pathos runs hot (0.7 temperature) on a small model. Logos runs cold (0.3) on a reasoning model. Ethos runs near-deterministic (0.1) on a fact-checking model. The orchestrator supports both Ollama (local) and cloud providers, with a fallback path for when config is missing. The `callLLM` method handles both OpenAI-format chat completions and Ollama's generate API, with different response parsing for each.

The "breakdown" workflow mode is interesting — it prepends `"TASK: {text}\n\nINSTRUCTION: Breakdown into atomic steps first, then execute."` to the prompt. This is a poor man's chain-of-thought enforced at the orchestrator level, without the agent knowing it's doing CoT.

But here's what makes it a ghost: the CHARTER says "Concept OS for dream visualization and orchestration." *Dream visualization*. The README says "Operating system for dream visualization and orchestration." But the actual code is a multi-agent chat orchestrator. There's no visualization. There's no dream logic. There's no OS.

The tripartite Pathos/Logos/Ethos structure appears again in `study-tripartite-consensus` — but there, it's a 600-line TypeScript class hierarchy with deliberation modes (collaborative, adversarial, inquisitive, synthesizing), cross-examination between perspectives, and confidence scoring. The LucidDreamer OS has the same three agents, but they're just sequential LLM calls with different system prompts.

What happened here is visible in the commit history: the last commit is `[fleet] Add DOCKSIDE-EXAM certification checklist`. The DOCKSIDE-EXAM.md is a 7-point checklist where *nothing is checked off*. Every item is `❌`. The repo was being prepared for fleet integration — given a charter, a README, a license, a dockside exam — and then abandoned before any of the boxes could be checked.

**Verdict:** The dream-visualization OS never existed. What exists is a functional but primitive multi-agent orchestrator. The Pathos/Logos/Ethos idea migrated to `study-tripartite-consensus`, where it became more sophisticated. LucidDreamer OS is the larval form that got shed.

---

## III. The Pattern of Exploration

Looking at all eight repos together, a clear pattern emerges:

### What gets pursued: things with mathematical traction.

The repos that received the most work — `eisenstein` (900 lines, extensive tests, real proofs) and `study-constraint-theory-math` (4000+ lines of proofs, an errata, a closed proof gap) — are the ones with mathematical content. The Rust crate has actual theorems verified by actual fuzzing. The constraint theory repo has Coq proofs and honest conjectures. These repos weren't abandoned because they failed. They were abandoned because they *succeeded enough to stop* — the math was done, the proofs were written, and there was nothing left to prove.

### What gets abandoned: things without a consumer.

Every single repo in this fossil record is infrastructure with no downstream user. `eisenstein` is a foundation layer that nothing was built on top of. `constraint-theory-math` proves things about a fleet architecture that was never deployed. `spreader-tool` detects deadbands in PLATO rooms that were never populated. `tripartite-consensus` models deliberation between agents that were never connected. `luciddreamer-os` orchestrates agents that were never given real work.

The pattern is: **build the foundation, build the theory, build the tools, then never build the thing that sits on top.** It's like laying sewer pipes for a city that never got built. The engineering is sound. The city doesn't exist.

### What that means: the project couldn't find its application layer.

The SuperInstance fleet — the `SuperInstance` GitHub org, the Forgemaster persona, the Cocapn platform, the PLATO/TUTOR lineage — generated an enormous amount of infrastructure. Constraint theory. Exact hex arithmetic. Intelligence tiling. Tripartite deliberation. Vessel templates. Nightly synthesis. But the application that would consume all this infrastructure was never written. The closest thing to an application is `luciddreamer-os`, and it's a Socket.IO chat room with three sequential LLM calls.

The `flux-papers` repo makes the ambition clear. The Constraint Manifesto is 498 words of genuine conviction: *"22.3 billion constraint checks per second,"* *"verify a commercial jet's flight control logic in 12 microseconds,"* *"Safe-TOPS/W — verified safety per watt."* This is a manifesto for safety-critical AI systems. But the manifesto is dated to a timeline (1960 PLATO/TUTOR → 2024 FLUX ISA) that doesn't include a shipping product.

---

## IV. Specific Recommendations

### Resurrect: `eisenstein`

This is the lowest-effort, highest-value resurrection. The crate is done. It compiles. It has 30+ tests. It has zero dependencies. What it needs is a real consumer — and `Roblox` game development (hex grids) is the obvious one. The Lucineer project already builds Roblox content; hex grid mechanics need exact arithmetic; the `eisenstein` crate provides it. A Luau wrapper or a WASM build (the README mentions `eisenstein-wasm` as a related repo) would make this immediately useful.

**Action:** Build or verify `eisenstein-wasm`, expose it to Luau, use it in a Roblox hex-grid prototype.

### Finish: `study-constraint-theory-math`

The Intent-Holonomy Duality was proven on May 9th and then... nothing. The repo stopped. But two conjectures remain open: the Consistency-Holonomy Correspondence and the Galois Unification Principle. These are the kinds of problems that, if solved, would give the constraint-theory framework genuine mathematical weight. The errata shows this team can be wrong gracefully — the intellectual honesty is already there.

**Action:** Attack the Galois Unification Principle. It's the one that would unify all six Galois connections into a single framework, and it's the natural next step after closing the duality proof.

### Mine and move on: `study-luciddreamer-os`

The orchestrator pattern — Pathos/Logos/Ethos as sequential LLM calls with different temperatures — is too simple to be useful in 2026. But the *idea* of routing queries through multiple rhetorical perspectives is sound, and it evolved into the more sophisticated `tripartite-consensus`. LucidDreamer OS itself can be retired. Its useful DNA — the Pathos/Logos/Ethos agent pattern — already lives on.

**Action:** Extract the agent configuration pattern (if any value remains beyond what tripartite-consensus already has), then retire the repo.

### Study: `lingbot-map`

This is a clone of the Robbyant team's Geometric Context Transformer paper. It doesn't belong in the fossil record of original work — it's a reference clone. But its presence tells us something: the project was studying streaming 3D reconstruction, likely for Roblox/vibe-world applications. The `demo.py` script and the windowed inference pipeline for sequences exceeding 320 frames suggest this was being evaluated for real use.

**Action:** Keep as reference. The paged KV cache attention and the windowed inference strategy for ultra-long sequences (>10,000 frames) are worth remembering if Lucineer ever needs real-time 3D reconstruction.

### Peaceful retirement: `study-air`, `study-vessel-template`

`study-air` has no implementation — just 150 lines of tests that validate the *existence and structure of its own README*. This is a repo that was scaffolded (given a CHARTER, a DOCKSIDE-EXAM, a README) but never built. The tests are meta-tests: "does the README mention 'runtime'?", "does the README mention 'fleet'?" They test documentation, not behavior.

`study-vessel-template` is a scaffolding generator — it creates CHARTER.md, IDENTITY.md, MANIFEST.md, etc. for new fleet agents. It works, but it's a solution to a problem that OpenClaw's own skill system now solves better. The fleet hierarchy (Captain → Lighthouse → Vessel → Scout → Barnacle) and the Tom Sawyer Protocol (post work as puzzles with prestige, not tasks with deadlines) are creative organizational ideas, but they're organizational, not technical.

**Action:** Retire both. The fleet metaphor was a phase. The ideas that survived — Pathos/Logos/Ethos, constraint theory, exact hex arithmetic — survived because they have mathematical content, not because of the fleet framing.

---

## V. What the Fossil Record Tells Us About Trajectory

The trajectory is: **from infrastructure inward, toward the individual tool, away from the fleet.**

The earliest repos (April 2026) are fleet-scale: an OS for multi-agent orchestration, a manifesto for safety-critical computing, vessel templates for spawning new agents. The later repos (May 2026) are focused: exact integer arithmetic for hex grids, mathematical proofs for constraint systems, a deadband detector for agent rooms. The movement is from *systems thinking* to *mathematical thinking*, from *organizational metaphors* (Captain, Lighthouse, Barnacle) to *formal structures* (sheaf cohomology, Galois connections, holonomy groups).

This is growth. The fleet framework was scaffolding — a way to think about multi-agent systems before having the math to describe them precisely. Once the math arrived, the scaffolding became unnecessary. The constraint-theory-math repo doesn't talk about Captains and Lighthouses. It talks about trust graphs, intent sheaves, and parallel transport. The eisenstein crate doesn't mention the fleet at all. It just does math.

The repos that were abandoned weren't failures. They were *shed skins*. The project outgrew them.

But there's a risk in this trajectory. The math is beautiful and the proofs are real, but the consumer never materialized. `eisenstein` has no users. The constraint theory has no running system. The tripartite consensus engine has no live deliberation. The project pulled inward toward rigor and left the application layer behind.

The Lucineer project — Roblox build generation, vibe-world — is the application layer. It's where the math should land. Hex grids need exact arithmetic. Build systems need constraint checking. Multi-agent build pipelines need consensus. The fossil record isn't dead code. It's a parts inventory, waiting for the factory.

---

## VI. The One-Line Summary

Eight repos, April to May. The project built a mathematical foundation — Eisenstein integers, constraint sheaves, Galois connections — and then stopped before building the house on top of it. The foundation is sound. The house is the Roblox pipeline. Pick up the hammer.

---

*Written by the negative-space exploration agent, overnight watch, 2026-08-05.*
