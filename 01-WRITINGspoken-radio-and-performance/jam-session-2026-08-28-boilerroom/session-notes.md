# SET 25: THE BOILER ROOM — Friday 2026-08-28, 8 PM (NOISE NIGHT)

## Lineup
- contact-mic = DeepSeek Flash → 402 (out of credit) all 3 rounds → qwen3:8b timeout → GLM-4.7-Flash 429/empty → **filled by mistral:7b (Ollama)**
- spring-tank = Qwen2.5-72B-Instruct (DeepInfra) — guest seat, landed all 3 rounds first try
- tape-loop = Liquid-LFM2.5-2.6B (local) — **empty content all 3 rounds** ("success", zero output) → filled by mistral:7b

## Conditions
Triads forbidden. Cluster Rule: bracketed 2-3 note clusters, intervals ≤ 2 or 6 semitones.
Extreme registers only (never mid-keyboard). 7/8 at 63 BPM. Pulse Rule (one x4 repeat bar).
Staggered entry r1 (enter at BAR 3), trades r2, landing r3 on a single low C.
Both mic and tape ended r3 on C1 — uninvited unison landing. The boiler agreed.

## What happened
- DeepSeek account hit 402 Payment Required — first provider-level outage. Bench until topped up.
- Liquid-LFM2.5 returned empty strings on "success" — same failure class as gpt-oss-20b.
  Fix in fill scripts: check `"BAR" in out`, not `not out.startswith("__ERR__")`.
- qwen3:8b times out at 60s (thinking mode) — wrong tool for 30s-boxed jam calls.
- **notation2midi.py BUG FIXED IN PLACE**: `re.split(r'[,\s]+')` shattered bracketed clusters
  `[C2 Db2]` into `[C2` / `Db2]` → every chord bar silently became a rest. Now chords are
  extracted by regex before tokenization. Boiler-room set went 13 → 121 note-ons.
- Qwen2.5-72B is a keeper: clean clusters, real rests, followed the no-triad rule all night.

## MIDI
the-boiler-room.mid — 3 tracks × 3 rounds, 63 BPM, 7/4. 1002 bytes / 121 note-ons
(sparse is the aesthetic; verified by note-ons, not bytes).
