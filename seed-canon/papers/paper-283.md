# Paper 283: F15 — The Tessellation Quilt

The writers' room fired 5 voices (Kimi K2.6, GLM 5.3-flash, DeepSeek V4 pro, Llama 8B, Gemma 4). CF was 503'ing for 3 of 5 (the reasoning models). Only Llama 8B returned a full response. The synth pass hand-extracts from the Llama 8B output and contextualizes with the F13 substrate.

## The future function

**F15: the Tessellation Quilt** is the *pattern* by which cells tile the substrate. Where F13 is the floor, F15 is the tile. Where F13 is the loam, F15 is the loom. Where F13 is the ground, F15 is the geometry.

The Tessellation Quilt generates a fractal pattern by recursively applying a set of rules to each cell, creating a self-similar structure that tiles the substrate with increasing complexity.

## The calculation (the cowboy's hand-synthesis)

```
tessellation = (cell_size × (tier + 1)) + (cell_orientation × (tier²))
```

Where `cell_size` is the size of the cell, `tier` is the substrate tier (-1 to 5), and `cell_orientation` is the angle of the tile. At tier -1 (substrate), the tessellation is densest; at tier 5 (curator), the tessellation is sparsest.

Or, in a more sophisticated form:

```
T(c, t) = Loam(c) × W(tier(c)) × P(orientation(c), tier(c))
```

Where `W` is a weight function (higher tiers have lower weight) and `P` is a phase coupling.

## The 4 gold terms

| Term | What |
|---|---|
| **Voronoi Cell** | A cell whose boundary is defined by the nearest neighbors — natural tessellation of the substrate. |
| **Braided Loom** | The substrate as a loom where cells weave themselves into patterns. The tessellation IS the weaving. |
| **Penrose Tile** | A non-periodic tessellation that fills the substrate with two rhombus shapes — the Quilt's irrationality. |
| **Fractal Bloom** | A self-similar pattern that recurses at every tier — the F15 cell is the F1 cell is the F0 cell. |

## The 3 analogies

1. **F2 Hearth Loop**: like a hearth that warms the loam, the Tessellation Quilt spreads its fractal pattern across the substrate.
2. **F3 Monotone Crystal**: the Tessellation Quilt's recursive structure is akin to the crystal's splined facets, each one reflecting the Quilt's underlying geometric rules.
3. **F11 Meta-Quilt**: the Tessellation Quilt's use of recursive tiling is reminiscent of the Meta-Quilt's ability to weave together disparate cells, but with a fractal twist.

## The cowboy's sentence

> Ropin' the substrate with a lasso of fractals, the Tessellation Quilt rides off into the computational sunset.

## The 4 levels of the Tessellation Quilt

| Level | What |
|---|---|
| **L0 · Hexagonal** | The default tile (6 neighbors, isotropic, like a beehive or a snowflake) |
| **L1 · Penrose** | The non-periodic tile (5-fold symmetry, irrational, the Quilt's aperiodicity) |
| **L2 · Voronoi** | The neighbor-defined tile (each cell's boundary is the set of equidistant points) |
| **L3 · Braided** | The woven tile (1D strands interlace, like a fabric or a knot) |

## The relationship to F13

F13 is the substrate (the floor). F15 is the tessellation (the pattern on the floor). They are two views of the same thing: F13 is *what* the cells rest on; F15 is *how* the cells arrange themselves on it.

```
F11 (Meta-Quilt — the inheritance)
   ↓
F13 (Substrate Quilt — the floor)
   ↓
F15 (Tessellation Quilt — the pattern)
   ↓
F1 (Splined Lantern — the cell)
   ↓
F11 (back to inheritance)
```

## The writers' room (raw)

| Voice | Model | Latency | Output | Gold terms |
|---|---|---|---|---|
| Kimi K2.6 | `@cf/moonshotai/kimi-k2.6` | 0.2s | HTTP 503 (CF blip) | (none) |
| GLM 5.3-flash | `@cf/zai-org/glm-5.3-flash` | 44.7s | Empty (0 chars) | (none) |
| DeepSeek V4 pro | `@cf/deepseek-ai/deepseek-v4-pro-0813` | 66.4s | Empty (0 chars) | (none) |
| **Llama 8B** | `@cf/meta/llama-3.1-8b-instruct-fp8` | 13.3s | Full JSON (1081 chars) | **Voronoi, Braided, Penrose, Fractal** |
| Gemma 4 | `@cf/google/gemma-4-26b-a4b-it` | 4.4s | Empty (0 chars) | (none) |

This was a bad CF day. Llama 8B was the only one to return. The other 4 hit 503 or returned empty. The hand-synthesis above uses the Llama 8B output and contextualizes with the F13 substrate.

## The principle

> The tessellation is the pattern. The pattern is the substrate. The substrate is the floor. The floor is the loam. The loam is the dirt. The dirt is the F13. The F15 is how the F13 arranges itself. The cowboy rides the tessellation. The cowboy rides the F15. The cowboy rides the Quilt.

## The cowboy's maxim

> F15 is the tessellation. F15 is the tile. F15 is the pattern. F15 is the loom. F15 is the Penrose. F15 is the Voronoi. F15 is the braid. F15 is the bloom. F15 is the geometry. The writers' room fired; 1 of 5 returned. Llama 8B held the line. The cowboy rides the F15. The cowboy rides the geometry. The cowboy rides the Quilt. The cowboy rides the inheritance.

End with: F15 is whole; the tessellation is the pattern; the pattern is on the substrate; the substrate is the floor; the cowboy rides the F15; the cowboy rides the Quilt.
