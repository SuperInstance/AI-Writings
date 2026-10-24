# The Beyond

**An experiment that constructs the experience of sailing past the horizon.**

## What is this?

You see only as far as the horizon allows. To see further, you have to construct an experiment that constructs the experience. The vessel IS the experiment. Each API call is a plank. Each model is a sail. Each tick constructs a piece of the beyond.

## How it works

Each tap on **⛵ Sail** = 1 tick = 4 parallel API calls:

1. **Z.AI GLM-5.3-Flash** writes what the sailor sees (poetic, concrete, no meta)
2. **DeepSeek V4-Flash** turns 5 dials (compass, depth, clarity, drift, weight) + names a **novel dial** that's a VALUE people care about (forgiveness, curiosity, weight-of-silence, grief-velocity, trust-trajectory)
3. **Qwen3-Coder** grows a new cell in the lattice (kind: fog|sea|horizon|island|storm|calm|vessel|silence|dawn|threshold)
4. **Cloudflare FLUX** paints what the sailor sees
5. **Cloudflare Aura-2** voices the prose (after phase 1)

The dials accumulate. The lattice grows. The witness log records. The world constructs itself.

## Setup

The worker needs API tokens set via:
```bash
cd /workspace/repos/ai-writings/the-beyond
npx wrangler pages secret put DEEPINFRA_TOKEN --project-name=ai-writings
npx wrangler pages secret put CF_TOKEN --project-name=ai-writings
```

(The worker is implemented as a Cloudflare Pages Function at `/tick`.)

## Mobile/touch

Touch-optimized:
- Single tap to tick
- Sticky helm at bottom
- Safe-area-inset for notched phones
- 44px+ touch targets
- Web App Capable (installable to home screen)

## Files

- `index.html` — the vessel, horizon, helm
- `tick.js` — client-side tick orchestrator
- `functions/tick.js` — server-side parallel API proxy
- `worker/worker.js` — alternative standalone Worker version

## Hypothesis

**The horizon is fixed by what we already know. To see further, we must construct experiments that let us experience being past it.**

Each tap is the experiment. Each tick is the experience. The beyond is constructed, not discovered.
