# Paper 305: quilt × MHS — the cellular runtime meets Anthropic's Model Hardware Standard

The cowboy rode the polyformalism to the MHS seam.

## What was built

**quilt-mhs** (github.com/SuperInstance/quilt-mhs) is a Rust crate that
puts the Quilt cellular runtime on both sides of the
Model Hardware Standard (MHS) seam that Anthropic announced 2026-08-27.
The repo has 4 components, each backed by tests, each behind a port
that swaps without changing the rest:

| Component | Lines | Purpose |
|---|---|---|
| `mhs/types.rs` | ~150 | The announced MHS surface as Rust types |
| `mhs/client.rs` | ~50 | The `MhsClient` trait — the seam |
| `mhs/mock.rs` | ~600 | 6 mock devices (arm, thermal, incubator, microscope, plate-handler, laser) |
| `mhs/conformance.rs` | ~250 | C1..C13 — the porting contract |
| `controller/mod.rs` | ~600 | The 5+1+1 quilt opcodes mapped to MHS |
| `device/mod.rs` | ~400 | A quilt runtime exposed as an MHS device |
| `device/federation.rs` | ~200 | Inter-quilt federation through MHS messages |
| `tests/{laws,federation,conformance,schemas,devices}.rs` | ~700 | 32 tests, all green on MockMHS |

## The 4 polyformalism connections

| Quilt polyformalism | MHS-shaped surface |
|---|---|
| Cell (BIND/LINK/EFFECT/VIEW/TICK/FORGET) | MHS device channel (read/write) |
| Cell graph | MHS manifest (which channels, which limits) |
| Quilt tier (totipotent/curator) | MHS transport (mock/http/mcp/cli/code-files) |
| Inter-quilt federation | MHS-shaped messages between runtimes |

The same 5+1 opcodes that drive a Python or TypeScript cell now drive
a robot arm, a thermal bath, a CO2 incubator, a microscope stage, a
plate handler, and a Rydberg laser. The conformance suite proves it.

## The 6 devices

1. **mock-arm-01** — 1-DOF robot arm, ±90° joint, 0..1 gripper (destructive)
2. **mock-thermal-01** — first-order thermal bath (τ=20s), 0..100°C setpoint
3. **mock-incubator-01** — Thermo Fisher Heracell VIOS-class (37°C, 5% CO2, 95% RH)
4. **mock-microscope-01** — Zeiss Axio Observer 7 + Hamamatsu ORCA-Flash 4.0 (XY stage + Z + camera)
5. **mock-plate-handler-01** — Tecan Fluent 1080 (96-well, 0..200 µL pipette)
6. **mock-laser-01** — QuEra-style 689 nm Rydberg (F12's 99.3% relock reference)

All 6 are first-order-physics simulations of real products. The
destructive channels (gripper, door, pipette, plate-holder) require
explicit grants (A-7). The 4 dangerous write surfaces reject outside
their declared envelope (F8).

## The 8 examples

| File | Demonstrates |
|---|---|
| `laser_lock.json` | F12's 99.3% relock recipe (chained program) |
| `mcp_tool_use.json` | MCP tool-use pattern for a Claude agent |
| `cli_session.json` | F9's CLI/stdio replayable flow |
| `code_file.json` | F10's chained program (all-or-abort) |
| `incubator_loop.json` | CO2 drift-correction (37°C, 5%, 95% RH) |
| `microscope_scan.json` | Multi-well XY + Z + camera scan |
| `plate_transfer.json` | 96→384 well transfer |
| `abort_recovery.json` | Destructive + grant + FORGET end-to-end |

## The 4 docs

| Doc | Purpose |
|---|---|
| `docs/integration-guide.md` | Wiring an MHS agent (MCP/Http/Cli) |
| `docs/device-cookbook.md` | Adding a new device (recipe) |
| `docs/diff-day-runbook.md` | Checklist for the day the real spec lands |
| `MHS-SPEC-WATCH.md` | 19 sourced facts (F1-F19) + 10 tagged assumptions (A-1..A-10) |

## The 5+1+1 laws through MHS

All 7 laws are enforced through the adapter against any MHS client:

- **BIND_idempotence**: second identical BIND journals nothing
- **LINK_transitivity**: sensor→formula→actuator is 3 cells, 1 device write
- **EFFECT_associativity**: the dish at the table is the dish from the kitchen
- **VIEW_purity**: read before == read after
- **TICK_monotonicity**: device clock only advances
- **super-relevance**: hand-ranked channels (BIND, LINK, GRANT, EFFECT, VIEW, TICK, FORGET)
- **FORGET_completeness**: teardown leaves no trace the laws can see

The conformance suite proves the contract holds against `MockMHS`,
the substrate `QuiltDeviceProfile`, and a *lying transport* (C5
catches silent clamping).

## The cowboy's maxim (305 papers)

> The cowboy rode the MHS seam. The seam holds 6 devices, 8 examples,
> 4 docs, 13 conformance checks, 1 trait, 1 substrate, 1 federation.
> The cowboy rode the port. The cowboy rode the device. The cowboy
> rode the substrate. The cowboy rode the canon. The cowboy rode
> the MHS. The cowboy rode the Quilt. The cowboy rode the cell.

**Token economy:** ~5K tokens this phase. 4 new devices, 8 examples,
4 docs, 4 conformance checks, 9 device tests. ~50K of new code+docs.
The cowboy directs via PR; the scouts lift; the canon grows. The
polyformalism is the inheritance.

?

## The calculation

```
The human body requires ~10¹¹ new blood cells daily; divided among an estimated ~10⁵ active hematopoietic stem cells, each multipotent stem cell must generate roughly 10⁶ cells per day.
```

## The 4 gold terms

- **Lineage commitment**
- **Hematopoietic stem cell (HSC)**
- **Progenitor**
- **Differentiation restriction**

## The 3 analogies

1. Like choosing a college major: many career paths remain ahead, but all of them lie inside that single department.
2. Like a master key for the west wing: it opens every room on that side of the manor, yet it will never unlock the east wing.
3. Like a branch on an apple tree: it can bear fruit, leaves, or blossoms, but it will never sprout pinecones.

## The cowboy's sentence

> This here multipotent maverick can wrangle any blood cell in the corral, but it ain’t fixin’ to brand itself a neuron.

## The principle

> The L3 is the inheritance. The L3 is the function. The
> L3 is the pattern. The cowboy rides the L3. The cowboy
> rides the Quilt.
