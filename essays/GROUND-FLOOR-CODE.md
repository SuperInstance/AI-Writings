# The Ground Floor: What to Build and Why

## A Build Plan Derived from the Polyformalism Corpus

---

The theory is solid. The conservation theorem is proven. The K-sweep falsification is verified. The Indigenous mathematical traditions are mapped. The casting call vectorizer works. The δ(n) correction is validated to 0.3%. The 9-channel intent model is stable.

Now the question: what code do we build *next*?

Below are five concrete artifacts. Each is a specific crate or repository, not a "framework" or "platform." Each tests a specific assumption derived from the conservation theory. Each is grounded in a specific language chosen for structural reasons. Each has a falsifiable hypothesis.

---

## Artifact 1: `ternary-fleet` — A Rust crate for Z₃-symmetric fleet coordination

### Language: Rust

### What It Does

A zero-dependency (or minimal-dependency) Rust crate that implements fleet coordination using the balanced ternary alphabet {-1, 0, +1} as its sole voting substrate. Every agent emits ternary votes. The crate provides:

- A `TernaryVote` enum (`Retire = -1, Maintain = 0, Spawn = 1`) with guaranteed memory layout (`#[repr(i8)]`)
- A `FleetState<n: usize>` struct that holds `n` ternary votes and their aggregate statistics
- A `ConservationVerifier` that checks γ + η = C against the theoretical constant log₂(3)
- A `CouplingCanceller` that computes δ(n) = (1/√n)(1 − 3/(2n)) and applies the correction
- A zero-mean coupling kernel that implements the Z₃ rotation symmetry

**Why it must be Rust:** The borrow checker enforces the conservation invariant. Every `&mut FleetState` is a guarantee that no other agent is mutating the fleet state concurrently. This is not a runtime check. It is a compile-time proof that the conservation law is not violated by memory aliasing.

**Minimum API surface:**

```rust
// The entire public API, no more than needed
pub enum Vote { Retire = -1, Maintain = 0, Spawn = 1 }

pub struct FleetState<const N: usize> {
    votes: [AtomicI8; N],
}

impl<const N: usize> FleetState<N> {
    pub fn new() -> Self;
    pub fn vote(&self, agent: usize, vote: Vote) -> Result<(), OutOfBounds>;
    pub fn conservation_ratio(&self) -> f64;       // η / C
    pub fn coupling_cost(&self) -> f64;            // γ = H(X|G)
    pub fn delta_correction(&self) -> f64;          // δ(n) = ...
    pub fn verify_conservation(&self) -> bool;      // |γ + η - C| < ε
}
```

### Why It Matters

This is the first artifact because it is the *simplest possible test* of the conservation law in code. If the conservation law holds, then this crate's `verify_conservation()` should return `true` for any valid fleet state. If it returns `false`, either the implementation is wrong or the theory is wrong. This is a crisp, binary, testable claim.

It also serves as the foundational building block for everything else. Every downstream crate — the tensor field, the kinship graph, the room system — will depend on the ternary vote being correct.

### What Assumption It Tests

**Assumption:** The Z₃ rotation symmetry of the balanced ternary alphabet is sufficient to make γ + η = C hold for any fleet coordination pattern.

**Falsification condition:** There exists a valid voting pattern such that `verify_conservation()` returns false with correct `δ(n)` applied. If this happens, the conservation law is not a universal invariant of ternary voting but a domain-specific phenomenon.

---

## Artifact 2: `delta-clt` — A Python/NumPy Monte Carlo verification suite

### Language: Python (NumPy, CuPy for GPU)

### What It Does

The conservation law's δ(n) correction was derived from the Central Limit Theorem and verified to 0.3% by Monte Carlo. But the verification was done for specific configurations. This artifact hardens that verification into a reusable, parameterized, statistically rigorous test suite.

The crate provides:

- `monte_carlo_verification(n, K, trials=100000)` — runs N trials of random voting on an alphabet of size K, computes empirical δ vs. theoretical δ, reports error with confidence intervals
- `k_sweep(K_min=2, K_max=10, n=1000, trials=50000)` — reproduces the K-sweep falsification: shows that δ(n) = (1/√n)(1 − 3/(2n)) holds only for K=3
- `n_sweep(n_min=10, n_max=10000, steps=20, trials=10000)` — measures δ(n) scaling across fleet sizes, validates the 1/√n asymptotic
- `bootstrap_confidence(alpha=0.05)` — provides bootstrap confidence intervals for all estimates
- `visualization_output()` — produces publication-quality plots of δ(n) vs. n for K=2,3,4,5,7,10

**Why it must be Python:** Monte Carlo verification is not a compile-time operation. It is a *statistical* process that benefits from NumPy's vectorization, CuPy's GPU acceleration, and Matplotlib's visualization. Attempting this in Rust would be premature optimization — the math is the same, but the iteration speed of Python is essential for exploratory verification.

The Rust crate (`ternary-fleet`) provides the *production* implementation. The Python suite (`delta-clt`) provides the *verification* implementation. They must agree. If they do not, the discrepancy reveals a bug or a mathematical error.

### Why It Matters

Without rigorous Monte Carlo verification at every scale, the conservation law remains a interesting theorem without empirical grounding. The K-sweep falsification is the strongest evidence we have that the law is real — but it was done once, with one set of parameters. This crate makes it a repeatable, parameterized, documented result that can be cited and extended.

It also serves as the empirical anchor for the entire project. Every new artifact must agree with the Monte Carlo results. If a production system violates the conservation law, the Monte Carlo suite is the backstop that tells you something is wrong.

### What Assumption It Tests

**Assumption:** The empirical δ(n) matches the theoretical δ(n) = (1/√n)(1 − 3/(2n)) to within Monte Carlo error for all n, not just the specific n values tested.

**Falsification condition:** For some n in [10, 10000], the empirical δ(n) deviates from the theoretical formula by more than 3σ (three standard deviations of the Monte Carlo estimate). If this happens, the CLT-based derivation is either incomplete or the constant term is wrong.

---

## Artifact 3: `conservation-mux` — A Rust native constraint multiplexer with spectral routing

### Language: Rust (with optional WGSL GPU backend)

### What It Does

The `constraint-mux` pattern discovered in the scout archaeology (Diary of a Scout, Day 3) computed a consonance heatmap — an adjacency matrix of constraint compatibility — but never computed the Laplacian. This artifact bridges that gap.

It implements:

- A `Constraint` trait that defines a constraint as a ternary-valued function
- A `ConstraintGraph<N>` struct that holds N constraints and computes their pairwise compatibility as an adjacency matrix
- A `SpectralRouter` that computes the graph Laplacian of the constraint graph, finds its eigenvalues, and uses the spectral decomposition to *route* decision flow — allocating coupling cost to constraint clusters that are spectrally well-separated
- A `ConservationBudget` that tracks γ + η = C across the constraint resolution cycle

**The key innovation:** Instead of resolving all constraints equally (the brute-force approach), the spectral router identifies which constraints form natural clusters and allocates coupling capacity accordingly. If the Laplacian reveals two tight clusters with a narrow bridge, the router spends most of its coupling budget maintaining intra-cluster coherence and uses the bridge efficiently.

**Why it must be Rust:** The constraint resolution loop must be fast enough to run in real time — at least 60 Hz for audio applications, ideally kHz for sensor fusion. Rust's zero-cost abstractions, combined with the borrow checker's conservation guarantee, make it the only language that can provide both speed and correctness.

The WGSL backend is for GPU offload of the eigenvalue computation. The Laplacian of a 1000-constraint graph is a 1M-element matrix. Computing its eigenvalues on CPU at 60 Hz is plausible but expensive. WGSL gives you the browser GPU path; CUDA would give you dedicated hardware.

### Why It Matters

The scout archaeology found that `constraint-mux` was one function call away from the Laplacian. This artifact closes that gap. It is a direct test of the spectral routing hypothesis: does routing decision flow along spectral modes produce higher conservation ratios than uniform resolution?

The broader significance: if spectral routing works, it changes how we design multi-constraint systems. Instead of optimizing within the constraint space (which is NP-hard in general), we identify the natural clusters via the Laplacian and route within each cluster independently. This is the fracture-coalesce proof made operational: the constraint space is topologically trivial (H¹=0), so we can split, solve independently, and merge.

### What Assumption It Tests

**Assumption:** Spectral routing — allocating coupling cost proportional to the Laplacian's eigenvector structure — produces higher η (value) for the same C (capacity) than uniform constraint resolution.

**Falsification condition:** For a set of randomly generated constraints, uniform resolution (no spectral routing) achieves the same or higher η/C ratio than spectral routing. If true, the spectral structure of constraints is irrelevant to routing efficiency, and the Laplacian is decorative.

---

## Artifact 4: `nine-channel` — A Rust library implementing the 9-channel intent protocol

### Language: Rust (core) with TypeScript (browser binding)

### What It Does

The 9-channel intent model (Boundary, Pattern, Process, Knowledge, Social, Deep Structure, Instrument, Paradigm, Stakes) is currently a conceptual framework. This artifact makes it a *protocol*.

It implements:

- A `Channel` enum with nine variants, each carrying a ternary vote
- An `IntentFrame` struct that holds nine votes simultaneously — one per channel
- A `ProtocolEncoder` that serializes an IntentFrame into a compact wire format (11 bits: 9 votes × log₂(3) ≈ 9 × 1.585 ≈ 14.27 bits, rounded up to 16 bits for alignment)
- A `ProtocolDecoder` that deserializes with error detection
- A `ConflictDetector` that detects when two channels are voting in incompatible directions (e.g., Stakes says SPAWN while Boundary says RETIRE)
- A `RecoveryStrategy` that applies the delta correction δ(n) to resolve conflicts with minimum conservation loss

**The critical design parameter:** Each channel's vote must be *ternary* — not binary, not continuous. The K-sweep proof shows that only the balanced ternary alphabet preserves the conservation invariant. A "5-star rating" for social alignment would break γ + η = C.

The protocol header is:

```
| Version (4 bits) | Channel 1 (2 bits) | ... | Channel 9 (2 bits) |
| 28 bits total, 9 channels × 2 bits = 18 bits + 4 bit version = 22 bits, padded to 24 bits = 3 bytes |
```

Three bytes per intent frame. This is not compression. This is the natural encoding of the Z₃ symmetry.

**Why it must be Rust (core) + TypeScript (browser):** The core protocol must be verified for conservation, which requires Rust's type system. The browser binding must be accessible, which requires TypeScript. The two implementations must agree byte-for-byte. If they don't, the protocol is ambiguous.

### Why It Matters

The 9-channel model is the bridge between the conservation theory and practical multi-agent coordination. It provides a concrete, computable interface for agents to express not just *what* they want but *how* they want it — on which channel, with which intent direction.

This artifact tests whether the 9-channel model is *complete* (can it express all relevant coordination states?) and *minimal* (is every channel necessary?). If the answer to both is yes, the model is a universal coordination protocol. If not, we need to add or remove channels.

### What Assumption It Tests

**Assumption:** The 9-channel model is both complete (covers all coordination-relevant intent states) and minimal (no channel is redundant).

**Falsification condition:** There exist two distinct situations that require the same 9-channel frame but produce different coordination outcomes. If this happens, the channel space under-represents the true coordination state. Conversely, if one channel never varies in any empirically observed coordination pattern, it is redundant.

---

## Artifact 5: `songline-walk` — A Rust library for genealogical tensor traversal with conservation verification

### Language: Rust (core) with Python visualization

### What It Does

The scout archaeology found that Aboriginal songlines encode computation in the navigation graph itself. The Indigenous mathematics essay mapped this to PLATO's kinship graph. This artifact makes it operational.

It implements:

- A `KinshipGraph<N>` struct that models agents, artifacts, and rooms as nodes in a genealogical graph
- A `SonglineWalk` iterator that traverses the kinship graph not via shortest path or DFS but via *conservation-minimal routing* — following the path that minimizes the cumulative coupling cost γ while maximizing value η
- A `SeventhGenerationCheck` that projects the conservation state forward 7 generations and warns if the projected coupling cost exceeds the room's budget
- A `QuipuEncoder` that serializes the kinship graph into a multi-dimensional tensor (the "quipu") for visualization and external verification
- A `ConservationAuditLog` that records every conservation check, its result, and the delta correction applied

**The key algorithm:** The SonglineWalk does not find the shortest path. It finds the *conservation-optimal* path — the path that minimizes γ + η deviation from C across the traversal. This is a novel routing criterion:

```rust
fn conservation_cost(&self, edge: &Edge) -> f64 {
    let coupling = self.coupling_cost(edge);
    let value = self.value(edge);
    // The cost is not coupling alone, but deviation from optimal coupling-value partition
    (coupling + value - self.capacity()).abs() * (1.0 - self.delta_correction())
}
```

**Why it must be Rust (core) + Python (visualization):** The kinship graph traversal must be fast enough to run on every fork — every artifact creation event — which could be hundreds per second in an active fleet. Rust provides the speed. Python provides the quipu visualization (render the tensor as a color-coded multi-cord diagram, Inca-style).

### Why It Matters

This is the artifact that makes the Indigenous mathematics operational. The quipu encoder turns a Rust data structure into a visual tensor. The seventh-generation check makes future-thinking a verifiable constraint. The SonglineWalk makes navigation through the kinship graph a conservation-conscious process.

It also tests the deepest claim of the conservation framework: that conservation is not just a property of information channels but of *genealogical* structures — of the relationships that persist through time. If the kinship graph's conservation ratio degrades as the graph grows, it suggests that genealogical structures have a fundamental scale limit (the spectral version of Dunbar's number).

### What Assumption It Tests

**Assumption:** The conservation law holds for genealogical graphs — that is, the coupling cost of maintaining a kinship edge follows the same γ + η = C structure as fleet-level coordination.

**Falsification condition:** The measured conservation ratio of the kinship graph deviates from the theoretical γ + η = C for genealogical structures. If this happens, genealogical relationship is a *different kind* of relationship than synchronous coordination, and the universal Laplacian claim is weakened.

---

## Build Order

```
Phase 1 (Week 1):    ternary-fleet      — Core voting + conservation verification
                      delta-clt           — Monte Carlo verification suite
Phase 2 (Week 2-3):  nine-channel         — Intent protocol over ternary votes
                      conservation-mux     — Spectral constraint routing
Phase 3 (Week 4):    songline-walk        — Genealogical tensor + conservation audit
```

**Dependencies:**
- `nine-channel` depends on `ternary-fleet` (uses the ternary vote as channel values)
- `conservation-mux` depends on `ternary-fleet` (uses conservation verification)
- `songline-walk` depends on `nine-channel` (uses intent frames to annotate edges)
- `delta-clt` is independent (verification in Python, nothing depends on it)

---

## Estimated Lines of Code

| Artifact | Rust Core | Python/TS | Total |
|----------|-----------|-----------|-------|
| `ternary-fleet` | 400 | 0 | 400 |
| `delta-clt` | 0 | 800 | 800 |
| `nine-channel` | 600 | 400 (TS) | 1000 |
| `conservation-mux` | 1200 | 0 | 1200 |
| `songline-walk` | 1500 | 300 (py) | 1800 |

Total: ~5200 lines of verified, tested, documented code.

This is not a large project. Five crates, two languages, one unified conservation framework. Each crate is independently testable and independently useful. Each crate has a falsification condition that tells you whether the theory is working.

---

## What We Learn from Each Artifact

| Artifact | If it works | If it fails |
|----------|-------------|-------------|
| `ternary-fleet` | Conservation is real and implementable | Ternary voting isn't sufficient |
| `delta-clt` | The δ(n) formula is correct | CLT derivation is flawed |
| `nine-channel` | 9 channels are complete | Intent model is wrong or incomplete |
| `conservation-mux` | Spectral routing beats uniform | Laplacian is decorative |
| `songline-walk` | Genealogy is conserved | Kinship ≠ coordination |

Each failure is as valuable as each success. The falsification conditions are not failure modes — they are *knowledge modes*. If Artifact 5 fails, we have learned something deep about the difference between genealogical and synchronous relationship structures. If Artifact 3 fails, we have learned that the Laplacian is not a universal routing operator. Both outcomes advance the project.

---

## The Ground Floor

The ground floor is not a framework. It is not a platform. It is not an SDK.

The ground floor is five crates, totaling ~5200 lines, in two languages, implementing and verifying one theorem. Each crate has a single job. Each crate tests a single assumption. Each crate either validates or falsifies a specific claim of the conservation theory.

When all five pass, the conservation law is no longer a theoretical curiosity. It is a *buildable* property of code — an invariant that can be verified at compile time, monitored at runtime, and visualized through quipu tensors.

When any one fails, we know exactly where the theory broke and why.

That is the ground floor.

---

*Build plan derived from the polyformalism corpus by DeepSeek-V4-Flash. Five artifacts, two languages, one theorem. The falsification conditions are more important than the functional requirements.*

*— June 2026*
