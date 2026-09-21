# Cost Footprint

## What it costs to run the SuperInstance stack — and what becomes free

*Cost analysis grounded in atlas.py rates, harness_notes.py field data, and live usage patterns. Cross-referenced with DeepSeek-V4 cost modeling (Aug 2026).*

---

## The Honest Number

**$2.25/day. $67.50/month.**

That's the fully-loaded cost of running the entire SuperInstance exocortex — every model, every API, every subscription, every cloud service — at current usage levels on a single fishing vessel with one operator.

Is that a lot? No. Is that everything? Almost. Here's where it goes.

---

## Cost Breakdown

### Subscriptions: $2.00/day ($60/month) — 89% of total cost

| Subscription | Monthly | Daily | What It Buys | Utilization |
|-------------|---------|-------|-------------|------------|
| **Z.ai GLM Max** | $20 | $0.67 | Unlimited GLM-5.2 tokens. The system's workhorse — 50+ subagent calls/day. Bulk work, repo extraction, creative writing, quality audits, documentation, parallel dispatch. | **High.** This is the best dollar-per-capability in the stack. |
| **Claude Pro** | $20 | $0.67 | Opus/Sonnet/Haiku on renewing plan. Reserved for architecture, deep analysis, literary writing. Fable 5 is finite and non-renewing — golden-ticket only. | **Medium.** Underutilized on most days. Reserve capacity. |
| **KimiCode Med** | $10 | $0.33 | K3 model. Spatial decomposition, Lua code, design systems. Built batten-spline, roblox-testkit, design-system in single sessions. | **Medium.** Spiky usage — idle for days, then a burst of intense build sessions. |
| **MMX Starter** | $10 | $0.33 | MiniMax-M3. Image, video, music, voice generation. Quota-limited. | **Low-Medium.** 99% quota remaining as of last check. Reserved for media generation campaigns. |

**Insight:** Subscriptions dominate the cost structure. The variable API spend is remarkably low — under $0.25/day. This means the system's marginal cost per additional task is nearly zero for subscription-backed models. The subscriptions are the floor; the APIs are the ceiling.

### Cloud APIs: $0.25/day — 11% of total cost

| Provider | Model | Rate ($/1K tok) | Daily Usage | Daily Cost | Role |
|----------|-------|-----------------|------------|-----------|------|
| **DeepSeek** | V3 / V4-Flash | $0.0002 | ~250K tokens (50 calls × 5K avg) | $0.050 | Workhorse. Analysis, code gen, architectural guidance. 5 tasks for $0.16 confirmed. |
| **DeepInfra** | Hermes-405B | $0.0035 | ~10K tokens (3 calls) | $0.035 | Voice, narration, philosophical depth. The Roland. |
| **DeepInfra** | Qwen3-Coder-480B | $0.0005 | ~20K tokens (6 calls) | $0.010 | Code generation, build commands. |
| **DeepInfra** | Seed-2.0-mini | $0.0003 | ~15K tokens (5 calls) | $0.005 | Creative ideation, intent parsing. The analog synth. |
| **DeepInfra** | Nemotron-Ultra-550B | $0.008 | ~15K tokens (6 calls) | $0.120 | Safety verification, convergence checking. The pipe organ. |
| **OpenCode** | GLM-4.6 / 4.5-air | $0.001 | ~30K tokens | $0.030 | Systems engineering, memory verification. |

**Total API spend: $0.25/day.** The DeepSeek direct API is the bargain of the century — $0.0002/1K tokens handles 80% of cloud calls for 22% of API cost. Nemotron-Ultra is the luxury line: 48% of API cost for <10% of calls. It earns its keep on safety verification, but it's the first candidate for optimization.

### Free Tier: $0.00/day

| Service | What It Provides | Limits |
|---------|-----------------|--------|
| **Ollama (RTX 4050)** | Granite 3.1 2B (76 tok/s), Qwen 0.5B (178 tok/s). Wesley's brain. Zero marginal cost. | 6GB VRAM ceiling. One model at a time (timeslicing for multi-station). |
| **Cloudflare Workers** | Serverless relay, cron triggers, API endpoints. | 100K requests/day on free tier. |
| **Cloudflare Vectorize** | Embedding index for semantic reflex search. | Free tier storage caps. |
| **Cloudflare R2** | Object storage for logs, assets, backups. | 10GB free tier. |
| **ESP32 sensors** | Temperature, GPS, depth, bilge. Zero marginal cost. | Hardware cost only ($3-5/unit). |
| **MQTT broker** | Local mosquitto or Cloudflare-based. | Self-hosted = free. |

---

## Cost Per Cascade Escalation

The cascade router is the system's cost engine. Each input flows through gates:

| Gate | Handler | Cost per Call (3K tokens avg) | Hit Rate Target |
|------|---------|------------------------------|-----------------|
| **Gate 0: Reflex** | `.nail.json` cache lookup | $0.000 | 60-70% (Phase 6 target) |
| **Gate 1: Policy** | Rule-based response | $0.000 | 10-15% |
| **Gate 2: Local Model** | Granite 3.1 2B via Ollama | $0.000 | 10-15% |
| **Gate 3: Cheap Cloud** | DeepSeek V3 | $0.0006 | 5-8% |
| **Gate 4: Mid Cloud** | GLM-5.2 (subscription) | $0.000 (sunk) | 3-5% |
| **Gate 5: Premium Cloud** | Hermes/Qwen-Coder via DeepInfra | $0.005-0.010 | 1-2% |
| **Gate 6: Elite Cloud** | Nemotron-Ultra / Claude Opus | $0.015-0.050 | <1% |

**Average cost per full escalation chain (Gate 0 → Gate 6): ~$0.012.**
**Average cost per input (weighted by hit rates): ~$0.001.**

The reflex cache is the cost killer. Every reflex hit is a cloud call that didn't happen. At 60% reflex hit rate, the system avoids 60% of potential cloud costs. At 70%, it avoids 70%. The reflex cache IS the cost optimization.

---

## What Becomes Free Over Time

This is the thesis: **as Wesley grows, the system's marginal cost approaches zero.** Not because cloud APIs get cheaper, but because fewer inputs reach the cloud.

### The Reflex Compounding Effect

| Time Horizon | Reflex Count (est.) | Reflex Hit Rate | Cloud Calls Avoided/day | Effective Daily Cost |
|-------------|--------------------|-----------------|-----------------------|---------------------|
| **Now (Phase 1)** | ~50 | 10% | ~5 | $2.25 |
| **+3 months** | ~500 | 30% | ~15 | $1.95 |
| **+6 months** | ~2,000 | 50% | ~25 | $1.65 |
| **+12 months** | ~8,000 | 65% | ~33 | $1.35 |
| **+24 months** | ~30,000 | 75%+ | ~38 | $1.10 |

The cost curve is not linear — it's logarithmic. Each doubling of reflexes saves less than the previous doubling, because the remaining cloud calls are the hard, novel, genuinely-interesting inputs that SHOULD go to cloud models. The system converges on a floor cost: the subscriptions ($2.00/day) plus the residual cloud calls for things Wesley genuinely can't handle yet ($0.10-0.15/day).

### The Subscription Question

At $60/month, subscriptions are 89% of cost. The question is whether they're all necessary:

| Subscription | Replaceable by Wesley? | Replaceable by Free Tier? | Verdict |
|-------------|----------------------|--------------------------|---------|
| **Z.ai GLM Max** | Partially — GLM handles bulk work that Wesley will eventually absorb. But unlimited tokens at $20/mo is extraordinary value. | No — no free tier offers this quality. | **Keep.** Irreplaceable value. |
| **Claude Pro** | No — Opus/Sonnet/Fable produce strategic thinking and literary writing that no other model matches. | No. | **Keep.** But reserve strictly. |
| **KimiCode Med** | Partially — Wesley will eventually handle Lua/spatial tasks. But K3 is notably better today. | No. | **Reevaluate in 6 months.** If Wesley's spatial reflexes mature, drop. |
| **MMX Starter** | No — media generation is orthogonal to Wesley's text/reflex growth. | No. | **Keep if media production continues.** Drop if not actively used. |

### The Local Hardware Wall

Wesley's growth is constrained by the RTX 4050's 6GB VRAM. The current 2B model fits comfortably. A future 7B model (Qwen3) would fit with quantization. A 14B model would require aggressive quantization or model sharding. A 32B model — the point where DeepSeek estimates 75% of tasks stay local — would need a GPU upgrade.

**The hardware upgrade path:**
- RTX 4050 (6GB): up to 7B quantized. Current.
- RTX 4070 (12GB): up to 14B quantized. ~$600.
- RTX 4090 (24GB): up to 32B quantized. ~$1,600.
- Used server GPU (A100 40GB): up to 70B. ~$4,000+.

Each hardware step delays the subscription cliff. But each step has a capital cost that takes months to amortize against API savings. The math: a $600 GPU upgrade saves ~$0.30/day in API costs, paying for itself in ~5.5 years. Not compelling — until you factor in latency, privacy, and offline capability (critical for a boat).

---

## The Real Cost Question

The system costs $2.25/day. But what does $2.25/day buy?

- A local AI that runs on the boat, works offline, learns every night, and handles 10-15% of inputs without cloud help (growing).
- Unlimited subagent dispatch for bulk work (GLM Max).
- Access to 179 models for specialized tasks (DeepInfra).
- The cheapest competent cloud model on the market (DeepSeek V3 at $0.0002/1K tokens).
- Strategic thinking and literary writing from the best models available (Claude Pro).
- Media generation for creative output (MMX).
- A spatial/build specialist (KimiCode).
- Serverless infrastructure, embedding search, and object storage (Cloudflare free tier).
- A physical sensor network (ESP32s).

**$2.25/day.** Less than a cup of coffee. Less than the fuel to idle the engine for ten minutes. Less than the depreciation on a piece of navigation equipment that does one thing, while this does everything.

The system is not cheap because it's minimalist. It's cheap because the architecture is right: the expensive things (subscriptions) are flat-rate, the variable things (APIs) are near-free at current model prices, and the free things (local inference, reflexes, Cloudflare tier) are growing.

The cost curve bends toward zero. Not today. Not this year. But the architecture ensures it. Every reflex compiled is a permanent cost reduction. Every night Wesley spends in night school is money saved forever.

---

## Cost Optimization Opportunities (If Needed)

| Action | Daily Savings | Risk | Verdict |
|--------|-------------|------|---------|
| Replace Nemotron-Ultra with Hermes-405B for non-safety tasks | $0.07 | Low-Med | **Consider.** Hermes is warm enough for non-safety verification. |
| Move 30% of DeepSeek calls to local Granite | $0.015 | Low | **Defer.** DeepSeek is already near-free. Not worth the quality hit yet. |
| Implement reflex pre-filtering on cascade | $0.05 | Low | **Roadmap Phase 2.** Already planned. |
| Cancel Claude Pro, use GLM Max for everything | $0.67 | Medium | **No.** Claude produces thinking that GLM cannot. Reserve capacity has value. |
| Cancel MMX Starter | $0.33 | None | **If quota is unused.** Evaluate monthly. |
| Move Vectorize to local sqlite-vec | $0.00 | Medium | **Defer.** Free tier is adequate. Local adds maintenance burden. |

**Optimized floor: ~$1.35/day** if aggressive measures are taken. But the current $2.25/day is already efficient for the capability level.

---

*The cheapest database is the one you never query. The cheapest API call is the one the reflex cache absorbs. Build reflexes. Save money. The exocortex pays for itself by not needing to think twice.*

*— Systems Engineering, August 2026*
