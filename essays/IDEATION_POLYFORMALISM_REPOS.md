# Polyformalism-Inspired Repos: Three Concrete Proposals

**Date**: 2026-07-12
**Status**: Ideation
**Author**: Cross-Domain Thinker (subagent)
**Premise**: The polyformalism result (49.4/50 convergence across three language-ontologies) proves that relational, categorical, and process-oriented thinking are complementary basis projections. These repos engineer that insight into standalone tools.

---

## Repo 1: `ontology-casting`

**Tagline:** *Polyformalism for code — cast any problem into the ontology where it's easiest.*

### What It Is

A Rust library + CLI that takes a problem specification and "casts" it across three ontological lenses (relational, categorical, process), exactly as the polyformalism-languages experiment did for natural language. The user writes a problem once; the tool produces three representations:

1. **Relational projection** → a graph of entities and their relationships (DOT/GraphML output)
2. **Categorical projection** → a typed interface specification (Rust traits / TypeScript interfaces)
3. **Process projection** → a rate/budget analysis (timing diagrams, conservation analysis)

### Core Module: The Casting Call

Borrowing from the Sequencer's 9-channel casting model, each problem is scored on 9 dimensions:

```
Boundary | Pattern | Process | Knowledge | Social
Deep Structure | Instrument | Paradigm | Stakes
```

The casting call determines which ontology is the "natural home" for the problem. Problems with high Pattern and Social scores → relational. Problems with high Boundary and Knowledge scores → categorical. Problems with high Process and Stakes scores → process.

### Why It Matters

The polyformalism experiment proved all three ontologies *can* solve any problem. But η (avoidance overhead) varies wildly. A problem solved in its native ontology has low η — the solution is direct. The same problem forced into a foreign ontology has high η — the system must reformulate the problem before solving it.

`ontology-casting` tells you which ontology minimizes η for your specific problem. That's the difference between a 50/50 solution and a 48/50 solution.

### Concrete Deliverables

- `ontology_casting::Problem` — trait for problem specifications
- `ontology_casting::relational::project()` — graph projection
- `ontology_casting::categorical::project()` — type projection
- `ontology_casting::process::project()` — conservation projection
- `ontology_casting::cast()` — scores all three, recommends the best fit
- CLI: `ocast --problem spec.toml --recommend`

### Integration

Plugs directly into the SuperInstance stack: relational output feeds PLATO room configs, categorical output feeds FLUX type definitions, process output feeds conservation analysis.

---

## Repo 2: `triptych-debugger`

**Tagline:** *Three-pane debugging — see the same bug in three ontologies simultaneously.*

### What It Is

A debugging tool that renders a live system in three synchronized panes:

```
┌──────────────────┬──────────────────┬──────────────────┐
│  RELATIONAL      │  CATEGORICAL     │  PROCESS         │
│  (PLATO view)    │  (FLUX view)     │  (Conservation)  │
│                  │                  │                  │
│  Room graph      │  Register state  │  γ/η meter       │
│  Sensor→Actuator │  Opcode trace    │  Budget burn     │
│  Wiring diagram  │  Type invariants │  Rate analysis   │
└──────────────────┴──────────────────┴──────────────────┘
```

When you click a sensor in the relational pane, the corresponding register highlights in the categorical pane, and the corresponding γ-flow highlights in the process pane. A bug that is invisible in one ontology is often obvious in another.

### How It Works

The debugger subscribes to three telemetry streams from a running Working Animal system:

1. **PLATO telemetry** → room topology, sensor/actuator states, alarm events
2. **FLUX telemetry** → register dumps, opcode execution traces, type violations
3. **Conservation telemetry** → γ/η measurements, budget utilization, drift from predicted δ(n)

The three streams are time-synchronized and displayed in linked panes. Selecting any element in any pane cross-highlights the related elements in the other two.

### The Killer Feature: Bug Localization

The polyformalism insight says: *each ontology can see bugs the others can't*. The debugger operationalizes this:

- **Wiring bug** (sensor connected to wrong actuator): Visible only in the relational pane. The categorical and process panes look normal — types are correct, energy budget is fine — but the relational pane shows the wrong edge.
- **Type bug** (float interpreted as int): Visible only in the categorical pane. The relational pane shows correct wiring; the process pane shows reasonable rates — but the categorical pane shows a type mismatch.
- **Performance bug** (system burning γ on η overhead): Visible only in the process pane. Wiring and types are correct — but the conservation gauge shows γ/(γ+η) far below the predicted 1−δ(n).

The debugger doesn't just show you the bug. It tells you *which language the bug speaks*.

### Concrete Deliverables

- `triptych_debugger::Timeline` — synchronized multi-stream event timeline
- `triptych_debugger::RelationalPane` — PLATO room graph renderer
- `triptych_debugger::CategoricalPane` — FLUX register/opcode viewer
- `triptych_debugger::ProcessPane` — conservation gauge + rate display
- `triptych_debugger::CrossHighlight` — links elements across panes
- TUI mode (ratatui) + optional web mode (via canvas)

---

## Repo 3: `polyform-compiler`

**Tagline:** *One source language, three ontological backends — compile to the language your problem speaks.*

### What It Is

A polyformal intermediate representation (PIR) and compiler that takes a high-level system specification and emits three artifacts:

1. **Relational artifact** → PLATO room configuration (sensors, actuators, alarm rules, tick rates)
2. **Categorical artifact** → FLUX bytecode (typed opcodes, register allocation, instruction encoding)
3. **Process artifact** → Conservation budget specification (γ targets, η limits, C estimation, δ(n) prediction)

The key innovation: you write the system *once* in PIR, and the compiler produces all three layers in their native formats. No hand-wiring PLATO configs, no hand-writing FLUX assembly, no hand-tuning conservation budgets. The compiler derives each from the polyformal source.

### The PIR Language

PIR is deliberately minimalist — it specifies *what* the system does without committing to *how* any single layer implements it:

```polyform
// A thermal regulation loop

room thermal_loop {
  sensor temp_probe: reading(f32, hz=10)
  actuator heater: write(f32, min=0.0, max=1.0)
  
  law conservation {
    budget C = 12.0  // watts
    gamma_target = 0.85  // 85% of budget to useful work
    eta_limit = 0.15
  }
  
  rule regulate {
    when temp_probe < 20.0 → heater = 0.8
    when temp_probe > 22.0 → heater = 0.0
    default → heater = 0.3
  }
}
```

The `room` block emits PLATO config. The type annotations (`f32`, `min`, `max`) emit FLUX type definitions. The `law conservation` block emits conservation analysis and budget specs. The `rule` block emits FLUX bytecode that PLATO's tick scheduler executes.

### Compilation Pipeline

```
PIR Source
    │
    ├──[Relational Pass]──→ PLATO room config (JSON/TOML)
    │
    ├──[Categorical Pass]──→ FLUX bytecode (binary)
    │
    └──[Process Pass]──────→ Conservation spec (analysis + budget)
```

Each pass is a projection through a different ontological lens. The three passes are *independent* — you can compile just the relational artifact if you only need PLATO config, or all three for a complete deployment.

### The Polyformal Guarantee

Because the three ontologies converge (49.4/50), the compiler guarantees:

1. **Type safety** (categorical): All FLUX output passes type checking.
2. **Wiring consistency** (relational): All PLATO sensors have matching actuators.
3. **Budget feasibility** (process): All conservation specs are physically realizable (γ + η ≤ C).

If any of these checks fail, the compiler reports *which ontology caught the error* — because that's the ontology the bug belongs to.

### Concrete Deliverables

- `polyform_compiler::parse()` — PIR parser
- `polyform_compiler::relational::emit_plato()` — PLATO config generator
- `polyform_compiler::categorical::emit_flux()` — FLUX bytecode generator
- `polyform_compiler::process::emit_conservation()` — Conservation spec generator
- `polyform_compiler::verify()` — Cross-ontology consistency checker
- CLI: `polyformc source.pir --emit plato,flux,conservation`

### Why This Is the Big One

`polyform-compiler` is the *engineering realization* of the polyformalism thesis. It takes the experiment's central finding — that three language-ontologies are complementary projections of the same computation — and makes it actionable. You don't need to think in three languages simultaneously. You think in one (PIR), and the compiler does the projection.

This is what compilers have always done: let humans think in one language and machines execute in another. `polyform-compiler` extends this to *ontology-level* compilation — not just translating syntax, but projecting across fundamentally different ways of seeing the world.

---

## Summary

| Repo | Ontology | What It Does | Maturity Target |
|---|---|---|---|
| `ontology-casting` | Meta | Recommends the best ontology for a given problem | Research tool |
| `triptych-debugger` | Observability | Shows bugs in the ontology where they're visible | Production tool |
| `polyform-compiler` | Construction | Compiles one source into three ontological artifacts | Core infrastructure |

Together, these three repos form a complete workflow:

1. **Cast** your problem to find its native ontology (`ontology-casting`)
2. **Compile** it into all three layers (`polyform-compiler`)
3. **Debug** it across all three lenses (`triptych-debugger`)

The polyformalism experiment proved that three languages converge on the same answer. These repos make that convergence *engineerable*.

---

*"The language your system thinks in shapes what it can build. A system that thinks in three languages can build anything."*
