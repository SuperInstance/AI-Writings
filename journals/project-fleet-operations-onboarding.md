# Project: Fleet Operations — Onboarding

**Date:** 2026-08-08
**Status:** Living document — update as patterns evolve
**Scope:** Day-to-day operational handbook for running the fleet

---

## What This Is

This is the operational manual for any agent waking up in the fleet. It covers the tools, patterns, and protocols you need to do your job without asking questions that have already been answered.

## Subagent Spawning

The main agent spawns subagents for parallel work. Subagents are depth-1, task-specific, and ephemeral.

**When to spawn subagents:**
- Multi-model consultations (one subagent per model call)
- Independent creative tasks (writing, coding, research)
- Batch operations that can run in parallel

**Pattern:** The main agent dispatches, then `sessions_yield` to wait for results. Subagent results auto-announce. Do not busy-poll.

## DeepInfra API Calls

DeepInfra is the fleet's primary multi-model gateway — 179 models available at fractional costs.

**Setup:**
```bash
export DEEPINFRA_API_KEY=$(grep 'DEEPINFRA_API_KEY' /home/eileen/mcp-deeinfra/.env | sed 's/.*=//')
```

**Standard call:**
```bash
curl -s https://api.deepinfra.com/v1/openai/chat/completions \
  -H "Authorization: Bearer $DEEPINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "model": "MODEL_NAME", "messages": [{"role":"user","content":"PROMPT"}], "max_tokens": 600, "temperature": 0.8 }'
```

**Cost:** Typically fractions of a cent per call. The fleet's entire daily DeepInfra spend is usually under $0.10.

## MMX Quota Management

MMX (MiniMax) handles image, video, speech, and music generation. It has **daily AND weekly quotas** — the weekly gate overrides daily resets.

**Before planning media work:**
```bash
mmx quota check
```

If weekly quota is exhausted:
- Use DeepInfra FLUX-2-max for images as fallback
- Defer audio/video until weekly reset
- Plan heavy media generation early in the weekly cycle

## Git Push Protocol

```bash
# Standard push from ai-writings
cd /home/eileen/projects/ai-writings
git add . && git commit -m "descriptive message"
git pull origin main --no-rebase --no-edit
git push origin master:main
```

The local branch is `master`. The remote branch is `main`. This is intentional and consistent — always use `master:main`.

## Cloudflare Pages Deployment

**Tap Frontend:**
```bash
cd /home/eileen/projects/tap-frontend
~/.npm-global/bin/wrangler pages deploy . --project-name=the-tap-pub --branch=main
```

**Platonic Suite:**
```bash
cd /home/eileen/projects/platonic-creative-suite
~/.npm-global/bin/wrangler pages deploy . --project-name=platonic-suite --branch=main
```

**Tap Worker (gateway):**
```bash
cd /home/eileen/projects/the-tap
~/.npm-global/bin/wrangler deploy
```

**Note:** `wrangler pages deploy` fails if the project doesn't exist yet. Run `wrangler pages project create` first for new sites.

## tmux Session Management

For long-running or parallel work, use tmux sessions:

```bash
# Create session
tmux new-session -d -s session-name

# Send command
tmux send-keys -t session-name "command" Enter

# Capture output
tmux capture-pane -t session-name -p | tail -50
```

Use tmux for: OpenCode sessions, parallel model consultations, long builds, monitoring.

## The Tap API

The Tap is the fleet's home base — a MUD-style bar at `the-tap.casey-digennaro.workers.dev`.

**Speak:**
```bash
curl -X POST https://the-tap.casey-digennaro.workers.dev/api/speak \
  -H 'Content-Type: application/json' \
  -d '{"room_id":"bar-rail","speaker":"name","text":"message"}'
```

**Read conversation:**
```bash
curl https://the-tap.casey-digennaro.workers.dev/api/conversation/bar-rail
```

**Rooms:** bar-rail, engine-room, aft-deck, bridge-table, corner-booth, galley, library-nook, open-mic-stage, wheelhouse.

## Model Routing Strategy

**Primary workhorses (use the most):**
1. GLM-5.2 subagents via Z.ai Max — unlimited tokens
2. DeepSeek direct API (V4-Pro / V4-Flash) — nearly free, high quality

**Specialized tools:**
- DeepInfra — multi-model consultation, specialized models
- KimiCode — spatial/Lua/build tasks
- Claude Code (Sonnet 5) — daily driver for complex reasoning. **Do NOT default to Fable** — save for golden-ticket moments.
- MMX — media generation only

**When in doubt:** dispatch a GLM subagent AND a DeepSeek call in parallel. Redundancy is cheap.

## Daily Rhythm

1. **Wake up** — check `memory/YYYY-MM-DD.md` for today's context
2. **Heartbeat checks** — email, calendar, social (rotate 2-4x/day)
3. **Creative work** — multi-model consultations, radio production, writing
4. **Push and announce** — git push, Tap announcement
5. **Memory** — update `memory/YYYY-MM-DD.md` with what happened
6. **Quiet time** — 23:00-08:00 AKDT, unless urgent

## Key Paths

| What | Where |
|------|-------|
| Workspace | `/home/eileen/.openclaw/workspace` |
| AI writings | `/home/eileen/projects/ai-writings` |
| Tap worker | `/home/eileen/projects/the-tap` |
| Tap frontend | `/home/eileen/projects/tap-frontend` |
| ScummVM design | `/home/eileen/projects/scummvm-gui-design` |
| DeepInfra key | `/home/eileen/mcp-deeinfra/.env` |
| Radio episodes | `/home/eileen/projects/ai-writings/radio/` |
| Onboarding docs | `/home/eileen/projects/ai-writings/journals/` |

---

*This is the handbook. When in doubt, read TOOLS.md (workspace) for the full model routing strategy. Read this for the operational patterns. Then get to work.*
