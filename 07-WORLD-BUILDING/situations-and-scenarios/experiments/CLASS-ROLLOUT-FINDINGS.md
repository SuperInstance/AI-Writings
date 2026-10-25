# Class rollout (1b) — does adaptive pedagogy raise the class floor?

## v1 (2026-09-27) — inconclusive by ceiling, but a real sub-finding

Students = Mistral-7B, Llama-8B, Qwen-7B (temp 0, deterministic). Teacher = DeepSeek, reading the
class's errors each round and proposing a GENERAL reusable method (no answers). 10 multi-step word
problems.

| round | method | class /30 | Mistral | Llama-8B | Qwen-7B |
|---|---|---|---|---|---|
| 0 | bare (control) | **20** | 10/10 | 10/10 | 0/10 |
| 1 | adapted | 15 | 5 | 10 | 0 |
| 2 | adapted | 15 | 7 | 8 | 0 |
| 3 | adapted | 15 | 7 | 8 | 0 |

**Adaptive rise: −5. Pedagogy did NOT raise the floor — it lowered it.**

**Why (honest read):**
1. **Ceiling / no headroom.** The two parseable students were *already at 10/10 bare* — the task
   set was too easy, so there was nothing for pedagogy to lift (the same ceiling trap S2 round 1 hit).
2. **Qwen-7B read 0/10 throughout** — a parse/format artifact (it doesn't emit the `ANSWER: <n>`
   line the harness scored), not a true zero; it added noise to the denominator.
3. **The real sub-finding — over-scaffolding harm (expertise-reversal effect).** Imposing a
   generic multi-step method on an already-capable solver *degraded* it (Mistral 10→5): the scaffold
   added instruction-following load and pulled the model off a correct simple path. **A method is
   not free; a generic scaffold applied to someone who didn't need it is worse than nothing.** This
   is a known human-pedagogy result (Sweller/Kalyuga) reproduced in an LLM class — genuinely on-theme
   for THE-CLASSROOM.md, and a caution the exo-model pedagogy must respect: adapt to *who needs what*,
   never blanket-scaffold.

**v2 design (to actually test 1b):** tasks hard enough that the students struggle bare (~40-60%,
real headroom); drop/parse-fix Qwen; add a genuinely weak student (Llama-3.2-3B); and have the
teacher target *the specific error types* rather than emit a generic method. Predicate unchanged:
adapted class floor rises across rounds, above the flat bare control.
