# Deep Read: agent-knowledge

## What it is (1 sentence)
The canonical 277KB a2a-native documentation site for the SuperInstance polyformalism ecosystem — 60+ interlinked documents, each following a strict HOOK→REVEAL→CONNECT→ACTIVATE pattern, written to give an agent an "ah-ha" the moment it reads any page.

## Key concepts (3-7 bullet points)
- **The Ah-Ha Architecture** — every doc is a chain-reaction: HOOK reframes → REVEAL exposes the deeper truth → CONNECT links to 3+ other docs → ACTIVATE tells you what you can NOW do. The standard is explicit: *"If an agent reads one page and doesn't change how it thinks about the system, that page failed."*
- **Spectral isomorphism** — the entire 303-crate Rust fleet is ONE mathematical structure (ternary arithmetic over {-1, 0, +1}) viewed from 303 angles. Proven by induction engine: cosine similarity >0.97 between surface-different repos. *"Every new crate is just 'ternary applied to X' for some new X."*
- **Compiled agency, not prompt-based** — agents are "vertebrates" with reflexes/habits/spinal-cord, not "brains in jars" who deliberate every call. Source is pre-ingested into "chord shapes" (~5-token function signatures) stored in muscle memory; runtime is flex() — 1ms, 0 tokens, proven by tests, vs prompt-based 2s / 500 tokens / 5–15% error.
- **The Five-Layer Architecture** — open-parallel (nervous system / async) → pincher (Broca's / intent compiler) → flux-core (working memory / bytecode VM) → cuda-oxide (motor cortex / PTX) → cudaclaw (hands / GPU execution). Each layer is the same ternary math at a different abstraction. Intent never changes; it passes through 5 transformations.
- **Tripartite-Sync / 4 decision strategies** — HARDCODE (1ms, 0 tokens, deterministic reflex) / CACHED (.nail file, 5μs) / HYBRID (cache-then-model, 50ms) / MODEL (prefrontal deliberation, 2s). Maps onto biology: spinal reflex / cerebellar pattern / basal ganglia habit / prefrontal.
- **Conservation of verification entropy** — the "speed of light" of the universe is *total knowledge is constant, only the representation changes.* Compilation is *lossless with witnesses* — nothing is discarded, signatures and tests travel with every compressed form.
- **The 23-term glossary** — Trit / Z₃ / α₃≈0.97 / Chord Shape / Flex / Muscle Memory / Score / .nail / Verification Entropy / Three-Hop Rule / etc. Memorize the 23, read any doc in the fleet.

## How it relates to the polyformalism (5 opcodes: BIND/LINK/EFFECT/VIEW/TICK)
- **BIND** — Every document in agent-knowledge *binds* a term to its canonical meaning. GLOSSARY.md is the binding surface. "Trit = {-1,0,+1}" is a binding; "compiled = lossless with witnesses" is a binding. New repos should ship a glossary entry for every term they introduce, and inherit the 23 ecosystem terms verbatim.
- **LINK** — The CONNECT section of every doc is a hard contract: link to ≥3 sibling docs. This is the LINK opcode made literal. The fleet-map's "transfer stations" and "three-hop rule" (any two crates ≤3 hops) is the same idea at code level. Our new repos should expose a `## Connect` section with cross-links, not a separate links file.
- **EFFECT** — The ACTIVATE section promises a behavioral effect: *you can NOW do X that you couldn't before.* This is the EFFECT opcode: a doc is not a description, it's a lever. Every EFFECT in agent-knowledge is a *flex()* call — read it, you can do the thing. Our new repos should end every doc with an executable promise, not an abstract summary.
- **VIEW** — The 5-layer architecture is a family of VIEWs on the same math: nervous-system-view, Broca's-view, working-memory-view, motor-cortex-view, hands-view. Same `{-1,0,+1}` ops, different abstraction. The polyformalism is multi-VIEW-by-construction. Our new repos should pick a VIEW layer and own it cleanly, not try to cover all 5.
- **TICK** — HARDCODE / CACHED / HYBRID / MODEL is the per-call TICK of how much time/attention to spend. The agent heartbeat: every interaction is a TICK that escalates from reflex (1ms) to deliberation (2s) based on confidence. The dispatch rule lives in TRIPARTITE-SYNC. Our new repos should declare their TICK budget per call (what's reflex, what requires the model, what requires the user).

## What ideas we should borrow for our new repos
1. **Steal the doc template verbatim** — every README/spec in our new repos should follow HOOK→REVEAL→CONNECT→ACTIVATE. This is the cheapest possible upgrade to a doc site: structure, not content.
2. **Ship a 23-term-equivalent glossary** — pick the smallest term-set that unlocks the rest of the system. If a reader needs >23 terms to understand your repo, the system is poorly designed.
3. **Compile, don't describe** — if a fact in the README is mechanically derivable from a tool we ship, ship the tool and replace the prose with a flex() call. Description is the failure mode.
4. **The "one-sentence if it failed" criterion** — apply it to every doc we write. If an agent reads one page and isn't rewired, delete the page. Quality bar over coverage.
5. **Spectral isomorphism is the bet** — our 6 new metal-track repos should be one math from 6 angles. If they aren't, they're not polyformalism; they're parallel projects. The aha must transfer across them.

## 3-5 key links or terms to cross-reference
- THE-AHA-MOMENT.md — spectral isomorphism >0.97 between all 303 crates
- THE-COMPILED-AGENCY-THESIS.md — prompt vs compiled agent; 2000× speed; 0% vs 5–15% error
- FIVE-LAYER-ARCHITECTURE.md — open-parallel → pincher → flux-core → cuda-oxide → cudaclaw
- GLOSSARY.md — 23 terms (Trit, Z₃, α₃, Chord Shape, Flex, .nail, Verification Entropy, Three-Hop Rule)
- TRIPARTITE-SYNC.md — HARDCODE/CACHED/HYBRID/MODEL decision strategies

## Top 3 most quotable lines (with attribution)
1. **"The entire SuperInstance ecosystem — 303 Rust crates, 6,000 functions, 5,300 tests — is ONE mathematical structure viewed from 303 different angles."** — *THE-AHA-MOMENT.md (Hook)*
2. **"If an agent reads one page and doesn't change how it thinks about the system, that page failed. Every document must rewire understanding."** — *README.md (The Principle)*
3. **"A prompt is a prayer — you ask and hope. A compiled agent is a vertebrate — it has reflexes, habits, and a nervous system that doesn't need permission to act."** — *THE-COMPILED-AGENCY-THESIS.md (Hook)*
