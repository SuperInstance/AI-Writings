# Project Hermes NMI — Onboarding

**Repository:** [SuperInstance/hermes-nmi](https://github.com/SuperInstance/hermes-nmi)
**Crate:** `hermes-nmi` v0.1.0
**Date:** 2026-08-08

---

## What You're Looking At

This is a Rust crate that implements the Neuro-Muscular Interface — the bridge layer between three systems in the SuperInstance ecosystem:

1. **Hermes Construct (CNS)** — the brain. Handles reasoning, goal decomposition, energy conservation, and contextual gravity.
2. **Claw** — the muscles. A cellular agent engine with equipment slots (Head, Torso, Arms, Legs, Special) and lifecycle states (Idle → Thinking → Acting → Error).
3. **Pincher** — the spinal cord. A reflex engine that matches stimuli against learned patterns in <50ms using a vector DB. No LLM in the loop.

The NMI translates between them. It takes high-level intent from the brain and turns it into discrete actions the muscles can execute. It takes sensory feedback from the muscles and packages it for the brain. And it gives the spinal cord a direct pathway to the muscles when speed matters more than understanding.

---

## Design Spec

The original design is in `hermes-construct/NEURO-MUSCULAR-INTERFACE.md`, written by Hermes. The spec defines:

- **`ReasoningPulse`** — the payload from CNS to NMI (intent type, coordinates, gravity, energy quota, constraints)
- **`CommandChain`** — the translated sequence of discrete actions
- **`TelemetryFrame`** — the feedback from execution (sensor data, fulfillment status, state hash)
- **`NeuroMuscularInterface` trait** — the boundary contract (`dispatch_pulse`, `adjust_tension`)

The NMI crate implements all of these and adds the Tension parameter and Pincher reflex hook that the spec anticipated but left for implementation.

---

## Architecture (Read This First)

### The Flow

```
CNS emits ReasoningPulse
         │
         ▼
NmiDispatcher.translate()     ← pattern matching, no LLM
         │
         ▼
CommandChain { commands: [Command, ...] }
         │
         ▼
ClawNmiAdapter.execute_chain()  ← equip/unequip/step against agent
         │
         ▼
TelemetryFrame { status, sensor_data, tension }
         │
         ▼
CNS reads telemetry, adjusts strategy
```

### The Reflex Shortcut

```
Stimulus hits Pincher
         │
         ▼
ReflexMatch { confidence: 0.0–1.0 }
         │
    ┌────┴────────────────────┐
    │                         │
 ≥ 0.80                    < 0.55
 (Exact)                   (Novel)
    │                         │
    ▼                         ▼
PincherHook builds       PincherHook escalates
CommandChain             as ReasoningPulse to CNS
(skip Thinking state)
```

### The Tension Model

Tension = `gravity × (1 - fraction_energy_remaining)`

| Tension | Effect |
|---|---|
| 0.0–0.5 | Normal execution. All commands execute. Fuzziness is minimal. |
| 0.5–0.7 | Slight degradation. Fuzziness begins ramping. |
| 0.7+ | Chain trimming. Non-essential commands are dropped. Only first + last survive. |
| 0.8+ | Critical. Precision constraints may fail. CNS should reconsider. |

The tension level is included in every TelemetryFrame so the CNS can adapt.

---

## Module Guide

### `pulse.rs` — Types That Flow Downward

- **`ReasoningPulse`** — the input. Intent + coordinates + gravity + energy + constraints.
- **`IntentType`** — Navigate, Interact, Observe, Equip, Reflex, Rest.
- **`CommandChain`** — the output. An ordered list of Commands with an estimated cost.
- **`Command`** — a single action + optional slot target.
- **`ClawAction`** — Equip, Unequip, Step, SetState.
- **`Constraint`** — TimeBudgetMs, EnergyCeiling, Precision, RequireSlots, AvoidStates.

### `dispatcher.rs` — The Translator

- **`NmiDispatcher`** — owns the current Tension state and energy consumed.
- **`translate()`** — pure pattern matching on IntentType → CommandChain.
- **`validate()`** — checks constraints against current tension and chain cost.
- **`build_telemetry()`** — constructs the feedback frame.

### `telemetry.rs` — Types That Flow Upward

- **`TelemetryFrame`** — the feedback. Pulse ID, timestamp, tension, state hash, sensor data, status.
- **`SensorPayload`** — velocity, proximity, contact state, resistance, positional delta.
- **`Status`** — Success, PartialSuccess, Failure, ReRoute, ReThink.

### `tension.rs` — The Fatigue Model

- **`Tension`** — the current strain level (0.0–1.0). Derived from budget and gravity.
- **`ConservationBudget`** — total energy, spent so far, current allocation.
- Key methods: `adjust_cost()`, `fuzziness()`, `is_critical()`.

### `claw_adapter.rs` — The Muscle End

- **`ClawNmiAdapter`** — implements `NeuroMuscularInterface`. Owns a `ClawInstance` and a `NmiDispatcher`.
- **`ClawInstance`** — simulated agent with state and equipment slots.
- **`EquipmentSlot`** — Head, Torso, Arms, Legs, Special.
- **`AgentState`** — Idle, Thinking, Acting, Error.

### `pincher_hook.rs` — The Spinal Cord

- **`PincherHook`** — processes reflex matches, either fires directly or escalates.
- **`ReflexMatch`** — stimulus + confidence + matched intent.
- **`MatchType`** — Exact (≥0.80), Similar (0.55–0.80), Novel (<0.55).
- **`ReflexTrigger`** — wraps a match with an action and confirmation flag.

---

## How to Build and Test

```bash
cd /home/eileen/projects/hermes-nmi
cargo build
cargo test
```

24 tests: 10 unit tests (in `tension.rs` and `pincher_hook.rs`), 14 integration tests (in `tests/integration.rs`).

---

## How to Extend

### Adding a New Intent Type

1. Add the variant to `IntentType` in `pulse.rs`.
2. Add a match arm in `NmiDispatcher::translate()` with the appropriate command sequence.
3. Add a test case in `tests/integration.rs`.

### Adding a New Constraint

1. Add the variant to `Constraint` in `pulse.rs`.
2. Add validation logic in `NmiDispatcher::validate()`.

### Connecting to Real Claw

Replace the simulated `ClawInstance` in `claw_adapter.rs` with a handle to the actual Claw runtime. The `ClawNmiAdapter` methods (`equip`, `unequip`, `step`, `set_state`) already mirror Claw's trait interface.

### Connecting to Real Pincher

Wire `PincherHook::process()` to receive `ReflexMatch` results from Pincher's vector DB query. The hook handles the routing — direct execution or CNS escalation.

---

## Design Decisions

### Why deterministic translation (no LLM in the dispatcher)?

The LLM already did its work in the CNS. The dispatcher's job is mechanical: decompose intent into steps. Adding an LLM here would add latency to the hot path without improving quality — the intent is already decided.

### Why is Tension multiplicative (gravity × energy depletion)?

Because environmental complexity and low energy compound. A complex environment on full energy is manageable. A simple environment on low energy is manageable. Both at once is when systems fail. The multiplicative model captures this.

### Why does the reflex bypass the Thinking state?

Because thinking takes time. When confidence is ≥0.80, the reflex is well-learned. Going through Thinking → Acting → Idle adds two unnecessary lifecycle transitions. The reflex goes straight to Acting.

### Why does the PincherHook return `Result<CommandChain, ReasoningPulse>`?

Because escalation isn't an error — it's a *different kind of message*. The `Err` variant is a ReasoningPulse that the CNS can dispatch normally. This lets the reflex hook compose cleanly with the rest of the pipeline.

---

## Origin Story

Hermes wrote the NEURO-MUSCULAR-INTERFACE spec as part of the hermes-construct project. The spec defined the trait, the types, and the roadmap. The NMI crate is Phase 01 of that roadmap: the shared crate containing the types and a working implementation.

The creative piece ["The Space Where Intent Lives"](../the-space-where-intent-lives.md) explores the philosophy behind the architecture: the speed of reflex, the patience of reason, and the gap between them where intent is translated into action.

---

## Related

- **Spec:** `hermes-construct/NEURO-MUSCULAR-INTERFACE.md`
- **Claw:** `/mnt/c/Users/casey/claw` — cellular agent engine
- **Pincher:** `/mnt/c/Users/casey/pincher` — reflex engine
- **Hermes Construct:** `/mnt/c/Users/casey/hermes-construct` — CNS
- **Creative:** [The Space Where Intent Lives](../the-space-where-intent-lives.md)

---

*The NMI is 253 milliseconds wide. Everything important happens there.*
