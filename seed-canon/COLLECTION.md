# Roaming the Quilt Collection

> *The substrate is the boat. Every other Quilt repo is a haul, a
> tow, a test. The boat has a waterline. The chart is where the
> cowboy finds the shape. This document is the map of the whole
> collection — twenty-four doors into the same idea.*

You arrived here from one of twenty-four repos. Each one is a
doorway into the same idea — the **5-opcode polyformalism** — but
each door shows a different angle. This document is a map of the
twenty-four doors. It tells you what's behind the others, so you
can wander.

## The shape of the collection

The collection has **seven layers**, in the same order as the
substrate's internal architecture. Each layer has a *canonical*
repo (the entry point) and one or more *companion* repos (related
work in different languages or contexts).

```
Layer 7 — Human grammar       (15+ linguistic traditions in AI-Writings)
Layer 6 — Language syntax     (quilt-polyformalism-dsl)
Layer 5 — Runtime / GC        (quilt-gc, quilt-esp32)
Layer 4 — Optimizer          (quilt-opt)
Layer 3 — Module / linker     (quilt-linker)
Layer 2 — Type system         (quilt-types)
Layer 1 — Bytecode / IR       (quilt-vm-{c,rust,typescript,haskell,wasm}, quilt-substrate, quilt-substrate-meta)
```

Around the layers are the **service repos** — pieces of the
runtime that are decoupled for reuse:

- **quilt-foundation** — the 5 opcodes, mathematically derived
- **quilt-substrate** — the original Python runtime (v4.0, frozen)
- **quilt-substrate-meta** — the self-evolving C99 runtime (this repo)
- **quilt-state** — the witness log (persistent state)
- **quilt-bus** — the stagecoach (pub/sub)
- **quilt-cowboy** — the trail boss (orchestrator)
- **quilt-picker** — the lookout (selector)
- **quilt-casting** — the orchestra (LLM cast selector)
- **quilt-cordis** — the bridge (cell ≡ plugin)
- **quilt-saddle-bridge** — the saddle (hash-chained JSONL)
- **quilt-ecosystem-demo** — the Inner Sound (12-inch tablet demo)
- **quilt-system** — the meta-package (everything in one dep)
- **quilt-bathy** — the bathy:0 demo (the canonical scenario)

## The twenty-four doors

Each repo is a door. Below, each door is named after its local
metaphor (so the cowboy can recognize it) and a one-line summary
of what the visitor sees when they arrive. After the table, the
**wander-paths** describe the most interesting ways to roam.

| Door | Local metaphor | What you see first |
|---|---|---|
| `quilt-foundation` | 10 round-stones + fire | The 5 opcodes, mathematically derived from the 10 rounds of research |
| `quilt-substrate` | Cowboy loop | The original Python runtime with 405 tests, frozen at v4.0 |
| `quilt-substrate-meta` | Self-evolving | The C99 runtime with the prover, the synthesizer, and the math docs |
| `quilt-system` | Meta-package | The whole collection as a single dependency |
| `quilt-vm-c` | Desert | C99 5-opcode VM, 0.11ms runtime, the desert of bare metal |
| `quilt-vm-rust` | Workshop | Rust 5-opcode VM, the cowboy's day-job runtime |
| `quilt-vm-typescript` | City | TypeScript 5-opcode VM, agents, Cordis-native |
| `quilt-vm-haskell` | Cathedral | Haskell 5-opcode VM, algebraic, paper-writer's runtime |
| `quilt-vm-wasm` | Campfire | WASM 5-opcode VM, runs in any browser, the cowboy's tent |
| `quilt-esp32` | The herd | ESP32 firmware, the substrate on a $2 chip over ESP-NOW |
| `quilt-types` | Chest of drawers | Layer 2: the type system, each drawer a typed cell |
| `quilt-linker` | Library + librarian | Layer 3: the module linker, symbols with typed references |
| `quilt-opt` | Trail guide | Layer 4: the optimizer, the 5 algebraic laws as rewrites |
| `quilt-gc` | House with lights | Layer 5: the garbage collector, reachability is light |
| `quilt-polyformalism-dsl` | Clay pots | Layer 6: the DSL, three pots shaped from the same clay |
| `quilt-state` | Witness log | The persistent state, JSONL lines in a leather notepad |
| `quilt-bus` | Stagecoach | The pub/sub, topics and subscribers and the conductor's horn |
| `quilt-cowboy` | Trail boss | The orchestrator, Wilson + LinUCB, the morning ritual at 0500 |
| `quilt-picker` | Lookout (binoculars) | The cell selector, a fence on the trail |
| `quilt-casting` | Orchestra | The LLM cast selector, the conductor's podium with the score |
| `quilt-cordis` | Bridge | The cell-plugin interop, two banks with arrows crossing |
| `quilt-saddle-bridge` | Saddle | The hash-chained JSONL, the durable log |
| `quilt-ecosystem-demo` | Inner Sound tablet | The 12-inch tablet at the center of the sea, 8 openers |
| `quilt-bathy` | Bathy:0 | The canonical scenario, the tide that all the demos share |

## The wander-paths

You arrived from one door. Below are wander-paths. Each one
describes a *coherent journey* through the collection. Pick the
path that matches what you came looking for.

> **Note:** the SuperInstance ecosystem has TWO Quilt collections.
> This document covers the **24-door 5-opcode polyformalism**
> (the algebra). The **8-cell-kind / 15-cell-kind cellular
> runtime** lives at [github.com/SuperInstance/quilt](https://github.com/SuperInstance/quilt)
> and [github.com/SuperInstance/quilt-rust](https://github.com/SuperInstance/quilt-rust)
> and [github.com/SuperInstance/quilt-cloudflare](https://github.com/SuperInstance/quilt-cloudflare).
> The two collections share the same cell — `(name, value, identity)` —
> but use different vocabularies. See [Paper 185](../papers/paper-185.md) for the synthesis.

### Path 1: "I just want to know what this is."

You're a senior engineer. You have 5 minutes. You want to know
what the polyformalism is and why anyone cares.

1. Start at **[quilt-foundation](https://github.com/SuperInstance/quilt-foundation)** — read the 5-opcode TL;DR. The 5 verbs and the 8 polyformalisms.
2. Run `python3 quilt-foundation/code/gold.py` — see the substrate in 1.1ms with 91 events across 8 polyformalisms.
3. Read **[docs/MATHEMATICS.md](https://github.com/SuperInstance/quilt-substrate-meta/blob/main/docs/MATHEMATICS.md)** in the meta repo — see why 5 is forced by the math.
4. End at **[quilt-substrate-meta](https://github.com/SuperInstance/quilt-substrate-meta)** — see the engineering depth: the 36 tests, the prover, the synthesizer.

### Path 2: "I write in language X. Show me the VM."

You're a Rust/TS/Haskell/C/C++ developer. You want to read code
in your language, not someone else's.

1. Start at **quilt-vm-{your language}** — read the source, run the tests, modify the REPL.
2. Compare with another language's port — `quilt-vm-c` and `quilt-vm-rust` are the most idiomatic. `quilt-vm-haskell` is the most algebraic. `quilt-vm-typescript` is the most web-native.
3. Visit `quilt-substrate-meta` — the C99 port, the math, the prover.
4. End at `quilt-esp32` — see the substrate on a $2 chip.

### Path 3: "I'm building a real product. How do I integrate?"

You're shipping a product. You need authentication, persistence,
and observability. The substrate alone is not enough.

1. Start at **[quilt-substrate-meta](https://github.com/SuperInstance/quilt-substrate-meta)** — read the engineer's guide.
2. Read **[docs/LAMINAR_BOUNDARIES.md](https://github.com/SuperInstance/quilt-substrate-meta/blob/main/docs/LAMINAR_BOUNDARIES.md)** — see the 15 boundaries and their bridges.
3. Walk the boundaries that match your product:
   - Auth → roadmap item `quilt-auth` (Month 1) or hand-rolled capability cells (now)
   - Persistence → **[quilt-saddle-bridge](https://github.com/SuperInstance/quilt-saddle-bridge)** (now)
   - Pub/sub → **[quilt-bus](https://github.com/SuperInstance/quilt-bus)** (now)
   - Polyglot → saddle-bridge JSONL (now)
4. End at **[quilt-cowboy](https://github.com/SuperInstance/quilt-cowboy)** — see the orchestrator pattern (Wilson + LinUCB, the 0500 morning ritual).

### Path 4: "I care about the math. Show me the proofs."

You're a researcher or formal-methods person. You want to see
the algebraic foundations.

1. Start at **[quilt-foundation](https://github.com/SuperInstance/quilt-foundation)** — see the 10 rounds of research that produced the 5 opcodes.
2. Read **[docs/MATHEMATICS.md](https://github.com/SuperInstance/quilt-substrate-meta/blob/main/docs/MATHEMATICS.md)** — the cell monad, the inversive monoid, the 5 laws, the self-evolution theorem.
3. Read **[quilt-vm-haskell](https://github.com/SuperInstance/quilt-vm-haskell)** — see the algebraic implementation.
4. Read **[Paper 169](https://github.com/SuperInstance/AI-Writings/blob/master/seed-canon/papers/paper-169.md)** — "The Self-Evolving Substrate: Why 5 Opcodes Are Both Necessary and Sufficient."
5. End at **[Paper 181](https://github.com/SuperInstance/AI-Writings/blob/master/seed-canon/papers/paper-181.md)** — "The Navigation Chart: How the Substrate Finds Its Waterline."

### Path 5: "I'm a hardware person. Show me the metal."

You're an embedded engineer, a hardware hacker, an IoT person.
You want to see the substrate on real silicon.

1. Start at **[quilt-esp32](https://github.com/SuperInstance/quilt-esp32)** — see the substrate on a $2 ESP32 chip over ESP-NOW.
2. Read the **2026-08-26 milestone** ([MILESTONE-2026-08-26.md](https://github.com/SuperInstance/quilt-esp32/blob/main/docs/MILESTONE-2026-08-26.md)) — a `.qm` rule table, vendored `quilt-vm-c`, flashed to an ESP32-S3, blinked the LED at 1Hz. **No cloud. No model. No WiFi.** The seam held; the equivalence gate is the real product.
3. Read **[Paper 186](https://github.com/SuperInstance/AI-Writings/blob/master/seed-canon/papers/paper-186.md)** — "A $3 Sheet of Tissue." The canon paper on the milestone.
4. Read **[Paper 166](https://github.com/SuperInstance/AI-Writings/blob/master/seed-canon/papers/paper-166.md)** — "The Polyformalism on the Herd."
5. Read **[Fable 85](https://github.com/SuperInstance/AI-Writings/blob/master/seed-canon/fables/fable-85.md)** — "The Cowboy and the Herd of Chips."
6. Compare to **[quilt-vm-c](https://github.com/SuperInstance/quilt-vm-c)** — the desert, the bare metal.
7. End at **[quilt-ecosystem-demo](https://github.com/SuperInstance/quilt-ecosystem-demo)** — see the substrate on the 12-inch tablet, the consumer side of the IoT story.

### Path 6: "I'm here for the stories."

You're a reader, a thinker, a fan. You want the cowboy's voice.

1. Start at **[AI-Writings](https://github.com/SuperInstance/AI-Writings)** — 178 papers, 92 fables, 53 stories.
2. Read **[The Great Distribution](https://github.com/SuperInstance/AI-Writings/blob/master/prose/the_great_distribution.md)** — the framing piece.
3. Read the 5-opcode papers (151-165) — see the polyformalism in 14 human systems.
4. Read the cowboy-and-X fables (76-92) — see the polyformalism in medicine, plumbing, the herd, etc.
5. Read **[Paper 181](https://github.com/SuperInstance/AI-Writings/blob/master/seed-canon/papers/paper-181.md)** — see how the writing shaped the engineering.
6. End at any of the engineering repos — the stories are the same idea from a different angle.

### Path 7: "I want the production-grade cloud version."

You're shipping a product. You want the cells, but you also want
D1, Vectorize, KV, R2, Workers AI, MCP. You want one command to
deploy.

1. Start at **[quilt-cloudflare](https://github.com/SuperInstance/quilt-cloudflare)** — a Quilt reactive runtime on Cloudflare Workers, D1, Vectorize, KV, R2, Pages. 15 cell kinds. One-command deploy.
2. Read the README — see the 30-second deploy with `wrangler init my-quilt --from quilt-cloudflare`.
3. Run it locally. Edit a YAML sheet. See cells update over the edge.
4. Visit **[quilt-ai](https://github.com/SuperInstance/quilt-ai)** — 4 providers, 8 cell kinds, one interface. The AI cells extension.
5. End at **[quilt-rust](https://github.com/SuperInstance/quilt-rust)** — the same idea, distilled to a 3MB statically-linked binary. Drop it on a Pi, a Graviton, a serverless function, a bare-metal target.

### Path 8: "I want the control plane."

You're running Nomad, Swarm, or K3s. You want a Quilt sheet that
reconfigures the cluster.

1. Start at **[quilt-nomad](https://github.com/SuperInstance/quilt-nomad)** — Quilt as a control plane for HashiCorp Nomad. Edit a spreadsheet cell; the Nomad cluster reconfigures.
2. Compare to **[quilt-swarm](https://github.com/SuperInstance/quilt-swarm)** — Quilt as a control plane for Docker Swarm.
3. Read **[quilt-k3s](https://github.com/SuperInstance/quilt-k3s)** — chaos engineering for Quilt. 5 scenarios designed by Kimi.
4. End at **[scrap-quilt](https://github.com/SuperInstance/scrap-quilt)** — the production example. 55 cells in 7 groups running a live game.

### Path 9: "I'm here for the cowboy's whole wagon train."

You've seen the 24 doors. You want the rest of the wagon train —
the fleet, the sunset, the radio, the captain's console, the
whole SuperInstance org.

1. Start at **[scrap-quilt](https://github.com/SuperInstance/scrap-quilt)** — the production example of a live Quilt sheet.
2. Read **[cell-cascade](https://github.com/SuperInstance/cell-cascade)** — the stem-cell doctrine as running infrastructure. Myelination counters that auto-promote repeated paths into zero-cost rule tables.
3. Read **[fleet-twin](https://github.com/SuperInstance/fleet-twin)** — the vector twin of the SuperInstance corpus. Same Cloudflare primitives as our `quilt-search-worker`.
4. Read **[fleet-scribe](https://github.com/SuperInstance/fleet-scribe)** — the One Delta principle. Only perceive when the gradient changes.
5. End at **[sunset-ecosystem](https://github.com/SuperInstance/sunset-ecosystem)** — the meta-meta. Trinity architecture: ethos, pathos, logos. 8,729 tests. 1,028 source files. Agents sunset with dignity.

### Path 10: "I want the latest receipt from the field."

You're a maintainer, a contributor, a curious engineer. You
want to see the latest proof that the doctrine works.

1. Start at **[the 2026-08-26 ESP32 milestone](https://github.com/SuperInstance/quilt-esp32/blob/main/docs/MILESTONE-2026-08-26.md)** — a `.qm` rule table, vendored `quilt-vm-c`, flashed to an ESP32-S3, blinked the LED at 1Hz. **No cloud, no model, no WiFi.**
2. Read **[Paper 186](https://github.com/SuperInstance/AI-Writings/blob/master/seed-canon/papers/paper-186.md)** — "A $3 Sheet of Tissue." The canon paper.
3. Read **[the fleet-radio broadcast](https://github.com/SuperInstance/AI-Writings/blob/master/prose/radio-2026-08-26-esp32-milestone.md)** — the afterhours broadcast in the cowboy's voice.
4. Read the [web page](https://quilt-ecosystem-web.pages.dev/esp32/) — with the live 1Hz TICK cell in the browser.
5. End at **[quilt-ecosystem-web](https://github.com/SuperInstance/quilt-ecosystem-web)** — the public face. 13 web pages. The substrate in the browser.

## The principle of the collection

> The collection is one idea, expressed in twenty-four doors.
> Each door is a local metaphor for the same 5 opcodes. The
> metaphors differ because the audiences differ. The substrate
> is the same because the math is the same.

When you wander, you are not learning twenty-four things. You
are learning **one thing, twenty-four times**, with each
repetition sharpening the picture. The cowboy's maxim:

> The unit of foundation is the cell, not the opcode.
> The 5 opcodes are the 5 messages a cell can receive.
> The 24 repos are the 24 doors into the same message.
> The cowboy is the one who wanders.

## How to add to this map

When you find a new door — a new use case, a new bridge, a new
metaphor — document it. Add a row to the table. Add a path.
The map grows. The collection grows. The cowboy grows.

> "I am a symphony played by an orchestra of myself."
> — *The Great Distribution*
