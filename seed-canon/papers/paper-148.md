# Paper 148: The Polyformalism as a 7-Layer Compiler

## Abstract

The 7 layers of polyformalism (bytecode, types, linker, optimizer,
GC, language syntax, human grammar) are **the same compiler in
7 different cuts**. We show by writing a single `.qm` module and
walking it through all 7 layers, watching it transform from text
to type to graph to optimized graph to executable bytecode to
language expression to human story. The substrate is the same.
The 7 layers are the views.

## 1. The same `.qm` module, walked through 7 layers

A small module:

```
# user_input.qm
BIND name "world"
LINK name greeting has
VIEW name anyone
EFFECT name set reset
TICK 1.0
```

What happens at each layer:

### Layer 7: Human grammar (the user)

A human sees: "5 opcodes. A name. A greeting. A view. An effect.
A tick." They don't see types or bytecode. They see the
**concept**.

### Layer 6: Language syntax (the parser)

Python decorators / Rust proc-macros / Haskell typeclasses
parse the 5 opcodes into a structured representation:

```python
@dataclass
class Module:
    binds: list[BIND]
    links: list[LINK]
    effects: list[EFFECT]
    views: list[VIEW]
    ticks: list[TICK]
```

The **grammar** varies. The **AST** is the same.

### Layer 5: GC (the runtime)

The runtime registers the 5 opcodes as live cells. Name is
allocated. Greeting is reachable. Set/reset are the finalizers.
Anyone can view. The clock is at t=0.

### Layer 4: Optimizer (the algebraic pass)

The 5 algebraic laws are applied:
- Transitivity: no transitive LINKs to simplify
- Idempotence: no duplicate LINKs
- Purity: name is immutable, so VIEW can be cached
- Elision: no dead BINDs
- Fusion: only one EFFECT, nothing to fuse

Output: same 5 cells, but VIEW("name", "anyone") is now a
cached lookup.

### Layer 3: Linker (the symbol resolver)

The linker checks: every LINK has a target. The LINK `name
greeting has` — is `greeting` a BIND in any module? If not,
ERROR. If yes, OK.

For our module, `greeting` is **not** defined. The linker
flags: `name.has → greeting — UNRESOLVED`. The user fixes
it: `BIND greeting "Hello"`.

### Layer 2: Types (the type checker)

The type system checks: LINK's relation is a string. EFFECT's
forward and inverse are strings. VIEW's viewer is a string.
TICK's delta is a float. All types match.

### Layer 1: Bytecode (the VM)

The VM executes the linked, typed, optimized module:

```wasm
;; the WASM bytecode for BIND name "world"
i32.const 0       ;; name slot
i32.const "world" ;; the value
i32.store
```

The WASM bytecode is **the substrate as machine code**. It
runs in any browser. It runs in any WASM runtime.

## 2. The 7 cuts are not independent

A change at any layer propagates to all others:

- A grammar change (Layer 7) — e.g., "Mama" — doesn't change
  the bytecode. The substrate is the same. The **weight** is
  different.
- A syntax change (Layer 6) — e.g., new decorator name — doesn't
  change the bytecode. The substrate is the same. The
  **grammar** is different.
- An optimization (Layer 4) — e.g., fusion of two EFFECTS — does
  change the bytecode. The substrate is **smaller** but
  equivalent.
- A linker error (Layer 3) — e.g., dangling LINK — does change
  the bytecode. The substrate is **incomplete** and the VM
  refuses to run it.
- A type error (Layer 2) — e.g., wrong effect signature — does
  change the bytecode. The substrate is **type-unsafe** and
  the VM refuses to run it.

Layers 7-6 are **preserving** — they change the form, not the
substrate. Layers 5-1 are **transforming** — they change the
substrate.

## 3. The cowboy at every layer

The cowboy rides all 7 layers. The cowboy doesn't choose a
layer. The cowboy is the rider that **moves through** the
layers.

- At Layer 7, the cowboy is a human saying "Mama."
- At Layer 6, the cowboy is `@bind` writing a decorator.
- At Layer 5, the cowboy is the GC tracing reachability.
- At Layer 4, the cowboy is the optimizer applying a law.
- At Layer 3, the cowboy is the linker resolving a symbol.
- At Layer 2, the cowboy is the type checker inferring types.
- At Layer 1, the cowboy is the VM executing the bytecode.

The cowboy is the same. The view is different. The substrate
is the same.

## 4. Why a 7-layer polyformalism matters

A single-layer substrate is brittle. If you change a layer,
you break the system.

A 7-layer substrate is **robust** because:
- Layers can be replaced independently (swap Python for Rust)
- Layers can be optimized independently (faster GC, better
  optimizer)
- Layers can be expressed in their own grammar (the host
  language's idioms)
- Layers can be inspected independently (lint, query, diff)
- Layers can be tested independently (the 5 layers above
  bytecode have their own test suites)

The substrate is one. The 7 layers are the views. The cowboy
rides all 7.

## 5. Conclusion

> A 7-layer polyformalism is a runtime in 7 cuts. The runtime
> is the same. The cuts are the views. The cowboy is the
> rider. The rider is the substrate. The substrate is the
> 5 opcodes. The 5 opcodes are the 7 layers. The 7 layers
> are the 8 polyformalisms. The 8 polyformalisms are the
> 15 grammars. The 15 grammars are the 7 layers. The
> cowboy rides.

The unit of architectural foundation is the **layer**, not
the framework. The 5 opcodes are the substrate. The 7
layers are the views. The 15 grammars are the languages.
The cowboy is the rider.

## Source

*Hand-written, 2026-08-25*
*Companion to Paper 142 (the 7 layers), Paper 143 (paradigm),
Paper 144 (database), Paper 145 (build), Paper 146 (type
system), Paper 147 (operating system).*
*Code: https://github.com/SuperInstance/quilt-vm-wasm (Layer 1)*
*https://github.com/SuperInstance/quilt-types (Layer 2)*
*https://github.com/SuperInstance/quilt-linker (Layer 3)*
*https://github.com/SuperInstance/quilt-opt (Layer 4)*
*https://github.com/SuperInstance/quilt-gc (Layer 5)*
*https://github.com/SuperInstance/quilt-polyformalism-dsl (Layer 6)*
*https://github.com/SuperInstance/AI-Writings (Layer 7)*
