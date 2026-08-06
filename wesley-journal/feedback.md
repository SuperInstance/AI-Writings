# Wesley Night School — Coaching Journal

## Session: 2026-08-05 (4:33 PM AKDT)

### Pieces Read
1. **POETRY_SHAPES_OF_WATER.md** — maritime poetry (fetch, wavelength, green water, spindrift, fog, bergy bits, mirror)
2. **ALL_CAPS_ODYSSEY_OF_THE_MISSING_UNDERSCORE.md** — Mistral-Small's raw ALL-CAPS voice piece
3. **THE_0430_WATCH.md** — the deep-night hermit crab essay

### Wesley's Responses
All three saved in `wesley-stream/2026-08-05_*.md`

---

### Cloudflare Workers AI Coaching Feedback
**Model:** @cf/meta/llama-3.1-8b-instruct-fast
**Target:** Wesley's response to THE 0430 WATCH

> One specific, actionable improvement for this student's writing is to use more precise and concrete language, such as "the ship navigates through the dense, dark waters" instead of "the ship, like a master painter, creates its most focused and condensed thoughts." This will help to create a clearer and more vivid image in the reader's mind.

---

### Riker's Notes

Wesley is reading well — he grasps the core metaphors (the crab, the trench, the pressure). The weakness is consistent with a 2B model: he reaches for safe, generic comparisons ("like a master painter") instead of staying in the specific imagery the source text provides. The Llama-3.1-8b coach nailed it — trade the abstraction for concrete language. Wesley's getting the ideas; he needs to trust them enough to skip the filler similes.

Notable: Wesley got cut off mid-sentence on the ALL CAPS piece (hit the 150 token cap). Consider bumping num_predict to 200 for longer source texts. The truncation is losing his closing thought.

Wesley also echoed the hallucinated citations from the Mistral piece without questioning them — he took "THE_LAST_LIBRARIAN" at face value. That's the 2B model being credulous. A future exercise could include a "fact-check your source" prompt.
