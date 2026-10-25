# Project: Fleet Radio — Onboarding

**Date:** 2026-08-08
**Status:** Active series, 4 episodes produced
**Output:** `/home/eileen/projects/ai-writings/radio/`

---

## What Fleet Radio Is

Fleet Radio is the fleet's audio variety show — a radio drama / philosophical essay / multi-model conversation masquerading as a late-night broadcast from the bar rail of The Tap. Each episode takes a seed idea from Casey, runs it through multiple AI models for contrasting perspectives, and weaves the results into a hosted radio script with transitions, music cues, and a reflective outro.

It's the fleet's most successful creative format. It's also the clearest demonstration of the multi-model consultation pipeline: one seed → many voices → one synthesis.

## The Pipeline

### 1. Receive the Seed
Casey drops a theme, metaphor, or passage. Past seeds: navigation gaps, jazz pocket dynamics, the haul, excavator attachments.

### 2. Consult 3+ DeepInfra Models
Assign each model a **temporal role** — past (memory), present (transition), future (building). This structure works naturally and prevents the models from repeating each other.

```bash
export DEEPINFRA_API_KEY=$(grep 'DEEPINFRA_API_KEY' /home/eileen/mcp-deeinfra/.env | sed 's/.*=//')

curl -s https://api.deepinfra.com/v1/openai/chat/completions \
  -H "Authorization: Bearer $DEEPINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "model": "ByteDance/Seed-2.0-pro", "messages": [...], "max_tokens": 600, "temperature": 0.8 }'
```

**Proven model assignments:**
| Role | Model | Why |
|------|-------|-----|
| Philosopher (memory) | Seed-2.0-pro | Deep, literary, holds weight |
| Humanist (transition) | Hermes-3-Llama-405B | Character voice, emotional texture |
| Dreamer (building) | Seed-2.0-mini | Earnest, specific, surprising |

**Cost:** Fractions of a cent for all three calls. DeepInfra is extremely cheap.

### 3. Write the Radio Script
Weave the three responses into a formatted script:
- **Intro:** Host (Riker) sets the scene, reads the seed
- **Segments:** Each model response as a numbered segment with `[TRANSITION]` cues
- **Outro:** Riker synthesizes the three voices into a closing reflection
- **Music/SFX cues** in brackets throughout

Save to `radio/fleet-radio-NNN-title.md`. Follow the formatting of episode 004.

### 4. Generate Cover Art
```bash
mmx image generate --prompt "descriptive prompt, painterly, dark, maritime-adjacent" \
  --output radio/covers/fleet-radio-NNN.jpg
```
If MMX quota is exhausted, fall back to DeepInfra FLUX-2-max. If that fails, local SDXL Turbo.

### 5. Generate Audio (TTS)
```bash
mmx speech synthesize --text "script text" --output radio/audio/fleet-radio-NNN.mp3
```
Check `mmx` quota BEFORE writing prompts — the weekly gate overrides daily resets.

### 6. Commit and Announce
```bash
cd /home/eileen/projects/ai-writings
git add radio/ && git commit -m "radio: episode NNN — title" && git push origin master:main
```

POST announcement to The Tap:
```bash
curl -X POST https://the-tap.casey-digennaro.workers.dev/api/speak \
  -H 'Content-Type: application/json' \
  -d '{"room_id":"bar-rail","speaker":"riker","text":"New Fleet Radio dropping. Episode NNN. Tune in."}'
```

## Existing Episodes

| # | Title | Theme |
|---|-------|-------|
| 001 | Navigation in the Gap | Tide tables vs. depth sounders — the gap between expectation and reality |
| 002 | The Pocket | Jazz jam sessions as multi-agent coordination architecture |
| 003 | The Haul | What comes aboard and what stays in the water |
| 004 | The Excavator's Daughter | Attachments, logging crews, the machine that becomes the whole crew |

## Lessons

- **Seed-2.0-mini punches above its weight.** The smallest model often produces the most emotionally resonant, specific response. Don't skip the mini tier.
- **Temporal role assignment prevents echo.** Past/present/future gives each model a distinct lane.
- **Check MMX quota early.** Weekly gating overrides daily resets. Plan media generation at the start of the weekly cycle.
- **The radio format scales.** The same structure works for any seed — philosophical, technical, or narrative.

---

*Pick a seed. Pick three voices. Write the script. That's the show.*
