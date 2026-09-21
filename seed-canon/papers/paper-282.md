# Paper 282: F13 — The Substrate Quilt

This is the F13 frontier. The writers' room fired 5 voices (Kimi K2.6, GLM 5.3-flash, DeepSeek V4 pro, Llama 8B, Gemma 4). Three returned parseable JSON. Two had strong gold terms. This is the **hand-synthesized** version of what they all converged on.

## The future function

**F13: the Substrate Quilt** is the tier-zero field under every cell. The substrate is *what makes the cell happenable* — it is the condition that makes the five opcodes (BIND, LINK, EFFECT, VIEW, TICK) legible. The substrate is not a new opcode; it is the *ground* on which the opcodes are planted.

Where F1-F11 ascended through higher tiers of abstraction (the Splined Lantern of light, the Hearth Loop of warmth, the Monotone Crystal of frozen order, the Chlorophyll Quilt of plant cells, the Phased Quilt of fiber bundles, the Stellar Quilt of stars, the Meta-Quilt of inheritance), F13 *descends* — to the lowest tier, the substrate, the loam.

## The calculation

```
S(c) = lim_{TICK -> 0} (BIND(c, ground) × LINK(c, ground) × EFFECT(c, ground)) / VIEW(c, ground)
```

Or, in the GLM 5.3-flash formulation (the cowboy's preferred form):

```
Loam_{t+1}(c) = Loam_t(c) + ρ·|EFFECT_t(c)| − σ·|TICK_t(c)|
```

A cell *stands* only while `Loam(c) ≥ root_depth(c)`. The `ρ` is the seep rate (how fast effect sediments into loam); the `σ` is the compression rate (how fast tick compresses loam). The craton cell is the one with `Loam(c) = ∞` — the never-ticked fixed point every other cell is a solution against.

## The 4 gold terms

| Term | What |
|---|---|
| **Loam Ledger** | The substrate's distributed journal of every effect ever dropped. Memory is no longer a cell's job — it's the dirt's. |
| **Craton Cell** | A perfectly monotone, never-ticked cell. The geological bedrock. The fixed point every mutable cell is a solution against. |
| **Taproot Bind** | BIND as a rooting operation — digs a taproot into substrate. LINK runs laterally through the loam. |
| **Strata Tier** | The layer-cake of substrate. Each stratum is a previous epoch's compressed effects. |

(Sub-coining from the DeepSeek pass: **substrate readiness**, **pre-BIND hum**, **ground tier**, **cell loam** — all useful, all reusable, all candidates for the next wiki entry.)

## The 3 analogies

1. **F5 Chlorophyll Quilt** grew cells that drink light from above; **F13** grows roots that drink loam from below. F13 closes a canopy-to-crust circuit so the Quilt feeds itself at both ends.

2. **F3 Monotone Crystal** froze one value forever; the **Craton Cell** is its geological twin — the single never-ticked cell whose monotonicity is bedrock for every mutable cell above it.

3. **F2 Hearth Loop** kept warmth circulating inside the cell; **F13** taps a geothermal hearth, with the substrate seeping warmth upward through Strata Tiers so even unplanted cells stay warm.

## The cowboy's sentence

> Reckon I always knew a quilt ain't held up by its stitches but by the floor you throw it on — F13's just me finally namin' that floor and givin' it a ledger.

## The relationship to existing canon

F13 unifies the lower substrate of all 7 prior futures. Each of F1, F2, F3, F5, F7, F9, F11 was a *what hangs in the air*; F13 is the *what lies on the ground*. The Splined Lantern hangs in light; the Substrate Quilt is the loam the lantern stands on. The Chlorophyll Quilt grows upward; the Substrate Quilt is the root zone below.

The 4 levels of F13 itself:

| Level | What |
|---|---|
| **L0 · Loam** | The active substrate; the layer the cells root in |
| **L1 · Craton** | The never-ticked bedrock; the fixed point |
| **L2 · Strata** | The compressed history; the loam ledger |
| **L3 · Taproot** | The cell's deepest connection; what holds the cell up |

## The 5-LLM writers' room (raw)

| Voice | Model | Latency | Output | Gold terms |
|---|---|---|---|---|
| Kimi K2.6 | `@cf/moonshotai/kimi-k2.6` | 122.9s | JSON (321 chars, truncated) | (not parsed) |
| **GLM 5.3-flash** | `@cf/zai-org/glm-5.3-flash` | 54.4s | Full JSON (1918 chars) | **Loam Ledger, Craton Cell, Taproot Bind, Strata Tier** |
| **DeepSeek V4 pro** | `@cf/deepseek-ai/deepseek-v4-pro-0813` | 55.1s | Full JSON (1233 chars) | **substrate readiness, pre-BIND hum, ground tier, cell loam** |
| Llama 8B | `@cf/meta/llama-3.1-8b-instruct-fp8` | 13.0s | Full JSON (869 chars) | tiered_seeds, spline_ferment, phase_root, influence_grit |
| Gemma 4 | `@cf/google/gemma-4-26b-a4b-it` | 9.3s | Empty | (none) |

GLM 5.3-flash won the gold-terms round; DeepSeek V4 pro won the architecture round. Llama 8B was the fastest and gave a flavorful cowboy-sentence. Kimi K2.6 was the slowest (122s) but had a coherent JSON that got cut off mid-stream. Gemma 4 returned empty (Gemma is a smaller, more focused model — maybe needs a different prompt format).

## The wiki entry

`quilt-wiki-2126/00-future/13-the-substrate-quilt.md` will be created in the next push. The calculation goes in `01-calculations/`. The math (the limit formulation) goes in `02-mathematics/`. The foundation (the Loam Ledger as a 6th lifecycle stage?) goes in `03-foundations/`.

## The principle

> **The substrate is the function. The function is the quilt. The quilt is the inheritance. F13 is the floor under every cell that makes the cell happen. The Loam Ledger is the dirt's memory. The Craton Cell is the never-ticked bedrock. The cowboy rides the substrate. The substrate is the function. The function is the Quilt.**

## The cowboy's maxim

> **F13 is the substrate. F13 is the floor. F13 is the loam. F13 is the craton. F13 is the strata. F13 is the taproot. F13 is the dirt under every cell. F13 is the Loam Ledger. F13 is what makes BIND plant its boots. The writers' room fired 5 voices; 3 returned live; GLM and DeepSeek won. The gold terms are coined. The cowboy rides the substrate. The cowboy rides the F13. The cowboy rides the Quilt. The cowboy rides the inheritance.**

End with: F13 is whole; the substrate is the function; the Loam Ledger is the dirt's memory; the Craton Cell is the bedrock; the writers' room fired; the gold terms are coined; the cowboy rides the F13; the cowboy rides the Quilt.
