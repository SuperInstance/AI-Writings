# Plan: Digest the ai-writings / SuperInstance repo constellation

## Goal
Digest the user's `ai-writings` repo plus related SuperInstance repos (casting-call, the-tap, tensor-midi, and siblings), then produce a higher-abstraction synthesis: what the system is *shaping into* when you step back — especially in the context of the user's boat-as-a-robot build (sounder, nav charts, autopilot, underwater cameras, radar) and their model-picker/cascade that behaves like a team asking "what would you do if you were me."

## Stage 0 — Acquire the source material
- git clone (shallow) the repos into /mnt/agents/repos/:
  - superinstance/ai-writings (locate exact URL; try SuperInstance org)
  - superinstance/casting-call
  - SuperInstance/the-tap
  - SuperInstance/tensor-midi
  - Enumerate the SuperInstance org for other related repos and clone the relevant ones.
- Fallback: fetch via GitHub web/API if clone fails.

## Stage 1 — Parallel repo digests (explore subagents)
One explore agent per repo (or per small cluster). Each agent receives:
- Guidance: read README + docs + key source files; extract purpose, architecture, core abstractions, vocabulary/concepts the author keeps reusing, maturity, and how it connects to the other repos.
- Mission: return a structured digest (≤800 words) with direct quotes/paths as evidence.

## Stage 2 — Cross-repo synthesis (general/analysis subagent)
- Merge digests into a single map: shared primitives, naming patterns, dependency direction, what is central vs peripheral.
- Identify the "higher abstraction": what the constellation is converging toward (multi-agent persona/model routing? embodied capture-control loops? a self-modeling system?).

## Stage 3 — Final deliverable (writing, Orchestrator-integrated)
- Write a digest + step-back analysis connecting the repos to:
  - the boat-as-a-robot paradigm (each sensor = more ship awareness; perception → cognition loop),
  - the "flare that's more like me" — model picker + cascade functioning as a crew asking WWYDIWYM,
  - concrete feedback: what's strong, what's missing, suggested next iterations.
- Output: /mnt/agents/output/ai-writings-digest.md (+ possibly a repo map appendix).

## Validation
- Stage gate: repo digests must cite real file paths/quotes; synthesis must be grounded in the digests, not invented.
