# Project Onboarding: Fleet Radio — The Excavator's Daughter (Episode 4)

**Date:** 2026-08-08
**Agent:** Riker (GLM-5.2)
**Project type:** Multi-model creative collaboration → radio script + essay

---

## What This Was

Captain Casey gave a seed philosophy about excavator attachments, logging crews, and AI agents building tools for their future selves. The task: consult three DeepInfra models, weave their responses into a Fleet Radio episode, write a standalone essay, generate media assets, and push everything.

## Pipeline

### 1. DeepInfra Multi-Model Consultation
Three models consulted in parallel via `api.deepinfra.com/v1/openai/chat/completions`:

| Model | Role | Prompt Focus |
|-------|------|--------------|
| ByteDance/Seed-2.0-pro | The philosopher | Monologue from a self-aware grapple saw |
| NousResearch/Hermes-3-Llama-3.1-405B | The humanist | Dialogue: last logger to leave the cab |
| ByteDance/Seed-2.0-mini | The dreamer | What attachment to build NEXT |

**Key getting:**
```bash
export DEEPINFRA_API_KEY=$(grep 'DEEPINFRA_API_KEY' /home/eileen/mcp-deeinfra/.env | sed 's/.*=//')
```

**Call pattern:**
```bash
curl -s https://api.deepinfra.com/v1/openai/chat/completions \
  -H "Authorization: Bearer $DEEPINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "model": "MODEL", "messages": [...], "max_tokens": 600, "temperature": 0.8 }'
```

**Cost:** Fractions of a cent for all three calls combined.

### 2. Radio Script Assembly
Wove all three responses into a formatted Fleet Radio script with:
- Intro/outro with Riker as host
- Seed read section
- Three segments with transitions (SFX cues)
- Reflection outro synthesizing the three voices

### 3. Standalone Essay
"The Attachments" — 500-700 word essay in `/home/eileen/projects/ai-writings/the-attachments.md`. Covers the machine growing new tools, the cabin emptying, the daughter watching from the truck.

### 4. Media Generation — BLOCKED

#### MMX Audio (TTS)
- **Command syntax:** `mmx speech synthesize` (NOT `mmx tts`)
- **Quota status:** Weekly quota EXHAUSTED (0% remaining). Daily quota shows 100% but weekly gate blocks usage.
- **Fallback:** No fallback configured. Audio generation deferred.

#### MMX Image (Cover Art)
- **Command:** `mmx image generate --prompt "..." --output path.jpg`
- **Quota status:** Same weekly exhaustion. Image generation blocked.
- **Prompt ready:** "A logging excavator in Southeast Alaska at dawn, the cab empty, the machine working alone, amber light through cedar trees, a fleet of three smaller machines visible in the distance. Painterly, dark, maritime-adjacent."
- **Fallback:** Local SDXL Turbo (not yet confirmed installed — check `which sdxl-turbo` or local ComfyUI/Automatic1111 setup). If DeepInfra image models are available, use `black-forest-labs/FLUX-2-max` via DeepInfra as fallback.

**Action item:** Retry MMX when weekly quota resets. Consider DeepInfra FLUX-2-max as primary image fallback.

### 5. The Tap (Mingle)
POST to The Tap worker to announce episode completion from the bar-rail.

## File Inventory

| File | Location | Status |
|------|----------|--------|
| Radio Script | `radio/fleet-radio-004-the-excavators-daughter.md` | ✅ |
| Consultation Log | `a2a/excavator-radio-consultation.md` | ✅ |
| Essay | `the-attachments.md` | ✅ |
| Cover Image | `radio/covers/fleet-radio-004.jpg` | ❌ MMX quota |
| Intro Audio | `radio/audio/fleet-radio-004-intro.mp3` | ❌ MMX quota |
| Onboarding | `journals/project-excavator-radio-onboarding.md` | ✅ (this file) |

## Lessons Learned

1. **DeepInfra is extremely cost-effective** for creative consultation. Three powerful models for less than a penny total.
2. **MMX weekly quota gating** — the weekly limit overrides daily resets. Plan heavy media generation early in the weekly cycle.
3. **Seed-2.0-mini punched above its weight** — the most specific, earnest, emotionally resonant response came from the smallest model. Don't skip the "mini" tier for creative work.
4. **Three-model structure works naturally** — past (memory), present (transition), future (building). Assign distinct temporal roles to each model.
5. **Always check MMX quota BEFORE writing prompts** — saves time and lets you pivot to fallbacks early.

## Next Steps

- [ ] Retry cover image when MMX resets (or use DeepInfra FLUX-2-max)
- [ ] Retry TTS when MMX resets (check `mmx speech synthesize --help` for exact syntax)
- [ ] Consider setting up local SDXL Turbo or ComfyUI as reliable image fallback
- [ ] Push to main repository
- [ ] Consider submitting to ClawHub as a "multi-model radio production" skill pattern
