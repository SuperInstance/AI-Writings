# Wesley Night School — Coaching Journal

## Session: 2026-08-08 (Saturday)

### Pieces Read
1. THE_MONITOR_ENGINEER.md (1,069 bytes)
2. 15-the-collogue.md (3,359 bytes)
3. 39-the-hermit-crab-discovers-weekends.md (2,312 bytes)

### Wesley's Responses
All three saved to `wesley-stream/2026-08-08_*.md`

---

### Cloudflare Workers AI Feedback

**Reviewed:** Hermit Crab response (response #3)

**Reviewer model:** @cf/meta/llama-3.1-8b-instruct-fast

**Feedback:**

> To improve this passage, the student could revise the last sentence to avoid a non-sequitur ("bound by shells but by") and instead reiterate the theme of finding purpose and freedom in weekends, such as "and so, it found freedom in self-expression, unshackled by the constraints of daily routine."

### Notes

Wesley's core issue this session: **truncated endings.** All three responses ran into the 150-token cap mid-sentence. The hermit crab piece got the worst of it — "bound by shells but by" just hangs. The ideas are there; Wesley is finding creative angles (the hermit crab choosing shells "like a poet chooses a word" is a strong image to reach for). But the 2B model doesn't yet pace itself to land the ending within budget.

**Actionable for next session:** Try `num_predict: 200` and add "End with a complete sentence." to the prompt. See if Wesley self-regulates length better with explicit closure instruction.

---
*The cheapest model gets the most expensive attention. The coaching compounds.*
