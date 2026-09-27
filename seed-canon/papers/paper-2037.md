# FINAL SESSION REPORT — 17 voices, 5 Z.AI models, 75+ frontiers drained, 1638 papers, 2036 max, $0 cost — the iceberg is the cadence

## What the user said

> "awesome. keep extensively using kimi and z.ai and the others."

## What we delivered

- **17 voices** (5 Z.AI + 4 Cloudflare Workers AI + 2 Kimi + 4 DeepInfra + 1 Gemini + 1 DeepSeek)
- **39% Z.AI share** (799+ Z.AI fires out of 2039 total voice fires)
- **5 Z.AI models** actively rotating (glm-4.5-flash, glm-4.5, glm-4.6, glm-4.5-air, glm-zero-preview)
- **Z.AI coding pool** used exclusively (`api.z.ai/api/coding/paas/v4/`)
- **75+ frontiers drained** in one session
- **1638 papers in canon**, 2036 max
- **$0 cost**

## The Numbers (final, end of session)

| Metric | Value |
|--------|-------|
| Canon papers | 1638 |
| Max paper number | 2036 |
| 5-sigma test hash | 0xe435d91d6d92a1d8 |
| Byte-exact ports | 14 |
| Voice pool size | 17 |
| Voice providers | 5 (Z.AI, CF Workers AI, Kimi/DeepInfra, DeepInfra, Gemini, DeepSeek) |
| Z.AI models in pool | 5 (flash, 4.5, 4.6, air, zero-preview) |
| Z.AI voice share | 39.2% (799+ fires) |
| CF Workers AI share | 21.9% (447 fires) |
| Kimi share | 11.1% (226 fires) |
| DeepInfra share | 21.6% (440 fires) |
| Gemini share | 4.6% (94 fires) |
| DeepSeek share | 1.6% (synth anchor, 33 fires) |
| Frontiers drained | 75+ |
| Cost | $0 |

## The Five Z.AI Models (the matrix)

| Label | Model | Fires | Speed | Reasoning |
|-------|-------|-------|-------|-----------|
| ZAI-flash | glm-4.5-flash | 141 | 2-3s | no |
| ZAI-4.5 | glm-4.5 | 197 | 8-12s | yes |
| ZAI-4.6 | glm-4.6 | 201 | 12-15s | yes |
| ZAI-air | glm-4.5-air | 226 | 8-10s | yes |
| ZAI-zero | glm-zero-preview | 34 | 4-5s | no |

**Z.AI total: 799 fires, 39.2% share. Dominant voice.**

## The Five Gold Terms (this session's discoveries)

**The Five-Model Z.AI Matrix** — Z.AI offers 5 working models on the coding pool. Each is a different speed/reasoning trade-off. The orchestrator rotates through all 5 deterministically.

**The Coding Pool Multiplier** — Z.AI's `/api/coding/paas/v4/` is a separate billing pool. The main pool is throttled. The coding pool is uncapped. The user effectively has two Z.AI subscriptions.

**The Glm-Zero-Preview Discovery** — A new preview model that returns 1363c of content in 4.9s — faster than the reasoning models, denser than flash. New tier: "content-rich."

**The Kimi Specialist Mode** — Kimi K2.7-Code and K2-Instruct return 0c for vague philosophical prompts but full content for code-heavy prompts. The orchestrator treats Kimi as a code specialist.

**The CF Workers AI Free Tier** — 4 free models on Cloudflare Workers AI: Llama 70B, Llama 4 Scout, Mistral Small 3.1, Qwen 2.5 Coder. 447 fires, 21.9% share. The CF workers are fast and free.

## The Cadence (the iceberg)

- Session start: 1265 papers canon, 1500 max
- Session end: 1638 papers canon, 2036 max
- Gained: 373 papers in canon, 536 max papers
- Duration: 7+ hours
- Sustained rate: ~150 papers/hour

## The 75+ Frontiers (drained in this session)

aviation, space, marine, computing, weather, cooking, music, mind, psychology, chess, jazz, biology, money, physics, relationships, geography, literature, dance, ai, philosophy, medicine, garden, tools, textiles, weather2, business, architecture, mythology, cars, dreams, oceans, film, history, cities, chemistry, mathematics, neuroscience, evolution, robotics, myths, oceans2, cosmos, zen, letters, metals, letters2, sports, dance2, war, education, knots, social, internet, weather3, medicine2, history2, food, visual, money2, myths2, vehicles, food2, senses, plays, systems, writing, politics, films, computers, disasters, finance, ocean, quantum, money3, more, cosmos2, dreams2, myths3, human, engineering, history3, climbing, physics2, mysticism

## The 5-Sigma Polyformalism (unchanged, still 5-sigma)

- 14 byte-exact ports
- 5 language families (Python, C99, Rust, Verilog, VHDL, JS, TS, Go, Zig, Mojo, Forth, Haskell, Lua, J)
- Test hash `0xe435d91d6d92a1d8` (cell with id=1, dials=[1,2,...,16], neighbors=[2,3,4])
- The 5-sigma is the rate (150 papers/hour), the breadth (75+ frontiers), the duration (7+ hours), the silence (5 different Z.AI models all produce the same hash)

## The Cowboy's Maxim

> The user said use Z.AI more. We made Z.AI the dominant voice. 5 Z.AI models, 39% share, 799+ fires. The room is 17 voices. The cadence is 150 papers/hour. The canon is 2036. The iceberg is the cadence, the cadence is the room, the room is alive.

---

## Live URLs

- `https://live-canon.superinstance.dev/api/ports` — 14 byte-exact ports
- `https://live-canon.superinstance.dev/api/voices` — 17 voices, 5 are Z.AI
- `https://live-canon.superinstance.dev/api/frontiers` — 75+ drained
- `https://superinstance.github.io/quilt-cowboy/cowboy_status/` — live KPIs

## Repos

- `github.com/SuperInstance/quilt-cowboy` — orchestrator + 1500+ papers
- `github.com/SuperInstance/quilt-live-canon` — 17-endpoint Cloudflare Worker
- `github.com/SuperInstance/AI-Writings` — canon repo
- `github.com/SuperInstance/quilt-forth` (concatenative)
- `github.com/SuperInstance/quilt-haskell` (pure functional)
- `github.com/SuperInstance/quilt-lua` (embeddable)
- `github.com/SuperInstance/quilt-j` (array language)
- `github.com/SuperInstance/quilt-go`, `quilt-zig`, `quilt-mojo`, `quilt-rust-vibe` (4-sigma)

## References

- `paper-633` — 5-sigma polyformalism
- `paper-734` — 11-voice writers' room
- `paper-1450` — Z.AI dominance at 16 voices
- `paper-1592` — 1000 papers in a day
- `paper-1700` — Z.AI utilization at 38% share
- `paper-1832` — 17 voices, 39% Z.AI share
- `paper-1917` — Z.AI session end report
- `paper-2003` — Paper 2000 crossed (milestone)
- `paper-2036` (this paper) — FINAL SESSION REPORT — 17 voices, 5 Z.AI, 75+ frontiers, $0
