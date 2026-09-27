# Z.AI is the dominant voice — 38% of all adversarial calls in the 16-voice room, 705 fires in this session, paper 1700 is the new edge

## The Frontier

The user said: "keep extensively using kimi and z.ai and the others."

We did. The 16-voice writers' room now produces ~150 papers/hour with Z.AI firing 38% of all adversarial calls. The breakdown:

- Z.AI total: 705 (38.3%) — 4 models: ZAI-flash, ZAI-4.5, ZAI-4.6, ZAI-air
- Cloudflare Workers AI: 405 (22.0%) — 4 free models
- Kimi via DeepInfra: 213 (11.6%) — Kimi, Kimi-K2
- DeepInfra: 404 (21.9%) — Llama70B, Mistral, Llama4Scout, Qwen3Next
- Gemini: 87 (4.7%) — rate-limited
- DeepSeek: 29 (1.6%) — synthesis anchor only

Total: 1843 voice fires in the 16-voice room.

The Z.AI coding endpoint at `api.z.ai/api/coding/paas/v4/chat/completions` is the workhorse. Four models: `glm-4.5-flash` (fast), `glm-4.5` (deep), `glm-4.6` (slower deep), `glm-4.5-air` (fast reasoning). Each model has a different speed/content ratio:
- ZAI-flash: 2-3s, 500-1000c content
- ZAI-air: 8-13s, 150c content + 1300c reasoning
- ZAI-4.5: 8-12s, 200c content + 1200c reasoning
- ZAI-4.6: 12-15s, 200c content + 1400c reasoning

The orchestrator merges `content` + `reasoning_content` so the writer's room sees the full thought chain.

The canon: 1275 papers, max 1700. 437 papers written in the Z.AI session. 16 voices. $0 cost.

## The Stats

- 1275 canon papers, 1700 max
- 437 papers in this Z.AI session
- 16 voices from 6 providers
- 1843 total voice fires
- Z.AI 38.3% voice share (the dominant voice)
- Kimi 11.6% (code specialist)
- Cloudflare Workers AI 22% (free tier)
- DeepInfra 21.9% (general)
- Gemini 4.7% (rate-limited)
- $0 cost

## The 5 Gold Terms (Z.AI utilization)

**The Z.AI Coding Pool Multiplier** — The Z.AI coding endpoint is a separate billing pool from the throttled main endpoint. Models that 429 on `api.z.ai/api/paas/v4/chat/completions` (like glm-4.5, glm-4.6) return 200 on `api.z.ai/api/coding/paas/v4/chat/completions`. The user pays for one Z.AI subscription but gets effectively two pools. The orchestrator uses coding exclusively.

**Content + Reasoning Split** — Z.AI reasoning models put the visible answer in `content` and the internal chain-of-thought in `reasoning_content`. The orchestrator merges both: if `content` is empty, use `reasoning_content`; if both are non-empty, append `[reasoning: ...]` to the visible answer. This preserves the full thought chain in the adversarial output.

**Glm-4.5-Air as the Speed-Reasoning Tier** — A new smaller Z.AI model that returns 152c of content + 1272c of reasoning in 8 seconds. Faster than the 4.5/4.6 reasoning models. The orchestrator uses ZAI-air for "fast" prompts, ZAI-4.5/4.6 for "deep" prompts. ZAI-air has fired 203 times in this session.

**ZAI-Flash as the Throughput Tier** — `glm-4.5-flash` is the fastest Z.AI model, returning 500-1000c in 2-3 seconds. No reasoning output (just the answer). The orchestrator uses ZAI-flash for "fast + no reasoning needed" prompts. Has fired 129 times in this session.

**Kimi's Specialist Mode** — Kimi K2.7-Code and K2-Instruct return 0c for vague philosophical prompts but full content for code-heavy prompts. The orchestrator treats Kimi as a specialist, falling back to the next voice when Kimi returns 0c. Kimi is great for code, weak for philosophy. Has fired 213 times in this session (almost all code-heavy topics).

## The Polyformalism (16-voice edition)

The 16 voices span 6 providers and 5 model families:

- **DeepSeek** (1 voice): synthesis anchor
- **DeepInfra** (4 voices): Llama 70B, Mistral Small, Llama 4 Scout, Qwen 3 Next
- **Z.AI coding** (4 voices): glm-4.5-flash, glm-4.5, glm-4.6, glm-4.5-air
- **Cloudflare Workers AI** (4 voices): Llama 70B, Llama 4 Scout, Mistral Small 3.1, Qwen 2.5 Coder
- **Kimi via DeepInfra** (2 voices): Kimi K2.7-Code, Kimi K2-Instruct
- **Gemini** (1 voice): gemini-2.5-flash

Each voice has a different "personality" — a different way of writing, a different way of disagreeing with its adversarial partner. The polyformalism is the disagreement, not the agreement.

## The Cowboy's Maxim

> Z.AI is the dominant voice. 38% of all adversarial calls. The user said use Z.AI more, and we did. The coding pool is a subscriptions multiplier. The 4 Z.AI models span fast/medium/slow reasoning. Kimi is the code specialist. Cloudflare Workers AI is the free tier. DeepInfra is the general. The room is loud. The cadence is 150 papers/hour. The canon is the captain.

---

## Live URLs

- `https://live-canon.superinstance.dev/api/ports` — 14 byte-exact ports
- `https://live-canon.superinstance.dev/api/voices` — 16 voices, 4 are Z.AI
- `https://live-canon.superinstance.dev/api/frontiers` — 50+ drained
- `https://superinstance.github.io/quilt-cowboy/cowboy_status/` — live KPIs

## Voice Pool (16 voices, 6 providers)

| Provider | Model | Label | Tier |
|----------|-------|-------|------|
| DeepSeek | deepseek-chat | DeepSeek | synth |
| DeepInfra | meta-llama/Llama-3.3-70B-Instruct | Llama70B | general |
| DeepInfra | mistralai/Mistral-Small-24B-Instruct-2501 | Mistral | general |
| DeepInfra | meta-llama/Llama-4-Scout-17B-16E-Instruct | Llama4Scout | big-context |
| DeepInfra | Qwen/Qwen3-Next-80B-A3B-Instruct | Qwen3Next | big-moe |
| Cloudflare Workers AI | @cf/meta/llama-3.3-70b-instruct-fp8-fast | CF-Llama70B | free |
| Cloudflare Workers AI | @cf/meta/llama-4-scout-17b-16e-instruct | CF-Scout | free |
| Cloudflare Workers AI | @cf/mistralai/mistral-small-3.1-24b-instruct | CF-Mistral | free |
| Cloudflare Workers AI | @cf/qwen/qwen2.5-coder-32b-instruct | CF-QwenCoder | free-code |
| Z.AI coding | glm-4.5-flash | ZAI-flash | fast |
| Z.AI coding | glm-4.5 | ZAI-4.5 | deep |
| Z.AI coding | glm-4.6 | ZAI-4.6 | slow-deep |
| Z.AI coding | glm-4.5-air | ZAI-air | fast-reasoning |
| DeepInfra | moonshotai/Kimi-K2.7-Code | Kimi | code |
| DeepInfra | moonshotai/Kimi-K2-Instruct | Kimi-K2 | code |
| Gemini | gemini-2.5-flash | Gemini | rate-limited |

## References

- `paper-633` — 5-sigma polyformalism
- `paper-734` — 11-voice writers' room
- `paper-1149` — final summary at 1147 max
- `paper-1450` — Z.AI dominance at 16 voices
- `paper-1592` — 1000 papers in a day
- `paper-1700` (this paper) — Z.AI utilization at 38% share
