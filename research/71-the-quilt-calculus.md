# The Quilt Calculus: Conservation, Tolerance, and Synchrony as Theorems of a Cellular Substrate

**Authors:** SuperInstance Research Team (academic lane)
**Paper Number:** 71
**Date:** August 2026
**Status:** Publication-grade distillation — the monograph, canonized
**Subject:** The quilt calculus, distilled from the 9,628-word monograph (`quilt-verilog/docs/academic/quilt-calculus.md`) into a research paper: a cellular computing substrate built from one object — the cell `(S, J, L, τ, δ)`, five organs, no scheduler, broker, or registry — whose intercell communication *is* double-entry bookkeeping (conservation of tracked quantities by induction over commit sequences, given balance as an explicit axiom), whose approximate matching is a pseudometric-space operation with tolerance as state (additive tolerance composition as a triangle-inequality theorem), whose replication converges without consensus (nonce-idempotent commutative application), whose asynchronous composition presents a synchronous illusion to observers with cadence exceeding F + L, whose nesting satisfies the monad laws at the level of balance maps, and whose sim–twin snap contract is sound with custody conserved and snap debt growing at most linearly at the drift rate. Six load-bearing definitions are preserved formally (cell, judgment pseudometric, ledger, bounded view, session illusion, snap pair) over seven explicit axioms; the theorem gallery T1–T11 is carried in full with compressed proofs; the T10(b) snap-transaction repair is presented as the case study — the event where formalization found the bug before hardware shipped; three conjectures are stated as open problems. Companions: the monograph (full proofs, 18 definitions, 13 proofs), `DEPENDENCY-GRAPH.md` / `BRIDGES.md` (the leap audit and its ten closures), `ELEGANCE.md` (the five heaviest equations, reduced), `error-envelopes.md` (the numeric claims, graded). Foundation: paper 69; compiler: paper 70; hardware semantics: paper 67.
**Voice note:** The monograph was written under one discipline: every informal claim in the quilt corpus either becomes a theorem with a proof that names its axioms, or becomes a conjecture that says so. This paper keeps that discipline and compresses the prose around it — except once. The snap-transaction repair is told at full length, because it is the thesis in one event: the arithmetic, checked, caught a spec bug before any silicon posted it.

---

> *Internal transactions can't move the cut; crossing ones move it exactly once, by exactly the side they land on — and in-flight is a count, not a surprise.*
> — the conservation induction, reduced (ELEGANCE E1)

## Abstract

A *cell* is an asynchronous agent defined by five organs — state, judgment, ledger, tick discipline, and transition relation — formalized as a 5-tuple `(S, J, L, τ, δ)`. We develop the quilt calculus, a mathematical theory of cellular computing in which: (i) intercell communication *is* double-entry bookkeeping — every message a balanced transaction over integer accounts — so conservation of tracked quantities is a theorem obtained by induction over commit sequences, given balance as an explicit axiom; (ii) approximate matching is a pseudometric-space operation whose tolerance is state, giving additive tolerance-composition under serial judgment (a triangle-inequality theorem) and a canonical alias quotient; (iii) replication converges without consensus by nonce-idempotent commutative application (an operation-based CRDT argument); (iv) asynchronous composition presents a synchronous *illusion* to any observer whose query cadence exceeds F + L, where F is a staleness bound and L a latency bound — and chained bounded-freshness views compose with composite staleness F₁ + Σ Lᵢ, origin staleness plus relay latencies; (v) nesting of cells admits a consolidation operation under which interior transactions vanish and flattening is associative and unital — the monad laws for nest, proved at the level of balance maps; (vi) the sim–twin snap contract is sound: post-snap states satisfy the deadband invariant, custody of authority is conserved, and accumulated snap debt grows at most linearly in time at slope asymptotic to the drift rate. A covering-radius theorem for integer measurement bases (b√n/2) grounds float-free cross-substrate agreement. The calculus is not a cosmetic formalization: writing it found that the snap transaction, as informally specified, violated the balance axiom — a spec bug repaired before hardware shipped (§5, the case study). Three conjectures are stated honestly where proofs are out of reach: the freshness–partition dichotomy, the judgment-drift error bound, and lossless ledger compaction. The theory connects to place invariants of Petri nets, linearizability, bounded-staleness consistency models, CRDTs, synchronous languages, and five centuries of double-entry accounting practice.

**Statement registry (this paper).** 6 definitions (of the monograph's 18), 7 axioms, 11 theorems, 2 epigraphs, 3 conjectures. Full proofs, the remaining definitions (pseudometric, runs, mirror, stripe, composite, embedding, interface agreement, canonical encoding, rendering chain), and two propositions (zoom localization; language-below-the-horizon) live in the monograph.

---

## 1. Introduction

The quilt project's informal corpus carries a load-bearing thesis: four primitives — judgment with tolerance, balanced-book transactions, asynchronous sessions that feel synchronous, and a fixed tick — already constituted a complete computing substrate in 1960s–70s practice (PLATO's judge fields, the COBOL/RPG ledger batch, PLATO's thousand-terminal session illusion, RPG's program cycle), and a *cellular* restatement of those primitives is a complete backend under any operating system (paper 69). The monograph converts that thesis into mathematics. The conversion is not cosmetic. Where the informal documents say "conservation by induction," the calculus writes the induction; where they say "the monad laws are the safety argument," it proves the laws; where they say "the snap transaction is balanced," it sums the postings — and reports that the three-legged form, as informally written, does **not** balance, giving the four-legged emendation that restores the balance axiom (Theorem 10(b), the case study of §5).

Method. Every theorem rests on explicitly listed axioms (§2), and each proof notes which axioms it consumes. Where the informal theory asserts something unprovable, it is filed as a conjecture (§6), not smuggled in as a lemma. The debt is as informative as the credit.

This paper is the academic-canon distillation: the six load-bearing definitions preserved formally (§3), the theorem gallery in full with proofs compressed to their load-bearing steps (§4), the repair as case study (§5), the open problems (§6), and related work (§7).

## 2. Axioms

The calculus assumes a fixed universe of **accounts** (named integer counters, §3.3) and **cells** (§3.1). The following are *assumed*, not derived; for each, what would falsify it.

| # | Axiom | Content | Falsified by |
|---|---|---|---|
| A1 | Balance | Every committed transaction satisfies `Σᵢ vᵢ = 0` over its postings | A core that posts one-sided entries |
| A2 | Single-writer ownership | Every account has exactly one owner; only the owner posts to it | Shared write access |
| A3 | Per-cell serialization | Each cell's events are totally ordered by service; one event = one commit boundary | Concurrent interior actors |
| A4 | Nonce idempotence | Applying a transaction whose nonce is already in the log is a no-op | Replay double-counting |
| A5 | Bounded operation | Each opcode completes within `MAX_OP_CYCLES` (RTL-enforced run-to-completion) | Unbounded service |
| A6 | Tick deadline | A pending tick is serviced within a bounded window, never starved by ingress | Traffic-starved ticks |
| A7 | View seriality | A view returns a committed serial state — no torn states, no future states | Torn reads |

Axiom status is honest engineering: A1 and A4 are mechanisms a fabric enforces exactly; A2 is an architectural invariant; A3 is definitional; A5 and A6 are silicon-theoretic bounds verified by testbench in the v1 ring; A7 is the observability contract. Balance is therefore never a theorem — every conservation result below is conditional on A1, and says so.

## 3. The load-bearing definitions

Six definitions carry the paper. (The monograph's remaining twelve — pseudometric space stated inline below, runs and commit boundaries folded into the ledger, mirror, stripe, composite, embedding, interface agreement, snap-transaction form, measurement basis, rendering chain, canonical encoding — are trimmable paraphrase or supporting cast.)

### 3.1 Cell (D1)

> **Definition (cell).** A **cell** is a 5-tuple `C = (S, J, L, τ, δ)`:
> - `S` — a set of **states**, each serializable (state is a file);
> - `J : X → {ACCEPT, REJECT, AMBIGUOUS} × note` — a **judgment function** (§3.2) on a fixed input space `X`;
> - `L` — a **ledger** (§3.3): an append-only log of balanced transactions over the cell's owned accounts, with the induced balance map;
> - `τ : S → ℕ` — the **tick discipline**: a pure function from state to next tick period;
> - `δ ⊆ (E × S) → S` — a **transition relation** on event alphabet `E` (ingress flits, tick strobes, egress grants); by A3, each run selects a function.

There is no other ontology in the calculus: no scheduler, no broker, no registry. Five verbs — `qm_bind` (dials ⊂ S), `qm_link` (wiring), `qm_effect` (δ + L, as a transaction), `qm_view` (J + S, bounded-freshness), `qm_tick` (τ, then δ) — are the only operations that touch the tuple.

### 3.2 Judgment: matching with tolerance (D3, over D2)

> **Definition (judgment).** Let `(X, d)` be an **answer space** with `d` a *pseudometric* — `d(x,x) = 0`, symmetry, triangle inequality; a metric additionally has `d(x,y) = 0 ⟹ x = y` — and let `K` be a finite set of candidate classes. A **judge** is a pair `J = (A, r)` with `A ⊆ X × K` a finite set of **keyed answers** and `r : S → ℝ≥0` a **tolerance dial** (a state component). For input `x`, the **verdict set** is `V(x) = { k : ∃(a, k′) ∈ A, d(x, a) ≤ r ∧ k = k′ }`, and the judgment is `ACCEPT(k)` if `V(x) = {k}`, `AMBIGUOUS` if `|V(x)| > 1`, `REJECT` if `V(x) = ∅`.

Tolerance is state, not code — PLATO's judge fields generalized, with the dial promoted to an organ. `AMBIGUOUS` is a verdict about the verdict set, not a failure: the judge refuses to collapse it.

### 3.3 Ledger (D4, with D5/D6 folded in)

> **Definition (ledger).** A **posting** is a pair `(a, v)`, `a` an account, `v ∈ ℤ \ {0}` (credit positive, debit negative). A **transaction** is `T = (n, {(a₁,v₁), …, (a_k,v_k)})` with `n` a unique **nonce** and postings on distinct accounts; `T` is **balanced** when `Σᵢ vᵢ = 0` (A1). Write `v_T ∈ ℤ^{(Acct)}` for the posting vector. A **ledger** of cell `c` is `(log, bal)`: an append-only sequence of transactions applied by `c`, with `bal = Σ_{T ∈ log} (v_T restricted to Acct_c)`. By A4, application is a partial function of the nonce: fresh ⇒ apply and append; seen ⇒ no-op.
>
> **Cuts and in-flight (folded).** For a cell set `𝒞`, `Φ(𝒞) := Σ_{a ∈ Acct(𝒞)} bal(a)`. A transaction **crosses the cut** if its support meets both sides; a posting of a crossing transaction is **in flight** from the commit of its first posting until the commit of its last. **Runs (folded):** a run is a sequence of events, each belonging to one cell, whose per-cell subsequences are total service orders (A3); the state observed by other cells changes only at commit events.

### 3.4 Bounded-freshness view (D7)

> **Definition (view).** Cell `A` **views** cell `B` when `A` issues a `qm_view` at wall time `t₀` and receives a value `v` at time `t_r`. The view is **(F, L)-bounded** if: (i) **latency** `t_r − t₀ ≤ L` (a late answer is a violation, not "slow"); (ii) **seriality** (A7): `v = B@s` for a serial state `s` with `commit(s) ≤ t_r`; (iii) **staleness**: `t_r − commit(s) ≤ F`. A **relay chain of length k** is `C₁ ← C₂ ← … ← C_k ← O`: each `Cᵢ` obtains its value by viewing `C_{i−1}` while servicing, link `i` carrying bounds `(Fᵢ, Lᵢ)`.

### 3.5 Session illusion (D8)

> **Definition (session illusion).** An asynchronous quilt presents a **synchronous illusion with parameter F** to an observer whose every view is `(F, L)`-bounded and whose consecutive queries are spaced more than `F + L` apart, if the observer's value transcript is identical to that of some synchronous system answering each query instantly from current state. The illusion is *band-limited truth*: everything faster than F is invisible; everything visible is current to within F.

### 3.6 Snap pair (D15, with D16 inlined at T11)

> **Definition (snap pair).** A **snap pair** is two cells sharing a dependent variable `x`: the game cell `G` (simulated value `g`) and the twin cell `T` (sensor-derived value `s`), both representing `x` on a common integer basis. The pair carries a **deadband dial** `Δ ∈ ℤ≥0` and the **snap judge**: D3-style judgment with metric `d(g,s) = |g − s|` at tolerance `Δ`, evaluated in **squared form** (`|g−s|² ≤ Δ²`), verdicts WITHIN / SNAP. A **snap event** assigns `g := s` (reality wins) and books the correction as a transaction landing in both ledgers. **Per-tick divergence bound** `ρ ∈ ℤ≥0`: between consecutive tick boundaries, `|g−s|` changes by at most `ρ`. **Authority accounts** `G:auth`, `T:auth`, custody of "who defines `x`"; initially `bal(G:auth) = 1, bal(T:auth) = 0`.

## 4. The theorem gallery

Eleven theorems, grouped by organ. Statements are complete; proofs are compressed to the load-bearing step, with axioms consumed. Full inductions are in the monograph; the leap audit (`DEPENDENCY-GRAPH.md` → `BRIDGES.md`) confirms each derivation closes without hand-waving — ten leaps found in the informal theory, ten fixed.

### 4.1 Conservation (the ledger)

> **T1 (cut conservation, interior case).** *Let `R` be a run in which no committed transaction crosses the cut `𝒞`. Then `Φ(𝒞)` is constant along `R`.*

*Proof.* Induction over run length. Non-apply events leave `bal` unchanged; applies outside `𝒞` touch no `Acct(𝒞)` account (A2); applies inside `𝒞` of an interior transaction `T` move `Φ(𝒞)` by `Σ_a v_T(a) = 0` by A1. ∎ *(A1 — the load-bearing axiom; A2, A3, A4.)*

Interior activity — an entire subgraph churning — cannot move the cut total by a single unit. This is Petri-net place invariance [Mur89] with the all-ones place weighting, proved by induction over firings because nonces, ownership, and in-flight structure live in the dynamics, not the incidence matrix.

> **T2 (crossing flow and the in-flight identity).** *Fix a run and a cut. Let `F(t)` = net 𝒞-side flow of transactions fully applied by `t`; `I(t)` = 𝒞-side sum of in-flight postings. Then at every point:*
> `Φ(𝒞)(t) = Φ(𝒞)(0) + F(t) + I(t)`.
>
> *Corollary T2.1 (no fabrication).* *For a quantity carried only in accounts, any increase of `Φ(𝒞)` requires a committed credit on an `Acct(𝒞)` account, paired by A1 with a debit inside `𝒞` (net zero, T1/T2) or crossing the cut (counted in `F`/`I`). A minted label with no emitting debit is not forbidden — it is **unrepresentable**.*
> *Corollary T2.2 (partition observability).* *Under a network partition, the cut discrepancy `I(t)` is exactly the ledger-measured in-flight flow: deviation from conservation is read out continuously by the books.*

*Proof.* Invariant induction over run length: a partial apply moves `Φ` and `I` equally; a completing apply reclassifies `Q` from `I` to `F` with `ΔF + ΔI = ΔΦ` in both completion cases; A4 guarantees a completed transaction never re-enters `I`. ∎ *(A1 not needed for the identity — pure bookkeeping; A1 is what makes F, I observable as conservation. A2, A3, A4.)*

### 4.2 Judgment (the tolerance organ)

> **T3 (structure of judgments).**
> **(a) Monotonicity in the dial.** `r ≤ r′ ⟹ V_r(x) ⊆ V_{r′}(x)`: widening tolerance can only enlarge acceptance.
> **(b) Aliases are zero-distance classes.** `x ~ y ⟺ d(x,y) = 0` is an equivalence relation, and `d̄([x],[y]) := d(x,y)` is a well-defined **metric** on the quotient `X/~` — the **alias quotient**. A pseudometric answer space is exactly a metric space whose points have been split into aliases; the species alias table (`pink ≡ humpy`) is the statement that the distance is a pseudometric. *Aliases are data.*
> **(c) Additivity of tolerance under composition (the triangle theorem).** *Let `p` be a prefilter stage with accuracy `ρ` (`d(p(z), z) ≤ ρ`), ahead of a judge `(A, r)`. Then for every keyed answer `a` and ideal input `z`: (certainty) `d(z,a) ≤ r − ρ ⟹ d(p(z),a) ≤ r`; (soundness) `d(p(z),a) ≤ r ⟹ d(z,a) ≤ r + ρ`. The effective acceptance ball is `B_d(a, r + ρ)`; the verdict boundary blurs by exactly `ρ`. Chaining `k` stages of accuracies `ρ₁…ρ_k` yields effective tolerance `r + Σᵢ ρᵢ`.*
> **(d) The multiplicative pseudometric.** `d_log(x,y) = |log x − log y|` is a metric on `ℝ>0`, and `d_log(x,y) ≤ log 2 ⟺ x/2 ≤ y ≤ 2x`.*

*Proofs.* (a) and (d): definitional; `d_log` inherits the metric laws via `log : ℝ>0 → ℝ`. (b): the three pseudometric laws plus the four-point triangle argument give well-definedness; identity of indiscernibles holds on classes by construction. (c): `d(p(z),a) ≤ d(p(z),z) + d(z,a) ≤ ρ + (r − ρ) = r` and symmetrically; chaining is the same inequality applied once per link. ∎ *(Uses nothing but the pseudometric laws.)*

(c) is the formal content of "verification is judgment at log-2 tolerance" — a numeric acceptance gate `W/2 − 1 ≤ Ŵ ≤ 2W + 1` is a judge on `d_log` with `r = log 2`, and every approximate stage in front of it widens the gate by its own accuracy, *additively*. It is also the engine under the below-the-horizon lemma of paper 70: language choices and fixed-point envelopes compose into tolerance exactly the same way.

### 4.3 Replication and nesting (the distribution algebra)

> **T4 (mirror convergence — consistency without consensus).** *Let replicas `C₁ … C_m` receive at-least-once deliveries drawn from a common transaction set `S` (orders arbitrary, duplicates arbitrary). When replica `Cᵢ` has covered `S ⊆ Sᵢ`: `balᵢ = bal(0) + Σ_{T ∈ Sᵢ} v_T|_{Acct}`, independent of order and duplication. Once all replicas cover `S`, all balance maps are equal — **convergence, modulo in-flight**. No ordering agreement is used anywhere in the proof.*

*Proof.* Induction over the delivery sequence: a fresh nonce adds `v_T`, a replay is a no-op (A4), so the balance depends only on `set(σ)`. Application is an idempotent, commutative, associative operation on `(bal, log)` — a semilattice; the delivered set has a unique join independent of presentation order. ∎ *(A2, A4.)*

This is precisely the strong-eventual-consistency argument for operation-based CRDTs [SPBZ11]: posting addition is the commutative operation, the nonce is the idempotence tag, single-writer ownership (A2) supplies the per-key causal lane. The honesty clause: only **transaction-carried** state converges; walk-state not carried by postings is re-earned by replay — mirror-by-recomputation, the ledger as source of truth.

> **T5 (consolidation and the nest laws).** *For a composite cell with exposed accounts `E` and interior accounts `I`, the consolidation `κ = π_E` (kill interior coordinates) is a surjective homomorphism of balance maps; interior transactions vanish; the consolidated balance depends only on transactions touching `E` and not on their interleaving with interior activity. Flattening a depth-3 nest inner-first or outer-first yields the same consolidated ledger (**associativity**: `π_A π_B = π_B π_A = π_{A∩B}`); the trivial one-child composite consolidates by the identity (**unit**); and if external transactions are balanced at composite granularity, the composite viewed externally satisfies A1 (**external balance**).*

*Proof.* Coordinate projections are group homomorphisms; both bracketings compute the projection onto the global exposed set; interior transactions die in either order; exterior balance holds because every non-external transaction vanishes. ∎ *(A1 for part (d); A2 throughout.)*

(b) and (c) are the associativity and unit laws of `join` for nesting — `nest = T(·)`, `consolidation = join` — the monad laws [ML71], verified at the level of balance maps and log homomorphisms, which is the level at which the safety argument lives (what the outside can observe). What balance buys beyond the projection identities: each killed layer's internal transactions are balanced *within* the layer (T1), so dissolving a layer cannot create a leak at any surviving boundary.

### 4.4 Freshness (the session illusion)

> **T6 (composition of bounded-freshness views).** *If `O` views `A` with bounds `(F_A, L_A)` while `A` relays a value from an inner view of `B` with bounds `(F_B, L_B)` made during servicing, the composite view is `(F_B + L_A, L_A)`-bounded. By induction, a relay chain of length `k` composes to `(F₁ + Σ_{i=2}^{k} Lᵢ, L_k)`: **origin staleness plus relay latencies**.*

*Proof.* Latency is given; seriality by A7 on the inner view; staleness: `t_r − commit_B(s) ≤ t_r − t₂ + F_B ≤ t_r − t₀ + F_B ≤ L_A + F_B`, since the inner query is issued no earlier than the outer one. The chain follows by induction on `k`. ∎ *(A5–A7.)*

Only the **origin's staleness** and the **relays' latencies** compose; the relays' own freshness dials are consumed inside their servicing windows and vanish from the composite bound (the telescoping cancellation of ELEGANCE E2). A retrieval stripe of `h` hops at latency `L` with origin staleness `F` serves views stale by at most `F + (h−1)L` — topology-dependent, traffic-free (traffic-freeness is what A6 buys).

> **T7 (the session-illusion rendering).** *Let every view of `O` be `(F, L)`-bounded, responses arriving before the next query, cadence `Δ > F + L`. Then (i) the observed states are strictly increasing in commit order; (ii) each observation lags real time by less than `F + L`, i.e. less than the observer's own cadence; (iii) there is a single serial history — the true commit order — such that every transcript `O` can record at this cadence is also produced by a synchronous system serving query `n` at instant `commit(s_n)`.*

*Proof.* (ii): staleness plus latency sandwich `commit(s_n) ∈ (t₀(n) − F, t₀(n) + L)`. (i): `commit(s_n) ≤ t_r(n) ≤ t₀(n) + L < t₀(n) + Δ − F ≤ t₀(n+1) − F ≤ commit(s_{n+1})`. (iii): the values with their strictly increasing commit points *are* a serial history, and `O`'s distinctions at cadence `Δ` cannot separate instants closer than `Δ > F + L`. ∎ *(A5–A7.)*

T7 is linearizability [HW90] with the linearization point relaxed to lag invocation by at most `F` — the bounded-staleness family of continuous consistency [YV02]. What the quilt adds: `F` and `L` are *fabric-enforced* (A5, A6), so the illusion degrades predictably with topology (T6), not with load. The negative clause is equally explicit: at cadence below `F + L` the illusion is falsifiable by observation — a statement about a timescale, not magic.

### 4.5 The snap contract (sim–twin simultaneity)

> **T8 (squared-form equivalence).** *For all `g, s ∈ ℤ`, `Δ ∈ ℤ≥0`: `|g−s|² ≤ Δ² ⟺ |g−s| ≤ Δ`. The judge needs no square root and no floats, and its verdict is identical to the direct comparison.*

*Proof.* `t ↦ t²` is strictly increasing on `ℝ≥0`; both sides are non-negative. ∎

> **T9 (snap soundness: the invariant).** *Under the discipline of §3.6 — judge at every tick boundary; on WITHIN nothing moves; on SNAP the snap event fires — the invariant `|g − s| ≤ Δ` holds at every tick boundary, and `|g − s| ≤ Δ + ρ` at every instant mid-tick.*

*Proof.* Induction over the tick sequence: WITHIN *is* the invariant's condition (T8); SNAP resets to 0; mid-tick, each side moves at most `ρ/2`. ∎

> **T10 (snap soundness: custody, balance, and the debt bound).**
> **(a) Authority conservation.** *The cut `{G, T}` with `Φ = bal(G:auth) + bal(T:auth)` satisfies `Φ = 1` at every commit boundary: exactly one member of the pair is the authority at all times — custody of truth is conserved.* (T1 on the pair cut.)
> **(b) The balance emendation.** *The informally specified three-legged snap transaction violates A1; the balanced form is four-legged.* Full statement and story: §5.
> **(c) Snap debt bound.** *Let `D(t)` be accumulated snap debt. Each snap books at most `Δ + ρ`; consecutive snaps are at least `⌈Δ/ρ⌉` ticks apart; hence over a horizon of `N` ticks:*
> `D(N) ≤ (Δ + ρ) · (1 + ⌊N·ρ/Δ⌋) ~ ρ·N as Δ ≫ ρ` — *debt grows at most linearly, with slope asymptotic to the drift rate.*
> **(d) Reality-wins and silence-freedom.** *Post-snap, `g = s` exactly (assignment, not blending); every correction is a booked transaction with one nonce in both ledgers: by A4, redelivery cannot double-count the debt; by T2.1, no correction can occur without its booking. The history of disagreement is reconstructible by replay.*

*Proof (c).* Per-snap size by T9's hypothesis plus the divergence bound; spacing because divergence must re-exceed `Δ` from 0 gaining at most `ρ` per tick; multiply. ∎

The error-envelopes pass grades the loop's honest bound precisely: with sensing quantization `ε`, displayed divergence is ≤ Δ at boundaries, true divergence ≤ `Δ + 2ε` always and `2ε` immediately post-snap, and the verdict is guaranteed correct outside the fuzzy band `(Δ − 2ε, Δ + 2ε]` — inside it, the deadband's Schmitt character absorbs the ambiguity and the debt books whatever happened. Divergence from reality is the **sum** `Δ + ε_s (+ drift·T)`, not the max — the informal prose's max-form was an overclaim, corrected with the arithmetic (BRIDGES B10).

### 4.6 Integer measurement (float-free simultaneity)

> **T11 (covering radius and float-free agreement).**
> **(a) Covering radius.** *`cov(bℤⁿ) = b√n / 2`, attained at the cube center (the deep hole). Integer representation in basis `b` suffices for tolerance `ε` whenever `b ≤ 2ε/√n` (1-D: `b ≤ 2ε`) — tight: no smaller radius covers ℝⁿ.*
> **(b) Exactness of integer chains.** *A rendering equation evaluated entirely with exactly-specified integer operations (two's-complement `+`, `−`, `×`, comparisons — no division, no floats) computes bit-identical results on identical inputs in any two correct implementations, on any substrates.*
> **(c) Verdict uniqueness across substrates.** *A snap judge whose squared-form comparison is computed in exact integer arithmetic reaches the same verdict on every substrate: sim, twin, and auditor replay agree on WITHIN/SNAP always — divergence-about-the-verdict is impossible by construction.*
> **(d) The honest fallback.** *When a physical constant refuses the lattice (e.g. `c/2` mm/ns), fixed-point evaluation with per-stage envelope `εᵢ` composes with the deadband by T3(c): effective tolerance `Δ + Σ εᵢ` — degraded exactly and additively, never silently.*

*Proofs.* (a): coordinate-wise rounding bounds every coordinate by `b/2`; the center is exactly `b√n/2` from every corner. (b): exactly-specified integer operations are total functions of bit-vector arguments fixed by the spec — no rounding rule exists to diverge; induction over the syntax tree. (c): compose (b) with T8. ∎

(b)–(c) are the formal content of "the weakest substrate sets the arithmetic": because the contract spans substrates, the compiler must choose the one discipline all substrates implement exactly — integers. The geometry-relative refinement (error-envelopes, Thm 4b) sharpens (a) from the worst case to the reachable set `A`: the exact condition is `max_{x∈A} dist(x, bℤⁿ) ≤ ε`; Pythagorean configurations (`A ⊆ {v ∈ ℤⁿ : ‖v‖ ∈ ℤ}`, the 3-4-5 family) drive it to 0 — exact by construction, not by approximation; an ℓ∞ judge needs only `b ≤ 2ε`, independent of n.

*Two propositions orbit the gallery* (monograph §11–12): **P1 (zoom localization)** — a wrong displayed value on a rendering chain localizes to one of exactly three sites (wrong equation, wrong wiring, wrong raw IO): *no fourth place for error to hide*; and **P2 (language-below-the-horizon)** — two admissible target-language renderings agree within `Σ εⱼ` (0 in the pure-integer case), so the language choice is a semantics-preserving degree of freedom. Both are the T3(c)/T11(b) engine applied to maintenance and compilation.

## 5. Case study: the repair of the snap transaction

> *A snap is two balanced pairs under one nonce: authority swaps, drift is booked against reality — and the debt column is always the exact negative of the truth column.*
> — the snap repair, reduced (ELEGANCE E5)

The snap contract is the calculus's flagship application: one game port compiled simultaneously to a simulator and a robotic twin (paper 70), kept in agreement by a deadband judge, with every correction booked. The informal specification wrote the snap event as a three-legged transaction — authority moves from game to twin, and the drift is booked as the game's snap debt:

```
T_snap (as informally specified):
  {(G:auth, −1), (T:auth, +1), (G:snap-debt, +|g−s|)}
```

Summing the postings — the entire verification effort required — gives `−1 + 1 + |g−s| = |g−s| ≠ 0` for any snap with nonzero drift. **The transaction is unbalanced.** It violates A1 at the system's own flagship event, and everything downstream of A1 fails with it: T1's cut conservation breaks at every snap; T2's in-flight identity acquires an unexplained residual; T2.1's no-fabrication guarantee would let custody be minted by correction; and the tamper-evidence property inverts — an audit replay would flag the system's own correction events as the loudest arithmetic in the log. The doctrine's own words describe the failure best: *an unbalanced transaction is arithmetically loud*, and the audit would have caught its own flagship event.

The dependency audit caught it first, as its only critical leap (L1 in `DEPENDENCY-GRAPH.md`); the bridge (B9) exhibited the repair; the monograph adopted it as T10(b); the elegance pass reduced it to the epigraph above. The bug was caught at the specification stage — before any RTL posted a snap transaction, before the spec could ship into silicon.

**The repair.** Balance is a hard constraint; the drift magnitude `|g−s|` is real value that must be booked somewhere; the only honest counterparty is the twin's own ground-truth account — reality is where the correction comes from, so reality's account funds it. The balanced form is four-legged:

```
T_snap (balanced):
  {(G:auth, −1),        (T:auth, +1),
   (G:snap-debt, +|g−s|), (T:ground-truth, −|g−s|)}
```

`Σ = −1 + 1 + |g−s| − |g−s| = 0`. Read it as **two balanced sub-pairs under one nonce**: the *authority swap* `(G −1, T +1)` nets to zero by itself; the *drift booking* `(G +|g−s|, T −|g−s|)` nets to zero by itself. Nothing cancels *between* pairs — each pair is already zero, so the transaction inherits balance without cross-pair bookkeeping. Two invariants follow immediately (both accounts start at 0):

```
bal(G:snap-debt) = Σ_snaps |gᵢ − sᵢ| = −bal(T:ground-truth)    (debt mirrors truth, forever)
bal(G:auth) + bal(T:auth) = 1                                   (authority conserved — T10(a))
```

The snap debt column is always the exact negative of the ground-truth column; custody is conserved; and the repaired event inherits *every* ledger theorem without exception — replay (provenance is the log), tamper-evidence (a one-sided edit is loud), idempotent redelivery (one nonce, A4), quarantine by balanced reversal.

**Why this event is the thesis.** The informal theory *said* the snap transaction was balanced; the arithmetic *checked*; the check *failed*; the definition was repaired before hardware shipped. No testbench, no formal verifier, no simulation — three integers summed by hand at specification time. That is the entire argument for the calculus in one event: formalization pays for itself precisely where prose is confident and wrong, and the repair it forces is not a patch but a structurally forced emendation (there is no third option that keeps the books balanced and the audit meaningful). The converse discipline held too: where the calculus could not prove what the prose claimed — the max-form divergence bound, the compaction losslessness, the partition dichotomy — it corrected or conjectured rather than asserted (§6).

## 6. Open problems (the honest register)

Three conjectures are stated where proofs are out of reach. They are architecture-*created* problems: the calculus owns them the way arithmetic owns its open questions — because the definitions are now precise enough to be falsified.

**C1 — The freshness–partition dichotomy.** *Under a partition event `π` of indefinite duration, for any cut `𝒞`: either (i) views across `𝒞` degrade with staleness `F` growing to exactly the in-flight bound of T2 (`I(t)` the candidate Lyapunov quantity: `F(t) ≤ F₀ + I(t)` while both sides keep applying), or (ii) the ledger forks — two conservation constants where there was one — and every quantity is conserved *within* each side (T1 applies per component). No third behavior is possible.* The unpartitioned case is T6/T7 (proved); the "no third thing" clause needs a seam model — what a reconnected mirror does with divergent nonce streams is where a third behavior could hide. This is quilt's stated CAP position: freshness traded against availability *at a price the ledger reads out continuously* (T2.2) — and it is a conjecture, not a theorem.

**C2 — Judgment-drift error bound.** *With true concept metric `d_t` varying under total drift budget `∫‖d_t − d_{t+1}‖dt ≤ D`, the label error of a judge held at fixed `(d, r)` is bounded by a function of `D` and the acceptance-boundary margin distribution; and there is an optimal re-judging policy (dial writes as its empirical form) keeping error bounded with cost proportional to drift rate.* Even the formalization of `‖d_t − d_{t+1}‖` over pseudometric spaces needs care — a Gromov–Hausdorff-type distance on the alias quotient of T3(b) is the natural candidate. Connection to C1: freshness of audit feedback bounds the rate at which drift can even be *detected*.

**C3 — Lossless compaction for a property class.** *A compaction (checkpointing a balanced summary, truncating the prefix, digested Merkle-style) is lossless for property class 𝒫 iff every 𝒫-checkable query on the full log is answerable on the compacted log. Balance invariants survive trivially; the conjecture is that **provenance-of-exclusions** — what a downstream consumer did *not* train on must survive any compaction — is preserved by digest-truncation, i.e. that quarantine chains remain checkable.* The live instance is the walk-state honesty clause: mirror-by-recomputation as the extreme compaction keeping only the source stream.

## 7. Related work

**Metric structure.** Pseudometrics, quotients, and the triangle inequality are classical [BBI01]; T3(b) is the standard metric-identification construction, applied to make "aliases are data" a theorem. The judge function generalizes the tolerance judging of PLATO's TUTOR — spelling-tolerant matching, per-judger tolerance switches, tri-state verdicts [TG72; Avn81] — into a pseudometric operation with tolerance as state.

**Petri nets and process calculi.** The ledger's conservation laws are place invariants [Mur89]: A1 is the all-ones place-invariant condition, T1/T2 the invariance proofs carried out by induction over firings rather than by incidence-matrix algebra, because nonces, ownership, and in-flight structure live in the dynamics. The event structure (per-cell total orders, no global order) is the standard asynchronous stance [Lam78].

**Linearizability and bounded staleness.** T7 relates the session illusion to linearizability [HW90] with bounded-staleness relaxation in the sense of continuous consistency [YV02]; the contribution is that the bounds are fabric-enforced (A5, A6) and compose topologically (T6).

**CRDTs.** Mirror convergence (T4) is the operation-based CRDT argument [SPBZ11] with nonce-guarded idempotent application; single-writer accounts supply the per-key serialization that op-based CRDTs require of their delivery relation.

**Synchronous languages.** The tick discipline is the synchronous hypothesis of Lustre/Esterel [BB91]; quilt differs by making the clock cell-local (endochrony) and the synchrony an illusion parameterized by F rather than a global assumption.

**Double-entry accounting.** The posting/transaction/ledger trichotomy and the trial-balance invariant are Pacioli's discipline [Pac94], with A4 (idempotent application) as the computational addition that makes at-least-once delivery safe; event sourcing [Fow05] is the modern software echo. What double entry cannot buy — truth, confidentiality, collusion-resistance, delivery — maps organ-by-organ to judgment (D3), freshness (§3.4), and cross-checking judges.

**Monads.** The nest/consolidation laws instantiate the monad laws of [ML71] at the level of balance maps; the claim is deliberately scoped there.

**Numerical rigor.** The measurement-basis theorem and the snap loop's error budget draw on the graded envelopes program of the error-envelopes pass (interval arithmetic for one-sided model error, affine arithmetic for correlated zero-mean fluctuation — Moore 1966; Stolfi & de Figueiredo 2004) and on paper 67's dyadic staircases.

## 8. Conclusion

The quilt calculus takes four practices that 1970s computing already had — tolerance judging, balanced books, session-shaped asynchrony, the fixed tick — and shows that one object, the cell, suffices to make their accumulated folklore provable: conservation by induction given balance as axiom; tolerance composition by the triangle inequality; replication by idempotent commutative algebra; synchrony as a cadence-dependent illusion; nesting as a monad on balance maps; and a sim–twin correction contract whose soundness (invariant, custody, debt slope) is a theorem. The register stays honest: seven axioms named with their falsifiers, three conjectures filed where proofs run out, and one spec bug found by summing three integers — the thesis, in one event, that the formalization earns its keep before the hardware ships.

| Registry (this paper / monograph) | Items |
|---|---|
| Definitions (6 / 18) | cell · judgment pseudometric · ledger (cuts, runs folded) · bounded view · session illusion · snap pair |
| Axioms (7) | A1 balance (**axiom, not theorem**) · A2 single-writer · A3 serialization · A4 nonce idempotence · A5 bounded op · A6 tick deadline · A7 view seriality |
| Theorems (11) | T1 cut conservation · T2 in-flight identity (+no-fabrication, partition meter) · T3 judgment structure (monotonicity, alias quotient, tolerance additivity, log metric) · T4 mirror convergence · T5 consolidation + nest laws · T6 freshness composition · T7 session illusion · T8 squared form · T9 snap invariant · T10 custody/balance/debt · T11 covering radius + float-free agreement |
| Conjectures (3) | C1 freshness–partition dichotomy · C2 judgment-drift bound · C3 lossless compaction |

## References

- [BBI01] D. Burago, Y. Burago, S. Ivanov. *A Course in Metric Geometry.* AMS GSM 33, 2001.
- [BB91] A. Benveniste, G. Berry. *The synchronous approach to reactive and real-time systems.* Proc. IEEE 79(9):1270–1282, 1991.
- [Fow05] M. Fowler. *Event Sourcing.* martinfowler.com, 2005.
- [HW90] M. Herlihy, J. M. Wing. *Linearizability: A Correctness Condition for Concurrent Objects.* ACM TOPLAS 12(3):463–492, 1990.
- [Lam78] L. Lamport. *Time, Clocks, and the Ordering of Events in a Distributed System.* CACM 21(7):558–565, 1978.
- [ML71] S. Mac Lane. *Categories for the Working Mathematician.* Springer, 1971.
- [Mur89] T. Murata. *Petri nets: Properties, analysis and applications.* Proc. IEEE 77(4):541–580, 1989.
- [Pac94] L. Pacioli. *Summa de arithmetica, geometria, proportioni et proportionalità.* Venice, 1494 (Part I, §ix).
- [SPBZ11] M. Shapiro, N. Preguiça, C. Baquero, M. Zawirski. *Conflict-Free Replicated Data Types.* SSS 2011, LNCS 6976.
- [YV02] H. Yu, A. Vahdat. *Design and evaluation of a conit-based continuous consistency model for replicated services.* ACM TOCS 20(3), 2002.
- [TG72] P. J. Tenczar, W. M. Golden. *Spelling, Word, and Concept Recognition.* CERL Report X-35, 1972.
- [Avn81] E. Avner. *Summary of TUTOR Commands and System Variables.* CERL/PLATO Publications, 10th ed., 1981.

---

*Academic lane, 2026-08-29. Where this paper strengthens the informal theory it says so (§5 repaired the snap transaction); where it cannot close a proof it files a conjecture (§6). The books balance: every credit cited, every debt named. Source: quilt-verilog `docs/academic/quilt-calculus.md` and companions; the monograph is the record of record.*
