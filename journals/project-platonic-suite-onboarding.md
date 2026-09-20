# Project: Platonic Randomness Creative Suite — Onboarding

**Created:** 2026-08-08
**Project:** platonic-creative-suite
**Live URL:** https://platonic-suite.pages.dev
**Repo:** /home/eileen/projects/platonic-creative-suite/

---

## What This Is

The Platonic Randomness Creative Suite is a single-page web app that lets non-programmers explore the aesthetic dimensions of geometric randomness. It's the democratization layer on top of the `platonic-randomness` library — taking a concept that lives in finite group theory and PRNG internals and making it tangible through a visual instrument.

The core idea: different Platonic solids produce randomness with different *textures*. All pass uniformity tests. The difference is not in correctness but in character. The suite lets you blend these textures like paint on a palette.

## Core Concepts

### The Pentagon Dial
A regular pentagon with each vertex mapped to one of the five Platonic solids (tetrahedron, cube, octahedron, icosahedron, dodecahedron). Drag the star inside the pentagon to blend solids by proximity. The barycentric weight of each solid determines how much it contributes to the combined random stream.

### The Five Solids
| Solid | Vertices | Symmetry Group | Character |
|-------|----------|---------------|-----------|
| Tetrahedron | 4 | A₄ (12 rotations) | Sharp, angular, fire-like |
| Octahedron | 6 | S₄ (24 rotations) | Balanced, even, airy |
| Cube | 8 | S₄ (24 rotations) | Stable, orthogonal, earthy |
| Icosahedron | 12 | A₅ (60 rotations) | Flowing, organic, watery |
| Dodecahedron | 20 | A₅ (60 rotations) | Golden-ratio textured, cosmic |

### The Textureoscope
A live visualization panel showing:
- **Value trace:** oscilloscope-style readout of RNG output over time, color-coded by solid
- **Orbit walk:** 2D random walk showing the path structure of each solid's state space
- **Stats:** mean, variance, orbit length, dominant solid

### Three Generation Modes
1. **🌍 World** — generates a procedural landscape with layered mountain silhouettes, stars, moon, and a text description of the world's biome, weather, and features
2. **🎵 Music** — generates a melodic sequence played through Web Audio API, visualized on a musical staff
3. **✦ Art** — generates a geometric pattern from RNG-driven shapes (circles, triangles, squares, pentagons, hexagons)

## How to Use

1. **Open the app** at https://platonic-suite.pages.dev
2. **Enter a seed** — any word or phrase. The same seed always produces the same output.
3. **Drag the star** in the pentagon dial toward different vertices to weight different solids
4. **Watch the Textureoscope** update in real-time as you drag — you'll see the orbit structure change
5. **Click a generate button** to create a world, piece of music, or artwork using the current blend
6. **Read the output panel** for a description of what was generated, including the solid signature

## The Math (for the curious)

The library uses the vertex coordinates of each Platonic solid to shape PRNG state rotation. At each step:
1. The current vertex (cycling through the solid's vertices) is mixed into the PRNG state via XOR with an imul hash of the vertex coordinates
2. The backend PRNG (Mulberry32) advances one step
3. The backend output is XOR-blended with the geometrically-mixed state
4. The result is normalized to [0, 1)

Because the vertex coordinates differ in algebraic structure (tetrahedron uses integers, dodecahedron uses φ-embedded irrationals), the orbit structure of the state space differs. This is the source of the textural difference.

The blend mode in the Creative Suite XORs the outputs of all active solids' RNGs together, preserving uniformity while combining their orbit structures.

## Tech Stack

- **Single HTML file** — no build step, no dependencies, no framework
- **Vanilla JavaScript** — the platonic-randomness library is reimplemented in-browser
- **Canvas API** — for the pentagon dial, main visualization, and textureoscope
- **Web Audio API** — for music playback
- **Cloudflare Pages** — static hosting at platonic-suite.pages.dev

## File Map

```
platonic-creative-suite/
  index.html    — the entire app (51KB, self-contained)
```

## Deployment

```bash
cd /home/eileen/projects/platonic-creative-suite
~/.npm-global/bin/wrangler pages deploy . --project-name=platonic-suite --branch=main
```

## Future Directions

- **Export to PNG/MIDI/JSON** — currently view-only
- **Solid per layer** — assign different solids to different generation layers (terrain, vegetation, drums, bass)
- **Comparison gallery** — same seed, five solids, side by side
- **Animated blending** — timeline that morphs the dial position over time, like a crossfader
- **Statistical tests panel** — show chi-square, autocorrelation, spectral analysis
- **Community gallery** — share seed+solid combinations
- **MIDI export** with solid-as-instrument mapping for the "Platonic Orchestra"
- **WebGL 3D planet renderer** for the World generator

## Key Insight

This is the thing that makes geometric randomness accessible to everyone. You don't need to understand finite groups or orbit structure or the golden ratio. You just drag a star inside a pentagon and *feel* the randomness change. The math is real, but the experience is primal: five shapes, five textures, one seed.

Every solid passes the same tests. The difference is texture, not correctness. That's the whole pitch.
