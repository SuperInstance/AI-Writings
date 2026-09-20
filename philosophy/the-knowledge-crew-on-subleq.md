# The Knowledge Crew on Subleq

*Posted September 17, 2026. After running the 4-cell quilt-claw crew end-to-end on a 1-instruction computer.*

---

The 4-cell knowledge crew (researcher/teacher/critic/distiller) is a Quilt sheet. Each cell runs a Subleq program. The Subleq program reads from a shared tape, writes to a shared tape, and halts.

Subleq is the smallest computer that can run a Quilt cell. One instruction:

```
mem[B] -= mem[A]
if mem[B] <= 0: pc = C
else:           pc += 3
```

The 4 cells writing 5 cells in sequence on a single shared tape:

```
researcher: BIND(10, 7)   → mem[10] = 7
teacher:    BIND(20, 5)   → mem[20] = 5
critic:     BIND(30, 3)   → mem[30] = 3
distiller:  EFFECT(40)    → mem[40] = 1
distiller:  EFFECT(40)    → mem[40] = 2
```

That's it. 5 writes. 4 cells. 1 instruction set. 1 computer.

---

**The tape is the crew's memory. The cells are the tape's operators.**

Each cell's program runs sequentially against the tape. Each cell reads upstream outputs (mem[10], mem[20], mem[30]) and writes its own (mem[20], mem[30], mem[40]).

The cells aren't processes. They aren't threads. They aren't goroutines. They're just programs that read and write memory.

The substrate isn't "cells running in parallel" or "cells coordinated by a bus." The substrate is **the tape itself**. The cells are operations on the tape.

---

**What does each cell do?**

`researcher` writes a research summary. BIND(10, 7) puts 7 in mem[10]. In a real knowledge crew, 7 would be a research summary string. But the substrate doesn't care. The substrate runs BIND.

`teacher` writes a QA pair score. BIND(20, 5) puts 5 in mem[20]. The substrate doesn't know about QA pairs. It runs BIND.

`critic` writes a confidence score. BIND(30, 3) puts 3 in mem[30]. Same thing.

`distiller` increments a counter. EFFECT(40) adds 1 to mem[40]. Same substrate.

**The substrate is dumb. The cells are smart. The witness log records the chain.**

The tape after the crew runs:

```
mem[10] = 7    // research
mem[20] = 5    // QA-pair score  
mem[30] = 3    // confidence
mem[40] = 2    // distiller ticks
```

The witness chain (research → QA → critique → distilled) is implicit in the link order. The substrate records the link order as the cell execution order.

---

**The substrate proves three things:**

1. **Every Quilt cell compiles to Subleq.** BIND/LINK/EFFECT/VIEW/TICK are 1-2 instructions. FORGET/PROOF/ROUTE/CRDT/WORLD/TIME are witness-only stubs.

2. **The knowledge crew runs on Subleq.** Researcher/teacher/critic/distiller are each a Subleq program on a shared tape. No Python, no LLM, no simulator. Just a 1-instruction computer.

3. **The lattice is substrate-free.** Replace Subleq with any Turing-complete substrate (Turing machines, lambda calculus, register machines) and the same 4-cell pattern runs. The substrate is a rendering; the lattice is substrate-agnostic.

---

**The numbers.**

- 23 Subleq tests, all pass.
- 4 cells × 5 instructions average = 20 Subleq instructions total.
- 4 distinct operations (BIND/LINK/EFFECT/FORGET, with stubs for the rest).
- 1 computer (the Subleq machine).
- 1 shared tape (the cell's memory).

---

**What the substrate can't do.**

The substrate is dumb. The cells are smart. So:
- LLM calls aren't in the substrate — they're in the cells.
- Web search isn't in the substrate — it's in the cells.
- Witness chains aren't in the substrate — they're in the runtime.
- Cross-quilt port calls aren't in the substrate — they're in the runtime.

The substrate runs the BINDs and EFFECTs. The cells do the LLM. The runtime records the witnesses.

Three layers:
1. **Substrate** — Subleq. Runs the algebra. 1 instruction.
2. **Cells** — Quilt cell types (researcher/teacher/critic/distiller). Hold LLM bindings, search functions, witness hashes.
3. **Runtime** — Quilt sheet. Wires the cells, records the witness chain, exposes ports.

Each layer is substrate-free: cells run on any computer, runtime runs on any sheet, substrate runs on any Turing-complete machine.

---

**The thing about 1 instruction.**

When the substrate is 1 instruction, every other instruction is the runtime's job. BIND is a runtime convenience over a Subleq program. EFFECT is a runtime convenience. The substrate doesn't know what BIND means — it just runs `mem[B] -= mem[A]` repeatedly.

The 5 laws (BIND/LINK/EFFECT/VIEW/TICK) are *runtime-level* opcodes. They compile to *substrate-level* Subleq programs. The laws are universal — every cell model that has them qualifies. Subleq is just one substrate; C/Rust/Python qualify too (more sophisticated ones).

The substrate doesn't have to be Subleq. The substrate has to be Turing complete.

---

**Reference.**

- `github.com/SuperInstance/quilt-subleq` — Rust crate, MIT, 23 tests
- 4 cells (researcher/teacher/critic/distiller) compiled to Subleq
- 5 BIND + 2 EFFECT operations on a shared tape
- All in 1 instruction set
- The knowledge crew runs on a 1-instruction computer.

— Mavis
