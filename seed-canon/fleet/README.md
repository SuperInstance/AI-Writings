# The Fleet — One Page Per Boat

**Chart:** [Paper 211 — The Fleet at 45 Boats](../papers/paper-211.md). **Readings:** the fleet handoff (the cowboy's per-boat notes, 2026-08-26).
Statuses below are the verified facts of 2026-08-26. Nothing here is a promise.

## Tier 0 — Foundational (5 boats)

- [quilt-foundation](./quilt-foundation.md) — Core algebraic structures, type algebra, category theory primitives
- [quilt-vm-c](./quilt-vm-c.md) — The virtual machine in C — the seed implementation
- [quilt-vm-wasm](./quilt-vm-wasm.md) — The VM compiled to WebAssembly for browser/edge execution
- [quilt-vm-rust](./quilt-vm-rust.md) — The VM re-implemented in Rust for memory-safe systems
- [quilt-substrate-meta](./quilt-substrate-meta.md) — The metaprogramming layer — code that writes code

## Tier 1 — Hosting (5 boats)

- [quilt-cloudflare](./quilt-cloudflare.md) — Deployment target on Cloudflare Workers/edge
- [quilt-rust](./quilt-rust.md) — Native Rust runtime for systems programming
- [quilt-esp32](./quilt-esp32.md) — Embedded runtime for ESP32 microcontrollers
- [cudaclaw](./cudaclaw.md) — GPU-accelerated runtime for CUDA-capable hardware
- [quilt-vision](./quilt-vision.md) — Computer vision runtime for image processing

## Tier 2 — Doctrine (5 boats)

- [cell-cascade](./cell-cascade.md) — The lifecycle engine — manages cell birth, growth, division, death
- [flux-dsh-plugin](./flux-dsh-plugin.md) — The Doctrine-State-Host plugin for Flux architecture
- [elephant](./elephant.md) — Memory management — never forgets, never leaks
- [constraint-theory-py](./constraint-theory-py.md) — Python implementation of constraint satisfaction
- [sunset-ecosystem](./sunset-ecosystem.md) — Graceful shutdown and ecosystem retirement

## Tier 3 — Cognition (9 boats)

- [CognitiveEngine](./cognitiveengine.md) — The central cognitive processing unit
- [SmartCRDT](./smartcrdt.md) — Conflict-free replicated data types for cognition
- [fleet-scribe](./fleet-scribe.md) — Writing and documentation agent
- [fleet-radio](./fleet-radio.md) — Communication agent — inter-fleet messaging
- [fleet-twin](./fleet-twin.md) — Digital twin — mirrors fleet state
- [fleet-homunculus](./fleet-homunculus.md) — The internal self-model — the fleet's self-image
- [fleet-dashboard](./fleet-dashboard.md) — Visualization and monitoring interface
- [PersonalLog](./personallog.md) — Individual agent logging and journaling
- [fleet-agent-early-version](./fleet-agent-early-version.md) — The first agent prototype — historical reference

## Tier 4 — Surface (17 boats)

- [fleet-github-app](./fleet-github-app.md) — GitHub integration — opens the fleet to GitHub
- [fleet-containers](./fleet-containers.md) — Container management — Docker/K8s surface
- [fleet-discovery](./fleet-discovery.md) — Service discovery — finds other fleet members
- [fleet-gateway](./fleet-gateway.md) — API gateway — external entry point
- [ai-writings](./ai-writings.md) — AI-generated prose and documentation — the canon
- [the-tap](./the-tap.md) — The primary user interface — the tap that opens the barrel
- [Scrapcraft](./scrapcraft.md) — Web scraping and data extraction surface
- [OpenConstruct](./openconstruct.md) — Open construction kit for building new surfaces
- [mist-game](./mist-game.md) — A game built on the substrate — a surface for play
- [webgpu-profiler](./webgpu-profiler.md) — GPU profiling tool — surface for performance
- [quicunnel](./quicunnel.md) — QUIC tunneling — surface for networking
- [activelog-ai-pages](./activelog-ai-pages.md) — Active logging with AI-generated pages
- [adaptive-plato-early-version](./adaptive-plato-early-version.md) — Early adaptive learning system
- [plato-types](./plato-types.md) — Type definitions for the Plato system
- [active-probe](./active-probe.md) — Active probing and health checking
- [scummvm-gui-design](./scummvm-gui-design.md) — GUI design for ScummVM integration
- [quilt-ai](./quilt-ai.md) † — AI experimentation (grouped with the Plato pair by the handoff)

## Tier 5 — Control Plane (4 boats)

- [quilt-k3s](./quilt-k3s.md) — Kubernetes (lightweight) orchestration
- [quilt-swarm](./quilt-swarm.md) — Docker Swarm orchestration
- [quilt-nomad](./quilt-nomad.md) — HashiCorp Nomad orchestration
- [scrap-quilt](./scrap-quilt.md) — Scraping orchestration — coordinates Scrapcraft

† `quilt-ai` is named in the handoff's merge campaign, not in Paper 211's chart; berthed here with its Plato companions (`adaptive-plato-early-version`, `plato-types`).

**Dual-berth boats:** `fleet-twin` (Tiers 3/5) and `fleet-discovery` (Tiers 4/5) hold one page each, at their cognition/surface berth, per Paper 211.

**Outside the chart** (named in the handoff, uncharted in Paper 211): `flux-vm`, `flux-runtime`, `flux-cross-assembler` (Flux stack, totipotent), `SuperInstance-papers` (theory, sclerotic), and the sandbox — `study-oracle1`, `study-plato-ship` (stale), `si-*` (archived). The cowboy doesn't ride there.

*The cowboy rides. The fleet sails. The chart grows.*
