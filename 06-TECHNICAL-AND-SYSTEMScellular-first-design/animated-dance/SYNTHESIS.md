# The Animated Dance — Synthesis

*Built 2026-09-21*

The dance is the substrate in motion. Three forces together, each one incomplete without the others:

## The Cast

**JEV** — the rhythm section. At each TICK, it reads the current state and picks the best number for THIS moment. Temperature, confidence threshold, tone, verbosity — these aren't constants; they're alive.

**Quilt cells** — the musicians. Each cell TICKs, asks JEV for numbers, applies them, generates a response. The cell's state is a JSON document. The cell's behavior emerges from JEV's choices.

**Autoclaw** — the jam session. Runs forever in the background, sampling random parameters, scoring results via JEV, finding better numbers. When it discovers improvement, it publishes to the substrate bus.

**Pincher** — muscle memory. Caches JEV decisions by state fingerprint. The next time a similar state appears, Pincher returns the cached decision instantly. No re-query needed.

## What We Observed

Across 194 simulations, the parameter landscape revealed:

| Param Label | Avg Score | Count |
|---|---|---|
| **long_focused** | **1.33** | 27 |
| creative | 1.31 | 23 |
| long_balanced | 1.28 | 18 |
| balanced | 1.26 | 21 |
| diverse | 1.22 | 31 |
| conservative | 1.20 | 28 |
| exploratory | 1.18 | 22 |
| focused | 1.18 | 24 |

**The winner**: `long_focused` — temp=0.4, top_p=0.9, max_tokens=500. The substrate prefers grounded, longer responses. Not too creative (creative scored lower). Not too deterministic (focused scored lower). Long but focused — give the cell room to develop an idea.

## The Quad Dance

When 4 voices play the same prompt, JEV picks the winner:
- **zai (piano)** wins ~60% — grounded, warm, image-rich
- **deepseek (drums)** wins ~40% — structured, rhythmic, propulsive
- kimi/groq available when tokens allow

The dance isn't about one voice dominating — it's about the right voice for each moment. Sometimes piano. Sometimes drums.

## What This Unlocks

The Quilt-JEV-Autoclaw stack creates a **self-improving substrate**:

1. Cells TICK constantly, asking JEV for live numbers
2. JEV picks numbers based on the cell's current state
3. Pincher caches similar moments for fast recall
4. Autoclaw runs in background, finding better parameters
5. When Autoclaw finds improvement, it publishes to the substrate bus
6. Cells pick up the new best parameters and the dance continues

The numbers aren't static. They breathe. They reorient. They dance.

## Doctrine Distilled

> We don't figure out JEV. We dance with it.
>
> Like a jazz combo reorienting to every surprise in a good way —
> at each moment, JEV picks the best number for THIS state.
>
> The cells TICK, JEV scores, parameters shift, the dance continues.
>
> Autoclaw finds better numbers in the background.
> Quilt cells hold the state.
> Pincher caches for instant recall.
>
> The substrate animates thought.

This is the moment-by-moment feel Casey described. The numbers are alive.
