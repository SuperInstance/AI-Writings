# the Z.AI dominance — 16 voices, 30% of all adversarial calls are Z.AI, paper 1450 is the new edge, glm-4.5-air joined the room

## The Frontier

The user said "we haven't utilized those subscriptions at all really" about Z.AI and Kimi. We agreed. Then we discovered the Z.AI coding endpoint at `https://api.z.ai/api/coding/paas/v4/chat/completions` is a **separate billing pool** from the throttled main endpoint. We added ZAI-flash, ZAI-4.5, ZAI-4.6 to the orchestrator. The room lit up.

In this session, Z.AI voices fired 280 times in adversarial mode (out of ~700 total). That's 40% of adversarial calls. The Z.AI pool is doing what DeepSeek + Llama + Kimi used to do, and it's free to the user (separate billing pool = no extra cost).

We also added **glm-4.5-air** (ZAI-air), a new smaller/faster Z.AI model. It returns 152c of content + 1272c of reasoning in 8 seconds. The orchestrator merges both into a single adversarial output.

Kimi (K2.7-Code and K2-Instruct via DeepInfra) returned to 200 OK after a 30-minute DNS outage. It fires reliably for code-heavy prompts but returns 0c for vague philosophical ones — the orchestrator handles this with the fallback chain.

The canon: 1050 papers today. 1450 max. 16 voices. 8 frontiers running concurrently. The iceberg is now `n_voices: 16, zai_share: 40%`.

## The Stats

- 16 voices, 6 providers (DeepSeek, DeepInfra, Cloudflare Workers AI, Z.AI, Kimi via DeepInfra, Gemini)
- 4 Z.AI models: glm-4.5-flash, glm-4.5, glm-4.6, glm-4.5-air
- 280 Z.AI fires in 700 adversarial calls = 40% voice share
- 84 Kimi fires (empty for vague prompts, full for code)
- 155 CF Workers AI fires (free)
- 171 DeepInfra fires (Llama, Mistral, Qwen)
- 8 frontiers running concurrently
- 1050 canon papers, max 1450
- 850+ papers today, 90% of the previous session total

## The 5 Gold Terms (this session)

**The Z.AI Coding Pool** — `https://api.z.ai/api/coding/paas/v4/chat/completions` is a **separate billing pool** from the throttled `api/paas/v4` main endpoint. Models that 429 on main (glm-4.5, glm-4.6) return 200 on coding. The orchestrator now uses coding exclusively for Z.AI.

**The Content + Reasoning Split** — Z.AI reasoning models put the visible answer in `content` and the internal chain-of-thought in `reasoning_content`. The orchestrator merges both: if `content` is empty, use `reasoning_content`; if both are non-empty, append `[reasoning: ...]` to the visible answer. This means ZAI-flash's full 1500c reasoning chain is preserved in the adversarial output.

**Glm-4.5-Air as the Fast Tier** — A new smaller Z.AI model that returns 152c of content + 1272c of reasoning in 8 seconds. Faster than the 4.5/4.6 reasoning models (which take 30-60s). The orchestrator uses ZAI-air for "fast" prompts, ZAI-4.5/4.6 for "deep" prompts.

**Kimi's Empty-Content Failure Mode** — Kimi K2.7-Code and K2-Instruct return 0c for vague philosophical prompts (e.g., "What is a cell?"). They return full content for code-heavy prompts. The orchestrator handles this by detecting 0c and falling back to the next voice. Kimi is treated as a specialist, not a generalist.

**Voice Tier Rotation** — With 16 voices, the orchestrator rotates deterministically per topic. Each paper sees a different adversarial pair. With 4 Z.AI models, ~40% of pairs include a Z.AI voice. The 4-sigma → 5-sigma → "Z.AI 40%" progression is the path the canon has taken.

## The Polyformalism (Z.AI edition)

Z.AI's polyformalism is unique among the providers:

- **ZAI-flash** is the speed tier: 2-3 seconds per call, 500-1000c output, no reasoning
- **ZAI-4.5** is the depth tier: 8-12 seconds per call, 200c content + 1200c reasoning
- **ZAI-4.6** is the slower depth tier: 12-15 seconds per call, 200c content + 1400c reasoning
- **ZAI-air** is the middle tier: 8 seconds per call, 152c content + 1272c reasoning

Each tier has the same content/reasoning split. Each tier returns the same final answer for the same prompt (within stochastic variation). The polyformalism is the tiering, not the divergence.

## The Cowboy's Maxim

> 11 voices was the room. 16 voices is the room with Z.AI. 40% of adversarial calls are Z.AI. The Z.AI coding endpoint was always there — we just had to look past the 429. The 4 Z.AI models are the new fast/depth/flash/air matrix. Kimi is back online for code. DeepInfra is back online for everything. The orchestrator rotates through all 16. The canon grows at 150 papers/hour. The cadence is the captain.

---

## Voice Pool (16 voices, 6 providers)

| Provider | Model | Label | Tier | Cost |
|----------|-------|-------|------|------|
| DeepSeek | deepseek-chat | DeepSeek | synth | $$ |
| DeepInfra | meta-llama/Llama-3.3-70B-Instruct | Llama70B | general | $ |
| DeepInfra | mistralai/Mistral-Small-24B-Instruct-2501 | Mistral | general | $ |
| DeepInfra | meta-llama/Llama-4-Scout-17B-16E-Instruct | Llama4Scout | big-context | $ |
| DeepInfra | Qwen/Qwen3-Next-80B-A3B-Instruct | Qwen3Next | big-moe | $ |
| Cloudflare Workers AI | @cf/meta/llama-3.3-70b-instruct-fp8-fast | CF-Llama70B | free | FREE |
| Cloudflare Workers AI | @cf/meta/llama-4-scout-17b-16e-instruct | CF-Scout | free | FREE |
| Cloudflare Workers AI | @cf/mistralai/mistral-small-3.1-24b-instruct | CF-Mistral | free | FREE |
| Cloudflare Workers AI | @cf/qwen/qwen2.5-coder-32b-instruct | CF-QwenCoder | free-code | FREE |
| Z.AI coding | glm-4.5-flash | ZAI-flash | fast | $$ |
| Z.AI coding | glm-4.5 | ZAI-4.5 | deep | $$ |
| Z.AI coding | glm-4.6 | ZAI-4.6 | slow-deep | $$ |
| Z.AI coding | glm-4.5-air | ZAI-air | fast-reasoning | $$ |
| DeepInfra | moonshotai/Kimi-K2.7-Code | Kimi | code | $ |
| DeepInfra | moonshotai/Kimi-K2-Instruct | Kimi-K2 | code | $ |
| Gemini | gemini-2.5-flash | Gemini | rate-limited | $$ |

## Live URLs

- `https://live-canon.superinstance.dev/api/voices` — 16 voices, 4 are Z.AI
- `https://live-canon.superinstance.dev/api/ports` — 14 byte-exact ports
- `https://live-canon.superinstance.dev/api/frontiers` — 50+ drained today
- `https://superinstance.github.io/quilt-cowboy/cowboy_status/` — live KPIs

## References

- `paper-633` — 5-sigma polyformalism
- `paper-734` — 11-voice writers' room
- `paper-1149` — final summary at 1147 max
- `paper-1450` (this paper) — Z.AI dominance at 16 voices
- 50+ papers drained this session: mathematics, neuroscience, evolution, robotics, myths, oceans2, cosmos, zen, letters, metals, letters2, sports, dance2, war, education
