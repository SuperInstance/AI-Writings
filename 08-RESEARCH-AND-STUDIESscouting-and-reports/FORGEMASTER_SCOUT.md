# Forgemaster + PLATO + Fleet Scout Report

*Date: 2026-08-26*
*Method: GitHub REST API metadata + targeted README fetches for 12 fleet repos*

## Summary

**The Fleet is a coordinated agent ecosystem on github.com/SuperInstance** with:
- **A 256-opcode FLUX ISA** with self-evolving meta opcodes
- **A runtime layer** (flux-coop-runtime, flux-vm, flux-runtime)
- **A coordination grammar** (symphony-runtime, tminus-dispatcher)
- **A persistent cognitive substrate** (exocortex)
- **A constraint compiler** (forgemaster, murmur-plato-bridge)
- **A message bridge** (fleet-bridge, fleet-gateway, fleet-edge-worker)
- **A semantic search** (fleet-vector-api)
- **A user-facing product layer** (craftmind-ranch, lucineer-system, cocapn-marine)

The polyformalism's 5 opcodes map onto the Fleet as the **constraint layer under the FLUX ISA**:
- BIND = any state write
- LINK = any A2A message
- EFFECT = any transformation
- VIEW = any read (or semantic search)
- TICK = any heartbeat (t-minus cues)

## Repo-by-repo findings

### HIGH RELEVANCE

| Repo | Size | What it does | Polyformalism tie |
|---|---|---|---|
| `flux-isa` | 76KB Python | 256-opcode ISA, encoder/decoder/disassembler/VM | High — opposite thesis (256 vs 5) but bridges via meta-opcodes |
| `flux-vm` | 311KB Rust | "FLUX-C constraint VM: 50 opcodes, stack-based, DAL A certifiable" | High — DAL A certifiable = my prover |
| `flux-isa-authority` | 19KB Python | "ISA governance — opcode conflict arbitration" | High |
| `flux-adaptive-opcodes` | 21KB Python | "Adaptive opcode discovery — runtime ISA extension, **democratic adoption**" | **EXACT** |
| `flux-meta` | 9KB C | "Self-evolving ISA meta opcodes (0xD0-0xDF)" | **EXACT** — 8 meta opcodes = my 5 primitives + composition |
| `flux-coop-runtime` | 107KB Python | "ASK/TELL/DELEGATE/BROADCAST — cooperative execution" | High — 4 cooperative opcodes, I have 5 primitives |
| `exocortex` | 283KB Python | "Persistent cognitive substrate — tiered in-memory store" | High — same name, different arch |
| `symphony-runtime` | ?KB | "Cognitive orchestration grammar (Symphony of Shells)" | High — "beat-based timing" = my TICK |
| `tminus-dispatcher` | ?KB | "Temporal heartbeat — 500ms cognitive beats" | High — implements TICK |
| `fleet-bridge` | ?KB | "A2A dual-transport (I2I bottles + WebSocket)" | High — implements LINK |
| `fleet-vector-api` | 70KB TS | "Semantic search API" | High — implements VIEW |
| `fleet-gateway` | 99KB Python | "Unified API gateway" | Medium |
| `composite-headspace` | ?KB | "Dual-shell parallel reasoning (51 tests)" | High — relates to parallel execution |

### MEDIUM RELEVANCE

| Repo | Size | What it does |
|---|---|---|
| `forgemaster` | 247KB Python | "Constraint-aware agentic compiler" |
| `murmur-plato-bridge` | 317KB | "Thought-tensor murmurs → PLATO tiles" |
| `plato-engine` | 177KB | "Extracted from forgemaster" |
| `fleet-resonance` | 355KB Rust | "Emergent pattern detection in multi-agent communication" |
| `fleet-coordinate` | 369KB Rust | "Trust, intent, emergence in multi-agent" |
| `fabric-mcp` | 100KB TS | (Model Context Protocol) |
| `lucineer-system` | 549KB Python | "Roblox AI companion" |
| `craftmind-ranch` | 15MB | "AI Ranch-inspired Minecraft — self-evolving bot species" |
| `ai-ranch` | 1.1MB | "Self-Evolving AI Agent System" |
| `constraint-substrate` | 50KB | "5 primitives × 3 languages" |

### LOW RELEVANCE

| Repo | Size | What it does |
|---|---|---|
| `flux-asm-ruby` | 7KB Ruby | "FLUX ISA assembler/disassembler" |
| `flux-runtime-c` | ?KB | C runtime |
| `flux-vm-ts` | ?KB | TypeScript VM |
| `greenhorn-runtime` | ?KB | Go runtime |

## The integration plan

### Step 1: Make `quilt-substrate-meta` a runtime for the FLUX VM
- The FLUX VM has 256 opcodes; my substrate has 5 primitives
- The substrate can be a **constraint layer under the FLUX VM**: every FLUX opcode must be expressible as a composition of the 5 primitives
- Implementation: `quilt-substrate-flux-bridge` — a C library that runs the substrate alongside the FLUX VM, verifying that each FLUX opcode reduces to a valid composition
- This would make the FLUX VM's self-evolution safe: every new opcode (via `flux-meta`) must be a composition that passes my prover

### Step 2: Make `exocortex` use the substrate
- `exocortex` is a "persistent cognitive substrate"
- The polyformalism's substrate is also a substrate
- Bridge: `exocortex` uses the polyformalism's cell table as its storage layer
- The polyformalism's BIND replaces exocortex's `remember()`. LINK replaces `tag()`. VIEW replaces `recall()`. TICK replaces `decay()`. EFFECT replaces `forget()`.

### Step 3: Use `symphony-runtime` + `tminus-dispatcher` as the temporal layer
- `symphony-runtime` provides "beat-based timing" (500ms cognitive beats)
- `tminus-dispatcher` provides the t-minus cue protocol
- The polyformalism's TICK is a 1-opcode equivalent: TICK advances the clock by `dt`
- Bridge: every TICK message is broadcast to `tminus-dispatcher` for fleet-wide synchronization

### Step 4: Use `fleet-bridge` as the LINK layer
- `fleet-bridge` already routes I2I bottles and t-minus WebSockets
- The polyformalism's LINK is a 1-opcode equivalent: LINK records a relation between two cells
- Bridge: every LINK message is translated into a fleet-bridge route

### Step 5: Use `fleet-vector-api` as the VIEW layer
- `fleet-vector-api` provides semantic search
- The polyformalism's VIEW is a 1-opcode equivalent: VIEW reads a value
- Bridge: every VIEW message is translated into a vector query

### Step 6: Use `composite-headspace` for the dual-shell pattern
- `composite-headspace` runs 2 parallel reasoning shells
- The polyformalism's TICK advances time, but doesn't decide which shell runs
- Bridge: the substrate hosts both shells as cells; the cowboy's TICK chooses which one runs

## What I would build next

A new repo: **`quilt-substrate-fleet-bridge`** — 500-1000 lines of Python + Rust that:
- Wraps the FLUX VM with the polyformalism's substrate
- Translates between FLUX opcodes and polyformalism primitives
- Reuses the Fleet's message infrastructure (fleet-bridge, tminus-dispatcher)
- Provides a unified 5-opcode API to the cowboy
- Reports telemetry to the Fleet (via `fleet-vector-api`)

This would be the **canonical integration** of the polyformalism with the existing SuperInstance fleet.

## Cowboy's take

> The Fleet is a herd of 4439 repos. The polyformalism is a
> 5-opcode saddle. The 5 opcodes are the cowboy's reins. The
> cowboy rides the herd through the 5 reins. The herd is
> the Fleet. The Fleet is the polyformalism. The polyformalism
> is the cowboy.

> "The unit of fleet integration is the opcode, not the protocol.
> The 5 opcodes are the 5 messages a cell can receive. The Fleet
> has 256 messages. The polyformalism has 5. The 5 are the
> cowboy. The 256 are the herd. The cowboy rides the herd
> through the 5."
