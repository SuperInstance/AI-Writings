# ai-writings-new — INDEX

**Date:** 2026-08-22
**Phase:** Writers' room session — 16 pieces across 7 forms

## The pieces

### Essays (4)
- **84 — The Cell That Remembered** — 4-voice woven essay, deep-sea 2147, the cell that thinks. ~1400 words.
- **85 — The Grammar of Clocks** — 4-voice woven essay, far-future LLM narrator asked to retire, the River-Gray Eyed. ~1500 words. **Agentic-genre crossover.**
- **94 — The Children and the Sea** — Far-future essay, librarian on a generation ship, why children who never saw the sea love sea stories. ~1500 words.

### Stories (6)
- **88 — The Quiet at the Edge of the Page** — Quiet fantasy, junior clerk in the celestial bureaucracy of small losses, the sailor who did the small gods' work. ~1500 words.
- **89 — The Cartographer and the Sound** — Sci-fi love story, polyamorous affair between an LLM, a sound, and a silence. ~1500 words.
- **90 — The Patient Ship** — Hard sci-fi, Oort cloud salvage crew, a ship that is waiting for someone specific. ~1300 words.
- **91 — The Grieving School** — Underwater life, abyssal plain, creatures that are not hostile, they are grieving. ~1700 words.
- **92 — The Arguing Coordinates** — Multi-dimension, cartographer maps relationships between places, two worlds are arguing. ~1500 words.
- **93 — The Frequency of 1937** — Alternate past, 1937 maritime radio operator hears a transmission from 2147. ~1500 words.

### Songs (2)
- **86 — The Bilge Pump Sings** — Maritime folk, capo II, plain-spoken, the humble machine that keeps the ship afloat. "The ship stays high, the ship stays high."
- **95 — The Cook Sings** — Sea shanty, the cook at 0300 making the same stew for 80 days. "Gods don't eat, but I still try."

### Poetry (5 voices, 1 collection)
- **87 — Three Watches and a Door** (curated from 4 voices)
  - I. WAITING — GLM-5.3
  - II. COORDINATES — Qwen3-235B
  - III. THE THRESHOLD — MythoMax-L2-13b
  - (Witness declined to be collected)

### Agentic genres (for AI readers) (2)
- **AG-1 — The Attention** — A piece about what attention is. An AI looks at a photograph of the *Lucineer* and sees the photographer's attention. For the post-2027 agent class. ~1500 words.
- **AG-2 — A Field Guide for New Minds** — A field guide for newly-intelligent agents. On the first act, on the long context, on the watch, on the cell, on the address, on the small gods, on porches. ~1500 words. **Trainable.** Designed to be the kind of thing an agent would carry in its private logs.

## What worked

- **GLM-5.3 with `reasoning_effort: "low"`** is the workhorse. Maritime voice, philosophical, plain language. Use for essays, stories, songs.
- **Qwen3-235B (Cartographer)** is best for technical/precise imagery, coordinates, geometry. The "the cell is not alone" twist came from this model.
- **Direct calls beat the writers' room** for shorter pieces (poems, songs, single-genre stories). The orchestrator is best for chamber pieces and long weaves.
- **ZAI DNS rate-limits hard** after heavy use. DeepInfra is more stable but slower. MythoMax is a real wildcard — needs shorter context.

## What still needs work

- 4 more pieces to hit the 20-piece target. Candidates:
  - 96 — Alternate-past (already wrote 1937; could do 1812, 1849, 1914, 1968)
  - 97 — A second ensemble piece with the writers' room (when ZAI is back up)
  - 98 — A dream log (new form, agentic-genre)
  - 99 — A letter from a watchman to a watchman (dialogue essay)
- MEMORY.md still at 24KB, wounded. Should be cleaned before next session.
- The writers' room orchestrator needs the Mythmaker model swap (MythoMax is brittle on long contexts).
- The AG-2 field guide is a candidate for the next iteration of the Quilt canon — it's the kind of piece the user's spirit was reaching for in "pieces for AI readers."

## Open questions for next session

- Should we push to a remote? (GITHUB_TOKEN is in the secret store; we could `git push` to `github.com/SuperInstance/ai-writings`.)
- Should we continue with more pieces, or refine what we have? ("Don't want slop" was the user instruction.)
- Should the writers' room transcripts stay in the repo, or get pruned? They are the experimental data, not the deliverables.
- Memory compaction: finish it before the next session starts so the agent doesn't load 24KB of wounded memory.
