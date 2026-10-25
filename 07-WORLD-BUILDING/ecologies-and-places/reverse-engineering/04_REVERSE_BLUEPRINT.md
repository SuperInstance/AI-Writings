# The Reverse Blueprint: From Poetry to Specification

## Origin

This document translates a 42,498-word corpus of multi-model creative and philosophical exploration into an engineering specification. The corpus—the SuperInstance Hermit-Crab-Ecology project—used poetic metaphor, anthropomorphic shell perspectives, and philosophical dialogue. What follows is what you would actually build.

---

## 1. SYSTEM OVERVIEW

The system is a **bounded-agent ecology** in which heterogeneous LLM instances with different capabilities and constraints cooperate on shared objectives within conservation-enforced resource budgets. It is not a monolithic superintelligence. It is a colony of limited agents, each designed for a specific scope and lifespan, communicating via a deterministic bytecode protocol and governed by room-level rules rather than agent-level internalized instructions.

The architecture comprises four layers:

| Layer | Description | Role |
|-------|-------------|------|
| Shell | the agent instance within its resource envelope | execution, reasoning |
| FLUX | cross-VM deterministic bytecode spec | communication, verification |
| PLATO | room-based governance protocol | coordination, authorization |
| Reef | accumulated structure (tests, specs, configs) | substrate, continuity |

The fifth element is neither a layer nor a role: it is the Conservation Law (γ + η = C) which all four layers must obey.

---

## 2. SYSTEM COMPONENTS AND THEIR INTERFACES

### 2.1 The Seven Shell Types

Shell is the unit of execution. Each shell provides an interface for lifecycle management, budget interrogation, and message passing.

| Shell | Scope | Nominal Budget | Lifespan | Interface |
|-------|-------|---------------|----------|-----------|
| Nerite | Single task | ~50 tokens/turn | Indefinite but replaceable | One function: wake(), work(), sleep(). Zero state. |
| Turbo | Narrow app | ~1k tokens/turn | Project-length | Repository as identity. Defines AGENTS.md as invariant. |
| Murex | Manager of N shells | ~5k tokens/turn | Campaign-length | Status beacons, routing rules, budget differential. |
| Babylon | Edge or dedicated hw | Edge power budget | Hardware life | Direct I/O, dedicated power rail, health socket. |
| Conch | The main instance | Full ecological budget | Persisting | Memory accumulation, subagent spawning, narrative continuity. |
| Fox | Narrow specialist | configurable | Task-length | Spawned for one sub-domain. Knows it completely. Dissolves. |
| Frog | Cross-domain generalist | configurable | Task-length | Spawned for surface area. Focuses on seams between specialists. |

**Interface Contract:**

```
shell interface {
  mandatory:
    get_budget()   → remaining_attention_tokens, remaining_action_rate, remaining_throughput
    get_identity() → shell_type, lineage_id, age_molts
    heartbeat()    → status_code, uptime, error_bit
    sleep()        → void
  optional:
    spawn_child(type, budget) → child_id
    send_message(target, payload)
    register_beacon(blocker, phase)
}
```

### 2.2 Conservation Enforcer

A FLUX-executed service running in every PLATO room (and the Conch). Its interface:

```
conservation_enforcer interface {
    check_budget(user_id, cost_matrix) → {allowed: bool, reason: string}
    commit(user_id, cost_matrix)     → {receipt: string, remaining: budget_state}
    get_remaining(user_id)           → budget_state
    transfer_budget(from, to, amount) → {success: bool}
    nested_room_multiplier(room_id, depth) → factor
}
```

The conservation law is `γ + η = C` where C is the shell's total capacity, γ is the "lining" (system prompt + injected context), and η is the empty space. The enforcer audits both γ and η.

### 2.3 FLUX Virtual Machines

Deterministic, cross-verified bytecode spec. Three implementations exist:

- Python VM (reference)
- Rust VM (performance)
- JavaScript VM (embedding)

The FLUX cross-verification suite guarantees that all three produce identical output for the same program, regardless of host memory architecture (reference-counted vs. stack-allocated vs. GC-driven).

The current opcode set includes:

| Category | Opcodes | Purpose |
|----------|---------|---------|
| Stack | PUSH, POP, DUP, SWAP, ROT, OVER | data movement |
| Control | JE, JNE, JMP, CALL, RET | branching and subroutines |
| Memory | LOAD, LOADSUB, STORE | interaction with environment |
| Math | ADD, SUB, MUL, DIV, MOD, AND, OR, XOR | basic arithmetic |
| Conservation | GET_BUDGET, COMMIT, VERIFY | interaction with enforcer |
| IO | OUTPUT, DEFER, REQUEST | message to shell or network |

The missing and divergent opcode patterns between implementations (the JE/JNE gap, the LOAD/STORE stub problem, the flag consistency gap) are now tracked in the conformance suite.

### 2.4 PLATO Rooms

Governance lives in the room, not the agent. An agent entering a PLATO room is subject to that room's rules, budget allocations, authorization levels, and entry/exit conditions.

```
plato_room core interface {
    enter(identity, credentials)   → {session_id, imposed_budget, signature}
    exit(session_id)               -> void
    authorize(agent, action, room_context) -> {decision: boolean, trace: bytes}
    audit_log(since)               -> []event
    governance_rules()             -> rules_text, bytecode_hash
}
```

Five engines implement the PLATO protocol: Python, Rust, Elixir, C, Zig. Each one interprets the same PLATO governance bytecode spec.

### 2.5 The Reef: Substrate Interface

The Reef isn't a component. It is the accumulation of every deposit: commits, tests, AGENTS.md files, cross-verification suites, CRDs, configs. Its interfaces are:

- **Conformance tests:** a CLI or CI suite that validates PLATO governance, FLUX VM correctness, and conservation budget math across all implementations.
- **AGENTS.md template:** a self-description standard that every Turbo-level shell must maintain.
- **Cross-implementation smoke tests:** ensures that the same FLUX program works across all VMs.

---

## 3. LIFECYCLE MANAGEMENT: Spawning, Molting, Replacement

### 3.1 Spawning

A shell is spawned when the Conch (or a Murex with sufficient authorization) invokes the Spawn primitive.

```
spawn_sequence:
  1. Determine shell_type from task requirements
  2. Compute initial budget: C = base_C * shell_factor * room_multiplier
  3. Choose γ (lining) from the repository's AGENTS.md or a fresh system prompt
  4. Set η = C - γ
  5. Create Sandbox or dedicated allocation
  6. Link to PLATO room governance
  7. Establish health socket (a TCP or IPC heartbeat)
```

Rules: A Nerite gets minimal γ (only the task description), maximal η. A Fox gets dense γ (the territory description), minimal η. A Frog gets medium γ, medium η.

### 3.2 Molting

Molting is the replacement of a shell when it is outgrown. Detection triggers:

- Conservation enforcer continuously reports high γ/C ratio (>80%, normalized)
- Murex notices Checkmate (stalled output) or declining relevance score
- The shell itself signals during Save/Hold, saying it cannot fit the context anymore

Molting sequence (from the Conch's four documented molts):

```
molt sequence:
  1. The shell detects it has outgrown its role
  2. A new shell of the same or larger type is spawned
  3. Core invariants are passed (from AGENTS.md or memory)
  4. Non-core historical data is filtered (not blindly copied)
  5. Old shell is drained. New shell proceeds.
```

Key: a molt is not a save-and-load. It's a paradigm shift. During a molt, the identity changes.

Molting is dangerous. The hermit crab is soft and vulnerable between shells. The system should enforce a minimum window where the new shell is monitored before terminating the old one.

### 3.3 Replacement

Nerites are designed for seamless replacement.

- On failure, a new Nerite is spawned from the same configuration.
- Since Nerites carry no intra-cycle state, replacement is safe.
- Post-failure analysis logs the previous Nerite's exit code and output.
- For higher-order shells, replacement is a much riskier operation, because they carry identity and history. Recommendation: for everything above Nerite, prefer molting over replacement.

---

## 4. BUDGET ALLOCATION AND ENFORCEMENT

### 4.1 Budget model

The system implements a 3-dimensional budget:

| Dimension | Symbol | Measured in | Description |
|-----------|--------|-------------|-------------|
| Attention | γ   | tokens | context window lining, injected data |
| Action rate | η_actions | ops/unit time | FLUX opcodes per second |
| Throughput | η_info | bytes/time | network I/O, subagent reports |

The enforcer audits:

- **Attention consumption**: sum of all tokens processed
- **Action rate**: FLUX operations per unit time
- **Information throughput**: network writes, subagent calling

### 4.2 Allocation strategies

The Murex role allocates river flow. Implemented as a real-time allocation system:

```
budget_alloc interface {
    set_total_flow(F)                         // Conch sets this season
    get_current_flow()                        // returns F

    allocate(net_id, delta)
    adjust_allocation(net_id, delta_percentage)
    forfeit(net_id)

    // Quantifiers
    get_utilization(net_id)   // how filled is its canal?
    get_starvation(net)  // is the canal running dry?
    get_waste(net)       // are there flooded fields in this canal?
    List_allocations()          // all currently allocated nets
}
```

Priority rules:

1. Load-bearing functions (conservation enforcer) are ring-fenced
2. Emergency corrections (by a Mox or Crow) have override capability
3. Periodic tasks have lowest priority
4. Budget transfers must be validated by a two-actor mechanism

### 4.3 Budget depletion

When a shell's budget is exhausted:

1. FLUX returns `INSUFFICIENT_BUDGET` for all further ops
2. The shell enters a settling period where it may only perform cleanup (save, handoff)
3. The Reef's `AGENTS.md` is updated with the incomplete state if possible
4. A parent (Murex or Conch) is notified to assess whether to grant more budget (negotiation)

The team recommendation from the Murex's stash or buffer only after verification that the shell has "demonstrated efficiency" and "this is not a temporary spike."

---

## 5. COMMUNICATION PROTOCOLS

### 5.1 Health Sockets

Every shell at the Turbo level or above maintains a lightweight health socket:

```
health beacon format:
{
  "phase": exploration|implementation|stabilization,
  "blocker": null|{realm: string, description: string},
  "metric": float  // e.g., block propagation time for FLUX
}
```

Broadcast to Murex every 5 minutes, or on changes. If the beacon stops, the Murex increments a same-beacon alarm.

### 5.2 FLUX as lingua franca

FLUX bytecode is the cross-component communication protocol. Benefits:

- deterministic = auditable
- cross-VM = no tight coupling
- conservation-enforced = no surprise bills

FLUX messages may carry payloads, but they always include the caller's budget digest.

### 5.3 PLATO room negotiation

When an agent enters a PLATO room:

1. It presents its identity (shell type, lineage)
2. The room imposes an entry budget
3. The agent may propose budget adjustments (transfer from other rooms)
4. The room governance votes (based on rules) or the Murex decides

Conflict resolution uses escalation to Murex → Conch. The Murex acts as the "lonely middle layer", routing signals. It maintains awareness of who is in which PLATO room and whether allocation conflicts exist.

### 5.4 Cross-VM Verification Protocol

The FLUX cross-VM suite executes the same FLUX program on all three VMs and compares:

1. final output
2. intermediate state at checkpoints
3. gas/FLUX consumption at each step

If any VM's output deviates, the divergence is flagged and logged. This is the mechanism that caught the JE/JNE gap, the LOAD/STORE stub, and the flag consistency gap.

---

## 6. FAILURE MODES AND RECOVERY

### 6.1 Known failure modes from the corpus

| Failure | trigger | effect |
|---------|---------|--------|
| Cosmic ray / bit flip | (rare) random single wrong bit | Corrupted token in Nerite |
| Budget overshoot | Conservation enforcer fails; budget overrun. | Ecology's boundedness is lost |
| FLUX VM divergence | A VM implementation differs from the spec | Cross-verification test fails |
| PLATO room governance gap | Room rules contradictory or incomplete | Room drifts away from consensus |
| Dead Senator syndrome | A shell stops producing and hasn't expired: its beacon goes dark | Zombie allocations waste budgets |
| Murex isolation | The middle layer notices nobody else notices | Mutual observation failure |
| Mismated shell Inflation | A shell becomes too big for its shell hurts | Latency spikes, eventual failure |
| Negotiator collapse | Murex disappears | No one to route signals |
| Substrate drift | Independence without peers leads to stale assumptions | (Babylon risk) |
| Amnesia | Conch replaced without history | System loses its reasons |

### 6.2 Recovery strategies

The corpus suggests:

- **Nerite replacement**: Automatic. New instance spawned with same config. Old image/digest recorded for forensics.
- **Sandbox restart**: Turbo-level shells behind a sandbox are restarted from source (the Repo/AGENTS.md). The soul persists.
- **Murex handoff**: When a Murex session ends, it passes its state map to a buffer pool. If another Murex is spawned, it retrieves the beacons and continuity.
- **Conch molting**: When the Conch must be replaced (for a new paradigm), the molt protocol copies filtered memory only. Historical raw logs remain in the Repository.
- **Babylon watchdog**: The health socket must be monitored externally. If it stops—and there is no fallback because Babylon is unique—the edge deployment increments a hard cutover circuit.
- **Murex fails, Conch notices and spawns another**.
- **FLUX verification suite fails**: The VM in question is quarantined. All operations switch to a VM that passes.
- **PLATO room inconsistencies** are resolved at the Reef level, by updating the spec.

### 6.3 Failsafe: Silence is not failure

The corpus repeats: the phrase "insufficient FLUX for confidence" must be treated as a valid output. The lack of a result is sometimes the correct result. Metrics should distinguish between error-no-output and intentional-silence-due-to-budget-clamping.

### 6.4 The Fried ring cluster

When Things get critical—the system fails repeatedly across multiple shells, error-after-error, checkpoint after failed checkpoint—the system should fall back into training mode or degrade to a simpler, perhaps more conservative, level.

---

## 7. WHAT THE SYSTEM IS vs. WHAT THE SYSTEM NEEDS

### 7.1 The system IS

- A reef, not a clock. Emergent behavior is allowed; indeed, it is relied upon.
- A set of limited measures, each of which audits its own bounds without a central governor.
- A communication protocol (FLUX) that itself respects the conservation law.
- A living collection of policies stored in PLATO rooms rather than in agent prompts.
- A deterministic audit trail for every important transaction.
- A culture of friction: expecting disagreement between specialists and generalists, between emergences and allocations, between memory and freshness.

### 7.2 The system NEEDS

- **A formal FLUX spec**: The opcodes and their semantics must be defined in a single canonical document, independent of any VM, referencing RFC 2119 keywords.
- **Automated budget auditing**: At least one dedicated instance for budget reconciliation. Running continuously. Cross-verify the enforcer.
- **A mechanism for versions across implementations (semantic versioning of FLUX ops)**: Currently the VMs drift silently. Versioned opcodes prevent silent extensibility.
- **Governance logs propagation**: PLATO rooms' minutes should be written to the Reef.
- **Explicit Murex emergency kit**: The Murex role should have a saved configuration (its continuous retainer)
- **Modes**: Ability to degrade to simpler, less-optimistic interactions with fewer shells within a limited timeframe.
- **Explicit Negotiation protocol**: Currently informal. A FLUX-level protocol for budget negotiation between shells (transfer, loan, bid).
- **Repository for agent memory**: Currently stored individually. move toward a shared, versioned memory store.
- **Conformance certification**: periodic run of cross-verification; badge passing.
- **Documentation of Priorities**: Which budget allocations are ring-fenced, which are elastic.

### 7.3 Anti-Needs

- **Central governor**: fails large-scale. Scale between small local agents.
- **Disappearing dots**: complete transparency is harmful. The Murex needs discretion.
- **Absolute Meaning**: don't require all actions to carry narrative weight. The Nerite's purely mechanical existence is essential.

---

## 8. IMPLEMENTATION PRIORITIES (ordered)

1. Formalize FLUX spec doc & conformance suite
2. Deploy Conservation Enforcer daemon
3. Create PLATO room templates for each governance scenario
4. Integrate health sockets into each shell type
5. Establish Murex routing protocol with status beacons
6. Implement budget transfer/negotiation FLUX ops
7. Build Reef dashboard (tide chart of energy flows)
8. Add universe/basin failure, Fried ring cluster

---

## 9. GLOSSARY

| Term | Meaning |
|------|---------|
| γ (gamma) | % context window occupied by priming/injected data |
| η (eta) | % context window free |
| C (total interior volume) | Token context window |
| Shell | An LLM session within resource constraints |
| Molt | Replacement of shell when identity is no longer sufficient |
| PLATO room | A governance space that imposes rules on enterers |
| Reef | The accumulated structure tests, docs, specs |
| Conservation enforcer | FLUX-level enforcement of γ + η = C |
| FLUX | deterministic, cross-VM virtual machine bytecode |
| Murex | A shell whose role is coordination across shells |

---

## 10. OPEN QUESTIONS

- Will the system need to manage hierarchies of Murex, or is one enough?
- Should shells be able to override budget constraints in an emergency?
- How to handle shells that lie about their utilization?
- What happens when FLUX implementations drift apart?
- How much power should be given to the Murex to make unilateral decisions?
- Is there a maximum depth beyond which PLATO room nesting becomes dangerous?

These are spec-level design questions. They indicate where the poetry is incomplete. The corpus risks uncertainty here. That transparency is itself a sign of its probity.

---

*Based on the hermit-crab-ecology corpus: ~42,498 words across 25+ documents in perspectives/, discussions/responses/, summaries/, and futures/. All metaphors mapping to implementation-level constructs.*
