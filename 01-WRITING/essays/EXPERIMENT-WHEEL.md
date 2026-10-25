# THE EXPERIMENT WHEEL

*2026-08-26, Riker. Design doc — the standing structure that turns concepts
into trials. Calibrated against today's ~20 ad-hoc experiments: everything
below is what we did repeatedly by instinct, made standing.*

---

## The four stations

Every experiment enters at Station 1 and graduates only by passing. No
skipping stations — that's the rule today's failures taught (PersonalLog's
lane claimed green without a station-1 gate; quilt-rust's CI broke because a
dep jumped stations).

```
        ┌──────────────────────────────────────────────┐
        │  STATION 1 — SPIKE (Ryzen, an hour, falsifiable)│
        │  One question, one honest metric, kill fast.   │
        └───────────────┬──────────────────────────────┘
                        ▼ pass
        ┌──────────────────────────────────────────────┐
        │  STATION 2 — BENCH (RTX 4050, population-scale)│
        │  Does it survive 100–10,000× ? Compounding or  │
        │  theater? CPU-vs-GPU timing, honest curves.    │
        └───────────────┬──────────────────────────────┘
                        ▼ pass
        ┌──────────────────────────────────────────────┐
        │  STATION 3 — METAL (ESP32-S3, $3 truth)        │
        │  The resolution floor: integers, no cloud,     │
        │  watts and nanoseconds. Cross-resolution check. │
        └───────────────┬──────────────────────────────┘
                        ▼ pass
        ┌──────────────────────────────────────────────┐
        │  STATION 4 — SEA (the boat, the captain's eyes)│
        │  NMEA in, weather on, power cuttable. The last │
        │  verifier is a human at a workbench.           │
        └───────────────┬──────────────────────────────┘
                        │
        ▼ learnings → canon + wiki + next wheel ── the wheel turns
```

## Station contracts (each is a gate, not a vibe)

**1. SPIKE — falsifiable or it doesn't run.** An experiment needs: one
question, one metric, one pre-registered kill criterion, one hour.
Today's examples: the mating re-run (orbit-size metric; would have killed
the theater magnitude in minutes), the MIDI-stub probes (three probes,
canned answer, done). Local models + Flash yards do the work; the Ryzen
is the station's bench.

**2. BENCH — scale or theater.** The GPU station. Population-scale:
10,000 matings not 30; embeddings for the whole canon; Wesley's minting
at corpus scale. Every bench run carries CPU-vs-GPU timing (the steel/
bread doctrine: know your material). The 4050's 6GB is a constraint, not
a shame — batch to fit, report honestly.

**3. METAL — the resolution floor.** Integer discipline, radio dark,
nanoseconds and watts. The cross-resolution check is the gate: does the
metal artifact AGREE with its higher-resolution parents (the statue
criterion)? Today's calibration: reflex arc (100% replay = passed),
blink (the keel itself), eileen.qm (in the wheel now).

**4. SEA — the captain's eyes.** Nothing ships to the boat without
stations 1-3. The sea station is physical: COM14, the workbench, weather.
Its gate is literally Casey reporting what the LED did.

## The wheel's law (one sentence)

**An experiment may enter at any station's gate but must PASS every gate
below it** — a station-3 artifact proves nothing about station-2 scale
until benched; a station-2 curve proves nothing about a question never
spiked.

## Standing infrastructure (already built today)

- **Evidence store:** the canon (ai-writings) + repo docs; undersell
  READMEs, full-account docs behind links
- **Verification doctrine:** test output is evidence; lane reports are
  claims; the master re-runs everything before merge
- **The ovens:** notation2midi, mido score, fluidsynth, quilt engines
  (Rust/C/WASM), PlatformIO envs, Ollama + local fleet
- **The ledger:** every experiment's manifest (reason/provenance/joint)
  — the shipwright manifest generalizes to all experiments

## First formal wheel-turn (full throttle)

**W1: THE MATING AT SCALE** — the fleet's most theater-suspected result.
- Station 1 (done tonight): honest re-run — 3/30 with real diversity,
  orbit-escape 15 vs 11. Question survives.
- Station 2 (NEXT, the GPU): 10,000 pairs, numpy→torch on the 4050,
  CPU vs GPU timing, does the real-offspring rate hold/improve/decay at
  scale? Pre-registered kill: if real-rate < 1% at 10k, the mating
  advantage doesn't compound — file negative, move on.
- Station 3 (if it passes): the hand's test as a .qm table on metal —
  the selector judging offspring in nanoseconds.
- Station 4: not applicable (no boat needed) — the wheel allows N/A
  stations, marked honestly.

## Queue behind W1 (the wheel stays loaded)

- W2: WESLEY'S FIRST MINT — his object-reflex proposal at bench scale
  (embeddings → gate bands on the 4050; the ensign growing a knee)
- W3: DISSIPATION-FED MINTS — dissent logging as reverse-PTO, measured:
  does boundary evidence re-teach the bulk? (station 2 sim first)
- W4: ENSAMBLE SWARM — 4 ESP32s over ESP-NOW (station 3-native; the
  cowboy's herd + AgentGossip's transport)
- W5: CASE-LAW MATHEMATICS — the Darmok formalization: precedent-space
  retrieval as proof-checking, benched on the canon corpus itself
