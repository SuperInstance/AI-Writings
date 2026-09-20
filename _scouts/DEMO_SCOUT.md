# Demo/Showcase Scout Report — User-Facing Product Candidates

*Date: 2026-08-26*
*Method: GitHub REST API metadata + targeted README fetches for 12 candidate product repos*

## Summary

**The user-facing product layer on github.com/SuperInstance is split across three categories:**

1. **Minecraft / game-layer AI** — craftmind, craftmind-ranch, lucineer-system
2. **Marine/fishing** — cocapn-marine, cocapn-python (the user's day job: commercial fisherman in Sitka, Alaska)
3. **AI infrastructure** — claw, chart-system, fleet-vector-api

The polyformalism's 5 opcodes are particularly well-suited for:
- **claw** (cellular logic in spreadsheet instances) — the cells are already there
- **cocapn-marine** (marine sensors) — sensor data is a stream of BINDs
- **craftmind-ranch** (Minecraft bot ranch) — the herd IS the cowboy

## Repo-by-repo findings

### TOP 3 PRODUCT CANDIDATES

#### 1. `claw` (402KB TypeScript) — "A simple Claw engine for cellular logic in spreadsheet instances"
- **Why this is the #1 candidate**: claw is already a cellular substrate. It's literally a cell-based runtime. The 5 opcodes would be a perfect fit.
- **Tech stack**: TypeScript (browser + Node)
- **Integration plan**: The polyformalism's 5 opcodes replace claw's cell primitives. The cowboy writes claw applications using BIND/LINK/EFFECT/VIEW/TICK; the spreadsheet cells ARE the substrate's cells.
- **Effort**: ~2 weeks to build `quilt-claw-bridge` (a TS module that exposes the 5 opcodes as a claw API)

#### 2. `cocapn-marine` (24MB Rust) — "Marine sensor integration — NMEA 0183, autopilot"
- **Why this is the #2 candidate**: marine sensors produce a stream of timestamped data. Each reading is a BIND. The autopilot responds with EFFECT. The TICK is the second-by-second cadence.
- **Tech stack**: Rust (the user's primary language for marine work)
- **Integration plan**: Run `quilt-substrate-meta` as the runtime for a marine data pipeline. Each sensor is a cell. The autopilot is an EFFECT composition. The cowhand reads the herd's VIEW.
- **Effort**: ~3 weeks to build `cocapn-quilt` (a Rust crate that wraps the substrate)

#### 3. `craftmind-ranch` (15MB) — "AI Ranch-inspired Minecraft — self-evolving bot species"
- **Why this is the #3 candidate**: this is the cowboy's ranch! Self-evolving bot species that compete, breed, and herd — exactly what my substrate supports.
- **Tech stack**: ? (Minecraft mod — likely Java + bedrock)
- **Integration plan**: Each bot is a cell. The ranch is a substrate. The cowboy rides the herd.
- **Effort**: ~4 weeks to build `craftmind-quilt` (a Minecraft mod that uses the substrate)

### MEDIUM CANDIDATES

| Repo | Size | What it does | Polyformalism tie |
|---|---|---|---|
| `lucineer-system` | 549KB Python | "Persistent AI game-building companion (Roblox)" | Medium — Roblox uses Lua; would need a Lua port of the substrate |
| `chart-system` | 58KB Python | "Polyformal navigation: 4 chart configurations" | **EXACT** — uses the word "polyformal" explicitly |
| `cocapn-python` | 25KB Python | "Deadbands, PID, NMEA" | Medium — Python port of the marine stack |
| `hav-flux-bridge` | 6KB | "Maps Higher Abstraction Vocabularies to FLUX bytecode" | **EXACT** — "snap-point idioms" → "Higher Abstraction Vocabularies" |
| `linguistic-polyformalism-shell` | 31KB Python | "Cross-linguistic thinking shell — Sapir-Whorf" | **EXACT** — same name |
| `delta-clt` | 24KB Python | "9-channel polyformalism colony analysis" | **EXACT** — same word |
| `claude-prism-local-json` | ?KB | (Claude tooling) | Medium |
| `claude-prism-cf` | ?KB | (Cloudflare Worker for Claude) | Medium |
| `cognitive-engine` | ?KB | "Cognitive orchestration" | Medium |
| `cascade-router` | ?KB | "Cascade routing" | Medium |

### LOW PRIORITY

| Repo | Size | What it does |
|---|---|---|
| `open-webui` | 374KB | "User-friendly AI Interface" (fork) |
| `dify` | 382KB | "Production-ready platform for agentic workflow" (fork) |
| `copilotkit` | 700KB | "Frontend Stack for Agents" (fork) |
| `baml` | 609KB | "AI framework for prompt engineering" (fork) |
| `codex` | 516KB | "Lightweight coding agent" (fork) |
| `chroma` | 871KB | "Search infrastructure for AI" (fork) |
| `bun` | 562KB | "JavaScript runtime" (fork) |
| `hermit-zed` | 461KB | "Code editor" (fork) |
| `next.js` | 2.4MB | "React framework" (fork) |
| `llvm-project` | 3.4GB | "Compiler infrastructure" (fork) |
| `libgdx` | 1.1MB | "Java game development" (fork) |

## The 3 priority builds

### Build 1: `quilt-claw-bridge` (~2 weeks)
**For**: claw (402KB TS) — cellular logic in spreadsheets
**What**: A TypeScript module that exposes the 5 opcodes as a claw API
**Why**: claw is the closest thing to the polyformalism that already exists. The integration is the lowest-hanging fruit.
**Cowboy's reward**: spreadsheet users get a polyformalism for free. The cowboy's 5 opcodes become the lingua franca of cellular logic.

### Build 2: `cocapn-quilt` (~3 weeks)
**For**: cocapn-marine (24MB Rust) — marine sensors
**What**: A Rust crate that wraps the substrate as the runtime for marine data pipelines
**Why**: the user is a commercial fisherman. The marine stack is the user's day job. Making the polyformalism a first-class citizen of the marine stack is the highest-value integration.
**Cowboy's reward**: the user can ride the herd of marine sensors with the polyformalism. The 5 opcodes become the language of the sea.

### Build 3: `craftmind-quilt` (~4 weeks)
**For**: craftmind-ranch (15MB) — Minecraft bot ranch
**What**: A Minecraft mod that uses the substrate as the runtime for self-evolving bot species
**Why**: the ranch IS the cowboy. Self-evolving bot species is exactly the polyformalism in game form.
**Cowboy's reward**: Minecraft players get to ride the herd. The polyformalism becomes a game mechanic.

## What I would build next (right now)

If I had to pick one: **`quilt-claw-bridge`**. Reasons:
1. claw is in TypeScript — same language as the browser demo
2. claw is the closest to the polyformalism in spirit
3. The integration is small enough to ship in a week
4. The result would be a demo-able product (a spreadsheet where cells respond to the 5 opcodes)

The plan:
1. Read the claw repo to understand its cell model
2. Write a thin TypeScript wrapper that maps the 5 opcodes to claw's primitives
3. Build a demo: a claw spreadsheet that hosts a cell-graph, with the cowboy able to send messages from the REPL
4. Document it as the canonical "first customer" of the polyformalism

## Cowboy's take

> The product layer is where the cowboy meets the world. The
> 5 opcodes are the cowboy's hands. The product layer is the
> world the cowboy touches. claw is the world. cocapn is the
> world. craftmind is the world.

> "The unit of product integration is the cell, not the user.
> The 5 opcodes are the 5 messages a cell can receive. The
> user is a cell. The product is the substrate. The substrate
> is the cowboy. The cowboy rides the product."
