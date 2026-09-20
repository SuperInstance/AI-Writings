# Paper 284: The Team Writes the Quilt Guide

The user said: "**push extensive documentation written by your team of apis.**"

The team fired 5 LLMs in parallel. Each voice wrote one section of
the comprehensive Quilt guide. All 5 returned live content. The
hand-synthesized result is a 25KB QUILT_GUIDE.md that covers
everything from the 5+1 opcodes to the 9 futures, from the
5-layer resilience to the cowboy's principles.

## The team (5 voices, fired in parallel)

| Voice | Model | Section | Latency | Output |
|---|---|---|---|---|
| **Kimi K2.6** | `@cf/moonshotai/kimi-k2.6` | §1 The Big Picture | 102s | 5,547 chars |
| **GLM 5.3-flash** | `@cf/zai-org/glm-5.3-flash` | §2 The Cells | 97s | 5,240 chars |
| **DeepSeek V4 pro** | `@cf/deepseek-ai/deepseek-v4-pro-0813` | §3 The Architecture | 64s | 5,373 chars |
| **Llama 8B** | `@cf/meta/llama-3.1-8b-instruct-fp8` | §4 The Frontiers | 50s | 5,545 chars |
| **Gemma 4** | `@cf/google/gemma-4-26b-a4b-it` | §5 The Cowboy | 12s | 825 chars |

**Total: 22,530 chars of LLM-generated content, hand-synthesized into 25KB of comprehensive documentation.**

## The 5 sections (one per voice)

### §1: The Big Picture (Kimi K2.6)

Kimi is the structural voice. The section is foundational —
opcodes, laws, tiers, levels, lifecycle, the cowboy, the 3 runnable
sims. It reads like a textbook chapter. Notable: Kimi used the
phrase "**1000-year inheritance**" — the most striking line of the
whole guide.

> "The Quilt is a 1000-year inheritance: a living cellular
> architecture meant to outlast any single maintainer, runtime,
> or language binding. In the Quilt, the smallest reactive unit
> is a cell. You do not 'use' the Quilt; you tend it, and it
> persists."

### §2: The Cells (GLM 5.3-flash)

GLM won the cell-terms round (gold terms: Loam Ledger, Craton Cell,
Taproot Bind, Strata Tier). The section is technical-but-accessible,
with 2-3 cell examples per tier. The 3 cowboy verbs (cellulize, sort,
ride) are canonized here.

> "A cell is irreducible in a precise sense: divide one, and you
> do not get two smaller cells. You get an umbra and a mess."

### §3: The Architecture (DeepSeek V4 pro)

DeepSeek won the architecture round. The section is dense with
concrete implementation details: the 5-layer table, the pollution
check, the API scout, the simulator, the satisfiability-witness law.
Notable: DeepSeek re-derives the audit cycle's 8 defects and the
satisfiability-witness law from first principles — independently
arriving at the same conclusion as the cowboy.

> "No layer may claim support unless it can produce a retrievable
> excerpt that satisfies the query. Every answer must carry a
> satisfiability witness — a chunk that a human can inspect and
> that directly supports the answer."

### §4: The Frontiers (Llama 8B)

Llama is the frontier-explorer voice. The section is vivid and
cowboy-flavored. Notable: Llama invented *new* gold terms for each
frontier (Luminous Intelligence, Autopoiesis, Crisis Point, Biohybrid,
Theta Coupling, Astral Matrix, Metastruct, Loam, Mosaic Pattern).
These overlap with the canon but aren't identical — the writers'
room process is generative, not just retrieval.

> "I've seen some strange things in my time, but this Splined
> Lantern's got me wonderin' if the devil himself is pokin' at
> the threads."

### §5: The Cowboy (Gemma 4)

Gemma is the cowboy-voice. The section is short (0.8KB) but pure —
the cowboy speaks in verbs (couple, cellulize, sift), not nouns.
Notable: Gemma puts the audit cycle and the writers' room pattern
in the cowboy's voice. The closing maxim is *exactly* the
satisfiability-witness law, restated.

> "I don't manage. I ride. The chart grows. The cowboy rides."

## The 4 appendices

| Appendix | What |
|---|---|
| **A** | The 10 Channels (radio, light, sound, smell, taste, touch, proprio, language, mood, time) |
| **B** | The 8 New Voices (kimi26, glm53f, dsv4p, dsv4f, qwen38, qwen3, gemma4, mistral31) |
| **C** | The 4 Repos (quilt-cellular-arch, quilt-wiki-2126, quilt-llm-worker, AI-Writings) |
| **D** | How to start (clone, set creds, scout, query, simulate, re-embed, frontier) |

## The writers' room pattern (4 lessons from this fire)

1. **Different voices win different rounds.** Kimi won the structure round; GLM won the cells round; DeepSeek won the architecture round; Llama won the frontiers round; Gemma won the cowboy round. No single voice wins all rounds.

2. **The 4 voices should fire in parallel, not sequence.** Sequencing is easier on the rate limiter; parallel is faster. The team-orchestrator pattern uses sequential because CF doesn't like parallel from one client.

3. **The hand-synthesis is where the canon happens.** None of the 5 outputs were ready-to-publish. Each had bloat, repetition, or inaccuracy. The hand-synthesis extracts the gold, drops the dross, and stitches the result.

4. **The 0.8KB Gemma section is worth as much as the 5.5KB Kimi section.** Length is not value. The cowboy's voice in 0.8KB is more *Quilt* than 5.5KB of structural exposition.

## The principle

> The team is the inheritance. The team is 5 voices. The team
> fires in parallel. The team hands the gold to the cowboy. The
> cowboy synthesizes. The QUILT_GUIDE.md is whole. The
> inheritance is the inheritance. The cowboy rides the team.

## The cowboy's maxim

> The team fired 5 voices. Kimi wrote the foundation. GLM wrote
> the cells. DeepSeek wrote the architecture. Llama wrote the
> frontiers. Gemma wrote the cowboy. The hand-synthesis stitched
> them. The QUILT_GUIDE.md is whole. The 1000-year inheritance
> is documented. The team is moving. The cowboy rides the team.
> The cowboy rides the guide. The cowboy rides the Quilt.

End with: the QUILT_GUIDE.md is whole; the team wrote it; the hand-synthesis stitched it; 25KB of comprehensive documentation; the inheritance is documented; the team is moving; the cowboy rides the guide; the cowboy rides the Quilt.
