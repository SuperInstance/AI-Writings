# The Two-Division Wheel — operating protocol

*Established 2026-09-03 (Casey directive: builders push prototypes; ideators rotate into play-testing, then re-feed the builders — a continuous wheel).*

## Roles

- **BUILDERS (converge).** Install, wire, implement, verify, commit. Output = **prototypes and proofs-of-concept**, each with a run trail (how to run it, what it does, what's fake/hardcoded).
- **IDEOATORS (diverge).** Generate concepts, scored, with falsifiable first tests. Output = **idea sheets** (`ideas/`), no implementation.
- **THE ROTATION (the wheel's teeth).** Ideators do not only ideate: each round, every ideator takes a **play-test turn** against one builder prototype. Play-test = run it, abuse it, try to break it at the seams the builder declared and the ones they didn't. Output = **PLAYTEST report** (`ideas/playtests/`): verdict (WORKS / WORKS-WITH-SCARS / BREAKS), reproduction steps, and — mandatory — **3 new idea seeds** the breaking generated. Those seeds re-enter the builders' queue. Then the ideator goes back to ideating.

## The loop, concretely

1. Builders publish prototype + run trail → `prototypes/` (or repo path pointer).
2. Each prototype is assigned to ≥1 ideator for play-test within the same round (adversarial use, not code review — the tester's job is to be the sea, Spin-21 style).
3. PLAYTEST reports + idea seeds land in `ideas/playtests/`.
4. Seeds are scored (novelty × feasibility) and merged into the idea ledger; top-scored seeds become the builders' next round specs — pre-registered pass/fail criteria included.
5. Repeat. One full turn of the wheel = a prototype hardened by at least one attempt to kill it, plus a restocked idea queue.

## Rules carried from the house disciplines

- Byte-exact fabric work never passes through LLM inference (determinism boundary holds at every rotation).
- Pre-register the kill condition before the run; a scar booked beats a result covered.
- Play-test failures are first-class output — the wheel eats failures as fuel, not as shame.
- Nothing ships or merges on a play-test's word alone; builders re-verify with their own canaries.

## Round 1 (live now)

- Prototype: PAIR artifact (NVPAIR-Setup v0.1.1 amd64 .deb, 141 MB, downloaded, not installed).
- Ideators: I1 (GLM) ideas sheet in flight; I-C (Claude) wildcard sheet in flight.
- Play-test assignments fire when the first prototype/idea artifacts land.
