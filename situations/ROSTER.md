# SuperInstance Model Roster

Live-verified 2026-09-27 against the account's own provider keys (presence
checked via env, no secret values ever printed or committed). Real model
ids and endpoint shapes below were confirmed with actual `GET /models` and
test calls — nothing here is guessed.

Client code: `src/providers.ts` (OpenAI-compatible chat providers),
`src/typesafe.ts` (the Jev judge API), `src/cli.ts` (manual CLI).

## Chat providers (OpenAI-compatible `/chat/completions`)

### DeepSeek — `deepseek`
- Endpoint: `https://api.deepseek.com` (env: `DEEPSEEK_KEY`)
- Real model ids: `deepseek-flash`, `deepseek-v4-pro`
- Auth: working, completions working
- Cost tier: cheap (flash) / mid (v4-pro)
- Cache: native prompt-cache accounting in every response
  (`usage.prompt_cache_hit_tokens`, `usage.prompt_tokens_details.cached_tokens`)
  — best target for the O10 cache-gaming strategy (stable prefix, vary tail).
- Observed shape: standard OpenAI `choices[0].message.content` + `usage`,
  plus a hidden `reasoning_tokens` count baked into `completion_tokens` even
  on `deepseek-flash` — short prompts can burn 30-90 reasoning tokens before
  any visible output.
- Example (redacted prompt/response, real behavior):
  - in: "A farmer has 17 sheep. All but 9 die. How many are left? ... prefix ANSWER:"
  - out: `"All but 9 die means 9 sheep survive.\n\nANSWER: 9"` — correct, ~1.1-1.7s latency
  - JSON-format test: valid JSON every time, no markdown fences
- Best org role: **cheap iterative dev** — fast, correct on simple reasoning
  and strict-format tasks, and the only provider whose cache economics we
  can exploit directly.

### DeepInfra — `deepinfra`
- Endpoint: `https://api.deepinfra.com/v1/openai` (env: `DEEPINFRA_KEY`)
- Real catalog: 187 models, incl. `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`,
  `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo`, `Qwen/Qwen3.5-27B`,
  `NousResearch/Hermes-3-Llama-3.1-405B`, `ByteDance/Seed-2.0-mini`,
  `ByteDance/Seed-2.0-pro`, plus image/audio/video engines.
- Auth: working, completions working
- Cost tier: sub-cent for 8B-class models (`estimated_cost` per call in
  response `usage`), scales up for 405B-class.
- Observed shape: OpenAI-standard, but `usage.prompt_tokens_details` is
  `null` (no cache accounting exposed) and `usage.estimated_cost` is present
  per call — good for cost tracking, not for cache-gaming.
- Gotcha (confirmed): `Qwen/Qwen3.5-27B` consumed its entire `max_tokens`
  budget on hidden reasoning and returned **empty** `content` at both 200
  and 600 max_tokens on a two-sentence creative prompt. Treat any
  DeepInfra "thinking"-class model as needing a large token budget
  (1000+) or it silently returns nothing.
- Best org role: **long-context digestion / cheap iterative dev**, split by
  model — small Llama-3.1-8B for cheap fast iteration (correct, well-
  formatted, sub-cent), Hermes-3-405B or Seed-2.0-pro for anything needing
  real depth, once given headroom for reasoning tokens.

### z.ai / Zhipu GLM — `zai`
- Endpoints: `https://api.z.ai/api/paas/v4` **and**
  `https://open.bigmodel.cn/api/paas/v4` (env: `ZAI_KEY`) — identical key,
  identical 11-model catalog on both hosts.
- Real model ids: `glm-4.5`, `glm-4.5-air`, `glm-4.6`, `glm-4.7`, `glm-5`,
  `glm-5-turbo`, `glm-5.1`, `glm-5.2`, `glm-5.3`, `glm-5.3-flash`,
  `glm-5.3-flashx`
- Auth: confirmed working (`GET /models` returns 200 on both hosts)
- Completions: **blocked** — `HTTP 429 {"code":"1113","message":"Insufficient
  balance or no resource package. Please recharge."}` on `glm-4.5-air`.
  This is an account-funding issue, not a code/auth issue.
- Best org role (once funded): **high-level ideation/orchestration** — GLM-5.x
  is the newest/highest tier in the account's roster and worth reserving for
  that once billing is resolved.

### Kimi/Moonshot — `kimi`
- Endpoint: `https://api.moonshot.ai/v1` (env: `KIMIAI_KEY`) — **not** `.cn`;
  the `.cn` host returned `HTTP 401 invalid_authentication_error` on this
  same key, `.ai` returned 200.
- Real model ids: `kimi-k3`, `kimi-k2.6`, `kimi-k2.7-code`,
  `kimi-k2.7-code-highspeed`
- Auth: confirmed working (`GET /models` 200 on `.ai`)
- Completions: **blocked** — `HTTP 429 exceeded_current_quota_error`,
  "account ... is suspended due to insufficient balance". Account-funding
  issue, not code/auth.
- Best org role (once funded): `kimi-k2.7-code`/`-highspeed` for cheap
  iterative dev on code tasks; `kimi-k3` for long-context digestion (Kimi's
  historical strength).

## Non-chat services (different shape — do not force into the chat adapter)

### MothQuantum
- Base: `$MOTHQUANTUM_BASE` = `https://api.mothquantum.com/api/v1`
  (env: `MOTHQUANTUM_KEY`)
- **Not an LLM API.** `GET /openapi.json` (title `moth-api`, v0.41.0) shows
  a "creative engines" platform: quantum-RNG (`comet-qrng-v1`), image/audio/
  MIDI/video generation engines (`qrc-image-v1`, `qrc-audio-v1`,
  `qrc-midi-v1`, `tessa-image-v1`, `blur-*`, `entanglement-shader-v1`,
  `tomography-api-v2`, `tamagotchi-v1`, etc.), plus asset storage and job
  management (`/api/v1/jobs`, `/api/v1/assets`).
- `GET /api/v1/me` confirms this is the account owner's own player account
  (`role: authenticated`, `platform_role: player`, email matches account).
- Best org role: **special-experimental** — true quantum randomness and
  generative-media engines, orthogonal to text LLMs. Not part of the chat
  casting call; worth its own integration if the fleet ever needs non-text
  generation or genuine hardware randomness.

### typesafe.ai
- Base: `https://api.typesafe.ai/v1` (env: `TYPESAFEAI_KEY`)
- **Not a chat API either.** It's "System One": `POST /v1/systemone` takes
  arbitrary `state` (string/object/array) plus named yes-no (`noul`),
  `choice`, or `score` questions, and returns per-question answers with
  confidence — a judge/classifier, not a generator.
- `GET /v1/models` lists `jev-latest` and `jev-preview`; a real call with
  `model: "jev-latest"` resolved to concrete id `jev-1.13.0` in the
  response.
- **This is the real thing this repo's `computeJev()` was named after.**
  `src/index.ts`'s `computeJev`/`jevFallback` are local hash-based
  placeholders standing in for exactly this API — a real confidence oracle
  that could gate the Pincher cache instead of a synthetic hash. Verified
  live: asking it to rate confidence of a vague, hedged statement ("The
  substrate observes: when cells compose, coherence increases.") returned
  `noul: 0.3` (low confidence) — plausible, real judgment, not noise.
- Best org role: **judging/gating**, not ideation — use it to replace the
  synthetic JEV math with a real confidence signal.

## No Fable-tier connection found
Searched the repo and environment for any whole-SuperInstance/Fable-level
wiring (config, env var, code reference) — none exists yet. `claude-fable-5-1`
is only a model id known to this session, not something referenced anywhere
in this repo or its env.

## Three most surprising things
1. **MothQuantum isn't an LLM at all** — it's a quantum-RNG + generative
   creative-media "engines" API tied to the account owner's own player
   profile, wildly different from every other provider in this roster.
2. **typesafe.ai's real model is literally named Jev** (`jev-latest` /
   `jev-preview`, resolving to `jev-1.13.0`), and it's a yes/no/score judge
   API — meaning this repo's pre-existing "JEV gating" concept was named
   after and should eventually call a real oracle, not the hash-based
   `computeJev` placeholder that shipped instead.
3. **Two of five chat providers are correctly wired but broke, not broken**
   — z.ai/GLM and Kimi/Moonshot both authenticate fine (`/models` returns
   200 with real, current-looking model catalogs) but reject every
   completion with an insufficient-balance error. Separately, DeepInfra's
   `Qwen/Qwen3.5-27B` silently eats an entire `max_tokens` budget on hidden
   reasoning and returns empty content unless given a large budget — a real
   gotcha for anything orchestrating these models automatically.
