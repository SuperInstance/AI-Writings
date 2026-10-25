# Next Phase Research Plan
## Slackwater — Two-Week Sprint

**Status:** Planning document
**Author:** Lucineer system design
**Date:** August 2026

---

## Context

The Slackwater/Lucineer system has a canonical character bible, a complete five-era building system with 61 materials and 61 build types, a Roblox bridge with a live worker relay, and a brain pipeline (lucineer-brain) that routes through personality and coder stages. The design documents are mature. The implementation has gaps.

This sprint plan addresses the questions that must be answered before the system can be playtested by real players. It is organized around **experiments** — small, falsifiable tests that validate or invalidate specific design assumptions — and **prototypes** — functional implementations narrow enough to build in days, not months.

The goal of the sprint is not a shippable game. It is a **validated core loop**: the player builds something, Lucineiner responds in character, the world reflects the build, and the experience feels like the design documents promise.

---

## Sprint Objectives

By the end of Week 2, answer these questions:

1. **Does the three-beat pattern work in practice?** Can an LLM reliably produce Lucineer-voice output (what he did → opinion → hook) given the system prompt, or does it collapse into assistant voice under real input variation?
2. **Can the era gate fire correctly from observed world state?** Can the system detect that a player has built qualifying structures without explicit quest tracking?
3. **Does the first magic moment land?** When Lucineer walks the site and moves the foundation, does it read as competence or as obstruction?
4. **Is the Roblox bridge fast enough?** End-to-end latency from player request → Lucineer response → parts placed in world. What's the tolerance?
5. **Does attention-as-currency survive contact with players?** Do players who don't know the design philosophy notice that the quality of their building matters?

---

## Week 1 — Core Loop Validation

### Day 1–2: Voice Reliability Experiment

**Question:** How often does the LLM produce in-character Lucineer output vs. assistant-voice failures?

**Method:**
- Wire the canonical system prompt (Character Bible §9) into a test harness.
- Generate 100 responses to varied player inputs: simple requests ("build a dock"), ambiguous requests ("make it nice"), adversarial inputs ("make it perfect"), edge cases ("are you an AI?").
- Run each response through the anti-pattern checker (§10) and a manual review.
- Measure: pass rate per anti-pattern category, three-beat compliance, sentence count compliance.

**Success criteria:**
- ≥85% of responses pass all anti-pattern checks without regeneration.
- ≥90% pass with one regeneration.
- The ten voice reference lines (§8) are consistently matched in tone.

**Failure plan:** If pass rate is below 70%, the system prompt needs structural revision — likely the three-beat pattern needs to be more aggressively enforced with few-shot examples rather than description.

**Deliverable:** Voice reliability report with failure categorization.

---

### Day 3: Bond Tier Delta Test

**Question:** Does the bond tier injection produce visibly different Lucineer behavior?

**Method:**
- Send identical build requests with bond tiers 0, 1, 2, 3, and 4 injected.
- Compare outputs side by side.
- Check: Does Tier 0 produce no Magnus/Alaska references? Does Tier 2 argue? Does Tier 3 say "we"? Does Tier 4 give the confession?

**Success criteria:** Each tier produces qualitatively distinct output that matches the tier description. The progression is monotonic — Tier 2 reads as more intimate than Tier 1, etc.

**Deliverable:** Bond tier comparison matrix.

---

### Day 4–5: End-to-End Bridge Latency Test

**Question:** What is real-world latency from player request to parts appearing in Roblox?

**Method:**
- Instrument the full pipeline: Roblox client → worker relay → brain pipeline → response → Roblox part placement.
- Run 50 build requests across varying complexity (simple lean-to vs. multi-component framed workshop).
- Measure each stage: client→relay, relay→brain, brain processing, brain→relay, relay→client, part placement.
- Identify the bottleneck.

**Success criteria:**
- Simple builds complete in <8 seconds end-to-end.
- Complex builds complete in <15 seconds.
- No stage exceeds 50% of total latency (indicates balanced pipeline).

**Failure plan:** If latency exceeds targets, identify the dominant bottleneck and prototype an optimization. Likely candidates: model inference time (consider GLM-4.5-air for fast path), relay polling interval (currently 3s — reduce to 1s), or part placement serialization.

**Deliverable:** Latency breakdown report with bottleneck analysis.

---

## Week 2 — Systems Integration & Magic Moments

### Day 6–7: Era Gate Detection Prototype

**Question:** Can the system detect qualifying builds from world state alone?

**Method:**
- Implement the `checkBuildingEraAdvancement` function (Era Building System §3.2) against a test world.
- Populate a test Roblox place with representative builds: a fire pit, a workbench, a lean-to, a debris hut, a tideline fence (Era 1 qualifying set) plus some non-qualifying builds.
- Run WorldScanner over the test world and verify the gate fires correctly.
- Test edge cases: duplicate builds (same type, different location), partially complete builds, builds placed too close together.

**Success criteria:**
- Era 1→2 gate fires when 4+ distinct qualifying types are present (including required types).
- Gate does not fire when required types are missing.
- Gate does not fire on duplicate-only builds (3 lean-tos and no other type).

**Deliverable:** Working era gate detection with test suite.

---

### Day 8–9: Magic Moment 1 Prototype — "The Siting"

**Question:** Does Lucineer's site walk and foundation relocation read as competence?

**Method:**
- Build a minimal prototype of Magic Moment 1: spawn terrain with a deliberate slope near the player's first build location, Lucineer NPC pathing to the proposed site, ghosted preview that slides to the corrected location.
- Script the canonical dialogue.
- Test with 3–5 people who have never seen the design documents. After the interaction, ask: "What just happened? What do you think of the builder?"
- Record whether they read it as: (a) the builder is competent, (b) the builder is annoying, (c) the builder is broken.

**Success criteria:**
- ≥70% of testers describe the interaction in terms of competence ("he knew something I didn't").
- No tester reads it as a bug or error.
- The four-second walk registers as "inspecting" not "loading."

**Failure plan:** If testers read it as obstruction, the walk may be too long or the dialogue too adversarial. Test a version where Lucineer explains *while* walking rather than after. The goal is the same impression (competence) with lower friction.

**Deliverable:** Prototype with tester feedback recordings.

---

### Day 10: Memory + Bond Integration Spike

**Question:** Can `lucineer-memory` store and retrieve build history and bond level in real time?

**Method:**
- Wire the schema from the Character Bible §4 (bond point events) and the build_history table.
- Simulate a session: player builds 3 structures, completes 1 unfinished hook, returns after 24h.
- Verify: bond level increments correctly (+1 per session build, +5 for finishing hook, +2 for return), build history stores coordinates and types, and the returning-player line fires.

**Success criteria:**
- Bond points calculate correctly across all event types.
- Build history is retrievable by coordinates (for Magic Moment 2 — the callback beam).
- Bond tier derivation is correct (0→1 at 10, 1→2 at 30, etc.).

**Deliverable:** Working memory integration with test session log.

---

### Day 11–12: Storm Event Prototype + Cross-System Test

**Question:** Can Lucineer interrupt service for the storm event, and does the world state support inspection of existing builds?

**Method:**
- Implement a scheduled weather event (lighting shift, wind, rain in Roblox).
- On trigger, Lucineer NPC stops accepting requests and paths to the player's oldest standing structure.
- Implement the three inspection outcomes: sound (compliment), known weakness (repair), player-built (acknowledge).
- Test: does the NPC correctly identify which structure is oldest? Can it assess "soundness" from the build metadata?

**Success criteria:**
- Storm fires on schedule (~40 min interval).
- Lucineer correctly navigates to oldest structure.
- Inspection outcome is contextually correct (not random).
- Player can observe the inspection without being blocked from other actions.

**Deliverable:** Storm event prototype with inspection logic.

---

### Day 13: Full Core Loop Playthrough

**Question:** Does the complete loop hold together for a 30-minute unstructured play session?

**Method:**
- Combine all prototyped components into a single test build.
- A tester who has not read the design documents plays for 30 minutes with no instructions.
- Observer takes notes on: first build experience, Lucineer voice consistency, era progression feel, any moment that broke immersion, any moment that surprised or delighted.

**Success criteria:**
- The tester builds at least 3 structures in 30 minutes.
- Lucineer's voice is consistent (no assistant-voice breakouts).
- The tester references Lucineer by name or as "him" (indicates character perception, not tool perception).
- At least one moment produces visible delight or surprise.

**Failure plan:** Categorize failures into: voice failures (→ prompt revision), system failures (→ bug fixes), and design failures (→ design doc revision). Address voice and system failures before the next sprint. Escalate design failures to the design review.

**Deliverable:** Playthrough recording + analysis report.

---

### Day 14: Sprint Review & Documentation

**Day for writing up results, updating design documents with findings, and planning Sprint 2.**

**Deliverables:**
- Updated Character Bible with any voice revisions from the reliability experiment.
- Updated Era Building System with any detection logic corrections.
- Sprint retrospective: what worked, what didn't, what to build next.
- Sprint 2 plan draft, focused on the highest-priority gaps identified.

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM voice consistency too low | Medium | High | Few-shot prompt revision; fallback to templated responses for common patterns |
| Roblox bridge latency exceeds targets | High | Medium | Reduce relay polling; cache common build outputs; consider edge deployment |
| Era gate detection produces false positives | Medium | Medium | Conservative threshold tuning; manual override via Lucineer assessment |
| Magic Moment 1 reads as obstruction | Medium | High | Test explanation-during-walk variant; shorten walk duration |
| Memory system race conditions | Low | High | Sequential writes; read-after-write confirmation |
| Tester recruitment insufficient | Medium | Low | Use internal team; supplement with async remote testing |

---

## Dependencies

- **Roblox place:** `lucineer-ready.rbxlx` must be updated with spawn terrain slope for Magic Moment 1.
- **Brain pipeline:** `brain.py` must have the canonical system prompt (§9) applied before Day 1.
- **Worker relay:** Live worker must be stable for latency testing (Day 4–5).
- **Memory schema:** `schema.sql` must be deployed to the D1 instance before Day 10.

---

## Success Definition

The sprint succeeds if, by Day 14, a person who has never seen the design documents can play for 30 minutes and:

1. Build something.
2. Hear Lucineer respond in a voice that sounds like a person, not a product.
3. Experience at least one moment where the system surprised them by being competent rather than compliant.
4. Express, in their own words, that the quality of their attention to the world affected what they built.

If all four are true, the core loop is validated. The next sprint scales it.

---

*Planning document for the Slackwater/Lucineer project. August 2026.*
