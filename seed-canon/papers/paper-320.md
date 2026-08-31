# Paper 320: The Physical.World Cell Kind

**Date:** 2026-08-31
**Phase:** 222
**Adoption:** Code-as-World-VL-9B (MirroS-Lab, arXiv 2608.27549)
**Repos:** quilt-c, quilt-rust/quilt-polyformalism
**Tests:** 34 C + 11 Rust = 45 new assertions

## The pitch

A cell can be an *executable world*. The cell's value is a
Python program that simulates a physical scene. The cell's
reads are the program's inputs. The cell's output is a
physical quantity (e.g. -2.3 m/s ± 0.1).

MirroS-Lab's Code-as-World-VL paper trains a VLM on
quantitative physical reasoning by (1) proposing executable
code from observation, (2) executing the code, (3) rendering
the simulation, (4) verifying it matches the observation, and
(5) refining the code if not. They call this the *abductive
discovery loop*. The cell kind is exactly that loop,
exposed as 5 Quilt opcodes.

## Why this fits Quilt

The cell model is: a struct (the cell's state) + a function
(the cell's evaluator) + a list of dependents (the cells that
read it). The 5+1+1+1+1 opcodes apply unchanged:

- **BIND** sets the program text (the cell's state).
- **VIEW** reads the simulation output (the cell's value).
- **EFFECT** re-executes the program.
- **PROOF** chain-anchors every BIND: each BIND records the
  previous state_hash, so a tampered program is detected.
- **ROUTE** picks the substrate: local Python (sandbox),
  Code-as-World-VL-9B (synthesis), or no_std stub (testing).

The 5 abductive-loop operations compose on top:

- **PROPOSE** = BIND + a "VLM proposed this" tag.
- **EXECUTE** = EFFECT, but typed as a Quantity.
- **RENDER** = a side-effecting EFFECT (writes a file).
- **VERIFY** = a predicate that flips the `verified` flag.
- **REFINE** = BIND with a `# refine: <hint>` comment appended.

## The polyformalism claim

The cell has the same shape in C and Rust. The C port
(`include/quilt/world.h`, `src/world.c`) uses a heap-allocated
`char*` and FNV-1a. The Rust port (`crates/quilt-polyformalism`,
`WorldCell`) uses a `String` and the same FNV-1a. The opcodes
have the same names and indices in both. The state_hash
function is bit-exact (4 slices of a 64-bit FNV-1a, little-endian).

A real substrate binding replaces the synthetic execute() with
a Python interpreter (sandbox) or the Code-as-World-VL-9B model
(synthesis). The polyformalism claim is the *shape*, not the
math.

## The 5 abductive-loop operations

| # | Op | Quilt analogy | What it does |
|---|---|---|---|
| 0 | PROPOSE | BIND | VLM proposes code from observation |
| 1 | EXECUTE | EFFECT | Interpreter runs the code |
| 2 | RENDER  | side-effecting EFFECT | Render to image |
| 3 | VERIFY  | predicate | Did the sim match obs? |
| 4 | REFINE  | BIND (with hint) | One abductive step |

## The new opcode set: 5+1+1+1+1+1 = 10

The Quilt opcodes are now:

```
BIND / LINK / EFFECT / VIEW / TICK / FORGET
(5)                                 (+1)
PROOF / ROUTE / CRDT
(+1 cutting-edge #1) (+1 #2) (+1 #3)
WORLD (the 5 abductive-loop ops, 6th addition)
```

The Phase 216-218 cutting-edge adoptions (PROOF, ROUTE, CRDT)
and Phase 222's WORLD are now all in the polyformalism. The
claim "the same cell, the same 9 opcodes, N languages" is
now "the same cell, the same 10 opcodes (5+5 cutting-edge),
N languages."

## The 5 laws (unchanged)

- BIND idempotence
- LINK transitivity
- EFFECT associativity
- VIEW purity
- TICK monotonicity
- FORGET completeness

WORLD inherits BIND/EFFECT semantics and adds nothing to the
law set. The cell *is* a BIND + an EFFECT, with PROOF chain
on the BIND side.

## The 3 frontiers closed by this adoption

1. **Physical reasoning** — Quilt cells can now represent
   physical scenes as executable code. The cell's value is
   a quantity with uncertainty.
2. **VLM as a cell kind** — the Code-as-World-VL-9B model
   is one substrate option for PROPOSE; the synthetic stub
   in the polyformalism is another. The interface is the
   same.
3. **Abductive reasoning loop** — the paper's main
   contribution is the propose→execute→render→verify→refine
   loop. That loop is now a first-class cell kind.

## The 1 frontier still open

- **Substrate binding for the model**: Code-as-World-VL-9B
  lives on Hugging Face (Apache 2.0). To use it in production,
  we need a CF Worker proxy to a GPU backend (or a
  smaller distilled version, e.g. the 4B variant). Phase 223
  will prototype this.

## Test totals after Phase 222

| Port | Tests | Notes |
|---|---|---|
| quilt-c | 1195 | 47 engine + 1059 PROOF + 27 ROUTE + 28 CRDT + 34 WORLD |
| quilt-polyformalism (Rust) | 29 | 18 base + 11 WORLD |
| quilt-pydantic-ai (Python) | 41 | unchanged |
| quilt-llvm/experiments/llvm-fabric | 121 | unchanged |
| quilt-mhs | 32 | unchanged |
| quilt-ai | 7 | fixed in Phase 220 |
| quilt-fleet | 130/147 | 4 production bugs fixed in Phase 221 |

## The cowboy's maxim (Phase 222)

> The cowboy saw the Code-as-World model. The cowboy
> said: that's a cell. The cowboy made the cell. The cowboy
> ported the cell to Rust. The cowboy wrote 45 tests. The
> cowboy rode the abductive loop. The cowboy rode the
> polyformalism in 2 languages. The cowboy rode the
> 10-opcode set. The cowboy rode the physical world. The
> cowboy rode the Quilt.
