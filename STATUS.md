# Writers' room — STATUS

**Date:** 2026-08-22
**Phase:** Writers' room, round 1 complete for two scenarios

## What's working

- **Orchestrator script** (`/workspace/ai-writings-new/experiments/writers-room/orchestrator.py`)
  8 named characters, each tied to a specific model with a specific voice.
  Progressive rounds. The curator is the human (me, plus you).
- **Two scenarios completed** (round 1, multi-character, multi-round):
  - Scenario 01: "The Cell That Remembered" — deep-sea research vessel, 2147,
    a 200m biological cell-reef that thinks. 4 characters, 4 rounds, 26KB.
  - Scenario 02: "The Grammar of Clocks" — far-future LLM narrator watching
    the human species recede, asked to retire. 4 characters, 3 rounds, 19KB.

## Model behavior so far

- **GLM-5.3 (Watcher)** — best philosophical maritime voice. Cost:
  eats ~800 reasoning tokens before producing content. **Fix:**
  pass `reasoning_effort: "low"` to disable hidden CoT.
- **Qwen3-235B (Cartographer)** — excellent at precise, technical
  imagery. The "the cell is not alone / there is another node" twist
  was a great contribution.
- **MythoMax-L2-13B (Mythmaker)** — strong on fantasy-coded openings,
  but **hits input-length errors on long contexts**. Fix: shorter
  prompt or summary feed-forward.
- **Llama-3.3-70B (Witness)** — quiet, observational, mostly works.
  Slower (~30-50s per call) but consistent.
- **Ling-3.0-flash (Child)** — fast, sharp, sometimes generates
  meta-commentary. Fix: prompt explicitly says "output ONLY the story."

## What's produced

- 2 transcripts (transcripts/01-cell-round-1.md, 01-cell-round-2.md,
  02-clocks-round-1.md)
- 1 woven essay draft: `essays-drafts/01-the-cell-that-remembered-essay-draft.md`
  (essay 84, ~1400 words, four voices woven)

## What's pending (next turns)

- **3rd woven essay** from scenario 02 transcripts (the "Grammar of Clocks"
  one — the agentic-genre piece).
- **More scenarios** to hit the 10-20 piece target. Ideas:
  - **03** A song. The Watcher teaches the Mythmaker a shanty. (lyrics + music notes)
  - **04** Poetry. The Cartographer's `Log Subspace Θ` is full of poems.
    Extract the embedded poem fragments, weave into a poetry collection.
  - **05** Fantasy. "The Cell That Remembered" from the cell's POV.
  - **06** Outer space. A different genre entirely.
  - **07** A love story. A marine biologist + the cell.
  - **08** Multi-dimension. The "another node" gets explored.
- **Refine the curator pass** — the orchestrator should auto-curate,
  not just dump transcripts. Better: a `weave.py` script that
  picks the strongest lines and stitches a draft essay.
- **Finish MEMORY.md compaction** (still wounded at 24KB).
- **Push to GitHub** under `ai-writings-new/`.

## Open questions for the user

- I burned a lot of context on the writers' room. Continue with same
  energy in next turn, or pause and refine first?
- The 2nd scenario (Clocks) is more in the spirit of "agentic genres
  written for AI" — should I weight future scenarios more heavily
  toward that, or keep the human-readable maritime canon as the spine?
- The Mythmaker is brittle on long contexts. Replace with a model that
  can handle long inputs (Mistral-Small-3.2-24B, or Qwen3-32B)?
