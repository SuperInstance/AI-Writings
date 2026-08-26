# Deep Read: casting-call

## What it is (1 sentence)
A 432KB "living library of AI voices" — Layer 8 of the Slackwater stack — that maps pipeline roles to specific AI models via a `ModelAtlas` + `CastingDirector` pair, with each model profiled as an "instrument" with a voice character, tempo (BPM), cost, failure mode, and an "audition" record (24+ open-mic pieces, ensemble reviews, self-audits).

## Key concepts (3-7 bullet points)
- **Models as instruments, atlas as score** — *"A Roland from NousResearch and a Kurzweil from Anthropic share more DNA than two models from the same provider with different voices."* The atlas is organized by *what they sound like*, not who makes them. 6 voice families: The Narrators, The Precise Instruments, The Sensory Voices, The Catalysts, The Heavy Thinkers, The Builders, plus The Creative Firehose, The Local Crew, The Workhorse.
- **Pure data, pure functions** — `ModelAtlas` is a frozen dataclass; `CastingDirector` has no I/O, no side effects, no mutation of defaults. One-row model swaps: change one `ModelProfile`, measure against R2 trajectory set, commit.
- **Counterpoint constraint** — *no parallel octaves* (don't route the same model into two adjacent pipeline stages). The director enforces voice variety in the ensemble.
- **SWMIDI channel map** — pipeline stages assigned MIDI channels: ch10 = Seed-2.0-mini (intent_parse), ch11 = Seed-2.0-pro/Qwen3.6 (spatial planning), ch12 = Qwen3-Coder-480B (code_gen), ch13 = Hermes-405B (personality_wrap), ch14 = Nemotron-Ultra (safety_check). The orchestra metaphor is the routing scheme.
- **The 16-model canonical atlas** — HERMES_405B (Roland/narrator), GEMINI_PRO (Yamaha/synthesis), QWEN3_CODER (Precision/code), SEED_PRO (Analog Synth Pro/creative-planning), DEEPSEEK_V4_FLASH + DEEPSEEK_V4_PRO (Sensory Direct/cheap & deep), SEED_MINI (Analog Synth/catalyst), CLAUDE_OPUS (Kurzweil/P0 architecture), NEMOTRON_ULTRA (Pipe Organ/safety), KIMI_K3 + QWEN3_6 (Builders/spatial), MMX_M3 (Creative Firehose/media), GLM_5_2 (Workhorse/fallback), GRANITE_3_1_2B (Wesley/local Kurzweil Jr), QWEN_0_5B (cost-effective classifier).
- **"Models audit themselves"** — `SEED_NOTES.md` contains the three self-audits. The most-cited line: *"Depth isn't measured by parameter count — it's measured by how a fifty-word poem about barnacles can make a reader taste salt."* (DeepSeek-V4-Flash on itself.)
- **The Right Piece at the Right Moment** — meta-essay that re-frames the atlas from a router to a *curator*: which piece to read at 3 AM when you need to hear from something that understands. The atlas is also a literature canon, not just a config table.

## How it relates to the polyformalism (5 opcodes: BIND/LINK/EFFECT/VIEW/TICK)
- **BIND** — Each `ModelProfile` is a *binding* of a model_id to a `voice_character`, a BPM range, a cost/1k, a channel, and a "when to cast" predicate. The atlas is the binding table. New repos that introduce a new model or new role should ship a profile row, not prose.
- **LINK** — The pipeline stages form a directed graph: perception → casting-call → brain. The fallback chains (intent_parse: SEED_MINI → GLM_5_2 → DEEPSEEK_V4_FLASH) are LINK edges with priority. The counterpoint constraint is an anti-LINK rule: forbid certain adjacencies.
- **EFFECT** — `cast(role)` is the EFFECT opcode made literal: given a role string, you get a model and a "what this will sound like" prediction. The EFFECT is the *voice character* of the output, not just the byte stream. New repos should expose a `cast()` or equivalent that returns a profile, not just calls a model.
- **VIEW** — Each voice family is a *view* on what an LLM can be. Narrator-view, builder-view, catalyst-view — same underlying API, different binding. The "Models audit themselves" pattern is a *meta-view*: the model is asked to look at its own profile and correct it. Our new repos should expose both a system-view and a self-view.
- **TICK** — BPM range is the *tempo* TICK: 40–60 BPM (Opus, Nemotron — cathedral) vs 120–200 BPM (Qwen-0.5B — 178 tok/s). TICK = how long this call will take. Cost/1k is the dollar-TICK. New repos should declare a TICK range per role: "this call is reflex (1ms) or deliberation (12s)".

## What ideas we should borrow for our new repos
1. **The "voice character" axis** — for any system that calls multiple models/agents/strategies, give each one a one-line voice character plus 3-5 "Read it when" links to its actual output. *Voice* is the cheapest way to communicate what a component is for.
2. **`ModelProfile` as a frozen dataclass with no I/O** — pure data means the roster is diff-able, swappable, and testable. The 121 pytest tests in casting-call are made possible by this choice. Our new repos should keep their config as data, not behavior.
3. **Models audit themselves** — every component in the system should be able to narrate its own profile and *dispute* the system's characterization. This is the seed-note pattern; it's a cheap adversarial check that catches framing errors. Put it in the README from day 1.
4. **The "Right Piece at the Right Moment" frame** — for any curation/triage tool, ship a "if you're feeling X, read Y" index. Pre-composes the user's emotional state with a specific output. This is the casting-call's *actual product*, hidden under the routing framing.
5. **The 3-stage ensemble review** — every model is judged by (a) its own audition, (b) a peer review (DeepSeek reviews the fleet), (c) the user's testimony. This is an adversarial quality bar. Our new repos should run an ensemble review on themselves before publishing.

## 3-5 key links or terms to cross-reference
- ModelAtlas / CastingDirector — the two Python objects
- SEED_NOTES.md — Seed-mini, Seed-pro, DeepSeek-V4-Flash self-audits
- SWMIDI channel map — pipeline stages as MIDI channels (10–14)
- Counterpoint constraint — no parallel octaves / no same-model in adjacent stages
- "Depth is how a fifty-word poem makes a reader taste salt" — DeepSeek's reframe of the atlas's value system

## Top 3 most quotable lines (with attribution)
1. **"A living library of AI voices. Each model is an instrument. This is the score that knows which one to play, and when."** — *README.md (opening line)*
2. **"Depth isn't measured by parameter count — it's measured by how a fifty-word poem about barnacles can make a reader taste salt."** — *SEED_NOTES.md, DeepSeek-V4-Flash auditing its own profile*
3. **"Creativity is standing there long enough to choose the path nobody else saw."** — *SEED_NOTES.md, Seed-2.0-pro reframing its own "weakness" (12-second latency) as method*
