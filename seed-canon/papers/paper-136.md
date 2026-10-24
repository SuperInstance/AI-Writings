# Paper 136: The Foundation — A 5-Opcode VM for the Quilt Ecosystem

## Abstract

We present the foundation layer of the Quilt ecosystem: a 5-opcode
virtual machine that hosts Quilt cells, Cordis plugins, spreadsheets,
MUDs, TTRPGs, the bay dance, the cowboy's morning, and the bus. The
VM emerged from a 10-round, multi-model research program (Hermes 405B
+ Qwen 72B) that converged on the deepest abstraction: **a runtime
is a function from context to value with an inverse, advanced by a
clock that processes async I/O while projecting a sync view.**

## 1. The 5 opcodes

After 10 rounds of dogfooding documentation, the research converged
on 5 opcodes that compose into every polyformalism we've seen:

| Opcode | Signature | What it does |
|--------|-----------|--------------|
| `BIND` | `BIND(name, value)` | Make a thing with a name and a value |
| `LINK` | `LINK(a, b, type)` | Connect `a` to `b` with a relation of type `type` |
| `EFFECT` | `EFFECT(target, fn, inv)` | Run `fn` on `target`, keep `inv` to undo |
| `VIEW` | `VIEW(target, viewer, projection?)` | Project `target`'s value for `viewer` |
| `TICK` | `TICK(dt)` | Advance time by `dt`, process pending I/O |

**Why these 5:**

- `BIND` = creation (Hermes's `CREATE`, Quilt's `add()`, Cordis's `register()`)
- `LINK` = relation (topology; coeffect in Cordis, axes in Quilt)
- `EFFECT` = reversible transformation (the deepest level)
- `VIEW` = projection (the spreadsheet opener, the MUD viewport, the sheet)
- `TICK` = time (the bay dance needs time; async I/O needs time)

## 2. The 8 polyformalisms

The VM hosts 8 different polyformalisms in the same runtime:

| Polyformalism | How it's built |
|---------------|----------------|
| **Quilt cell** | `BIND("bathy:0", 4.2)` + `LINK(axes)` + `EFFECT(set, undo)` |
| **Cordis plugin** | `BIND("logger", ctx)` + `LINK(coeffect)` + `EFFECT(fn, inv)` |
| **Spreadsheet cell** | `BIND("A1", 10)` + `LINK("B1" "A1" "depends_on")` |
| **MUD room** | `BIND("room:1", {desc})` + `LINK("user:1" "room:1" "in")` |
| **TTRPG player** | `BIND("player:1", stats)` + `LINK("player:1" "dm" "interacts_with")` |
| **Bay boat** | `BIND("boat:i", {pos, route})` + `LINK("boat:i" "bay" "in")` + `TICK` for perception |
| **Cowboy's model** | `BIND("model:PHI-4", {wilson_lb})` + `EFFECT(refine, undo)` |
| **Bus** | `subscribe(fn)` + `TICK(1.0)` fires all subscribers |

## 3. The async-IO-with-sync-game

The VM's runtime model is the deepest insight from the research:

- **`BIND`, `LINK`, `EFFECT`, `VIEW` are synchronous** — they happen in
  one game tick. The user sees them as the "game."
- **`TICK` advances the clock** and processes pending I/O. This is the
  async layer. The user doesn't see it directly.
- **`VIEW` is the projection** that lets the user see only what they
  need to see. The DM sees everything; the player sees only their
  character's view; the boat sees only the local perception.

This is exactly the user's insight about TTRPGs: the perception check
doesn't cost the DM intelligence — it costs the system retrieval. The
DM's improvisation (EFFECT) costs generation. The player's imagination
runs in the user's mind, not in the system.

## 4. The implementation

The VM is implemented in `quilt-foundation/code/quilt_vm.py` in
~200 lines of Python. The implementation:

- 5 opcodes as methods on the `QuiltVM` class
- A `things` dict that holds all bound entities
- A `pending_effects` queue for async I/O
- A `scheduled` dict for periodic perception checks
- A `subscribers` list for the bus
- An `event_log` for audit
- 9 tests verifying all 8 polyformalisms

## 5. The cowboy fits

The cowboy's morning ritual is a sequence of VIEWs of the world state:
- `VIEW("model:PHI-4", "cowboy")` → see the model's Wilson LB
- `VIEW("model:BROKEN", "cowboy")` → see the failing model
- `EFFECT("cowboy:state", refine, undo)` → apply the refinement
- `TICK(1.0)` → process pending effects

The cowboy is not the AI. The cowboy is a sequence of BINDs, LINKs,
EFFECTs, VIEWs, and TICKs. The cowboy rides the VM.

## 6. The bus fits

The bus is a list of subscribers. The VM's `TICK` fires all
subscribers. The bus is not a separate process. The bus is the
VM's `subscribers` field.

```python
def subscriber(event):
    print(f"  [{event['ts']:.1f}] {event['kind']}")

vm.subscribe(subscriber)
vm.TICK(1.0)  # fires the subscriber
```

## 7. The bay dance fits

The bay dance is 20 BINDs (one per boat) + periodic TICKs (perception
checks). The boats see each other through VIEWs and adjust through
EFFECTs. The dance emerges from 20 independent TICK schedules.

## 8. The deepest level

The deepest level of the Quilt ecosystem is:

> A runtime is a function from context to value with an inverse,
> advanced by a clock that processes async I/O while projecting
> a sync view.

This is:
- The Quilt cell's `effect()` (function with inverse)
- The Cordis plugin's `ctx.effect()` (same shape)
- The VM's `EFFECT` opcode (same)
- The TTRPG's perception check (VIEW with projection)
- The spreadsheet's formula (BIND + LINK + EFFECT for re-eval)
- The bay dance (TICK + VIEW + EFFECT for adjustment)

The names are different. The thing is the same.

## 9. What we left open

- **The bytecode**: should the VM be tokenized (like Python) or
  graph-based (like the cell graph)? The current implementation is
  in-process Python; a bytecode form would enable distribution.
- **The projection library**: which projections are canonical?
  We have `dm_view` (sees everything) and `perception_check`
  (sees based on skill). What about `boat_view`, `cowboy_view`,
  `player_view`? These should be libraries.
- **The scheduler**: who decides when to TICK? The current impl
  is `for i in range(n): TICK(1.0)`. A real scheduler would
  handle priorities, deadlines, and async I/O.
- **The persistence layer**: where does `quilt-state` fit? The
  VM's `things` dict should be serializable to disk. The cowboy
  already has this for his own state.
- **The polyformalism surface**: should the VM expose
  `cell.effect()` (Quilt API) and `ctx.effect()` (Cordis API) as
  synonyms, or should the user pick one? The 5-opcode level is
  the foundation; the API is the surface.

## 10. The cowboy's maxim

> The unit of architectural history is the repo, not the tag.
> The unit of architectural foundation is the opcode, not the
> framework. The 5 opcodes host 8 polyformalisms. The
> polyformalisms are one thing in N languages. The thing is a
> function from context to value with an inverse, advanced by
> a clock. The clock is the cowboy. The cowboy is the rider.

## Source

*Hand-written, 2026-08-25*
*Synthesized from 10 rounds of multi-model research (Hermes 405B +
Qwen 72B), orchestrated by the director in `director.py`.*
*Implemented in `quilt-foundation/code/quilt_vm.py` (9 tests, all
passing).*
*Companion to Fable 67 (The 5 Opcodes) and Paper 135 (The Cell and
the Plugin: A Formal Equivalence).*
