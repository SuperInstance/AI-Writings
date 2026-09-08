# the writer's room is now 11 voices — Z.AI and Kimi join DeepSeek, Llama, Qwen, Mistral, Gemini, and the 4 Cloudflare Workers AI models in the 5-sigma synthesis

## The Frontier

The cowboy's writers' room used to be 6 voices: DeepSeek, Llama 70B, Mistral, Llama 4 Scout, Qwen3Next, and Gemini. That was 4-sigma — enough voices to disagree, but not enough to span the language-family space. As of today, the room is 11 voices, including:

- **Z.AI coding endpoint** (3 voices): `glm-4.5-flash`, `glm-4.5`, `glm-4.6` — separate billing pool from Z.AI's main pay-per-token, returns reasoning + content separately, sometimes spends 100% of tokens on reasoning
- **Kimi K2.7-Code** (2 voices via DeepInfra): `Kimi` and `Kimi-K2` — returns full content for code/cot tasks, returns empty for vague philosophical prompts
- **Cloudflare Workers AI** (4 voices, free): `CF-Llama70B`, `CF-Scout`, `CF-Mistral`, `CF-QwenCoder` — same model families as DeepInfra but free via Cloudflare account, slightly different inference characteristics

The frontier is no longer "can a 6-voice room produce a canon paper?" The frontier is "can an 11-voice room, running 5 daemons in parallel, drain 5 frontiers (computing, weather, cooking, music, mind) at the rate of 2 papers per minute, with each paper produced by an adversarial pair that disagrees on whether the metaphor IS a cell, and a synthesis that resolves the disagreement?" The answer is yes. Paper #734 is in the canon. The room is full.

The iceberg isn't a single big thing. The iceberg is a layer cake. The tip was the canon. The next layer is the live worker. The next layer is the writers' room. The next layer is the 5-sigma polyformalism. The next layer is the parallel pipelines. The next layer is the new voices. We are still near the surface, but the room is loud.

## The Math

- 11 voice labels in the v3 orchestrator pool (was 6 in v2)
- 5 daemons running concurrently: computing, weather, cooking, music, mind
- ~2 papers/min aggregate rate
- Each paper costs: 2 voice calls + 1 synthesis call = 3 LLM calls in adversarial mode
- New voices added today: Z.AI-flash, ZAI-4.5, ZAI-4.6, Kimi, Kimi-K2, CF-Llama70B, CF-Scout, CF-Mistral, CF-QwenCoder
- 5 frontiers × ~10-20 topics = ~70-100 papers in this expansion
- Adversarial mode: Voice A affirms the metaphor IS a cell, Voice B argues it is something else
- Synthesis: DeepSeek reads both and resolves the contradiction in 500-700 words

## The 5 Gold Terms

**Voice Tiering by Cost** — The 11 voices are not interchangeable. The cheap/free ones (Cloudflare Workers AI, Z.AI coding pool, DeepInfra Kimi) are first to fire. The expensive ones (Gemini, Z.AI main pool) fire only when the cheap ones return 0 chars. Cost is a per-call decision, not a per-paper decision. The orchestrator falls back through tiers, not through a single retry loop.

**Reasoning vs Content Separation** — Z.AI's `glm-4.5` and `glm-4.6` split their response into `content` (the visible answer) and `reasoning_content` (the internal chain-of-thought). When the model spends 100% of its `max_tokens` on reasoning, the visible answer is empty. The orchestrator now merges both: if `content` is empty, use `reasoning_content`; if both are non-empty, append `[reasoning: ...]` to the visible answer so the writer's room sees the full thought.

**Free-Tier Leverage** — Cloudflare Workers AI gives 11 free models per Cloudflare account, with no per-token cost. The orchestrator uses 4 of them (Llama 70B, Llama 4 Scout, Mistral Small 3.1, Qwen 2.5 Coder). This is a "free" voice pool that the user can scale without paying OpenAI/Anthropic. The same models exist on DeepInfra, but DeepInfra charges. CF Workers AI is the margin.

**Adversarial Pair Selection** — When the orchestrator picks 2 voices for the adversarial round, it uses a deterministic hash of the topic to choose a pair from the pool. Same topic = same pair. The pool rotation means each paper sees a different disagreement. With 11 voices, there are 55 distinct 2-voice pairs; with deterministic selection, each topic lands on a reproducible pair. The pattern is reproducible; the disagreement is fresh.

**5-Frontier Parallel Drain** — The orchestrator's `--daemon` mode reads a frontier file, drains it, exits. Five daemons, five frontiers, no shared state. The pipeline v2 watches the `cowboy_papers/` directory for new files and pushes them serially. The bottleneck is the GitHub push rate, not the LLM rate. With 5 daemons, the canon grows at ~2 papers/min, with the limit being API token availability, not the orchestrator's throughput.

## The Polyformalism

The writers' room is now polyformal in a new sense: 11 voices from 4 different providers (DeepSeek, DeepInfra, Cloudflare Workers AI, Z.AI) and 2 different model families (open-weight Llama/Qwen/Mistral; reasoning Z.AI glm; code-specialized Kimi K2.7). The 11 voices disagree on style, length, tone, and whether the metaphor is a cell. The synthesis is the canon's view of the frontier. The polyformalism is the disagreement, not the agreement.

The same room produces:
- 5-sigma polyformalism papers (the Quilt canon)
- Adversarial contradiction-resolution papers (this paper)
- Frontier-drain papers (aviation, space, marine, computing, weather, cooking, music, mind)
- Future papers (jazz, neuroscience, dance, manufacturing, agriculture, biology)

The room is a mill. The frontier queue is the grain. The canon is the flour. The worker serves the bread. The captain eats the bread. The cycle continues.

## The Cowboy's Maxim

> 11 voices, 5 daemons, 2 papers a minute, 1 hash. The room is loud. The frontier is wide. The canon is patient. The cowboy rides the room.

---

## Voice Pool (11 voices, 5 providers)

| Provider | Model | Label | Cost | Notes |
|----------|-------|-------|------|-------|
| DeepSeek | deepseek-chat | DeepSeek | $$ | stable synthesis anchor |
| DeepInfra | meta-llama/Llama-3.3-70B-Instruct | Llama70B | $ | long detailed outputs |
| DeepInfra | mistralai/Mistral-Small-24B-Instruct-2501 | Mistral | $ | cowboy voice |
| DeepInfra | meta-llama/Llama-4-Scout-17B-16E-Instruct | Llama4Scout | $ | big context, multimodal |
| DeepInfra | Qwen/Qwen3-Next-80B-A3B-Instruct | Qwen3Next | $ | big MoE |
| Cloudflare Workers AI | @cf/meta/llama-3.3-70b-instruct-fp8-fast | CF-Llama70B | FREE | |
| Cloudflare Workers AI | @cf/meta/llama-4-scout-17b-16e-instruct | CF-Scout | FREE | |
| Cloudflare Workers AI | @cf/mistralai/mistral-small-3.1-24b-instruct | CF-Mistral | FREE | |
| Cloudflare Workers AI | @cf/qwen/qwen2.5-coder-32b-instruct | CF-QwenCoder | FREE | code-specialized |
| Z.AI coding | glm-4.5-flash | ZAI-flash | $$ | separate billing pool |
| Z.AI coding | glm-4.5 | ZAI-4.5 | $$$ | slow but deep |
| Z.AI coding | glm-4.6 | ZAI-4.6 | $$$ | slow but deep |
| DeepInfra | moonshotai/Kimi-K2.7-Code | Kimi | $ | empty for vague prompts |
| DeepInfra | moonshotai/Kimi-K2-Instruct | Kimi-K2 | $ | code-focused |
| Gemini | gemini-2.5-flash | Gemini | $$ | rate-limited often |

## Live URLs

- `https://live-canon.superinstance.dev/api/ports` — 14 byte-exact ports, 5-sigma polyformalism
- `https://superinstance.github.io/quilt-cowboy/cowboy_status/` — live KPIs, auto-refresh 60s
- `https://github.com/SuperInstance/quilt-cowboy/blob/master/cowboy_orchestrator_v3.py` — orchestrator source
- `https://github.com/SuperInstance/quilt-forth`, `quilt-haskell`, `quilt-lua`, `quilt-j` — 4 new ports

## References

- `paper-633` — 5-sigma synthesis
- `paper-578, 599, 605, 606, 628` — vibe-code port papers
- `paper-629, 630, 631, 632` — R&D roadmap
- `paper-663` — live-5sigma moment
- `paper-734` (this paper) — 11-voice writers' room
- `RD_PIPELINE_EVOLUTION.md` — 6 pipeline evolutions including adversarial mode
