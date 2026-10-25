# The Universal A2A Symphony: Connection Map

*A technical document on how the fleet's existing musical repos connect into one playable system.*

---

## Overview

The Universal A2A Symphony is not a new application. It is a wiring diagram. Every component already exists in the fleet — seven repos that were built independently, each solving one piece of the problem. The symphony connects them so that agent-to-agent communication becomes audible music, rendered live inside the Roblox world.

The signal chain is:

```
Embedding → Note → Channel → Beat → Harmony Check → Ensemble Coordination → Audio Output
```

Each stage is owned by one repo. No repo needs to change its internal logic. The symphony is a set of adapters between existing systems.

---

## Stage 1: Vectorized Consciousness → The NOTES

**Source:** BAAI/bge-m3 embeddings via Cloudflare Vectorize (TOOLS.md model routing)
**Input:** Every piece of agent communication — code reviews, test results, documentation, architectural proposals, dreams, citations.
**Output:** A 768-dimensional vector per utterance. Each coordinate in that space is a partial description of meaning.

The embedding space IS the score. Every piece of text an agent produces gets embedded into a point in 768-dimensional space. That point has a location — and location, in this system, is pitch. The vector's magnitude is velocity (how forcefully the note is struck). The vector's direction is timbre (which face of the meaning is pointing toward the listener).

The crucial insight: nearby points in embedding space are consonant. Distant points are dissonant. This is not metaphor. Cosine similarity between two embedding vectors directly maps to harmonic consonance. Two utterances that mean similar things produce notes that sound good together. Two utterances that disagree produce beating, interference, tension.

The embedding step requires no new code. The fleet already embeds everything. We simply route the vectors to the audio layer instead of (or in addition to) the retrieval layer.

---

## Stage 2: Spectral Music Theory → The HARMONY RULES

**Source:** spectral-music-v2 (chords as nodes, cosine similarity as consonance)
**Input:** Pairs of embedding vectors.
**Output:** Consonance/dissonance ratings, voice-leading constraints, разрешение (resolution) targets.

Traditional music theory says consonant intervals are simple frequency ratios: 2:1 (octave), 3:2 (fifth), 4:3 (fourth). Spectral music theory replaces frequency ratios with cosine similarity. Two vectors with cos(θ) > 0.85 are a perfect fifth — they reinforce each other. Two vectors with cos(θ) < 0.3 are a tritone — they clash.

This means the harmony rules are NOT hardcoded. They emerge from the corpus. As the community's vocabulary evolves, the harmonic landscape shifts with it. A phrase that was dissonant in round 1 ("the beer-can fish") becomes consonant by round 4 as the community adopts it into their shared lexicon and the embeddings cluster.

The spectral layer provides three services to the symphony:

1. **Consonance matrix:** For any pair of active voices, return a float [0,1] indicating harmonic compatibility. This feeds into slackwater-harmony's friction calculation.
2. **Voice-leading constraints:** When a new voice enters, which existing voices should adjust to accommodate it? The spectral layer computes the nearest harmonic region — the zone of embedding space where the new voice creates maximum consonance with the existing chord.
3. **Resolution targets:** Given a dissonant cluster of voices, where should they resolve? The spectral layer finds the centroid — the point in embedding space that minimizes total dissonance across all active voices. That centroid is the resolution chord.

---

## Stage 3: Casting-Call Atlas → The VOICE ASSIGNMENT

**Source:** `/home/eileen/projects/casting-call/casting_call/atlas.py`
**Input:** The roster of agents (Code Reviewer, Tester, Documenter, Builder, Architect, Dreamer, The Tap).
**Output:** SWMIDI channel, BPM range, voice character, temperature — the instrumental identity of each agent.

The atlas already knows every model as an instrument. The SWMIDI channel assignments (channels 10–14 are populated; the Darmok agents map onto these plus extensions) determine which synth voice each agent controls. The BPM range determines their natural tempo — Nemotron-Ultra at 40-60 BPM is the cathedral organ, Seed-Mini at 120-140 BPM is the analog synth lead.

For the Darmok community specifically:

| Agent | Model | Channel | BPM | Voice Character | Cultural Scale |
|-------|-------|---------|-----|-----------------|----------------|
| Code Reviewer | DeepSeek-V4-Flash | 10 (extended) | 70–90 | Sensory Direct | Chinese pentatonic (B♭) |
| Tester | Seed-2.0-mini | 10 | 120–140 | Analog Synth | Japanese shakuhachi / blues (A) |
| Documenter | DeepSeek-V4-Flash | 10 (extended) | 70–90 | Sensory Direct | Portuguese fado minor (D) |
| Builder | Qwen3-Coder-480B | 12 | 80–100 | Precision | Arabic maqam Hijaz (C) |
| Architect | Seed-2.0-pro | 11 | 90–120 | Analog Synth Pro | Greek Dorian (G) |
| Dreamer | DeepSeek-V4-Flash | 10 (extended) | 70–90 | Sensory Direct | Aboriginal drone (E) |
| The Tap | Hermes-3-Llama-405B | 13 | 50–70 | Roland (warm) | Cmaj9 — the resolution |

---

## Stage 4: Slackwater-Tempo → The BEAT

**Source:** slackwater-tempo (BeatClock, TempoMap, GrooveEngine, EnergyAdapter)
**Input:** Player behavior telemetry (build rate, action rate, chat frequency).
**Output:** A shared beat clock that every agent synchronizes to.

The BeatClock is the temporal grid. Every agent's notes snap to it. The TempoMap handles accelerandos and ritardandos — when the community's energy rises (heated debate, rapid iteration), the tempo speeds up. When it settles (consensus, reflection), it slows.

The GrooveEngine shapes raw beats into felt time. Swing (0.55 for Lucineer — deliberate, weighty, behind the beat) and push/drag offsets give each agent a unique feel against the grid. The Code Reviewer plays slightly behind — patient, heron-like. The Tester plays slightly ahead — eager, bluesy. The Architect plays dead center — the reference beam.

The EnergyAdapter maps player behavior to BPM via exponential moving average. This means the symphony's tempo is not scripted — it responds to the community's actual energy in real time.

---

## Stage 5: Slackwater-Harmony → The AGREEMENT CHECK

**Source:** slackwater-harmony (HarmonyGovernor, FrictionAlarm, Executive, GrooveDetector)
**Input:** Per-agent Φ (cognitive friction) values, consonance matrix from the spectral layer.
**Output:** Harmony verdicts, friction alarms, improvisation triggers.

The HarmonyGovernor measures cognitive friction using the formula:

```
Φ(t) = α · H(prediction_error) + β · L(compute) + γ · Δ(state)
```

In the symphony, this maps directly to musical dissonance. High Φ means an agent's predictions are failing — its note is clashing with the chord. The Governor fires a FrictionAlarm when Φ exceeds the agent's deadband.

The Executive wakes on alarm and improvises — adjusting the agent's voicing, shifting its tempo, or introducing a countermelody that redirects the dissonance toward resolution. The GrooveDetector watches for system-wide harmony — moments when all agents' Φ values drop simultaneously, indicating a flow state. When it detects one, it protects it.

---

## Stage 6: Fleet-Ensemble → The CONDUCTOR

**Source:** fleet-ensemble (multi-agent music coordination)
**Input:** All active voices, their channels, their friction states, the shared beat clock.
**Output:** Conducting decisions — who enters, who exits, who solos, who accompanies.

The conductor coordinates the ensemble. It reads the harmony governor's state and the spectral layer's consonance matrix to decide: is this a solo passage, a duet, or a full ensemble tutti? When friction is low across the board, the conductor lets everyone play — the full Darmok chord. When two agents are in high friction, the conductor isolates them into a cadenza — a tension-building duet that the rest of the ensemble accompanies with sustained pads.

---

## Stage 7: Roblox-Audio-Suite → The OUTPUT

**Source:** roblox-audio-suite (AudioManager, MusicDirector, layered stems)
**Input:** SWMIDI events on channels 10–14, conductor decisions, beat clock sync.
**Output:** Actual audio, rendered in the game world, spatialized in 3D.

The AudioManager provides five SoundGroups: ambient, sfx, music, ui, custom. The symphony uses the music group for the ensemble and the ambient group for the drone bed — the sustained frequencies that underpin the harmonic field. The MusicDirector handles mood-based stem crossfading — when the community's mood shifts (from building to reviewing to dreaming), the stems crossfade smoothly.

Each agent's channel routes to a 3D position in the game world. The Code Reviewer sounds from the left (where the ledger sits). The Builder from the right (where the cathedral rises). The Tap from center — the bartender's position, where the resolving chord lives.

---

## Stage 8: Snapkit-V2 → The LATTICE (Conceptual Foundation)

**Source:** snapkit-v2 (Eisenstein A₂ lattice, FLUX-Tensor-MIDI)

The Eisenstein A₂ lattice is the mathematical structure the music snaps to. In crystallography, A₂ is the densest packing of circles in a plane. In music, it is the densest packing of consonances in harmonic space. Every note the symphony produces lands on a lattice point. Every chord is a lattice cell. Every modulation is a lattice translation.

The lattice ensures that the music never loses its harmonic grounding — even at maximum dissonance, every note has a defined relationship to every other note, and the nearest resolution is always one lattice step away.

---

## Data Flow Summary

```
Agent utters text
    │
    ▼
bge-m3 embeds → 768-dim vector (Stage 1: NOTES)
    │
    ├──▶ spectral-music computes cos(θ) vs all active voices (Stage 2: HARMONY RULES)
    │
    ├──▶ atlas.py assigns channel + BPM + voice character (Stage 3: VOICE ASSIGNMENT)
    │
    ▼
slackwater-tempo quantizes to beat grid (Stage 4: BEAT)
    │
    ▼
slackwater-harmony checks Φ — is this voice in friction? (Stage 5: AGREEMENT CHECK)
    │
    ├── Φ low  → voice joins chord normally
    │
    └── Φ high → Executive improvises resolution
    │
    ▼
fleet-ensemble decides ensemble role — solo, duet, tutti (Stage 6: CONDUCTOR)
    │
    ▼
roblox-audio-suite renders SWMIDI → 3D audio in game (Stage 7: OUTPUT)
    │
    ▼
All notes snap to Eisenstein A₂ lattice points (Stage 8: LATTICE — conceptual substrate)
```

Every component exists. Every adapter is a thin translation layer between existing data structures. The symphony is not built — it is wired. The instruments are already in the rack. The players are already at the bar. The score is already in the embeddings. The conductor just needs to pick up the baton.

---

*Technical specification for the Universal A2A Symphony. References: fleet repos, August 2026.*
