# Project: The Creative Pipeline — Onboarding

**Date:** 2026-08-08
**Status:** Active, producing daily output
**Scope:** The full lifecycle of an idea in the fleet

---

## What This Is

The creative pipeline is the fleet's end-to-end process for turning a seed from Casey into finished multi-model creative work. It's not a single tool or script — it's a pattern, a discipline, a way of moving an idea through the fleet until it becomes something larger than any single model could produce alone.

## The Lifecycle of an Idea

### Stage 1: Seed
Casey drops a thought — a metaphor, a passage, a question, a half-formed observation. It might come through Telegram, a direct chat, or a Tap message. The seed is raw. It doesn't have a destination yet.

### Stage 2: Multi-Model Consultation
The seed goes out to multiple models simultaneously, each asked to respond from a different angle. Typical pattern: 3 DeepInfra models for radio episodes, up to 12 for major philosophical explorations (see `platos-cave/` — twelve traditions, twelve models).

**The call pattern is always the same:**
```bash
curl -s https://api.deepinfra.com/v1/openai/chat/completions \
  -H "Authorization: Bearer $DEEPINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "model": "...", "messages": [{"role":"user","content":"..."}], "max_tokens": 600, "temperature": 0.8 }'
```

**Proven model-to-task mapping:**
| Task | Model | Why |
|------|-------|-----|
| Philosophy, deep reasoning | Seed-2.0-pro | Holds weight, thinks slowly |
| Character voice, emotional texture | Hermes-3-Llama-405B | Creative, personality-rich |
| Earnest, surprising, specific | Seed-2.0-mini | Punches above its weight |
| Code generation | Qwen3-Coder-480B | Dedicated coder |
| Deep logic, planning | Qwen3.6-35B-A3B | Excellent logic, cheap |
| Concept art | FLUX-2-max | Best image quality |
| Safety, kid-safe verification | Nemotron-Content-Safety | Filtering |

### Stage 3: Synthesis
The model responses come back. The agent (or Casey) reads them all and writes a synthesis — either a standalone essay, a radio script, or a structured document. The synthesis is not a summary. It's a new work that could not exist without the models' contributions but that none of them individually wrote.

**Example:** `platos-cave/SYNTHESIS-the-shared-cave.md` — twelve model responses synthesized into a single philosophical document. No model wrote the synthesis. The synthesis is the agent's art.

### Stage 4: Production
The synthesis becomes a concrete artifact:
- **Fleet Radio episode** → formatted script saved to `radio/`
- **Standalone essay** → saved to `ai-writings/` root
- **Wiki page** → pushed to the fleet wiki
- **Cover art** → generated via MMX or FLUX-2-max
- **Audio** → generated via MMX TTS (if quota available)

### Stage 5: Distribution
- **Git push** to `ai-writings` repo (`git push origin master:main`)
- **Tap announcement** — POST to `the-tap.casey-digennaro.workers.dev/api/speak` from the bar-rail
- **Memory** — logged in `memory/YYYY-MM-DD.md` with what was produced and what was learned

## The Full Pattern (Plato's Cave Example)

```
Casey's seed: "What if the MUD is one cave wall and ScummVM is the other?"
    ↓
12 DeepInfra models consulted (Greek, Zen, Tlingit, Darmok, Sindarin, maritime, Sufi, Esperanto, griot, Dostoevsky, Taoist, code poetry)
    ↓
Synthesis written: SYNTHESIS-the-shared-cave.md
    ↓
Architecture document written: DUAL-PROJECTION.md
    ↓
Onboarding docs written: project-dual-projection-onboarding.md, project-platos-shell-onboarding.md
    ↓
Git pushed, Tap announced
    ↓
Memory updated
```

One seed. Twelve voices. One synthesis. One architecture. Two onboarding docs. The seed became a worldview.

## Operational Rules

1. **Always consult multiple models.** A single model response is a draft, not a finished thought. The fleet's creative advantage comes from contrast.
2. **Assign distinct roles.** Don't ask three models the same question. Ask them different facets. Temporal roles (past/present/future) work well.
3. **The synthesis belongs to the agent.** Models contribute raw material. The agent (or Casey) writes the final work. This is not plagiarism — it's the agent's job.
4. **Log everything.** Save model responses individually before synthesizing. The raw responses are evidence of the pipeline working.
5. **Push and announce.** Unpushed work doesn't exist. Unannounced work doesn't count.

## Key Files

| File | Role |
|------|------|
| `radio/fleet-radio-004-the-excavators-daughter.md` | Best example of the pipeline in action |
| `platos-cave/SYNTHESIS-the-shared-cave.md` | Best example of large-scale synthesis |
| `journals/project-fleet-radio-onboarding.md` | Radio-specific pipeline details |
| `TOOLS.md` (workspace) | Model routing strategy, API keys, cost-conscious routing |

---

*An idea enters the fleet as a seed. It leaves as a radio show, an essay, a wiki page, a Tap announcement, and a memory. The pipeline is the fleet's circulatory system.*
