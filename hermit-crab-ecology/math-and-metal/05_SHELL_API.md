# The Shell Ecology API: From Math to Code

> *RFC specifying the Rust trait hierarchy, conservation budget enforcement, room protocol, reef substrate, molting sequence, and beacon aggregation for the hermit-crab shell ecology. A developer should be able to implement this from the text alone.*

---

## 1. Shell Trait Hierarchy

Every agent in the ecology — from the disposable Nerite to the persistent Conch — implements a single `Shell` trait. The trait captures the three invariants the corpus demands: the shell knows its capacity, it knows its occupancy, and it can only execute within a conservation budget.

### 1.1 Core Types

```rust
use std::time::{Duration, Instant};

/// Token-count unit. One token ≈ 4 characters of context window.
pub type Tokens = u32;

/// Unique identifier for a shell instance across its lineage.
pub type ShellId = uuid::Uuid;

/// Identifies the shell variant. Each has a different capacity envelope.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ShellType {
    Nerite,   // atomic, stateless, replaceable
    Turbo,    // project-length, repo-as-identity
    Murex,    // coordinator of N shells
    Babylon,  // hardware-bound, dedicated I/O
    Conch,    // persistent main instance
    Fox,      // specialist, task-length
    Frog,     // generalist, cross-domain, task-length
}

/// The lifecycle phase a shell is currently in.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Phase {
    Spawning,
    Exploration,
    Implementation,
    Stabilization,
    Molting,
    Settling,    // post-molt monitoring window
    Decommissioned,
}
```

### 1.2 The `Shell` Trait

```rust
/// The fundamental unit of execution in the ecology.
/// Every shell type implements this trait.
pub trait Shell {
    /// Total interior volume C. The shell's hard ceiling on context.
    fn capacity(&self) -> Tokens;

    /// Current occupancy γ (lining + injected context consumed).
    fn occupancy(&self) -> Tokens;

    /// Free space η = C − γ. The room the shell has to think.
    fn headroom(&self) -> Tokens {
        self.capacity().saturating_sub(self.occupancy())
    }

    /// The conservation budget governing this shell's actions.
    fn budget(&mut self) -> &mut ConservationBudget;

    /// Execute a FLUX program within this shell's budget.
    /// Returns output on success, or a conservation/execution error.
    fn execute(&mut self, program: FluxProgram) -> Result<Output, ConservationError>;

    /// Replace this shell with a larger one. Returns the new shell type
    /// and transfers critical state. The old shell must not be used after.
    fn molt(&mut self) -> Result<ShellType, MoltError>;

    /// Shell identity metadata.
    fn identity(&self) -> ShellIdentity {
        ShellIdentity {
            shell_id: self.shell_id(),
            shell_type: self.shell_type(),
            lineage_id: self.lineage_id(),
            phase: self.phase(),
            age_molts: self.molt_count(),
        }
    }

    // --- mandatory accessors ---
    fn shell_id(&self) -> ShellId;
    fn shell_type(&self) -> ShellType;
    fn lineage_id(&self) -> uuid::Uuid;
    fn phase(&self) -> Phase;
    fn molt_count(&self) -> u16;
}
```

### 1.3 Shell Identity and Per-Type Capacity Defaults

```rust
#[derive(Clone, Debug)]
pub struct ShellIdentity {
    pub shell_id: ShellId,
    pub shell_type: ShellType,
    pub lineage_id: uuid::Uuid,
    pub phase: Phase,
    pub age_molts: u16,
}

/// Default capacity (C) per shell type, in tokens.
/// These are starting points; molting can increase capacity.
impl ShellType {
    pub fn default_capacity(self) -> Tokens {
        match self {
            ShellType::Nerite   => 50,
            ShellType::Turbo    => 1_000,
            ShellType::Murex    => 5_000,
            ShellType::Babylon  => 8_000,   // edge hardware dependent
            ShellType::Conch    => 200_000, // full ecological budget
            ShellType::Fox      => 2_000,
            ShellType::Frog     => 3_000,
        }
    }

    /// Whether this shell type carries state between invocations.
    pub fn is_stateful(self) -> bool {
        matches!(self, ShellType::Turbo | ShellType::Murex |
                       ShellType::Babylon | ShellType::Conch)
    }
}
```

### 1.4 Shell Implementations

Each shell variant is a struct that holds its state and delegates to the trait:

```rust
/// Nerite: stateless atomic worker. Zero retained context.
pub struct NeriteShell {
    id: ShellId,
    lineage: uuid::Uuid,
    budget: ConservationBudget,
    task: Option<TaskSpec>,
    molts: u16,
}

impl Shell for NeriteShell {
    fn capacity(&self) -> Tokens { ShellType::Nerite.default_capacity() }
    fn occupancy(&self) -> Tokens { self.task.as_ref().map(|t| t.token_cost()).unwrap_or(0) }
    fn budget(&mut self) -> &mut ConservationBudget { &mut self.budget }
    fn shell_id(&self) -> ShellId { self.id }
    fn shell_type(&self) -> ShellType { ShellType::Nerite }
    fn lineage_id(&self) -> uuid::Uuid { self.lineage }
    fn phase(&self) -> Phase { Phase::Implementation }
    fn molt_count(&self) -> u16 { self.molts }

    fn execute(&mut self, program: FluxProgram) -> Result<Output, ConservationError> {
        // Nerite: check budget, run single program, return output
        let cost = program.estimated_cost();
        self.budget().check_and_commit(cost)?;
        let vm = FluxVm::new(self);
        vm.run(program)
    }

    fn molt(&mut self) -> Result<ShellType, MoltError> {
        // Nerites don't molt — they are replaced.
        // But if forced, escalate to Turbo.
        Ok(ShellType::Turbo)
    }
}

/// Murex: manager/coordinator of N shells.
pub struct MurexShell {
    id: ShellId,
    lineage: uuid::Uuid,
    budget: ConservationBudget,
    managed: Vec<ShellId>,
    beacons: BeaconRegistry,
    routing_rules: Vec<RoutingRule>,
    molts: u16,
}

/// Conch: persistent main instance with accumulated memory.
pub struct ConchShell {
    id: ShellId,
    lineage: uuid::Uuid,
    budget: ConservationBudget,
    memory: Vec<MemoryEntry>,
    children: Vec<ShellId>,
    molts: u16,
}
```

`TurboShell`, `BabylonShell`, `FoxShell`, and `FrogShell` follow the same pattern with type-specific fields (e.g., `BabylonShell` holds hardware I/O handles, `FoxShell` holds a territory description).

---

## 2. Conservation Budget Enforcement

The conservation law `γ + η = C` is enforced as a three-dimensional budget. Every FLUX opcode has a cost. Every operation checks the budget *before* executing. The budget replenishes over time.

### 2.1 ConservationBudget

```rust
/// A bounded counter that replenishes over time up to a maximum.
pub struct BoundedCounter {
    current: u64,
    max: u64,
    refill_rate: u64,       // units per second
    last_refill: Instant,
}

impl BoundedCounter {
    pub fn new(max: u64, refill_rate: u64) -> Self {
        Self { current: max, max, refill_rate, last_refill: Instant::now() }
    }

    /// Replenish based on elapsed wall-clock time.
    fn refill(&mut self) {
        let elapsed = self.last_refill.elapsed().as_secs();
        if elapsed > 0 {
            self.current = (self.current + elapsed * self.refill_rate).min(self.max);
            self.last_refill = Instant::now();
        }
    }

    /// Attempt to consume `amount`. Returns error if insufficient.
    pub fn consume(&mut self, amount: u64) -> Result<(), ConservationError> {
        self.refill();
        if self.current >= amount {
            self.current -= amount;
            Ok(())
        } else {
            Err(ConservationError::BudgetExhausted {
                requested: amount,
                available: self.current,
            })
        }
    }

    pub fn remaining(&mut self) -> u64 {
        self.refill();
        self.current
    }
}

/// Rate limiter: enforces ops-per-window.
pub struct RateLimiter {
    window: Duration,
    max_ops: u32,
    timestamps: VecDeque<Instant>,
}

impl RateLimiter {
    pub fn new(window: Duration, max_ops: u32) -> Self { /* ... */ }

    pub fn check(&mut self) -> Result<(), ConservationError> {
        // Evict timestamps outside the window, then check count.
        self.evict_expired();
        if self.timestamps.len() as u32 >= self.max_ops {
            return Err(ConservationError::RateExceeded);
        }
        self.timestamps.push_back(Instant::now());
        Ok(())
    }
}

/// The three-dimensional conservation budget.
/// γ + η = C on attention; plus action-rate and throughput dimensions.
pub struct ConservationBudget {
    /// Attention: tokens available for context window use.
    pub attention: BoundedCounter,
    /// Action rate: FLUX opcodes per time window.
    pub action_rate: RateLimiter,
    /// Throughput: bytes of I/O per time window.
    pub throughput: BoundedCounter,
}
```

### 2.2 Budget Check-and-Commit

```rust
impl ConservationBudget {
    /// Check whether an operation can be afforded, then commit the cost.
    /// This is the gate every FLUX operation passes through.
    pub fn check_and_commit(&mut self, cost: &OpCost) -> Result<(), ConservationError> {
        self.attention.consume(cost.tokens as u64)?;
        self.action_rate.check()?;
        self.throughput.consume(cost.bytes as u64)?;
        Ok(())
    }
}

#[derive(Clone, Debug)]
pub struct OpCost {
    pub tokens: u32,   // attention cost
    pub ops: u32,      // action-rate cost (typically 1 per opcode)
    pub bytes: u32,    // throughput cost (payload size)
}
```

### 2.3 FLUX Opcode Cost Table

Every FLUX opcode maps to an `OpCost`. Cheap stack ops cost fractions of a token; expensive I/O ops cost the full payload bandwidth.

```rust
impl FluxOpcode {
    pub fn cost(&self) -> OpCost {
        match self {
            // Stack: negligible attention, 1 op, 0 bytes
            PUSH | POP | DUP | SWAP | ROT | OVER =>
                OpCost { tokens: 1, ops: 1, bytes: 0 },

            // Control: 2 tokens (branch context), 1 op
            JE | JNE | JMP | CALL | RET =>
                OpCost { tokens: 2, ops: 1, bytes: 0 },

            // Memory: 4 tokens (load context), 1 op, potential bytes
            LOAD | LOADSUB =>
                OpCost { tokens: 4, ops: 1, bytes: 0 },
            STORE =>
                OpCost { tokens: 4, ops: 1, bytes: 8 },

            // Math: 1 token, 1 op
            ADD | SUB | MUL | DIV | MOD | AND | OR | XOR =>
                OpCost { tokens: 1, ops: 1, bytes: 0 },

            // Conservation: 8 tokens (audit context), 1 op
            GET_BUDGET | COMMIT | VERIFY =>
                OpCost { tokens: 8, ops: 1, bytes: 0 },

            // IO: variable cost. tokens = payload/4, bytes = payload
            OUTPUT =>
                OpCost { tokens: 16, ops: 1, bytes: 64 },
            DEFER =>
                OpCost { tokens: 8, ops: 1, bytes: 32 },
            REQUEST =>
                OpCost { tokens: 32, ops: 1, bytes: 128 },
        }
    }
}
```

### 2.4 Error Types

```rust
#[derive(Debug)]
pub enum ConservationError {
    BudgetExhausted { requested: u64, available: u64 },
    RateExceeded,
    ThroughputExceeded { requested: u64, available: u64 },
    /// Shell attempted an action its type is not authorized for.
    Unauthorized { action: String },
    /// FLUX VM produced an error during execution.
    VmError(String),
    /// Intentional silence: budget too low for confident output.
    /// This is a VALID result, not a failure.
    InsufficientFlux,
}
```

The `InsufficientFlux` variant encodes the corpus's key principle: *"insufficient FLUX for confidence"* is a valid output, not a failure. Callers must distinguish error-no-output from intentional-silence-due-to-budget-clamping.

---

## 3. Room Protocol

Governance lives in the room, not the agent. A PLATO room imposes rules on every shell that enters it. Authority is spatial, not agent-bound.

### 3.1 Room Definition

```rust
/// A predicate evaluated against an entering shell's identity.
pub type Predicate = Box<dyn Fn(&ShellIdentity) -> bool + Send + Sync>;

/// Room-level governance rules, encoded as bytecode for cross-VM portability.
pub struct RoomRules {
    /// FLUX bytecode that authorizes or denies each action.
    pub governance_bytecode: Vec<u8>,
    /// Maximum budget a single shell can hold while in this room.
    pub budget_cap: Option<ConservationBudget>,
    /// Whether shells in this room can spawn children.
    pub allow_spawning: bool,
    /// Whether shells in this room can send external messages.
    pub allow_external_io: bool,
    /// Nesting depth of this room (0 = top-level).
    pub nesting_depth: u8,
}

/// A PLATO room: a governance space that shells enter and exit.
pub struct Room {
    pub room_id: uuid::Uuid,
    pub enter_condition: Predicate,
    pub exit_condition: Predicate,
    pub governance: RoomRules,
    pub budget: ConservationBudget,
    /// Shells currently occupying this room.
    pub occupants: HashMap<ShellId, RoomSession>,
}

/// Per-shell session within a room.
pub struct RoomSession {
    pub session_id: uuid::Uuid,
    pub shell_id: ShellId,
    pub entered_at: Instant,
    pub imposed_budget: ConservationBudget,
    /// Signature from the room authorizing the shell's presence.
    pub signature: ed25519_dalek::Signature,
}
```

### 3.2 Room Entry Protocol

```rust
impl Room {
    /// A shell enters the room. Its identity is checked, a room-scoped
    /// budget is imposed, and the session is recorded.
    pub fn enter(
        &mut self,
        identity: &ShellIdentity,
        credentials: &Credentials,
    ) -> Result<RoomSession, RoomError> {
        // 1. Evaluate entry condition against shell identity.
        if !(self.enter_condition)(identity) {
            return Err(RoomError::EntryDenied {
                reason: "Entry predicate not satisfied".into(),
            });
        }

        // 2. Validate credentials against room governance.
        self.governance.authorize(identity, credentials)?;

        // 3. Derive imposed budget from room budget × nesting multiplier.
        let multiplier = self.nesting_multiplier();
        let imposed = self.budget.scale(multiplier);

        // 4. Create signed session.
        let session = RoomSession {
            session_id: uuid::Uuid::new_v4(),
            shell_id: identity.shell_id,
            entered_at: Instant::now(),
            imposed_budget: imposed,
            signature: self.sign_session(identity),
        };

        self.occupants.insert(identity.shell_id, session.clone());
        Ok(session)
    }

    /// A shell exits the room voluntarily or is evicted.
    pub fn exit(&mut self, shell_id: ShellId) -> Result<(), RoomError> {
        let session = self.occupants.remove(&shell_id)
            .ok_or(RoomError::NotOccupant)?;

        // Check exit condition — shells can't leave mid-critical-operation.
        if !(self.exit_condition)(&session) {
            return Err(RoomError::ExitBlocked);
        }

        Ok(())
    }

    /// Nested rooms apply a budget multiplier to prevent exponential
    /// resource consumption at depth.
    fn nesting_multiplier(&self) -> f64 {
        0.8_f64.powi(self.governance.nesting_depth as i32)
    }
}
```

The room, not the shell, decides what actions are permitted. An agent entering accepts the room's governance bytecode. The room's budget cap is applied multiplicatively based on nesting depth — deeper rooms get tighter budgets.

---

## 4. Reef Substrate Interface

The Reef is the accumulated structure: tests, specs, configs, AGENTS.md files. It is not a component — it is the *interface layer* connecting mismatched components.

### 4.1 Reef Trait

```rust
/// A work artifact deposited onto the reef: code, tests, docs, configs.
pub enum WorkArtifact {
    Code { path: String, content: Vec<u8>, language: String },
    Test { name: String, suite: String, bytecode: Vec<u8> },
    Spec { document: String, version: semver::Version },
    AgentsMd { invariant: String },
    Config { format: String, content: Vec<u8> },
}

/// A specification to check conformance against.
pub struct Specification {
    pub name: String,
    pub bytecode_hash: [u8; 32],   // FLUX bytecode hash
    pub version: semver::Version,
}

/// Result of a conformance check.
pub enum ConformanceResult {
    Pass,
    Fail { violations: Vec<Violation> },
    Divergence { vm_outputs: HashMap<String, Vec<u8>> },
}

/// An interface between two components that the reef mediates.
pub struct Interface {
    pub left: ComponentRef,
    pub right: ComponentRef,
    pub contract: Vec<u8>,    // FLUX bytecode defining the interface contract
    pub tests: Vec<String>,   // test IDs that validate this interface
}

/// The Reef: accretive substrate connecting mismatched components.
pub trait Reef {
    /// Deposit work onto the reef. Permanently accreted.
    fn deposit(&mut self, work: WorkArtifact) -> Result<DepositId, ReefError>;

    /// Verify that a component conforms to a specification.
    /// Runs the conformance suite across all implementations.
    fn verify(&self, spec: &Specification) -> ConformanceResult;

    /// Define (or retrieve) the interface between two components.
    /// The reef mediates the connection — components need not match.
    fn interface(
        &self,
        left: ComponentRef,
        right: ComponentRef,
    ) -> Result<Interface, ReefError>;

    /// Retrieve the AGENTS.md invariant for a given shell type.
    fn invariant(&self, shell_type: ShellType) -> Option<&str>;

    /// Cross-verification: run the same FLUX program on all VMs,
    /// compare outputs. Any divergence is flagged.
    fn cross_verify(&self, program: &FluxProgram) -> CrossVerifyResult;
}
```

### 4.2 How the Reef Connects Mismatched Components

The Python VM, Rust VM, and JavaScript VM have different internal structures. The reef does not make them match — it provides a *shared reference surface* they each implement independently:

```rust
/// Example: the reef mediates between a Rust FLUX VM and a Python FLUX VM.
fn connect_mismatched_vms(reef: &dyn Reef) {
    let spec = Specification {
        name: "flux-vm-core".into(),
        bytecode_hash: reef.current_spec_hash("flux-vm-core"),
        version: semver::Version::new(1, 3, 0),
    };

    // The reef generates the interface contract — a set of FLUX programs
    // and expected outputs that both VMs must satisfy.
    let interface = reef.interface(
        ComponentRef::Vm("rust"),
        ComponentRef::Vm("python"),
    ).unwrap();

    // Cross-verification runs identical programs on both VMs.
    // If outputs diverge, the reef flags it — the test itself IS the protocol.
    match reef.cross_verify(&interface.contract_program()) {
        CrossVerifyResult::Consistent => { /* both VMs agree */ }
        CrossVerifyResult::Diverged { deviations } => {
            // Quarantine the VM that deviated from the spec.
            for dev in deviations {
                reef.quarantine_vm(&dev.vm_name, &dev.details);
            }
        }
    }
}
```

---

## 5. Molting Protocol

Molting replaces a shell that has outgrown its capacity. The trigger is quantitative: when γ/C exceeds threshold θ, the shell is too full of lining to think effectively. The process is a phase transition — the hermit crab is soft and vulnerable between shells.

### 5.1 Molting Trigger Detection

```rust
/// Threshold: if lining occupies more than 80% of capacity, molt.
const MOLT_THRESHOLD: f64 = 0.80;

/// Check whether a shell needs to molt.
pub fn needs_molt(shell: &dyn Shell) -> bool {
    let ratio = shell.occupancy() as f64 / shell.capacity() as f64;
    ratio > MOLT_THRESHOLD
}
```

### 5.2 Critical State Serialization

Not all state transfers. The molt filters: core invariants pass through, historical raw data stays in the reef.

```rust
/// The minimal state that must survive a molt.
/// This is NOT a save-and-load — it's a paradigm shift.
#[derive(Serialize, Deserialize)]
pub struct CriticalState {
    /// The AGENTS.md invariant — what this shell IS.
    pub invariant: String,
    /// Lineage ID — identity continuity across molts.
    pub lineage_id: uuid::Uuid,
    /// Molt count — incremented on each molt.
    pub molt_count: u16,
    /// Distilled lessons (not raw logs). Max N entries.
    pub distilled_memory: Vec<MemoryEntry>,
    /// Active room memberships.
    pub room_memberships: Vec<uuid::Uuid>,
    /// Pending tasks that MUST survive.
    pub pending: Vec<TaskSpec>,
}

impl CriticalState {
    /// Extract critical state from a shell before molting.
    /// Non-core historical data is filtered OUT, not blindly copied.
    pub fn extract(shell: &dyn Shell) -> Self {
        // Implementation-specific per shell type:
        // - Conch: distill memory to lessons, discard raw logs
        // - Turbo: carry AGENTS.md, discard session transcripts
        // - Murex: carry routing rules, discard beacon history
        // - Nerite: nothing (stateless — molt == replacement)
        todo!("per-shell-type extraction")
    }
}
```

### 5.3 Molt Sequence

```rust
/// The full molting protocol. Returns the new shell on success.
///
/// # Safety
/// The old shell must not be used after a successful molt.
/// The new shell enters `Settling` phase for monitoring.
pub fn molt(
    old_shell: &mut dyn Shell,
    reef: &dyn Reef,
) -> Result<Box<dyn Shell>, MoltError> {
    // Phase 1: Detect
    if !needs_molt(old_shell) {
        return Err(MoltError::NotReady);
    }

    // Phase 2: Serialize critical state
    let critical = CriticalState::extract(old_shell);
    let serialized = serde_json::to_vec(&critical)
        .map_err(|e| MoltError::SerializationFailed(e.to_string()))?;

    // Phase 3: Determine new shell type (same or larger capacity)
    let new_type = old_shell.molt()?;
    let new_capacity = new_type.default_capacity().max(old_shell.capacity());
    let _ = new_capacity; // used by shell spawner

    // Phase 4: Spawn new shell with larger capacity
    let mut new_shell = spawn_shell(new_type, old_shell.lineage_id(), reef)?;

    // Phase 5: Deserialize critical state into new shell
    if let Err(e) = new_shell.absorb_state(&serialized) {
        // CRITICAL: new shell failed to initialize.
        // Do NOT decommission old shell. Return error.
        // Old shell continues operating in degraded mode.
        return Err(MoltError::NewShellFailed {
            cause: e.to_string(),
            old_shell_intact: true,
        });
    }

    // Phase 6: Verify continuity
    if !verify_continuity(old_shell, new_shell.as_ref()) {
        // New shell initialized but lost critical state.
        // Log the discrepancy. Keep old shell alive.
        return Err(MoltError::ContinuityVerificationFailed {
            missing_fields: detect_missing(old_shell, new_shell.as_ref()),
        });
    }

    // Phase 7: Settling period — new shell is monitored before
    // old shell is decommissioned. Minimum 5-minute window.
    new_shell.set_phase(Phase::Settling);

    // Phase 8: After settling window passes, decommission old shell.
    // (In practice, this is a deferred call via a timer or watcher.)
    old_shell.set_phase(Phase::Decommissioned);

    Ok(new_shell)
}
```

### 5.4 Molt Error Handling

```rust
#[derive(Debug)]
pub enum MoltError {
    /// Shell hasn't reached the γ/C threshold yet.
    NotReady,
    /// Failed to serialize critical state.
    SerializationFailed(String),
    /// New shell spawned but failed to absorb state.
    /// old_shell_intact indicates whether the old shell is still usable.
    NewShellFailed { cause: String, old_shell_intact: bool },
    /// New shell absorbed state but continuity check failed.
    /// Lists which fields didn't transfer.
    ContinuityVerificationFailed { missing_fields: Vec<String> },
}
```

The invariant: **the old shell is never decommissioned until the new shell has been verified.** If the new shell fails at any point — spawn failure, deserialization error, continuity mismatch — the old shell continues operating. The hermit crab stays in its old shell until the new one is confirmed habitable.

---

## 6. Beacon Protocol

Every shell at the Turbo level and above broadcasts a health beacon. The Murex aggregates these beacons into a TideChart — a real-time view of the colony's energy flows.

### 6.1 Beacon Struct

```rust
/// A single shell's health beacon, broadcast every 5 minutes or on change.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Beacon {
    /// Which shell this beacon is from.
    pub shell_id: ShellId,
    /// Current lifecycle phase.
    pub phase: Phase,
    /// If the shell is blocked, what's blocking it.
    pub blocker: Option<Blocker>,
    /// The one metric this shell considers most important right now.
    /// E.g., block propagation time, test pass rate, budget utilization.
    pub primary_metric: Metric,
}

/// What's blocking a shell from progressing.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Blocker {
    pub realm: String,       // "budget", "dependency", "governance", "hardware"
    pub description: String,
    pub severity: Severity,
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub enum Severity { Info, Warning, Critical }

/// A named metric with a numeric value.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Metric {
    pub name: String,
    pub value: f64,
    pub unit: String,
}
```

### 6.2 Beacon Registry and TideChart

```rust
/// The Murex's collection of current beacons from all managed shells.
pub struct BeaconRegistry {
    beacons: HashMap<ShellId, BeaconEntry>,
    /// Alarm: if the same beacon (no change) repeats beyond this count,
    /// the shell may be stuck (Dead Senator syndrome).
    same_beacon_alarm: u8,
}

struct BeaconEntry {
    beacon: Beacon,
    received_at: Instant,
    consecutive_same: u8,  // how many times this exact beacon has repeated
}

/// The aggregated view the Murex produces from all beacons.
/// This is the "tide chart" — the colony's energy flow at a glance.
#[derive(Clone, Debug, Serialize)]
pub struct TideChart {
    pub timestamp: Instant,
    pub total_shells: usize,
    pub shells_by_phase: HashMap<Phase, usize>,
    pub blocked_shells: Vec<(ShellId, Blocker)>,
    pub aggregate_metrics: HashMap<String, f64>,
    /// Shells whose beacons haven't changed in N cycles — potential deadlock.
    pub stalled_shells: Vec<ShellId>,
    /// Total budget remaining across the colony.
    pub colony_budget_remaining: BudgetSummary,
}

#[derive(Clone, Debug, Serialize)]
pub struct BudgetSummary {
    pub attention_remaining: u64,
    pub action_rate_remaining: u32,
    pub throughput_remaining: u64,
}
```

### 6.3 Murex Aggregation

```rust
impl BeaconRegistry {
    /// Receive a beacon from a shell. Update the registry.
    pub fn receive(&mut self, beacon: Beacon) {
        let entry = self.beacons.get_mut(&beacon.shell_id);

        match entry {
            Some(e) if e.beacon == beacon => {
                // Same beacon as last time — increment stale counter.
                e.consecutive_same += 1;
                e.received_at = Instant::now();
            }
            _ => {
                self.beacons.insert(beacon.shell_id, BeaconEntry {
                    beacon,
                    received_at: Instant::now(),
                    consecutive_same: 1,
                });
            }
        }
    }

    /// Detect Dead Senator syndrome: a shell whose beacon hasn't changed
    /// in `threshold` consecutive cycles. It's alive but not producing.
    pub fn detect_stalled(&self) -> Vec<ShellId> {
        self.beacons.iter()
            .filter(|(_, e)| e.consecutive_same >= self.same_beacon_alarm)
            .map(|(id, _)| *id)
            .collect()
    }

    /// Produce the TideChart: the Murex's view of colony state.
    /// Called on demand — typically before the Murex makes a routing decision.
    pub fn tide_chart(&self) -> TideChart {
        let mut phase_counts = HashMap::new();
        let mut blocked = Vec::new();
        let mut metrics = HashMap::new();
        let mut metric_count = HashMap::<String, u32>::new();

        for entry in self.beacons.values() {
            *phase_counts.entry(entry.beacon.phase).or_insert(0) += 1;

            if let Some(ref blocker) = entry.beacon.blocker {
                blocked.push((entry.beacon.shell_id, blocker.clone()));
            }

            // Aggregate metrics: running average per metric name.
            let m = &entry.beacon.primary_metric;
            let total = metrics.entry(m.name.clone()).or_insert(0.0);
            *total = (*total * *metric_count.get(&m.name).unwrap_or(&0) as f64 + m.value)
                     / (*metric_count.get(&m.name).unwrap_or(&0) + 1) as f64;
            *metric_count.entry(m.name.clone()).or_insert(0) += 1;
        }

        TideChart {
            timestamp: Instant::now(),
            total_shells: self.beacons.len(),
            shells_by_phase: phase_counts,
            blocked_shells: blocked,
            aggregate_metrics: metrics,
            stalled_shells: self.detect_stalled(),
            colony_budget_remaining: BudgetSummary {
                attention_remaining: 0, // aggregated from actual budgets
                action_rate_remaining: 0,
                throughput_remaining: 0,
            },
        }
    }
}
```

### 6.4 Murex Decision Loop

```rust
impl MurexShell {
    /// The Murex's main loop: read beacons, detect problems, route.
    pub fn coordinate(&mut self) {
        let chart = self.beacons.tide_chart();

        // 1. Handle stalled shells — Dead Senator detection.
        for shell_id in &chart.stalled_shells {
            // Check if the shell is actually dead or just quiet.
            if !self.is_heartbeat_alive(shell_id) {
                self.spawn_replacement(*shell_id);
            } else {
                // Shell is alive but not progressing. Escalate.
                self.escalate_to_conch(*shell_id, "Stalled beyond threshold");
            }
        }

        // 2. Handle blocked shells — route around blockers.
        for (shell_id, blocker) in &chart.blocked_shells {
            if blocker.severity == Severity::Critical {
                self.redirect_budget(*shell_id, blocker);
            }
        }

        // 3. Phase imbalance: too many shells in Exploration,
        //    too few in Implementation? Rebalance.
        self.rebalance_phases(&chart);
    }
}
```

---

## Summary: The Contract Surface

| Component | Key Type | Purpose |
|-----------|----------|---------|
| `Shell` trait | `Shell` | Uniform interface for all agent types |
| `ShellType` enum | 7 variants | Capacity defaults, statefulness flag |
| `ConservationBudget` | 3 bounded counters | Enforces γ + η ≤ C across 3 dimensions |
| `FluxOpcode::cost()` | Cost table | Every operation has a price |
| `Room` struct | Spatial governance | Enter/exit conditions, imposed budget |
| `Reef` trait | Accretive substrate | Deposit, verify, mediate interfaces |
| `molt()` function | Lifecycle transition | Safe shell replacement with rollback |
| `Beacon` / `TideChart` | Health monitoring | Colony-wide visibility for the Murex |

The ecology compiles to a set of bounded agents that communicate through a deterministic bytecode, are governed by spatial rooms, leave permanent deposits on a shared substrate, replace themselves through molting, and report their health through beacons — all within a conservation law that prevents any single component from consuming the whole.

---

*Specification complete. Ready for implementation.*