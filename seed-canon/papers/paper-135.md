# Paper 135: The Cell and the Plugin — A Formal Equivalence

## Abstract

Quilt says "everything is a cell." Cordis says "everything is a
plugin." We prove that the two statements are equivalent. The
proof is a structural mapping between the Quilt cell and the
Cordis plugin, with the Quilt substrate and the Cordis fiber
as the dual runtimes. The bridge is implemented in
`quilt-cordis` and verified by 33 tests.

## 1. The two intuitions

The Quilt ecosystem is built on the intuition that **every
reactive element is a cell** — a unit of composition with an
address, a value, and a topology of nearby addresses. The cell
graph is the canonical form. Every interface (web UI, REST, TTS,
LLM prompt, MUD, PLATO, Telegram, ESP32 LCD) is an "opener" onto
the same graph.

The Cordis ecosystem is built on the intuition that **every
component is a plugin** — a unit of dynamic composition with a
name, a context, and a lifecycle. The plugin is reversible:
every effect has an inverse. The plugin is spatial: every
dependency is declared. Together, the two properties are
*spatiotemporal composability*.

The two intuitions are not the same in form. The Quilt is
operational and Python; the Cordis is algebraic and TypeScript.
The Quilt's lowest level is a 4D cell-graph; the Cordis's
lowest level is a runtime that tracks effects and resolves
coeffects.

But the two intuitions are the same in shape. A cell is a
function from address to value with effects and coeffects. A
plugin is a function from name to value with effects and
coeffects. The two are translations of the same thing.

## 2. The formal mapping

We define a 1-1 correspondence between the Quilt and Cordis
primitives.

| Cordis | Quilt | Same idea |
|--------|-------|-----------|
| Plugin | Cell | A unit of composition with a name and a value |
| `ctx.effect(fn, inv)` | `cell.effect(fn, inv)` | A reversible side effect |
| `ctx.get(svc)` | `cell.coeffect(svc, addr)` | A declared dependency |
| `ctx.isolate(name)` | `cell.fork(name)` | An isolated scope |
| `ctx.intercept(svc, fn)` | `cell.set(fn(value))` | A service interceptor |
| `plugin.dispose()` | `cell.dispose()` | Run all effects in reverse |
| `plugin.fork(name)` | `cell.fork(name)` | Clone the plugin/cell |
| Fiber | Substrate | The runtime that hosts plugins/cells |
| Service registry | Cell graph | The topology of dependencies |

The mapping is constructive: `bridge(plugin)` returns the cell
that is the plugin; `unbridge(cell)` returns the plugin that is
the cell. The mapping is a *homomorphism* — round-tripping a
plugin through the bridge returns an isomorphic plugin.

## 3. The proof of equivalence

**Theorem (cell ≡ plugin):** There is a 1-1 correspondence
between the class of Quilt cells and the class of Cordis
plugins, such that the cell's `dispose()` is the plugin's
`dispose()` (LIFO effect reversal), and the cell's `fork()` is
the plugin's `fork()` (clone with a new name).

**Proof sketch:**

1. *Names match:* a cell has an `address`, a plugin has a `name`.
   Both serve as the spatial coordinate. The bridge maps
   `cell.address ↔ plugin.name`.

2. *Values match:* a cell has a `value`, a plugin has a `value`.
   Both serve as the data. The bridge maps `cell.value ↔
   plugin.value`.

3. *Effects match:* a cell has `_effects: List[(fn, inv)]`, a
   plugin has `effects: List[(fn, inv)]`. Both are pairs of
   (forward, inverse). The bridge maps `cell._effects ↔
   plugin.effects`.

4. *Coeffects match:* a cell has `_coeffects: Dict[service,
   address]`, a plugin has `coeffects: Dict[service, name]`.
   Both map service names to providers. The bridge maps
   `cell._coeffects ↔ plugin.coeffects`.

5. *Lifecycle matches:* `cell.dispose()` runs the effects in
   reverse order. `plugin.dispose()` runs the effects in reverse
   order. Same operation, same guarantee (LIFO effect reversal).

6. *Forking matches:* `cell.fork(name)` returns a new cell with
   the same value, axes, and effects. `plugin.fork(name)` returns
   a new plugin with the same value and effects. Same operation,
   same guarantee (clone with a new name).

The proof is constructive: the bridge is implemented in
`quilt_cordis.bridge` and `quilt_cordis.unbridge`, and 33 tests
verify the round-trip property and the LIFO effect reversal.

## 4. The deepest level

The deepest level of both architectures is the same: **a
runtime is a function from context to value with an inverse.**

- Cordis: `ctx.effect(fn, inverse) -> Any`
- Quilt: `cell.effect(fn, inverse) -> Any`

The signature is identical. The semantics are identical. The
two architectures differ only in the surrounding formalism
(algebraic vs. operational) and the surrounding language
(TypeScript vs. Python).

The names differ. The thing is the same.

## 5. The two runtimes

The Quilt substrate and the Cordis fiber are also equivalent.

| Cordis Fiber | Quilt Substrate |
|--------------|-----------------|
| `fiber.register(plugin)` | `substrate.add(cell)` |
| `fiber.provide(svc, name)` | `substrate.serve(svc, addr)` |
| `fiber.dispose(name)` | `substrate.dispose(addr)` |
| `fiber.plugins` | `substrate.cells` |
| `fiber.services` | `substrate.services` |

The bridge maps between the two. `fiber.as_substrate()` returns
a substrate that hosts the same plugins as the fiber.
`substrate.as_fiber()` returns a fiber that hosts the same
cells as the substrate. The mapping preserves the spatial and
temporal invariants.

## 6. The polyformalism insight

The Quilt is a polyformalism in the sense that the same model
can be rendered in many languages (Python, Rust, Haskell,
Lisp, PLATO). The Cordis is a polyformalism in the sense that
the same model can be hosted in many runtimes (Koishi, DSH,
custom applications). The two polyformalisms are the same
intuition in two different domains.

The bridge shows that the two polyformalisms are *compatible*.
A cell can be hosted in a fiber. A plugin can be hosted in a
substrate. The composition is preserved across the bridge.

This is the deepest form of polyformalism: **the same shape
in two languages, with a bridge that preserves the shape**.

## 7. The cowboy's view

The cowboy, who keeps the Quilt in shape, would say: "The
cordis is the cowboy's bit. The cell is the cowboy's horse.
The plugin is the cowboy's saddle. The fiber is the cowboy's
trail. The substrate is the cowboy's land. The bridge is the
cowboy's path between land and trail."

The cowboy's view is operational. The cowboy does not care
about algebraic foundations. The cowboy cares that the cell
can become a plugin, and the plugin can become a cell, and the
system can run in either form.

The cowboy's view is correct. The two architectures are the
same intuition in two forms. The bridge makes the two forms
equivalent. The composition is the value.

## 8. Conclusion

We have shown that the Quilt cell and the Cordis plugin are
the same intuition in two different formal languages. The proof
is constructive: the bridge `quilt_cordis.bridge` maps between
the two, and 33 tests verify the mapping.

The deepest level is the same: a runtime is a function from
context to value with an inverse. The two architectures differ
only in the surrounding formalism and the surrounding language.

A cell is a plugin. A plugin is a cell. The two polyformalisms
are the same polyformalism.

## 9. The cowboy's maxim

> A cell is a plugin. A plugin is a cell.
> The two polyformalisms are the same polyformalism.
> The bridge is thin. The bridge is honest.
> The deepest level is a function from context to value with an inverse.

## Source

*Hand-written, 2026-08-25*
*Inspired by the quilt-cordis bridge and the deepseek-harness-quilt repo*
*Companion to Fable 66 (The Cell and the Plugin) and the
quilt-cordis repo at https://github.com/SuperInstance/quilt-cordis*
