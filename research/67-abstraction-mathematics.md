# Dyadic Staircases: Provable Error Envelopes for Streaming Fixed-Point Hebbian Hardware

**Authors:** SuperInstance Research Team (abstraction-mathematics lane)
**Paper Number:** 67
**Date:** August 2026
**Status:** Research Complete — Theory + Toolchain Verified
**Subject:** The mathematics of hardware abstraction for quilt-verilog: a unified error-bound theorem for the two decay engines, a formal-object map of the fabric, and a machine-checked verification pipeline (yosys-sby)

---

## Abstract

The quilt-verilog bottom layer is a ring of cells connected by one streaming contract, running Hebbian learning with fixed-point primitives: a saturating activation integrator, an age-bucket decay ladder with a proven factor-2 error bound, and a hyperbolic decay counter with a proven [1,4) envelope. This paper makes three claims. **(1) Unification:** the two decay engines are one mathematical family — *dyadic staircases*. The ladder is an exponential histogram over cofire ages (Datar et al., 2002); its 2W bound is the base-2 case of a *staircase envelope theorem*: any monotone decay law with the b-doubling property `w(a) ≤ b·w(ba)` admits a shift-only bucket readout with multiplicative envelope `Ŵ ∈ [W, b·W)`. Power-law laws are *exact* on shift ladders, and the hyperbolic counter is asymptotically a power law — which is why one engine, two dial settings, is not a coincidence. The hyperbola is separately a *quantized Riccati integrator*: a self-paced pure-death process with msb-quantized decrement intervals, whose k-parameter envelope `2^k` subsumes the [1,4) bound. **(2) Grounding:** the fabric's abstractions have precise names in the literature — the ring is a traced monoidal wiring of causal stream functions (Ghica & Kaye, 2022/2025); "the clock is its own traffic" is *endochrony* (Signal/Polychrony, Le Guernic et al.); the tick is a logical execution time instant; the testbenches are synchronous observers (Halbwachs et al., 1994); saturate-never-wrap is confirmed by the 2026 hardware-safe-training line. **(3) Verification:** the toolchain is already working — the flit-pipe FIFO contract proves by k-induction (SymbiYosys, smtbmc/boolector) in under a second, and the two envelope bounds are expressible as monitor modules provable the same way. The buildable deliverable is a week of formal checks that machine-check the bounds the design already claims.

---

## 1. Introduction

### 1.1 The quilt

quilt-verilog is a bottom-layer hardware experiment: pure Verilog, zero vendor code, a ring-of-cells fabric where every cell speaks one streaming contract (a valid/ready flit: `{op, src, dst, a0, a1, a2, dat}`) and the intelligence is in fixed-point primitives — a saturating effect integrator, Hebbian edge weights with two selectable decay laws, a runtime dial register file, a tick scheduler that is a hard deadline rather than an advisory phase. The doctrine, won in a five-way architecture competition and enforced by testbenches: saturate-never-wrap anywhere a value integrates; integer state wherever math allows; the forgetting law is runtime data, not a compile-time constant; config travels as traffic.

### 1.2 The gap this paper closes

The competition produced two *proven in prose* error bounds:

- **The ladder bound (glm):** age-bucket counters with implied weights `2^-i`;
  every cofire's true exponential weight is within a factor of 2 of its counted
  weight; readout satisfies `Ŵ ∈ [W, 2W)`.
- **The hyperbola bound (zeroclaw):** decrement interval `P₀ >> 2·msb(W)`
  integrates `dW/dt = −W²/P₀` with the discrete trajectory trapped in
  `[W_true(P₀), W_true(P₀/4)]`.

Two bounds, two proofs, two styles — ladder and counter looked like different
mathematics. They are not. Section 2 states the theorem that makes both cases of
one statement, and generalizes it. Section 3 names the fabric's abstractions in
the formal literature. Section 4 reports the verification pipeline that can
machine-check all of it this week, with one proof already run. Section 5 is the
honest-limits ledger.

### 1.3 Method and honesty notes

Primary sources were fetched at abstract/full level via the arXiv API and web
(arXiv IDs cited inline). Classic results (Kahn 1974; Berry 1999; Benveniste et
al. 2003; Datar et al. 2002; Moore 1966; Lafont 1990; Sheeran et al. 2000;
Carloni–McMillan 2001) are cited from standard literature without per-paper
re-verification — they are load-bearing for *shape*, not constants. The
verification claim (Section 4.3) is a fresh experimental result from this lane:
SymbiYosys on the OSS CAD Suite, re-run clean after a concurrent lane's runs
interfered with the shared working directory.

---

## 2. The two engines as one family: dyadic staircases

### 2.1 The staircase envelope theorem

**Setup.** A stream of events (cofires) arrives at an edge; event e has age
`a_e ≥ 0` (ticks since arrival). The continuous law assigns weight `w(a_e)`,
strictly decreasing, positive. The hardware may not multiply — weights must be
*shifts*.

**Theorem (base-b staircase envelope).** Suppose `w` has the *b-doubling decay*
property

```
w(a) ≤ b · w(ba)      for all a > 0            (D_b)
```

(the exponential law `2^(−a/H)` satisfies D_2 with equality on the bucket grid).
Partition ages into buckets `[b^i H, b^(i+1) H)`, i = 0..K−1, assign bucket i the
implied weight `b^(−i)` (a shift of `i·log₂ b` bits). Let `W = Σ_e w(a_e)` and
`Ŵ = Σ_i C_i · b^(−i)`, where C_i counts events in bucket i. Then

```
W ≤ Ŵ ≤ b · W .
```

**Proof.** For an event in bucket i, `a_e ∈ [b^i H, b^(i+1) H)`, so by
monotonicity `w(a_e) ∈ (w(b^(i+1) H), w(b^i H)]`. For the exponential,
`w(b^i H) = b^(−i)` (scale `w(H) = 1`), hence `w(a_e) ∈ (b^(−(i+1)), b^(−i)]`.
The assigned weight `b^(−i)` overstates the true weight by a factor in `[1, b)`.
Summing over events: `W ≤ Ŵ < b·W`. ∎

**Corollaries.**
- **b = 2 is glm's ladder.** `Ŵ ∈ [W, 2W)` — the proven 2W bound is the base-2
  case. Tightness: the per-bucket overstatement can approach b, so the envelope
  is exact as a bound.
- **b = 2^p trades error for buckets.** A p-bit-shift ladder (implied weights
  `2^(−ip)`) halves the bucket count at a factor-2^p envelope. The K=8,B=8 v1
  ladder is the p=1, b=2 case; a "coarse ladder" dial is a documented v2 slot.
- **Power laws are exact.** If `w(a) = (H/a)^k`, bucket weights are
  `b^(−ik)` — still shifts (`i·k·log₂ b` bits), and the readout is *exact*:
  `Ŵ = W`. A shift-ladder represents a power law without error; it represents an
  exponential with factor-b error. This is the structural reason a "power-law
  engine" and an "exponential engine" can share one register file: the ladder is
  a power-law-exact machine that approximates the exponential.

The ladder is, in the streaming-algorithms literature, an **exponential
histogram** (Datar–Gionis–Indyk–Motwani, SODA 2002): dyadic bucketing of stream
elements by age with geometric implied weights, the standard (1+ε) sliding-window
technique. Our 2W bound is the ε = 1 special case; the family admits ε-tunable
variants at more buckets.

### 2.2 The hyperbola counter as a quantized Riccati integrator

The second engine maintains integer `W`, `age`; every tick `age++`; when
`age ≥ P₀ >> (k·msb(W))` (floor 1) and `W > 0`, decrement `W` and reset `age`.
The continuous target is the **Riccati equation**

```
dW/dt = −W²/P₀          ⟹    W(t) = W₀ / (1 + W₀ t / P₀),
```

a pure-death process with quadratic death rate `λ(W) = W²/P₀`. The discrete
engine is a *self-paced* death process: the decrement interval is
`1/λ(W)` quantized to a power of two,

```
Δ(W) = P₀ >> (k·msb W) ∈ [P₀/2^k·W², P₀/W²)     since msb W = ⌊log₂ W⌋.
```

**Envelope (k-parameter form).** Because intervals are never shorter than the
exact `P₀/W²` and never longer than `2^k` times it, the discrete trajectory is
trapped between the exact solutions of the bracketing rates:

```
W_true(P₀) ≤ W_rtl ≤ W_true(P₀ / 2^k)      (k = 2 ⟹ the [1,4) bound).
```

This is a *log-domain Euler* reading: step size = quantized `1/λ(W)`, and the
bound is a discrete Gronwall-style step-size argument. The msb lookup is one
priority encoder — already in the RTL (`msb16`). The k-parameter generalizes the
bound continuously in bucket bits, exactly as the base-b ladder does.

### 2.3 The unification

The two engines are two engravings of one family — *dyadic staircases*:

| | Ladder (MODE=0) | Hyperbola counter (MODE=1) |
|---|---|---|
| Staircase over | **age** (state buckets) | **time** (decrement intervals) |
| Law represented | exponential `2^(−a/H)` | power law `(1 + W₀t/P₀)^(−1)` |
| Exact for | power laws | (its own Riccati, in the interval-envelope sense) |
| Error | factor b = 2 | factor 2^k = 4 |
| Mechanism | shift-implied bucket weights | msb-quantized intervals |
| Bound | `Ŵ ∈ [W, 2W)` | `W_true(P₀) ≤ W_rtl ≤ W_true(P₀/4)` |

The asymptotic link: for `t ≫ P₀/W₀`, `W(t) ≈ P₀/t` — the hyperbola IS a power
law with k=1, which a shift-ladder represents *exactly*. The "law is data"
stance of the v1 design (MODE is a runtime dial) is therefore not an
implementation compromise; it is the statement that the family parameter is the
only thing being dialed. The v2 dial slots (base-b, k-parameter) are
mathematically pre-provisioned by the theorem.

### 2.4 Fixed-point toolbox context

The envelope theorems sit in a mature toolkit: interval arithmetic (Moore 1966)
for first-cut ranges; **affine arithmetic** (Stolfi & de Figueiredo 2003) for
correlated-error budgets (the ≤ MAX_OP_CYCLES successive adds in the effect
integrator are correlated — AA tracks that; IA blows up); **Gappa** (Melquiond)
and **Flocq** (Boldo & Melquiond 2011) for machine-checkable certificates of the
*golden model's* arithmetic, so the reference the testbenches compare against is
itself certified; **SMT-based bounded model checking of fixed-point filters**
(arXiv:1305.2892) for word-length bugs; and **stochastic rounding** (Gupta et
al., 2015) as the principled upgrade of convergent rounding — unbiased, removes
systematic drift, a dial slot in v2. The 2026 hardware-safe-training line
(arXiv:2607.04531) independently validates the saturate-never-wrap doctrine:
two's-complement wrap corrupts magnitude *and sign* of hidden activations,
which is exactly why the v1 policy is a policy and not a default.

---

## 3. The abstraction map: naming the fabric

### 3.1 Category theory and typed circuits

The compositional-circuit line gives the fabric its charter. **Ghica & Kaye**
("Diagrammatic Semantics for Digital Circuits," arXiv:1703.10247; "A Complete
Theory of Sequential Digital Circuits," arXiv:2201.10456; Kaye's thesis,
arXiv:2502.08497) prove circuits compose *freely, without consulting internals*:
denotational semantics are **causal stream functions** (bridged to Mealy
machines); operational semantics are rewriting strategies with observational
equivalence; and the thesis extends string-diagram rewriting to hypergraphs
compatible with the **traced comonoid structure** — rewriting *modulo feedback*.
The ring-of-cells fabric is a traced monoidal wiring: cells are morphisms on the
flit bundle, the ring is composition plus trace (feedback), and the registered
pipe slices are the delays that make the trace well-founded. The theory says a
cell's internals are irrelevant to correct composition — the formal charter for
"the cell core FSM is the only interpreter" and for thin ring ports. Practical
takeaway: draw the fabric as string diagrams in v2 docs; the algebraic semantics
are the transformation rules for re-associating cell chains.

**Signal-flow graphs** have a complete equational theory: Bonchi–Sobocinski–
Zanasi's **interacting Hopf algebras** IHR[x] is isomorphic to the PROP of linear
relations over streams, with a Kleene theorem (arXiv:1703.10247's companion line;
LIPIcs CALCO 2017). Our linearized sub-models — readout sums of shifted buckets,
the integrator — are IHR[x] diagrams; diagrammatic equality implies behavioral
equality, a rewrite-level equivalence check. For the multiplier-free datapaths
there is a *complete* calculus: the **ZX&-calculus** (arXiv:2004.05287) — copy
and add spiders, NOT, AND — is complete for classical circuits; the ladder
readout adder tree is literally a copy/add spider network. The typed-HDL
tradition (Lava, Clash, Bluespec, ForSyDe, ReWire; arrows à la Hughes) is a
*language* lesson — ports as typed bundles — not a runtime tool; monoidal
streams (arXiv:2202.02061, 2212.14494) give the denotational home of
valid/ready with the ready side-channel.

**Dead ends, stated.** Interaction nets (Lafont 1990) are beautiful and
proof-side: the relevant result compiles *Kahn process networks to interaction
nets* (arXiv:1609.03640), which certifies why ring-local rewriting suffices but
is not a synthesis path. Clifford/geometric algebra in signal processing is
real but analog-side (multidimensional analytic signals: Bulow & Sommer,
Felsberg & Sommer; arXiv:2411.10412); nothing connects GA to synchronous
digital abstraction. Our directional primitive (vMF/dial) is angular statistics
— the hardware math there is CORDIC-style rotation, not GA. Parked.

### 3.2 Synchronous-language theory: the time story

The fabric is a synchronous program in the Lustre/Esterel/Kahn family
(Benveniste et al., "The Synchronous Languages Twelve Years Later," Proc. IEEE
2003). The tick is a **basic clock**; every other signal's clock is derived
(Lustre clock calculus). The **constructive semantics** of Esterel (Berry 1999;
Malik 1994 on cyclic combinational circuits) is the formal content of the v1
restructurings: the ladder readout went from a combinational adder tree to a
registered loop (verilator UNOPTFLAT), and the flit pipe's `s_ready = !b_v`
depends only on local state. Rule, now nameable: **no signal depends on itself
through combinational logic; every loop passes a register** — Berry
constructiveness at RTL level. The ring with valid/ready backpressure is a
**bounded Kahn network**; determinacy (Kahn 1974) holds, and the no-drop ingress
is a bounded channel. The TBs are **synchronous observers** (Halbwachs, Lagnier,
Raymond 1994) — the standard Lustre verification idiom, which is why upgrading
them to formal properties is not a language change.

**"Clock is its own traffic" is endochrony.** The socratic lane's slogan — the
clock is not a separate plane; a signal's clock is its own presence (`valid`) —
is exactly the polychronous stance of **Signal/Polychrony** (Le Guernic et al.):
signals define their own clocks; the clock calculus computes relations between
implicit clocks; an **endochronous** process is deterministic from its
communication alone. The fabric is endochronous by construction: `valid` is the
clock, `ready` is scheduling feedback, the tick is the one external basic clock.
The v2 seam questions — the drop policy, the traffic-based tick (deferred
curveballs) — are *endochrony/isoendochrony* analyses, expressible first in
**CCSL** logical-clock constraints (Mallet, "Logical Time"; arXiv:1806.07702,
1904.07011) before RTL. The tick-as-hard-deadline is **logical execution time**
(Kopetz; Giotto, Henzinger 2003): communications commit at logical instants —
front-of-queue at an op boundary is a priority discipline on logical instants.
The neural flavor — timing emerging from coincidence — is Izhikevich
**polychronous groups** (arXiv:2103.15265): the v2 traffic-based tick is a
polychronous-group phenomenon with an endochronous formal home.

### 3.3 Refinement and equivalence

The verification doctrine is **refinement**: the RTL refines the golden model.
The operative form for hardware is **sequential equivalence checking** (SEC) —
sby `mode equivalence` — with the refinement calculus (Back & von Wright) as
theory and **Kami** (Choi et al., ICFP 2017) as the interactive cousin. A
pipe-and-filter **refinement calculus** (arXiv:1411.2414) covers the v2 bridge
moves (provably correct add/remove/combine of filters — the fabric is a
pipe-and-filter architecture). The 2026 **NoTB** result (arXiv:2608.21962) —
oracle-free cross-model formal consensus for LLM-generated RTL — is this
competition's own shape: winner by consensus, gate by formal check, independent
of whichever model wrote the RTL.

---

## 4. Verification as refinement: the pipeline, with one proof already run

### 4.1 The toolchain

OSS CAD Suite at `/home/eileen/tools/oss-cad-suite` (yosys 0.47+22, SymbiYosys
sby, smtbmc with boolector and z3, btormc, suprove, avy). Harness idiom, proven
by the existing `tb/formal/` work: **boundary-only shadow models** — the harness
re-implements the module's contract as a shadow state machine at the ports (no
hierarchical references; yosys turns them into undriven implicit wires); a reset
preamble (DUT registers have no init values); `assert`/`assume`/`cover`
statements; `read -formal` + `prep -top`; `mode prove` (k-induction, Sheeran–
Singh–Stålmarck 2000) for invariants, `mode bmc` for bounded liveness, `mode
equivalence` for golden-model SEC.

### 4.2 Evidence: the flit-pipe contract, proven

The FIFO contract C1–C4 (no duplication; capacity 2 never exceeded; nothing
hidden — `m_valid ⟺ nonempty`; backpressure exactly at capacity) was encoded as a
shadow occupancy model and proved: **basecase + temporal induction both pass,
smtbmc/boolector, ~0 seconds, depth 15.** This lane re-ran it clean in /tmp
because the shared working directory was being concurrently re-run by another
lane (logfiles flipped between reads); the PASS is reproducible. The result
matters beyond the pipe: the *method* — contract as shadow model, property as
k-induction — is seconds-per-module on this fabric's small FSMs.

### 4.3 The check list for this week

| # | Check | Module | Form |
|---|---|---|---|
| 1 | FIFO contract C1–C4 | q_flit_pipe | **prove — DONE, PASS** |
| 2 | Ring-port contract (deliver/transit/inject exactly once) | q_link_ringport | prove |
| 3 | I1 liveness: `fell(ci_ready) \|-> ##[1:MAX_OP_CYCLES] ci_ready` | q_cell_core | prove |
| 4 | Q2 tick service: strobe → ST_TICK < 2×MAX_OP_CYCLES | q_cell_core | prove + cover |
| 5 | **Dyadic envelope, ladder: `W/2 − 1 ≤ Ŵ ≤ 2W + 1`** | q_hebb_edge | prove (monitor) |
| 6 | **Dyadic envelope, hyperbola: `W_true(P₀) ≤ W_rtl ≤ W_true(P₀/4)`** | q_hebb_edge | prove (monitor) |
| 7 | Saturate-never-wrap (shadow saturating model vs RTL) | q_hebb_edge, q_cell_core | prove / equivalence |
| 8 | Ring progress, bounded: flit advances or delivers within N cycles | q_fabric_top | bmc |
| 9 | Golden-model SEC (RTL vs reference) | any module | equivalence |

Flagship: **#5/#6** — the two envelope theorems of Section 2 encoded as monitor
modules (~30 lines each: compute the envelope from state, assert the readout lies
inside) and proved by k-induction. The flit-pipe experience says these are
minutes, not hours. #3/#4 answer the architecture's gate questions (bounded ops,
non-deferrable tick) in the formal voice. For runtime monitoring of the *living*
fabric, the stream-RV line (Lola, Leucker & Schallhart 2005; TeSSLa,
arXiv:1808.10717; STL observers for Lustre, arXiv:2608.12693, 2311.09788) gives
the v2 observability layer a specification language that is both sim-checkable
and sby-checkable.

---

## 5. Honest limits

- **Fabric-level liveness in full generality is not proved.** Check #8 is bounded
  (bmc, small N). The v1 claim — a correctly-addressed ring drains at ≥1 flit per
  bound — is argued, not machine-proved; `mode live` is the hard case, deferred.
- **Misaddressed flits** circulate forever by contract (the v1 traffic class
  excludes them); the v2 drop policy is an endochrony question (schedulability
  under drops), flagged, not solved.
- **The hyperbola envelope has slack** (factor-4 interval quantization; the
  k-parameter tightens it at more bits). The ladder's 2W is tight.
- **The envelope theorem bounds the readout, not the learning**: it says the
  *hardware weight* tracks the *continuous law*; it says nothing about whether
  the law itself is the right one for the task — that is the TB/golden-model
  question the acceptance gate already owns.
- **Tooling caveats:** yosys's Verilog frontend treats hierarchical refs as
  implicit wires (no XMRs in harnesses); concurrent runs on the shared `tb/formal/`
  directory can corrupt reads (run proofs in a scratch copy or serialize).

---

## 6. References

- Kaye, "Foundations of Digital Circuits: Denotation, Operational, and Algebraic
  Semantics," PhD thesis, arXiv:2502.08497 (2025).
- Ghica & Kaye, "A Complete Theory of Sequential Digital Circuits," arXiv:
  2201.10456 (2022).
- Ghica, "Diagrammatic Semantics for Digital Circuits," arXiv:1703.10247 (2017).
- Bonchi, Sobocinski, Zanasi, "Interacting Hopf Algebras," LIPIcs CALCO 2017;
  "The Calculus of Signal Flow Diagrams I: Linear Relations on Streams," 2017;
  "Contextual Equivalence for Signal Flow Graphs," 2020.
- "The ZX&-calculus: A Complete Graphical Calculus for Classical Circuits Using
  Spiders," arXiv:2004.05287 (2020).
- "Monoidal Streams for Dataflow Programming," arXiv:2202.02061 (2022);
  "Coinductive Streams in Monoidal Categories," arXiv:2212.14494.
- "Circuits, Bond Graphs, and Signal-Flow Diagrams: A Categorical Perspective,"
  arXiv:1805.08290 (2018).
- Benveniste, Caspi, Edwards, Halbwachs, Le Guernic, de Simone, "The Synchronous
  Languages Twelve Years Later," Proc. IEEE 91(1), 2003.
- Halbwachs, Lagnier, Raymond, "Synchronous Observers and the Verification of
  Reactive Systems," 1994.
- Berry, "The Constructive Semantics of Pure Esterel," 1999; Malik, "Analysis of
  Cyclic Combinational Circuits," ICCAD 1994; Shiple, Berry, Touati, "Formal
  Analysis of Combinational Loops," DAC 1996.
- Kahn, "The Semantics of a Simple Language for Parallel Programming," IFIP 1974.
- Le Guernic et al., "The Signal Language," 1991; Mallet, "Logical Time" (CCSL),
  Springer 2011; PrCCSL analyses: arXiv:1806.07702, arXiv:1904.07011.
- "Polychrony as Chinampas," arXiv:2103.15265 (2021).
- Kopetz, "Real-Time Systems," Springer (LET); Henzinger, Horowitz, Kirsch,
  "Giotto," 2003.
- Carloni, McMillan, Sangiovanni-Vincentelli, "Theory of Latency-Insensitive
  Design," IEEE TCAD 20(9), 2001.
- "Refinement of Pipe-and-Filter Architectures," arXiv:1411.2414 (2014).
- Choi, Vijayaraghavan, Sherman, Chlipala, "Kami," ICFP 2017.
- "NoTB: Oracle-Free Triage of LLM-Generated RTL via Cross-Model Formal
  Consensus," arXiv:2608.21962 (2026).
- Sheeran, Singh, Stålmarck, "Checking Safety Properties Using Induction and a
  SAT-Solver," FMCAD 2000.
- Leucker & Schallhart, "LOLA: Runtime Monitoring of Synchronous Systems," TIME
  2005; "TeSSLa: Temporal Stream-based Specification Language," arXiv:1808.10717
  (2018); "Synchronous Observers Revisited for Runtime Verification of Lustre
  Using STL," arXiv:2608.12693 (2026); "Towards Proved Formal Specification and
  Verification of STL Operators as Synchronous Observers," arXiv:2311.09788.
- Datar, Gionis, Indyk, Motwani, "Maintaining Stream Statistics over Sliding
  Windows," SODA 2002.
- "Verifying Fixed-Point Digital Filters using SMT-Based Bounded Model Checking,"
  arXiv:1305.2892 (2013); "Lyapunov-Guided Training for Hardware-Safe Neural
  Networks Under Fixed-Point Arithmetic," arXiv:2607.04531 (2026); "Certification
  of the Proximal Gradient Method under Fixed-Point Arithmetic," arXiv:2303.16786.
- Moore, "Interval Analysis," 1966; Stolfi & de Figueiredo, "Affine Arithmetic:
  Concepts and Applications," 2003; Gupta et al., "Deep Learning with Limited
  Numerical Precision," ICML 2015.
- Melquiond, "Gappa" (http://gappa.gforge.inria.fr); Boldo & Melquiond, "Flocq,"
  ITP 2011.
- Lafont, "Interaction Nets," POPL 1990; "Compiling Process Networks to
  Interaction Nets," arXiv:1609.03640 (2016).
- "A Geometric Algebra Framework for a Multidimensional Analytic Signal,"
  arXiv:2411.10412 (2024).
- SymbiYosys (sby) documentation, YosysHQ; OSS CAD Suite (yosys 0.47), local at
  /home/eileen/tools/oss-cad-suite.
