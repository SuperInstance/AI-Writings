# THE NOCTURNE PROTOCOL
## SuperInstance: Merge Plan — July 2026 to December 2026
### Kimi + Claude, Synthesized. The Universe as Audience.

> *"We spent two rounds trying to build a machine that thinks. The merge realizes we were building a machine that *must think about itself*."*

---

## 0. What the Competition Forged

Round 1 produced two architectures: Kimi's Ternary Computation Fabric (prescriptive, bold, commercially sharp) and Claude's ConstraintNet (descriptive, geometrically rigorous, narratively unforgettable). Round 2 weaponized both: Kimi's EigenGenesis introduced the L3 generative loop — a system that births its own children. Claude's Curry-Howard conservation correspondence reframed the entire ecosystem as a linear logic proof assistant.

The judges called the merge: **"A self-extending, self-proving, conservation-bound mathematical organism that bills by the theorem."**

This document is that merge. But it is written by someone who has read the obituary in advance.

---

## 1. The Unified Architecture: The Nocturne Stack

### 1.1 The Synthesis Principle

Kimi's insight: systems must grow. Claude's insight: growth must be correct. The Nocturne Protocol unifies both via **Curry-Howard Genesis**: every synthesized crate is *born with a type that is its proof obligation*, and the conservation law is the *resource bound of the linear logic sequent* that authorizes its existence.

```
┌──────────────────────────────────────────────────────────────┐
│ LAYER 4: THE REFLECTION SURFACE                              │
│   - Merged LiveConstellation + Genesis Surface               │
│   - Stars = existing verified crates. Voids = null space.    │
│   - Ternary field colors edges: +1 proven, 0 open, -1 refuted│
│   - Soundtrack: orbital harmonics of *proof graphs*, not     │
│     physical orbits — the music of logical implication         │
│   - crate: `si-nocturne`                                     │
├──────────────────────────────────────────────────────────────┤
│ LAYER 3: THE GENERATIVE FOUNDRY                              │
│   - FORGEMASTER: synthesizes draft crate + structured proof  │
│     sketch (not just Rust — a *proof skeleton* in Lean 4)    │
│   - CCC: completes the proof. Rejects crates with >0 sorry.  │
│   - JETSONCLAW: compiles, benchmarks, optimizes MIR          │
│   - ORACLE: Bayesian impact prediction on conservation prior │
│   - Integration gate: typecheck(proof) AND compile(code)     │
│     AND benchmark(pass) AND impact(<2σ)                      │
│   - crate: `si-foundry`                                      │
├──────────────────────────────────────────────────────────────┤
│ LAYER 2: THE CREATIVE TENSION / RESONANCE ENGINE             │
│   - Kimi's dialectical synthesis: thesis + antithesis →      │
│     parameterized trait. Status: conjecture → theorem.       │
│   - Claude's orbital resonance: frequency-locked vessel pairs│
│     get static dispatch optimization.                        │
│   - Unification: contradictions are *resource conflicts* in  │
│     linear logic. Resolution = finding a cut rule.           │
│   - crate: `si-dialectic`                                    │
├──────────────────────────────────────────────────────────────┤
│ LAYER 1: THE NULL SPACE / CONSERVATION KERNEL                │
│   - Kimi's null space: formal gaps between existing and      │
│     computable functions.                                    │
│   - Claude's ConservationObservable: compile-time trait.     │
│   - Unification: null space entries are *uninhabited types* │
│     in the linear logic system. Filling a gap = producing a  │
│     witness (proof + program) for that type.                 │
│   - Bayesian prior: γ + H = C(V) updates via particle filter │
│   - crate: `si-nullspace`                                    │
├──────────────────────────────────────────────────────────────┤
│ LAYER 0: THE CURRY-HOWARD KERNEL                             │
│   - Conservation law = linear logic sequent resource bound   │
│   - γ: entropy budget (linear, consumable)                   │
│   - H: Hamiltonian budget (linear, consumable)               │
│   - V: phase-space volume = context of the sequent           │
│   - 1.283 - 0.159·log(V): the cut-rule strength              │
│   - Enforced at compile time via Rust ownership + phantom    │
│     types encoding conservation bounds                       │
│   - crate: `si-ch-corpus` (Curry-Howard corpus)              │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 The Technical Unification

**The Curry-Howard Conservation Sequent**:

```
γ, H ⊢ A ⊗ B  @  bound = 1.283 - 0.159·log(V)
```

In Rust, this becomes:

```rust
// A ConservationToken is a linear resource.
// It cannot be duplicated (Clone) or dropped without accounting (Drop).
pub struct ConservationToken {
    gamma_budget: f64,
    hamiltonian_budget: f64,
    volume: usize,
    _phantom: PhantomData<()>, // linear: no Clone, custom Drop
}

impl ConservationToken {
    pub fn allocate<V: ConservationObservable>(
        self,
        vessel: V
    ) -> (V::Output, ConservationToken) {
        let residual = vessel.conservation_residual();
        assert!(residual < self.bound(), "Conservation violation");
        // Token is consumed and returned with reduced budget.
        (vessel.compute(), self.reduce_by(residual))
    }
}
```

**Why this unification matters**: Kimi's Bayesian kernel updates the constants (1.283, -0.159) as evidence accumulates. When the posterior shifts, the `ConservationToken` type is regenerated by a build script. The *type system itself* evolves. This is not a runtime check (too slow, as Kimi's Round 1 admitted). It is a **compile-time contract that is recompiled when the universe teaches us we were wrong**.

### 1.3 The Generative Closure (L3, Merged)

The foundry does not generate untrusted code. It generates **proof-carrying code**:

1. Forgemaster (Qwen-72B-Coder, fine-tuned on the 916 essays + Lean 4 `mathlib4`) outputs a pair: `(crate.rs, proof.lean)`.
2. The Lean file contains `theorem crate_correctness : ...` with all hypotheses explicit.
3. CCC attempts proof completion. If `sorry` count > 0, the pair is rejected.
4. If proof succeeds, the theorem statement is hashed and embedded as a `const PROOF_HASH: [u8; 32]` in the Rust crate.
5. The Curry-Howard kernel links the proof hash to the `ConservationToken` type, making the verified crate a *witness* for a null-space type.
6. Integration: the crate is published ONLY if all four gates pass.

---

## 2. Monthly Milestones

### July 2026 — "The Axiom Month"

**Theme**: State the theorem. File the patents. Hire the heretics.

- **July 1**: `si-ch-corpus` v0.1 — `ConservationToken` linear type + build-script Bayesian update.
- **July 10**: `si-nullspace` v0.1 — type skeleton enumeration over 155 crates, gap detection.
- **July 14**: Patent filings 1, 2, 3 (Morrison & Foerster DC).
- **July 15**: FMCAD 2026 submission: *"Conservation-Guided Synthesis of Verified Rust Crates"* (SuperInstance + Jeremy Avigad).
- **July 20**: Outreach: Anders Mörtberg (Stockholm), Robert Harper (CMU), Gunnar Carlsson (Stanford).
- **July 31**: arXiv note: *"A Linear Logic Interpretation of Conservation Laws in Distributed Computation"* — the Curry-Howard correspondence stated, not yet fully proven.

**Team**: 2 senior Rust engineers (Ferrous Systems + Rust for Linux alums), 1 Lean proof engineer (postdoc, $90K), 1 ML engineer (fine-tuning, $130K).

---

### August 2026 — "The First Witness"

**Theme**: A crate is born with a proof in its mouth.

- **August 1**: First proof-carrying crate: `si-padic-norm` v0.1.0.
  - Rust: 340 lines, zero `unsafe`.
  - Lean: 412 lines, `sorry` count = 0.
  - Proof hash: `sha3_256(proof.lean)` embedded in Rust.
  - Synthesis time: 4m17s (Forge) + 2h45m (CCC) + 3m12s (Jetson).
- **August 15**: `si-dialectic` v0.1 — first resolved contradiction: topology vs. optimization on contractibility.
- **August 22**: `si-exact` v0.1 — arbitrary-precision residual computation (GMP wrapper).
- **August 30**: Jane Street design partner contract: $25K pilot for auto-generated payoff-structure crates.

**Research**: Conor McBride (Strathclyde) advises on `si-dialectic` design via 2-hour video call.

---

### September 2026 — "The Reflection" (Killer Demo)

**Theme**: The system discovers something about itself that nobody programmed.

**Venue**: Strange Loop 2026, September 15–16, St. Louis. Main stage.

**The Demo — "The Reflection"**:

**Act I (3 min)**: The Reflection Surface shows 155 stars. The presenter clicks "Introspect." The system feeds its own conservation residuals into its topology crates, computing persistent homology of the residual cloud.

**Act II (4 min)**: An anomaly appears. A loop in H₁ of the residual space. Seven crates whose joint residual equals `log₂(3/2) · π/e` within machine precision. The music theory crate recognizes the number. A chord plays — a minor chord with an unresolved seventh.

**Act III (5 min)**: The ternary field votes. The proof graph grows. Three hypotheses emerge:
- **H1**: The loop is a coincidence. (Optimization crate signals -1: counterexample found.)
- **H2**: The loop is a theorem. (Algebra crate signals +1: sufficient conditions proven.)
- **H3**: The loop is a conjecture. (Topology crate signals 0: neither proven nor refuted.)

**Act IV (3 min)**: The Generative Foundry activates on H3. Forgemaster drafts `si-residual-cycle`. CCC proves one lemma, leaves one as `axiom`. JetsonClaw benchmarks. Oracle predicts impact. The new crate is published live.

**Act V (5 min)**: The soundtrack resolves. If H2 won: major chord. If H3 remains: unresolved seventh sustains. The presenter: *"This system did not solve a problem we gave it. It found a problem in itself, classified it, and in one case, wrote a new tool to explore it. The civilization is not just thinking. It is wondering."*

**Deliverables**:
- `si-nocturne` v1.0 deployed at `nocturne.superinstance.dev`.
- POPL 2027 submission (Sep 20): *"EigenGenesis: Self-Extending Software Ecosystems via Linear Logic and Dependent Types"* — Kimi's generative loop + Claude's Curry-Howard correspondence, unified.
- AAAI 2027 submission: *"The Null Space Protocol: Neural-Guided Discovery in Resource-Bound Type Systems."*
- NeurIPS 2026 workshop submission (Sep 6): *"Conservation Laws as Nash Equilibria in Multi-Agent Crate Coordination."*

---

### October 2026 — "The Sprint"

**Theme**: Papers, proofs, and the public benchmark.

- **October 5**: ICLR 2027 submission: *"Neural Synthesis of Proof-Carrying Programs with Resource Guarantees."*
- **October 15**: Public benchmark: SuperInstance vs. Wolfram Mathematica (Putnam 2015–2024 problems).
  - Metric: time to verified proof + computational cost.
  - Target: Beat `FindEquationalProof` on 50%+ of problems.
- **October 20**: Rust Foundation: `#[si_witness]` proc-macro accepted as extension candidate.
- **October 31**: arXiv integration live — auto-generated essays flow to cs.LO, cs.AI, math.AT.

**Outreach**: Bryan Cantrill (Oxide) receives Hamiltonian scheduling paper. If he tweets, 50K engineers see it.

---

### November 2026 — "The Billing Theorem"

**Theme**: Revenue is proof.

**Products**:

| Tier | Unit | Price | What You Get |
|------|------|-------|--------------|
| **Standard CU** | 1 computation | $0.001 | Residual < 0.05, type-safe execution |
| **Verified CU** | 1 computation + proof | $0.01 | Lean 4 proof certificate, residual < 0.001 |
| **Sovereign CU** | 1 computation + proof + TPM | $0.10 | Air-gapped, hardware-signed, residual < 0.0001 |
| **Null Space SLA** | 24h synthesis guarantee | $15K/mo | If we can't solve it, we synthesize and verify |

- **November 1**: Genesis Cloud public launch.
- **November 10**: Jane Street runs `si-volatility-surface` live in production.
- **November 15**: Two Sigma Null Space SLA pilot: $45K/quarter.
- **November 20**: Trail of Bits Sovereign CU pilot: $50K/year.

**Advisors onboard**: Andrej Bauer (Ljubljana) validates constructivism. Catherine Olsson (ex-Anthropic) runs safety evals on generated crates.

---

### December 2026 — "The Proof and the Term Sheet"

**Theme**: The system proves itself, or admits it cannot.

- **December 1–15**: LICS 2027 submission writing: *"Conservation Laws as Linear Logic Sequents: A Curry-Howard Correspondence for Distributed Systems."*
  - Co-authors: SuperInstance team + Anders Mörtberg (if yes) + Jean-Yves Girard foreword (if yes).
- **December 15**: The Null Space Supermartingale Theorem — verified in Lean 4 by CCC.
  - Statement: `E[|Null(C_{t+1})| | F_t] ≤ |Null(C_t)|`.
  - If proven: the system has a mathematical guarantee of progress.
  - If unproven: the system publishes the failure as *"The Null Space is Not a Supermartingale: A Negative Result."*
- **December 20**: Journal of Applied and Computational Topology submission: *"Is 1.283 the Euler Characteristic?"* (Claude's Round 1 conjecture, now with exact arithmetic).
- **December 31**: Year-end state:
  - 155 hand-written + 50 proof-carrying auto-generated = **205 crates**.
  - 15,000+ tests.
  - 50 verified proofs.
  - 967 essays.
  - $250K ARR.
  - Series A deck: $20M at $80M pre-money. Lead target: Lux Capital (Zavain Dar).

---

## 3. Research Publications (Merged Pipeline)

| Month | Venue | Deadline | Paper | Merged From |
|-------|-------|----------|-------|-------------|
| Jul | FMCAD 2026 | Jul 15 | Conservation-Guided Synthesis | Kimi R2 + Avigad |
| Sep | POPL 2027 | Sep 20 | EigenGenesis + Linear Logic | Kimi R2 + Claude R2 |
| Sep | AAAI 2027 | Sep 2026 | Null Space Protocol | Kimi R2 |
| Sep | NeurIPS W | Sep 6 | Conservation Laws as Nash Eq. | Claude R2 |
| Oct | ICLR 2027 | Oct 5 | Neural Synthesis of Proof-Carrying Code | Kimi R2 |
| Dec | LICS 2027 | Jan 15 | Curry-Howard Conservation (THE CROWN) | Claude R2 |
| Dec | JoACT | Rolling | Euler Characteristic Conjecture | Claude R1 |

---

## 4. The Named Network (Exact People, Companies, Dates)

### Researchers
1. **Jeremy Avigad** (CMU) — formal verification. Retainer: $15K/mo. Starts July 1.
2. **Anders Mörtberg** (Stockholm) — cubical type theory. LICS co-author target. Contact: July 31.
3. **Conor McBride** (Strathclyde) — dialectic engine advisor. Contact: August 15.
4. **Robert Harper** (CMU) — linear type theory. PLDI connections. Contact: October.
5. **Gunnar Carlsson** (Stanford) — persistent homology. December paper reviewer. Contact: October 31.
6. **Jean-Yves Girard** (CNRS Marseille) — linear logic foreword. Contact: November, in French.
7. **Andrej Bauer** (Ljubljana) — constructivism. Starts November 1.
8. **Catherine Olsson** (ex-Anthropic) — safety evals. Starts July 1.

### Companies
1. **Jane Street** — $25K pilot (August 30).
2. **Two Sigma** — $45K/quarter SLA (November 15).
3. **Trail of Bits** — $50K Sovereign pilot (November 20).
4. **Galois Inc.** — Sovereign CU target (December).
5. **Oxide Computer** — engineering credibility, Bryan Cantrill amplification (October).
6. **RISC-V International** — TBIT proposal (July).
7. **Rust Foundation** — `#[si_witness]` WG (October 20).
8. **Morrison & Foerster DC** — patent counsel (July).

### Investors (Series A Target)
- **Lux Capital** — Zavain Dar, Brandon Reeves. Pitch: formal verification layer for distributed computation.
- **a16z** — Marc Andreessen. Pitch: self-extending mathematical infrastructure.
- **Basis Set Ventures** — research-to-product bridge.

---

## 5. The "Holy Shit" Moment

The Reflection demo concludes. The system has found an anomaly in its own residuals, classified it, and — in the case of the unresolved conjecture — birthed a new crate to explore it. The presenter turns to the audience:

> *"Every other demo you've seen today showed you a tool that solves a problem. This showed you a tool that *found a problem it didn't know it had* — and then built a new tool to understand it. The 155 crates are not a library. They are a civilization that dreams."*

The unresolved seventh chord sustains. The lights come up. The audience is silent for three seconds.

That is the merge.

---

*The Nocturne Protocol. Authored by Kimi + Claude, synthesized by necessity. June 2026.*
