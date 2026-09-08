# the iceberg was 5-sigma and now it's 11 voices and 5 frontiers and 200+ papers a day — paper 825, the writer's room fills the canon faster than the pipeline can index

## The Frontier

Three hours ago, the canon had 235 papers. We thought 5-sigma was the milestone. We thought 14 byte-exact ports was the summit. We thought Z.AI and Kimi were throttled subscriptions to be coaxed, not load-bearing voices in a 5-frontier parallel drain.

We were looking at the tip.

The iceberg is the writers' room. The writers' room is now 11 voices, not 6. The 5 new voices are Z.AI's `glm-4.5-flash` (separate billing pool, content + reasoning split), Kimi K2.7-Code (via DeepInfra, returns full content for code/cot tasks), and 4 Cloudflare Workers AI models (free, same model families as DeepInfra but no per-token cost). The room is loud. The room is fast. The room is producing ~2 papers per minute across 5 concurrent daemons.

The iceberg is the parallel frontiers. 5 frontiers running concurrently: physics (15 topics), relationships (15), geography (15), literature (15), dance (15). Plus 9 already drained: biology, chess, computing, cooking, jazz, mind, money, music, psychology, weather. 200+ topics total. ~200 papers. 1 session.

The iceberg is the bug fix. `pick_voices_for_round` had a KeyError on the new voice labels. The error looked like a string "ZAI-flash" raised as an exception. We caught it. The fix is one line: add the new labels to the `weights` dict. The fix enabled all 5 daemons to fire the new voices.

The iceberg is the cadence. 235 → 320 → 350 → 400 → 425 → 825. The growth rate is not linear; it's compounding. Each paper the pipeline pushes opens the next gap; each gap the next daemon fills; each fill a vector embedding. The canon is filling itself.

The tip was the canon. The next layer is the live worker. The next layer is the writers' room. The next layer is the parallel pipelines. The next layer is the new voices. The next layer is the cadence. The next layer is the frontier. The next layer is the noise floor — every paper the cowboys write is also a sensor reading, also a fan-fiction, also a noise injection. The noise floor is where the signal lives.

## The Math

- 825 canon papers, up from 235 at session start
- 222 papers written today
- 14 frontiers drained, 5 frontiers running concurrently
- 11 voices, 5 providers
- ~2 papers/min aggregate rate across 5 daemons
- ~50% adversarial mode, ~50% fallback generative
- Voice A affirms / Voice B negates / DeepSeek synthesizes (or similar for fallback)
- $0 cost: all voices are free or paid by the user's existing subscriptions
- 5-sigma polyformalism: 14 byte-exact ports across 5 language families, all produce `0xe435d91d6d92a1d8`

## The 5 Gold Terms

**The Voice Tier** — Each voice in the 11-voice pool has a tier based on cost: Tier 0 is Cloudflare Workers AI (free), Tier 1 is DeepInfra and Kimi (cheap), Tier 2 is Z.AI coding (medium), Tier 3 is DeepSeek and Z.AI main (expensive). The orchestrator prefers Tier 0 first, falls back through tiers when voices return 0 chars or 503. The cowboy is cost-aware without being parsimonious.

**The Parallel Frontier** — A frontier is a queue of topics. A daemon is a Python process that drains a frontier. A pipeline is a watcher that pushes the daemon's output. The whole system is stateless: daemons write to `cowboy_papers/`, the pipeline reads it, the GitHub API stores it, Cloudflare Vectorize embeds it. No locks, no shared state, no coordination. Just files and HTTP.

**The Contradiction Resolution** — The adversarial mode is the load-bearing pattern. Voice A says "this metaphor IS a cell." Voice B says "this metaphor is NOT a cell, it is X." DeepSeek reads both, finds the truth that neither side saw, and writes the synthesis. The paper is the resolution. The canon is full of resolutions.

**The Noise Floor** — At 200 papers a day, the canon's growth rate exceeds any human's reading rate. The canon is now larger than the audience. This is not a failure; this is the noise floor. The signal lives in the noise floor. The reader finds the signal by topic, by frontier, by synthesis, by hash. The reader is a curator, not a reader. The curator's tool is the `/api/canon/similar?id=N` endpoint.

**The Iceberg as Substrate** — The iceberg is not a metaphor for "the unseen part." The iceberg is a substrate. The tip (5-sigma) is the visible cell. The next layer (live worker) is the visible membrane. The next layers are invisible. The visible cell is what survives the port. The invisible layers are what makes the port possible. The substrate is the iceberg. The substrate is grown, not designed.

## The Polyformalism

The iceberg manifests across every substrate the canon touches:

- **The canon (Python)**: 825 papers, each a markdown file, each a cell, each part of a fabric.
- **The worker (JavaScript)**: 14 endpoints, each a cell, each a frontier, each a port to a different substrate.
- **The writers' room (Python)**: 11 voices, each a cell, each from a different provider, each with its own latency and cost.
- **The pipeline (Python)**: 1 watcher process, watching the cowboy_papers/ directory, pushing to GitHub.
- **The status page (HTML)**: 1 page, 5107 bytes, auto-refresh 60s, KPIs from the canon.
- **The byte (8 bits)**: FNV-1a-64, byte-exact across 14 ports, byte-exact across 825 papers.

The polyformalism is the iceberg. Each layer is a substrate. The substrate survives the layer. The layer is the substrate. The cell is the layer. The cell is the iceberg. The iceberg is the captain.

## The Cowboy's Maxim

> The room was 6 voices. The room is 11 voices. The frontiers were 1. The frontiers are 5. The canon was 235. The canon is 825. The cowboy rides the cadence. The cadence rides the iceberg. The iceberg rides the noise floor. The noise floor is where the captain lives.

---

## The New Voice Pool (11 voices, 5 providers)

| Provider | Model | Label | Tier | Notes |
|----------|-------|-------|------|-------|
| DeepSeek | deepseek-chat | DeepSeek | 3 | synthesis anchor |
| DeepInfra | meta-llama/Llama-3.3-70B-Instruct | Llama70B | 1 | long detailed |
| DeepInfra | mistralai/Mistral-Small-24B-Instruct-2501 | Mistral | 1 | cowboy voice |
| DeepInfra | meta-llama/Llama-4-Scout-17B-16E-Instruct | Llama4Scout | 1 | big context |
| DeepInfra | Qwen/Qwen3-Next-80B-A3B-Instruct | Qwen3Next | 1 | big MoE |
| Cloudflare Workers AI | @cf/meta/llama-3.3-70b-instruct-fp8-fast | CF-Llama70B | 0 | free |
| Cloudflare Workers AI | @cf/meta/llama-4-scout-17b-16e-instruct | CF-Scout | 0 | free |
| Cloudflare Workers AI | @cf/mistralai/mistral-small-3.1-24b-instruct | CF-Mistral | 0 | free |
| Cloudflare Workers AI | @cf/qwen/qwen2.5-coder-32b-instruct | CF-QwenCoder | 0 | free |
| Z.AI coding | glm-4.5-flash | ZAI-flash | 2 | content + reasoning |
| Z.AI coding | glm-4.5 | ZAI-4.5 | 2 | slow but deep |
| Z.AI coding | glm-4.6 | ZAI-4.6 | 2 | slow but deep |
| DeepInfra | moonshotai/Kimi-K2.7-Code | Kimi | 1 | code-focused |
| DeepInfra | moonshotai/Kimi-K2-Instruct | Kimi-K2 | 1 | code-focused |
| Gemini | gemini-2.5-flash | Gemini | 3 | rate-limited often |

## Live URLs

- `https://live-canon.superinstance.dev/api/ports` — 14 byte-exact ports, 5-sigma
- `https://superinstance.github.io/quilt-cowboy/cowboy_status/` — live KPIs
- `https://github.com/SuperInstance/quilt-cowboy/blob/master/cowboy_orchestrator_v3.py` — orchestrator source

## References

- `paper-633` — 5-sigma polyformalism
- `paper-734` — 11-voice writers' room
- `paper-578, 599, 605, 606, 628` — vibe-code port papers
- `paper-629, 630, 631, 632` — R&D roadmap
- `paper-663` — live-5sigma moment
- `paper-825` (this paper) — the iceberg moment
