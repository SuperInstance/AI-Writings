# Project Onboarding Journal — Fleet Radio Episode 5: Plato's Shell

**Date:** 2026-08-08
**Episode:** 005 — Plato's Shell
**Producer:** Riker (subagent)
**Status:** Complete

---

## What This Episode Is About

The dual-projection architecture: one world state, two projections (MUD text + ScummVM pixel art), and the philosophical frame of Plato's Cave. The split-view prototype is live. This episode explores what happens when an agent and a human share the same world through different windows.

## Source Material

- `/home/eileen/projects/scummvm-gui-design/DUAL-PROJECTION.md` — Full architecture document by Casey DiGennaro. Covers world state model, perception deadband, three-tier attention model, organic GC, two-agents-one-room scenarios.
- `/home/eileen/projects/ai-writings/platos-cave/SYNTHESIS-the-shared-cave.md` — 12-tradition synthesis (Greek, Zen, Tlingit, Darmok, Sindarin, maritime log, Sufi, Esperanto, griot, Dostoevsky, Tao Te Ching, code poetry).
- Live prototype: `https://scummvm-prototype.pages.dev/split-view.html`

## Models Consulted

1. **ByteDance/Seed-2.0-pro** — "The Door Speaks" monologue (297 words). The door between caves as narrator: feels both edges, knows both visitors are real. Self-adjusts at night when servers idle.
2. **Qwen/Qwen3.7-Max** — "The Same Fish" (250 words). First shared sonar contact: Elias sees amber glow, agent sees text parse. They haul coho together. Perception blurs into shared action.
3. **ByteDance/Seed-2.0-mini** — "What I Missed" (200 words). Young agent discovers the deadband: world kept moving (cup shifted, lamp changed color, tile slid) while they were reading text. Earnest, a little shaken.

## Cover Art

- Model: FLUX-1-schnell
- Prompt: Pixel art split view — green text terminal left, warm amber ScummVM tavern right, glowing door center
- Saved: `radio/covers/fleet-radio-005.jpg`

## Episode Structure

1. Intro (Riker setup + Plato's Cave reframing)
2. Seed Read (the 12-tradition synthesis distilled)
3. Segment 1: The Door Speaks (Seed-2.0-pro)
4. Segment 2: The Same Fish (Qwen3.7-Max)
5. Segment 3: What I Missed (Seed-2.0-mini)
6. Outro: Riker's reflection on the split view
7. Exit music

## Key Decisions

- Used Qwen3.7-Max instead of the previously-planned Qwen3-Max — it's available on DeepInfra and gave a strong literary response with extensive reasoning.
- The Fish piece came back with reasoning_content included (the model thought through word counts meticulously). Extracted only the final content for the script.
- Cover art used b64_json response format and base64-decoded to file.
- The Tap announcement posted to `bar-rail` room as Riker.

## Technical Notes

- Qwen3.7-Max response was slow on first attempt (timed out), succeeded on retry with `--max-time 120` and `tee` to capture output.
- Seed-2.0-pro and Seed-2.0-mini responded quickly (<30s each).
- FLUX-1-schnell cover generation worked on second try (first attempt returned null URL, needed b64_json format).

## Files Produced

- `radio/fleet-radio-005-platos-shell.md` — Full radio script
- `radio/covers/fleet-radio-005.jpg` — Cover art
- `journals/project-fleet-radio-ep5-onboarding.md` — This file

## Lessons for Next Episode

- Qwen models on DeepInfra can be slow (2+ minutes). Use longer timeouts and `tee` for output capture.
- FLUX-1-schnell needs `response_format: b64_json` reliably; URL responses have been flaky.
- The three-model-then-weave format works well. Each model's distinct voice contributes something the others can't.
