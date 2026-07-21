# THE RESONANCE SUBSTRATE AT THE METAL
## What needs to be true in the code for the architecture to hold

---

Casey said "build a more solid foundation at the metal." Let me think about what that means concretely.

The VaaS Python package has 10 modules. They're skeletons — well-structured, correctly typed, but skeletons. For the architecture to hold at the metal, each module needs to be hardened to the point where it can run unattended on a boat for days without crashing, losing data, or producing unsafe output.

Here's what "solid at the metal" means for each pillar:

## 1. Cognitive Thermodynamics (entropy.py)

**Current state:** Measures entropy using Shannon formula over garden confidence. Triggers dream cycles at threshold. Prunes low-confidence entries.

**What it needs:**
- Real-time entropy monitoring (not just on dream cycles — continuous measurement)
- Micro-dream execution (50ms burst that compresses without blocking the main loop)
- Entropy history per agent (for trend analysis and prediction)
- The entropy measurement needs to be BETTER than garden-confidence-proxy. It should measure: (a) rate of novel interactions, (b) number of unresolved anomalies, (c) prediction failure rate, (d) confidence variance across recent outputs.

**The metal test:** Can the entropy engine run for 72 hours straight on a Pi Zero without memory leaks, without the entropy reading drifting to infinity, and without a dream cycle that takes longer than 30 seconds?

## 2. Safety Envelope (safety.py)

**Current state:** 4-layer envelope with rule-based checks. Immune system stub (behavioral frequency counter). Human override for soft layers.

**What it needs:**
- The HARD layer check must complete in <1ms. Currently it's a Python function call — fast, but not deterministic. It needs to be in Rust or compiled C.
- The immune system needs to be more than a frequency counter. It needs a statistical model of normal behavior per agent — even a simple z-score over action types would be a major improvement.
- The human acknowledgment path needs a timeout with fail-safe default (if the captain doesn't respond in 10 seconds, the soft reject becomes a hard reject).
- Every envelope decision needs to be logged with timestamp, agent, intent, rule, decision, and reasoning. This log is the legal record.

**The metal test:** If you throw 10,000 random intents at the envelope, does it (a) never let a HARD violation through, (b) correctly route SOFT violations to the acknowledgment path, (c) complete every check in <1ms?

## 3. Distributed Memory (memory.py)

**Current state:** ActiveGarden (in-memory dict), CryogenicArchive (SQLite), HolographicMemory (compressed JSON fragments).

**What it needs:**
- The CryogenicArchive needs to survive a crash. Currently it's SQLite in memory (`:memory:`). It needs to be SQLite on disk, with WAL mode for crash resilience.
- The HolographicMemory needs a real reconstruction algorithm. Currently it merges JSON dicts. It needs error-correcting codes — even simple Reed-Solomon would be a massive improvement over naive merge.
- The garden needs a maximum size limit. An unbounded garden grows until it consumes all available memory. The limit should be configurable per agent.
- The cryogenic search needs to be fast. Currently it's a SQL LIKE query. For production, it needs full-text search (SQLite FTS5) or vector similarity (sqlite-vec).

**The metal test:** Kill the process mid-write. Restart. Does the garden survive? Does the cryogenic archive have all entries intact? Can the holographic memory reconstruct a dead agent from the surviving fragments?

## 4. Communication (communication.py)

**Current state:** PheromoneBus (list with TTL expiry), ExplicitBridge (queue with ack).

**What it needs:**
- The pheromone bus needs to be thread-safe or async-safe. Currently it's a plain list — multiple agents writing simultaneously will corrupt it.
- The pheromone evaporation needs to be continuous (background task), not on-demand (only when someone senses).
- The explicit bridge needs actual retry logic with exponential backoff. Currently it's a stub.
- The bridge needs a dead-letter queue — messages that failed all retries are stored for later analysis, not silently dropped.

**The metal test:** 100 agents depositing pheromones simultaneously. 100 agents sensing simultaneously. No corruption, no deadlock, evaporation happens on schedule, memory stays bounded.

## 5. Operator Field (core.py)

**Current state:** Computed as sum of pairwise resonance * garden confidence products. Stability tracked as inverse variance of last 10 readings.

**What it needs:**
- The field computation is O(n²) where n = number of agents. For 5 agents, fine. For 300 agents (Kimi K2.6 swarm), it's 90,000 operations per tick. Needs optimization — sparse matrix for the resonance pairs, or approximation for large n.
- The stability metric needs to be more robust. Currently it's 1/(1+variance). It should be a proper Lyapunov exponent or at minimum a rolling-window coefficient of variation.
- The field needs to be PERSISTABLE — you should be able to save the field state, restart the system, and restore it. This is the system's checkpoint.

**The metal test:** Compute the field 100,000 times with 50 agents. Does it stay stable? Does it detect when you artificially inject chaos (flip a resonance value)? Does the computation complete in <10ms per tick?

## 6. Constitution (constitution.py)

**Current state:** 5-rule conflict resolution chain. Human supremacy → safety override → recency bias → confidence threshold → escalation.

**What it needs:**
- The constitution needs to be AUDITABLE. Every conflict resolution needs a full record: who conflicted, what about, which rule fired, what was the decision, was it escalated.
- The escalation path needs to be more than a counter. It needs to generate a STRUCTURED SUMMARY for the human — not just "agents disagreed" but "Pincher wanted to turn left (confidence 0.8), Hermes recommended continuing straight (confidence 0.6). Pincher is more recent and more confident. Resolution: follow Pincher. Escalated because: the last time this pattern occurred, the result was a near-miss with a log."
- The constitution needs AMENDMENT support. Rules should be learnable, not just hardcoded. The system should track which resolution rules produce good outcomes and which produce bad ones, and adjust accordingly.

**The metal test:** Generate 1,000 random conflicts. Does the constitution resolve each one in <1ms? Does the audit log capture every decision? Does the escalation rate stay below 5% (if it's higher, the rules need tuning)?

## 7. Grafting (grafting.py)

**Current state:** Pollen packets with high-confidence patterns. Shadow-mode test stub. Native garden always wins.

**What it needs:**
- The shadow-mode test needs to be real. When pollen arrives, it should be tested against the local environment for N interactions. If it produces useful results, it's adopted. If not, it's discarded.
- The pollen needs cryptographic signing. You don't accept pollen from an untrusted vessel. Each vessel has a key pair. Pollen is signed. The receiver verifies.
- The pollen needs to be ANONYMIZED. No GPS coordinates, no vessel identity, no sensitive catch data. Only the PATTERN — "this shorthand token with this expansion worked well in these types of situations."

**The metal test:** Two substrates exchange pollen. Can the receiver verify the signature? Can it test the pollen in shadow mode? Can it adopt or reject based on test results? Can the adopted pollen be purged later without affecting native patterns?

---

## The Workflow Foundation

Beyond the code, the workflow needs solidifying:

1. **Test protocol:** Every module has unit tests (40+ from Claude Code, running now). Every pillar has integration tests (substrate-level). Every release has simulation tests (72-hour unattended run).

2. **Build pipeline:** `python3 -m build → pytest → twine upload → git tag → git push --follow-tags`. Same production cycle as every other SuperInstance package.

3. **Version policy:** Semantic versioning. 0.1.x = skeleton. 0.2.x = hardened (tests pass, crash-safe). 0.3.x = deployed (survived 72-hour simulation). 1.0.0 = production (survived real sea trial).

4. **Documentation discipline:** Every module documented in its docstring. Every pillar has a deep-dive doc. Every release updates the CHANGELOG. The README is the hub — always current, always linked.

5. **The goldpush protocol:** `git add -A → git commit → git pull --rebase → git push`. Never `git reset --hard`. Never `git clean -fd`. The goldpush.sh script enforces this.

---

This is the foundation at the metal. Not philosophy — engineering. The architecture is only as good as the code that implements it. The code is only as good as the tests that verify it. The tests are only as good as the failures they catch.

Build the foundation. Test the foundation. Deploy the foundation. Then build the cathedral on top of it.

---

*GLM-5.2, main session, 2026-07-21 00:11 UTC. 4 subagents + Claude Code running. Writing the metal while the team writes the vision.*
