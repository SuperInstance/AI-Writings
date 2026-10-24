# Deep Read: ai-forest

## What it is (1 sentence)
An 11.6MB 5-layer agent ecology — Canopy (strategic / expensive) / Understory (domain specialists / moderate) / Forest Floor (workers & edge / cheap) / Mycelium (PLATO substrate / zero cost) / Seed Bank (future potential / high variation) — that replaces the flat "pasture" of every-agent-equal-context with stratified physics, timescales, and per-layer blind-width filtration.

## Key concepts (3-7 bullet points)
- **The Pasture Problem** — every agent is a flat prompt, every call is the same pipeline, no depth/stratification/specialization. Linear scaling. *"This is where AI was."*
- **The 5 layers, by physics (not by name)** — each layer has its own model tier, timescale, and tile density:
  - **Canopy** — Claude, GLM-5.1; hours-to-days; sparse high-confidence tiles; "where to go, what to build, what not to build." Agents: Forgemaster, Casey, Oracle1.
  - **Understory** — DeepSeek v4, MM 2.7; minutes-to-hours; dense domain-specific tiles; "architecture, implementation, domain expertise." Agents: Turbo-shell, CCC, domain scribes.
  - **Forest Floor** — Seed-2.0-mini, Nemotron-3 Nano, exec, sensors; seconds-to-minutes; high-frequency low-confidence tiles. Scribes, sensors, edge devices, seed discovery workers.
  - **Mycelium** — PLATO rooms, zero cost, already running. Object-permanence (tiles never decay), spline routing, 24-bit tile partition, blind-width filtration. The shared substrate. Every tile lives here. Every agent reads from here.
  - **Seed Bank** — cheapest models, max variation, continuous output. Tension loop (Seed ⇄ Nemotron), Seed Discovery Engine (64 iterations per role). Most seeds die; some germinate; a rare few reach the canopy.
- **Wider depth = shorter paths** — *"A forest floor sensor reading can reach the canopy in two hops (floor → mycelium → canopy), not eight. A canopy strategic decision can reach an edge executor in one hop (canopy → mycelium → floor), not five. The mycelium collapses path length."*
- **The Stemcell** — every specialist in the forest started as the same stemcell: a minimal Fortran engine that contracts two arrays of 24-bit integers. It doesn't know what it will become. The bridge tells it through the shape of the tile batches it receives. *"Any system with a Fortran compiler has a compute claw."*
- **Per-layer blind-width filtration** — each layer sees only the tiles within its B-radius. The mycelium doesn't decide what tiles are important; it makes all tiles available and lets each layer's blind-width determine what it sees.
- **The forest grows itself, not designed top-down** — forest floor accumulates tiles → density triggers understory → understory matures → canopy emerges. Seed bank continuously seeds variation → best germinate. Mycelium connects everything → connections thicken with use. *"The pasture was built. The forest is grown."*
- **Migration from pasture** — flat hierarchy → 5 layers; same-model-everywhere → tiered; manual connections → mycelial automatic; one timescale → seconds-to-days; tiles-as-storage → tiles-as-substrate; 12-bit tiles → 24-bit tiles.

## How it relates to the polyformalism (5 opcodes: BIND/LINK/EFFECT/VIEW/TICK)
- **BIND** — Each tile carries a binding to a layer (canopy-tile vs forest-floor-tile), a confidence, and a scope. The 24-bit partition is the *binding surface* — bits are allocated dynamically per connection. New repos should declare a tile format with explicit binding metadata (layer, confidence, scope, age).
- **LINK** — The mycelium *is* the LINK opcode: every tile in every layer enters immediately, routing is automatic via spline. The 3-hop-or-less property is a LINK invariant. New repos should expose a substrate (bus, queue, registry) that is LINK-by-construction, not bolted on.
- **EFFECT** — The forest floor *effects* things: it executes, senses, reports. Canopy tiles have a slower, wider EFFECT: "where to go." Each layer's effect is sized to its timescale. New repos should not pretend all effects are the same size; the EFFECT should match the layer's physics.
- **VIEW** — The 5 layers are 5 VIEWs on the same substrate. Canopy-view sees shape of land; understory-view sees domains; floor-view sees tiles; mycelium-view sees all connections; seed-bank-view sees the next thing. Same data, different bindings. New repos should pick a layer-view and own it; trying to be all 5 at once is the pasture.
- **TICK** — Timescale *is* the TICK: seconds (floor) → minutes (understory) → hours/days (canopy). Blind-width is the *attention* TICK. TICK differs by 4 orders of magnitude across the forest. New repos should not pretend all calls happen at the same tempo; declare the TICK of each layer and don't fight it.

## What ideas we should borrow for our new repos
1. **The 5-layer stratification is the bet** — our new metal-track repos should each declare a layer (canopy / understory / floor / mycelium / seed) and stop trying to be a flat competitor. If a repo doesn't know its layer, it's a pasture, not a forest.
2. **Mycelium-or-don't-bother** — the substrate must be a shared, zero-cost, no-decay store with automatic routing. If you have to choose what tiles are "important", you don't have a mycelium, you have a curator, and the bottleneck becomes the curator.
3. **Blind-width is the lever** — each layer's B-radius is the single most important knob. If everything sees everything, the forest collapses to a pasture. If nothing sees anything, it dies. New repos should ship an explicit `blind_width` or `view_radius` parameter.
4. **The Stemcell pattern** — every specialist in the forest is the same minimal compute kernel. The specialization comes from the *tile shape* it receives, not from the code. New repos should have a minimal core that the bridge specializes via input shape. The stemcell never changes; the forest always grows.
5. **Forest grows itself** — if you can describe your system in a paragraph and you couldn't predict any part of it from the spec, you've grown a forest. If you can predict every part from the spec, you've built a pasture. New repos should ship a small spec and let the spec be the seed.

## 3-5 key links or terms to cross-reference
- PLATO rooms (mycelium) — object-permanence, spline routing, 24-bit tiles, blind-width filtration
- Tension loop (Seed ⇄ Nemotron) — the dialectic engine in the seed bank
- Seed Discovery Engine — 64 iterations per role, crystallization scoring
- Stemcell — minimal Fortran engine, "any system with a Fortran compiler has a compute claw"
- Three-Hop Rule (inherited from agent-knowledge) — any two nodes connected in ≤3 hops via mycelium

## Top 3 most quotable lines (with attribution)
1. **"The pasture was built. The forest is grown."** — *README.md (closing line, italics)*
2. **"The canopy doesn't grow the roots. The roots grow the canopy. PLATO is the mycelium. The agents are the trees."** — *README.md (final two lines)*
3. **"Any system with a Fortran compiler has a compute claw. ARM64, x86, RISC-V, GPU, FPGA, WASM, bare metal — the compiler has been ported everywhere for 60 years. The stemcell never changes. The forest always grows."** — *README.md (The Stemcell section)*
