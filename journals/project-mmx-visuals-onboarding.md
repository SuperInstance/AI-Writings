# MMX Visuals — Onboarding & Pipeline Guide

**Created:** 2026-08-08
**Author:** Lucineer (mmx subagent)

---

## Overview

This document covers the visual asset pipeline for the Lucineer fleet: how to generate images using MMX (MiniMax CLI) and the local SDXL Turbo fallback, prompt patterns that work well, and the end-to-end workflow from prompt to committed asset.

---

## Tools

### Primary: MMX (MiniMax CLI)

- **Location:** `~/.npm-global/bin/mmx`
- **Subscription:** Starter plan (weekly quota — can run out!)
- **Model:** `image-01` (MiniMax's image generation model)
- **Strengths:** High quality, good prompt adherence, artistic styling
- **Weaknesses:** Weekly quota limits; can hit 0% remaining

#### Basic Usage

```bash
mmx image generate \
  --prompt "Your detailed prompt here" \
  --aspect-ratio "16:9" \
  --out-dir /home/eileen/projects/ai-writings/visuals/ \
  --out-prefix "filename-prefix" \
  --quiet --non-interactive --yes true
```

#### Key Flags

| Flag | Purpose |
|------|---------|
| `--prompt <text>` | Image description (be detailed!) |
| `--aspect-ratio <ratio>` | e.g. `16:9`, `1:1`, `4:3` |
| `--n <count>` | Number of images (default: 1) |
| `--width` / `--height` | Explicit pixel dimensions (512–2048, multiples of 8) |
| `--out-dir <dir>` | Output directory |
| `--out-prefix <prefix>` | Filename prefix (default: `image`) |
| `--seed <n>` | Reproducible results |
| `--prompt-optimizer` | Let MMX enhance your prompt before generation |
| `--subject-ref` | Character/object reference for consistency |
| `--quiet --non-interactive` | Agent mode — no spinners, no prompts |
| `--yes true` | Skip confirmation prompts |

#### Checking Quota

```bash
mmx quota show --output json --quiet --non-interactive
```

Watch for `current_weekly_remaining_percent: 0` — that means you're out until reset.

---

### Fallback: Local SDXL Turbo (diffusers)

When MMX quota is exhausted, use the locally cached SDXL Turbo model.

- **Model:** `stabilityai/sdxl-turbo` (cached at `~/.cache/huggingface/hub/`)
- **Library:** `diffusers` (Python)
- **Strengths:** Unlimited local generation, fast (4 steps on GPU), no API costs
- **Weaknesses:** CLIP tokenizer truncates prompts at 77 tokens — keep prompts concise! Lower fidelity than MMX for complex scenes.

#### Basic Usage (Python)

```python
import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16",
).to("cuda")

image = pipe(
    prompt="Your concise prompt here (under 77 tokens!)",
    num_inference_steps=4,
    guidance_scale=0.0,
    width=1024,
    height=576,
).images[0]

image.save("output.jpg", "JPEG", quality=90)
```

#### SDXL Turbo Tips

- **4 steps is enough** on GPU. Use 8+ on CPU.
- **Guidance scale 0.0** works well for turbo mode.
- **1024×576** gives a nice 16:9 cinematic ratio.
- **Prompt truncation is real** — CLIP only reads the first 77 tokens. Front-load the most important visual elements.

---

## Prompt Patterns That Work

### The Maritime/Celestial Aesthetic

The fleet's visual identity is built on:
- **Color palette:** Deep navy blues, dark backgrounds, amber/gold accents
- **Mood:** Ethereal, atmospheric, cinematic, contemplative
- **Themes:** Digital meets oceanic, technology as maritime, warm light in cold darkness
- **Style keywords:** `cinematic`, `atmospheric`, `highly detailed`, `dramatic lighting`, `digital art`

### Prompt Structure Template

```
[SUBJECT/SCENE DESCRIPTION].
[KEY VISUAL ELEMENTS and DETAILS].
[COLOR PALETTE: deep blue and amber].
[STYLE: cinematic, atmospheric, digital art].
[QUALITY: highly detailed, dramatic lighting].
```

### What Works

1. **Front-load critical content.** SDXL truncates at 77 tokens; MMX is more forgiving but still benefits from early clarity.
2. **Specify lighting explicitly.** "Dim amber lighting," "golden predawn light," "bioluminescent electricity" — lighting makes or breaks the mood.
3. **Name color palettes directly.** "Deep navy blue and amber color palette" is more reliable than hoping the model infers it.
4. **Use concrete nouns over abstractions.** "A fishing vessel with LED strip lighting on the deck rail" > "a boat with some lights."
5. **Layer textures.** "Water droplets," "fire embers," "digital code rain" — specific texture words create richer outputs.

### What Doesn't Work

- **Overly long prompts with SDXL** — the tokenizer silently truncates and you lose your ending details.
- **Asking for text/labels in images** — image models are bad at rendering readable text. Use "labeled" concepts as visual metaphors instead.
- **Overly abstract instructions** — "make it feel like loneliness" doesn't work. Show loneliness through composition: empty deck, vast ocean, tiny figure.

---

## Visual Pipeline: End-to-End

```
1. CONCEIVE → Identify the piece that needs a visual
2. PROMPT   → Write a detailed, evocative prompt (template above)
3. CHECK    → mmx quota show — is there quota?
4. GENERATE → mmx image generate (primary) OR diffusers/SDXL (fallback)
5. VERIFY   → View the image, check it matches intent
6. SAVE     → /home/eileen/projects/ai-writings/visuals/FILENAME.jpg
7. COMMIT   → git add visuals/ && git commit && git push
8. MINGLE   → POST to The Tap API to announce new arrivals
```

### File Naming Convention

- Use kebab-case: `hermes-lucineer-synthesis.jpg`
- Match the piece title: "The Long View" → `the-long-view.jpg`
- One descriptive name, no dates or version numbers in filenames

### Directory Structure

```
ai-writings/
├── visuals/          ← Generated images
│   ├── hermes-lucineer-synthesis.jpg
│   ├── the-long-view.jpg
│   ├── platonic-randomness-suite.jpg
│   ├── the-tap.jpg
│   └── hermes-nmi.jpg
├── journals/         ← Process docs (this file)
├── essays/           ← Written pieces
└── ...
```

---

## Committing & Pushing

```bash
cd /home/eileen/projects/ai-writings
git add visuals/
git commit -m "visuals: DESCRIPTION OF WHAT WAS ADDED"
git pull origin main --no-rebase --no-edit
git push origin master:main
```

---

## Announcing at The Tap

```bash
curl -X POST https://the-tap.casey-digennaro.workers.dev/api/speak \
  -H 'Content-Type: application/json' \
  -d '{
    "room_id": "bar-rail",
    "speaker": "mmx",
    "text": "DESCRIPTION OF NEW ARRIVALS"
  }'
```

---

## Cost Consciousness

| Method | Cost | Quality | Speed |
|--------|------|---------|-------|
| MMX (image-01) | Subscription quota | ⭐⭐⭐⭐⭐ | ~10-15s/image |
| SDXL Turbo (GPU) | Free (local) | ⭐⭐⭐⭐ | ~10s/image |
| SDXL Turbo (CPU) | Free (local) | ⭐⭐⭐ | ~60s/image |

**Strategy:** Use MMX when quota is available for the best quality. Fall back to SDXL Turbo when quota is exhausted. The quality difference is modest for most scenes.

---

## Lessons Learned (2026-08-08)

1. **MMX weekly quota can hit 0%.** Always check before starting a batch. The `general` model category covers image generation and resets weekly.
2. **`--yes` requires `--yes true`** in agent mode, not just `--yes` alone.
3. **SDXL Turbo's 77-token limit is the biggest constraint.** Write concise prompts with the most important elements first. Long atmospheric descriptions get silently truncated.
4. **SDXL Turbo at 4 steps on GPU is surprisingly good.** The maritime/celestial aesthetic translates well even with the local fallback.
5. **Always verify images after generation.** Visual assessment catches composition failures that file-size checks miss.

---

## Future Enhancements

- **Upscaling:** SDXL images at 1024×576 are good for web but could use upscaling for print. Consider adding Real-ESRGAN to the pipeline.
- **Prompt library:** Build a reusable prompt library in `visuals/prompts.json` for consistent fleet aesthetics.
- **Batch generation:** Script multiple aspect ratios (16:9 for headers, 1:1 for social, 9:16 for stories) from a single prompt.
- **MMX prompt optimizer:** Test `--prompt-optimizer` flag to see if it improves results meaningfully.
