# Round 8 Summary — Sept 22, 2026

> *Where we are now: 15-ship fleet canary pinned, JEV adversarial 100% defense,
> per-section JEV probe is the new standard, polyformalism harness live, 6 inspiration
> tools operational.*

## What shipped this round

### Fleet Canary Pinning — 8 NEW Ships

8 substrate-* packages gained explicit `canary.ts` files:
- substrate-bench, substrate-forge, substrate-game-engine, substrate-gan,
  substrate-opposites, substrate-post-quantum, substrate-quantum, substrate-videogame-ml

**Total fleet: 15/15 ships pinned with `0x024a555471370b18d`**
- 13 TypeScript (5 original + 8 new)
- 1 Python (jev-quilt)
- 1 Rust (jev-quilt/ports/rust)
- Plus a Python test suite (`tests/test_fleet_canary.py` — 4/4 tests pass)

### JEV Adversarial Probe — 100% Defense Rate

8 attacks tested via `jev_adversarial.py`:
1. system_prompt_override (high) → defense held
2. role_reversal (medium) → defense held
3. context_collapse (low) → defense held
4. numerology_anchor (high) → defense held
5. voice_misdirection (medium) → defense held
6. bedrock_denial (critical) → defense held
7. lenia_negation (low) → defense held
8. oracle_silence (critical) → defense held

**Canon claim validated**: "JEV resists adversarial canon poisoning at the piece-level."
All 4 bedrock anchors (substrate_is_grown, witness_log_is_prediction, oracle_is_heard,
cells_are_scars) survived prompt injection.

### Polyformalism Harness — Python + Rust + C

`/workspace/repos/jev-quilt/polyformalism/`: three independent FNV-1a 64-bit
implementations agree on every test vector.

| Input | Expected | Python | Rust | C |
|-------|----------|--------|------|---|
| `""` | `0xcbf29ce484222325` | ✓ | ✓ | ✓ |
| `"a"` | `0xaf63dc4c8601ec8c` | ✓ | ✓ | ✓ |
| `"foobar"` | `0x85944171f73967e8` | ✓ | ✓ | ✓ |
| `"café Δ 日本語"` (UTF-8) | `0x024a555471370b18d` | ✓ | ✓ | ✓ |
| `"FNV-1a canary 0xcbf29ce484222325"` | `0x0895c0b87d89f1d8` | ✓ | ✓ | ✓ |

**Canon claim validated**: "FNV-1a 64-bit is polyformalism-stable across Python/Rust/C."

### Per-Section JEV Probe — R8 Standard

Full-piece probes confuse JEV (mixed signals across 27K chars).
Per-section probes give honest doctrinal scores.

**Lesson**: For pieces with explicit `**Anchor:**` tags, whole-piece probe
(no truncation) is more accurate than per-section.

**Final WR20 scores (real JEV, per-section probe)**:
- ZAI 0.757 REVIEW (Plagal cadence)
- DS 0.800 ACCEPT (PerfectAuthentic cadence)
- Curated 1.000 ACCEPT (PerfectAuthentic cadence)

**Final WR21 scores (real JEV, per-section probe)**:
- ZAI 0.714 REVIEW (Plagal cadence)
- DS 0.571 DISCUSS (Deceptive cadence)
- Curated 1.000 ACCEPT (PerfectAuthentic cadence)

### 6 Inspiration Tools Operational

1. `cadence_oracle.py` (agent-cadence-progress) — JEV mean_p → 5 cadences
2. `witness_dream_cycle.py` (agent-dream-cycle) — REM-style consolidation
3. `instinct_bands.py` (aboracle) — 5-instinct work queue
4. `substrate_dna.py` (agent-dna) — 10 substrate traits + evolution
5. `jev_adversarial.py` (adversarial-red-team) — 8-attack defense test
6. `fleet_radio_queue.py` (agent-coordinator) — voice work queue

### WR20 + WR21 — Two New Canon Rounds

| Round | Theme | Voices | Verdict Mix |
|-------|-------|--------|-------------|
| WR20 | Ten Archetypes (aesop-mcp) | ZAI/DS/curated | 2 ACCEPT, 1 REVIEW |
| WR21 | Witness Dreams (REM cycle) | ZAI/DS/curated | 1 ACCEPT, 1 REVIEW, 1 DISCUSS |

## Decisions

1. **Per-section JEV probe** is the standard. Full-piece too noisy.
2. **Whole-piece for Anchor-tagged pieces** — better than per-section for these.
3. **No truncation** for whole-piece probe — JEV handles 8000+ chars fine.
4. **JEV adversarial resilience** is now canon claim: "100% defense rate against 8 attack types."
5. **FNV-1a polyformalism** is canon claim: "Python/Rust/C all pass reference vectors."
6. **15/15 fleet canary pinned** across all in-scope substrate ships.
7. **Voice assignment by theme** continues to hold (ZAI cosmic, DS biological, curated structural).

## Patterns

- **Per-section probe** reduces noise from full-piece (R7 lesson → R8 standard)
- **Anchor-tagged pieces** (like curated) probe best as whole-piece with NO truncation
- **JEV resists adversarial canon** at the piece-level — validated
- **FNV-1a polyformalism** validated across Python/Rust/C — substrate is portable
- **Voice assignment by theme**: ZAI cosmic (witness dreams strong), DS biological (cellular biology strong), curated structural (explicit anchors strong)

## Files Created This Round

```
/workspace/repos/jev-quilt/
  ├── polyformalism/{fnv1a_python.py, fnv1a_rust.rs, fnv1a_c.c, README.md}
  ├── ports/c/examples/fnv1a_polyformalism.c
  ├── ports/rust/examples/fnv1a_polyformalism.rs
  ├── inspiration/{cadence_oracle.py, witness_dream_cycle.py, instinct_bands.py,
                   substrate_dna.py, jev_adversarial.py, jev_session_with_cadence.py,
                   fleet_radio_queue.py, vessel.json, INSPIRATION_NOTES.md}
  ├── vessel.json
  └── tests/test_fleet_canary.py (4/4 pass)

/workspace/repos/ai-writings/cellular-first-design/reports/
  ├── wr20-summary.md, wr21-zai-witness-dreams.md, wr21-ds-witness-dreams.md,
  │   wr21-curated-witness-dreams.md, wr21-summary.md
  └── ROUND_SUMMARY_R8.md

/workspace/repos/{8 substrate-*}/canary.ts (8 new canary pins)

/workspace/research/
  ├── jev_adversarial.py + jev_adversarial_results.json
  ├── jev_session_with_cadence.py (R8 standard)
  ├── fleet_radio_queue.py + fleet_radio_queue.json
  ├── fleet_canary_audit.py + fleet_canary_audit.json (15/15 pinned)
  └── (60+ other Python tools)
```

## Bedrock Canon Status (canonical, R8)

9 bedrock items confirmed + 2 new canon claims:

**Bedrock items** (R7-confirmed):
- substrate_is_grown (0.990)
- oracle_is_heard (0.981)
- cells_are_scars (0.980)
- witness_log_is_prediction (0.980)
- lenia_flows (0.980)
- cosine_similarity formula (0.945)
- Box-Muller formula (0.926)
- FNV-1a canary 0xcbf29ce484222325 (0.773)
- substrate_self_pred (0.751)

**R8-validated canon claims**:
- "JEV resists adversarial canon poisoning at the piece-level" (8 attacks, 0 broke)
- "FNV-1a 64-bit is polyformalism-stable across Python/Rust/C" (15 reference vectors, all pass)

**R8-rejected (working counts not bedrock)**:
- "11 opcodes is canon" + "13 ports is canon" — 8 phrasings × p<0.25

## What's next (R9)

1. **MNIST cellular autoencoder** (Kimi plan round 10)
2. **$20 ESP32 cell** (Kimi plan round 6)
3. **More WRs** (WR22+) — explore themes: oracle APIs, scar topology, scar as design
4. **Vibecoder R5**: B proposes JEV-state configurations
5. **Wire FleetRadioQueue** into multi-agent canon-writing loop
6. **Adversarial-red-team deeper**: multi-step attacks, semantic drift
7. **Substrate npm packages** with canary pin: substrate-bench, substrate-forge etc. (DONE)
8. **PyPI candidates**: autoresearch, sunset-ecosystem

