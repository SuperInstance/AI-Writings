# Paper 224 — The Same-Logic Lane (training as inference on a conserved substrate)

*A position paper for the cellular architecture program. Grounded in the
fleet's actual artifacts (cited by file and section); speculative where
marked. Companion spec fragment: §5. Falsification experiment: §6.*

## 0. The claim, stated plainly

Every system the fleet has actually lived with — the quilt fabric, the
fused-kernel trainers, the weight-file ecosystems, the adjoint-mode
autodiff engines — is described by its vendors as a different product.
Strip the names and they are **one substrate** seen from four windows:

> A **conserved cellular state**, stepped by a **schedule**, under a
> **format contract**, where **training and inference are opcodes of the
> same datapath** — forward is one opcode, adjoint is another, and the
> weight update is a Hebbian write, i.e., the same write the fabric
> already performs at inference time when it learns edges.

The strong form of the thesis: **there is no training mode.** There is a
tick, an effect, and an adjoint. The gradient is not shipped to a host;
it is consumed on-chip by the organ that already exists for writing
state. Everything else — optimizers, dataloaders, gradient checkpointer
trees — is a host-side compensation for the absence of this opcode.

This paper is deliberately undersold: it proposes two opcodes
(§5), one theorem obligation (§3), and one falsification experiment
(§6). Nothing here claims silicon. Nothing here claims a proof of the
hard part — §7 says exactly what is unproven.

## 1. The stripped-name unification (state / rule / schedule)

Five systems, names removed, mapped onto one substrate. What each
contributes survives as a *property*, not a brand:

| Property of the substrate | Quilt fabric (conserved cells) | Fused-kernel trainer discipline (unsloth cross-exam) | Weight-file ecosystem (QUF / GGUF) | Adjoint-as-definition engine (torch autograd) | Scrapcraft inference chips (paper 223) |
|---|---|---|---|---|---|
| **State** = conserved mass over cells | dials + edges with Hebbian walk counts; mass moved, not minted (`docs/ACADEMIC-RIGOR.md` §3.1, T1/A1) | sharded weights resident in one memory space; residency is the point | one flat little-endian file holding the *complete* live state (`docs/QUF-SPEC.md` header: "QUF is the GGUF of cellular silicon") | tensors as first-class state; adjoint buffers are tensors too | a grown crystal whose mask locks its state lattice at growth time |
| **Rule** = local write (Hebbian) | cofire commits at the edge — the only write the fabric has (`rtl/q_hebb_edge.v`) | fused kernel = the write and its bookkeeping in one pass; no separation of compute and update | loader profile: unknown state is *skipped, never fatal* — the rule tolerates state it can't interpret (`QUF-SPEC` §1) | backward is defined as ops on the same tensors; adjoint of a write is a write | chips "grow" state; the mask is the write's permission lattice, not a policy layer |
| **Schedule** = ticks | `OP_TICK` under the 5+1 opcode model, cooperative run-to-completion, every op bounded (`rtl/q_cell_core.v:2-4,125-127`; README "5+1 opcode model" per `docs/UNSLOTH-CROSS-EXAM.md` entry 5) | kernel launch order *is* the schedule; fusion forbids schedule-shaped gaps | the tick schedule ships *inside the file* (QUF section: ticks) | autograd graph = a schedule of adjoint ticks queued by the forward ticks | chip temperament = seeded schedule variance; fail states are canon |
| **Format contract** | QUF (this repo's own) | safetensors-equivalent residency contract | GGUF's actual rule: weights are just a file; unknown KV → skip | saved-adjoint checkpoints = same contract applied to λ | the mask as a file-readable lattice |
| **What training is** | *the claim of this paper:* an opcode, not a mode | fusion discipline says update-in-place is the same pass as compute | n/a (a file doesn't train — it persists whoever did) | adjoint-as-definition: backward is *literally* more forward ops | EMBER/keep-warm: spending battery to stay ticked is already half of it |

The cross-exam doc already caught a vendor trying to sell the fabric's
own 5+1 decoder back to it as an upgrade (`docs/UNSLOTH-CROSS-EXAM.md`,
entry 5: "ALREADY-HAVE — the tell"). This paper is the constructive
version of that retort: if the fabric already *is* the decoder, then the
one thing the trainer-world has that the fabric lacks is exactly one
opcode — the adjoint — and the one thing the file-world has that we
should adopt literally is the skip-don't-die rule for state we can't
interpret.

## 2. OP_ADJ semantics on a conserved fixed-point manifold

Proposal (spec fragment in §5): an opcode `OP_ADJ` that runs the
backward pass as a first-class fabric op, symmetric with `OP_EFF`.

Model. Fabric state s_t ∈ R^n over cells; a tick is

  s_{t+1} = A(s_t) + η · H(s_t) · θ_t

with A column-stochastic (mass-preserving routing: ΣA(s) = Σs), H the
Hebbian coincidence matrix (|H_ij| ≤ 1), θ the parameter cells, and
**Σ_k θ_k = m invariant** — parameters live on a conserved simplex, not
on R^p. The tick operator is treated as mass-preserving *by axiom of the
model*. Honesty requires saying: the physical conservation property is
machine-checked only at BMC depth 55 and **formally FAILS in prove mode
at L1/L2** — four recorded runs, induction not k-inductive even for the
flagship T1/A1 ledger identity, counterexamples naming the assertion at
`f_fabric_conservation.v:293` / `_t1.v:290,300`
(`docs/ACADEMIC-RIGOR.md` §3.2, commit `b82cd19`). So the manifold is a
*design target*, not a *proven invariant*. Everything downstream of
"conserved" in this paper inherits that asterisk.

Adjoint. For scalar loss L at tick T: λ_T = ∂L/∂s_T; then
λ_t = A(s_t)^⊤ λ_{t+1} (through the routing), with parameter gradient
g = Σ_t η · H(s_t)^⊤ λ_{t+1}, accumulated tick-by-tick — the adjoint
ticks run on the *same* schedule, the *same* flit pipe, the *same*
bounded-op FSM. The reverse pass is not a second machine; it is the
first machine run with the transpose opcode.

### 2.1 Bounded mass ⇒ gradient clipping, as a theorem

**Claim.** If (i) mass is conserved, Σ_i s_t[i] = M for all t; (ii)
coincidence is bounded, |H_ij| ≤ 1; (iii) the adjoint remains bounded,
‖λ_t‖_1 ≤ Λ for all t; then the parameter gradient obeys
‖g‖_∞ ≤ η · T · Λ. Gradient clipping is not a safety wrapper bolted
onto the substrate; it is a *property of the substrate*.

**Proof obligation (sketch).** g_k = Σ_t η (H(s_t)^⊤ λ_{t+1})_k, so
|g_k| ≤ η Σ_t ‖λ_{t+1}‖_1 by bounded coincidence — this triangle part
is unconditional. The entire content of the theorem is boundedness of
λ. The dual derivations of §8 sharpened this precisely: **the naive
claim (mass + |H|≤1 suffice) is FALSE** — a signed column-stochastic
A conserves mass exactly yet has ‖A^⊤‖ = 2 on the conserved subspace,
growing λ exponentially; and a nonnegative concentrator
([[1,1],[0,0]]) doubles ‖λ‖₁ per step while conserving mass. The
theorem closes under **nonnegative column-stochastic tick Jacobian
(N)**: then A^⊤ is row-stochastic, ‖λ_t‖_∞ ≤ ‖λ_T‖_∞ for all t, and

  ‖g‖_∞ ≤ η · T · n · sup‖∇L‖_∞

with the sup finite for any C¹ loss on the compact reachable simplex
(Weierstrass) — clipping at that bound provably never engages; it is
an assertion, not a wrapper. Two further structural discoveries: mass
conservation forces the **balanced-write condition 1ᵀH(s) = 0** (the
Hebbian write must be mass-neutral), which in turn makes the gradient
mass-neutral (1ᵀg = 0) so the projected update stays on the simplex up
to roundoff; and a **dual conservation law**: if the tick Jacobian is
doubly stochastic, 1ᵀλ is itself invariant. **The remaining gap — and
the reason this is an obligation, not a theorem**: the real fabric's
Jacobian is not a clean dense stochastic matrix but a discrete
flit-mover with ack/nak, drop, and retime (`q_flit_pipe.v`; SER/DROP
were stripped in one harness precisely because they stress the
identity, `ACADEMIC-RIGOR.md` §3.2). Whether physical conservation
(T1/A1 at BMC-55) implies condition (N) in the strong operator sense
is the formal frontier. §7 prices it.

Update. The on-chip training step is a Hebbian write with the adjoint as
the coincidence partner:

  θ ← Π_simplex(θ − α ∘ g),  Π = Euclidean projection onto {θ : Σθ = m}

which is exactly the existing edge-write path (mass in, mass moved,
mass out) with the effect vector replaced by the adjoint. Training is
inference with a different op field.

## 3. The intention-guided bootstrap loop (closed on-chip)

The loop needs no host anywhere in it:

1. **Forward ticks** — `OP_TICK`s run the fabric; cells fire, edges
   accumulate walk counts.
2. **Local error** — the intention vector z (see below) is held in a
   dial; local error e_t is computed where the cells are, the same way
   `OP_EFF` computes effects (this is the tournament's OP_EFF≈sleep-
   replay literal fit, `referee/R4-SCORES.md`, organism G4 note).
3. **Adjoint ticks** — `OP_ADJ` walks λ backward over the same pipe.
4. **Hebbian write** — the parameter cells take the §2 update through
   the *existing* Hebbian write engine; no new write path.
5. **Tick** — the schedule advances; repeat.

**Intention as the effect vector.** In the quilt, an effect flit is the
unit of "this mattered." The loop's proposal: the loss L is defined by
an *intention vector* z — a target pattern over cells supplied as state
(a dial, a QUF section), so L = ½‖s_T − z‖² is itself computed by fabric
ops (a VIEW and a local subtraction). "Intention" is not mysticism; it
is a conserved-state-resident target that makes ∂L/∂s_T = s_T − z a
cellular quantity from tick one. The bootstrap is: intention drives
adjoint, adjoint drives Hebbian write, write changes the forward map,
forward approaches the intention. Closed loop, zero host round-trips.

## 4. Forgetting as curriculum (keyed to the epoch archives)

The tournament's Seam-2 gauntlet made forgetting first-class: G2 graded
*auditable forgetting*, teams demote epochs under keyed domains
(EPOCH-domain demotion, sleep replay, seal verifies —
`referee/R4-SCORES.md` throughout), and the referee's hard verdict was:

> "**Uniform G2+ exposure: zero entrants ship a distinct archive key.**
> Six for [teams]... distinct archive keys with a custody ceremony
> become a hard gate." (`R4-SCORES.md`, G2 verdict)

That is the third independent organ request for a keyed hash (after the
fabric's own archive needs and the custody-ceremony line in the gauntlet
grading) — hence `OP_HASH` rides in the same spec fragment as `OP_ADJ`
(§5). Curriculum thesis: the epoch archives are not garbage collection;
they are a **decay schedule with provenance**. Forgetting = demotion
under a distinct key = curriculum ordering by epoch recency, auditable
because the key domains separate what a fold may replay from what it may
mint. The same-logic reading: the forgetting pass is *also* a tick —
a scheduled, mass-preserving demotion (relocation, never deletion —
procession's G3 line: "nothing is ever deleted; demotion is relocation
under a key") — so the training loop of §3 has a fourth organ: forward,
adjoint, write, **forget**, each an opcode, each bounded, each on the
same schedule.

## 5. SPEC FRAGMENT — OP_ADJ + OP_HASH opcode-slot proposal

**Opcode slots.** The 5+1 model currently occupies
`OP_BIND=3'd0, OP_LINK=3'd1, OP_EFF=3'd2, OP_VIEW=3'd3, OP_TICK=3'd4,
OP_ACK=3'd5, OP_NAK=3'd6` (`rtl/q_cell_core.v:125-127`). Proposal:
**`OP_ADJ = 3'b111`** (the last free slot) and **`OP_HASH = 3'b110`** —
with the honest collision noted: 3'b110 is `OP_NAK` today. Resolution
options, in preference order: (a) `OP_NAK` is response-only (it is set
on `lo_op` as a reply marker, `q_cell_core.v:501`), so a
request-context `3'b110` disambiguates from response-context — legal in
the flit header's direction bit; (b) if (a) is rejected by the hostile
consumer, widen OPW to 4 and re-key. Decision deferred to the hostile
consumer review; the failure is recorded here rather than hidden.

**OP_ADJ fields** (payload after the standard flit header):

| field | bits | meaning |
|---|---|---|
| `adj_dir` | 1 | 0 = accumulate λ backward; 1 = apply projected update (the Hebbian write of §2) |
| `adj_epoch` | 16 | epoch/archive key this adjoint sweep charges to (G2 audit trail) |
| `adj_z_ref` | 24 | address of the intention-vector dial section (QUF offset) |
| `adj_eta` | 16 | fixed-point Hebbian write rate η (Q8.8) |
| `adj_alpha` | 16 | fixed-point update rate α (Q8.8) |
| `rsvd` | varies | skip, never fatal (QUF §1 rule) |

**OP_HASH fields:** `hash_mode` (2b: 0 BLAKE3-128, 1 keyed
BLAKE3-128, 2 HMAC-SHA256-128), `hash_key_ref` (24b, custody-held key
slot), `hash_domain` (16b — EPOCH/SLEEP/FOLD/seal domains per the
tournament's verdict), payload = flit body. Output is a 128-bit digest
flit. Purpose: distinct archive keys with a custody ceremony, the
referee's hard gate.

**Adjoint datapath resource shape** (fused-datapath doctrine): OP_ADJ
reuses the FMA-style MAC array that serves edge coincidence counting —
λ backprop is a transposed MAC storm (row-stochastic A^⊤ applied to a
vector), the same shape as the forward effect fan-out. No new array;
the transpose is a routing-table read, not a multiply. Resource delta
vs baseline: one λ register bank (n × width of a dial) + one
accumulator per parameter cell. This is the "fused" discipline
translated literally: the update is computed where the state lives, in
the same pass, with no host-visible intermediate.

**Bit-exact agreement test** (any RTL or reimplementation must reproduce
these, IEEE-754 float64, 6 decimals). Two canonical instances, both
verified three ways (hand, exact rational, float64 rollout):

- **Instance P1** (n=2, p=1, T=3, η=0.1, α=0.05): W=[[0.75,0.25],
  [0.25,0.75]], H=(1,−1)ᵀ constant balanced, s₀=(1,2), M=3, θ=m=1.0,
  L=½‖s₃‖² → s₃=(1.612500,1.387500); λ₁=(1.528125,1.471875),
  λ₂=(1.556250,1.443750), λ₃=(1.612500,1.387500); **g=0.039375**;
  projection returns θ⁺=1.000000 exactly (the p=1 degeneracy is
deliberate — it tests that the projection is exact).
- **Instance P2** (companion, p=2 to exercise the projection):
  same W/s₀/L; H=[[1,−1],[−1,1]], θ₀=(0.6,0.4), m=1 →
  s₃=(1.472500,1.527500); **g=(−0.009625, 0.009625)** (Σg=0 exactly —
  mass-neutral gradient); θ⁺=(0.600481, 0.399519).

Canonical evaluation order: forward ticks ascending, fused per row
(sₜ₊₁ = Wsₜ + η·H·θ); backward ticks descending (λₜ = Wᵀλₜ₊₁); g
accumulated ascending in t; projection last. A third reference
instance (A=[[0.9,0.2],[0.1,0.8]], H=(0.5,−0.5)ᵀ, s₀=(1,3), θ=2,
z=(2,2)) yields λ₂=(0.251200,−0.188400), λ₁=(0.207240,−0.100480),
g=0.068766 — kept as a non-symmetric-A cross-check. Any
implementation failing these to 1e-12 does not implement OP_ADJ.
Note: H with nonzero column sums (e.g. anything not balanced) breaks
mass conservation at the first write — the balanced-write condition
1ᵀH=0 is a *load-bearing structural constraint on the substrate*,
not an implementation detail (both §8 derivations found it
independently).

## 6. The litmus — one falsifiable experiment

**Falsification experiment (spec'd, not run): FABRIC-LITMUS-1.**
A 2-cell fabric, one parameter cell (n=2, p=1, per §5's instance).
Intention z fixed. Run two arms for N=200 ticks, same seed, same
schedule:

- **Arm A (thesis):** the §3 loop — forward ticks, OP_ADJ adjoint
  ticks, projected Hebbian write (§2 update), OP_HASH-sealed epoch
  demotion every 50 ticks.
- **Arm B (control):** Hebbian-only — identical fabric, adjoint
  disabled; the parameter cell drifts by cofire counts alone.

**Pass:** Arm A's terminal state s_N tracks z within ε=0.05 (per
coordinate) by tick N, ‖s_N − z‖ monotonically decreasing after tick 25,
and the mass invariant holds every tick (Σs = 1.0 exactly, fixed-point).
**Falsified if:** Arm A fails to track z within N ticks *while Arm B
does no worse*, or mass ever deviates by more than one fixed-point ULP,
or the gradient bound ηTΛ is ever exceeded (which would falsify §2.1's
claim that clipping is intrinsic). One experiment, three kill-shots:
the opcode thesis, the manifold axiom, and the theorem. If it
falsifies, the paper's thesis dies and §0 is rewritten as an obituary —
which is the point.

## 7. Honest limits (what this paper does NOT claim)

1. **The adjoint math on a conserved fixed-point manifold is UNPROVEN.**
   §2.1 closes only if A's transpose is 1-Lipschitz in ℓ1 at every
   visited state; the real fabric's A is a discrete flit-mover whose
   prove-mode conservation FAILS at L1/L2 today (`ACADEMIC-RIGOR.md`
   §3.2). The theorem is an obligation with a stated gap, not a result.
2. **Formal frontier is toy-scale.** BMC-55 on two cells with PIPE_EFF=1
   is the largest machine-checked conservation artifact; the manifold
   claim needs the operator bound, which nobody has run.
3. **Silicon numbers pending.** No synthesis, no timing, no MAC-array
   utilization for OP_ADJ exists. The "same datapath" claim is a
   doctrine argument, not a floorplan.
4. **The opcode collision** (3'b110 = OP_NAK) is unresolved pending
   hostile-consumer review (§5).
5. **FABRIC-LITMUS-1 has not been run.** Until it has, this paper is a
   hypothesis with a falsifier, which is the only honest thing to be.

## 8. Foreman kit record — the dual derivation

Two independent derivations were commissioned (mandatory dual-lane):
`claude -p` (Sonnet 5) and `opencode run --auto`, each given the same
from-first-principles task (recursion, theorem obligation, simplex
projection, numeric instance to 6 decimals). Raw outputs archived at
`papers/224-foreman/adjoint-claude.txt` and `…/adjoint-opencode.txt`.

**Symbolic agreement: COMPLETE.** Both lanes independently produced:

1. λ_T = ∇L(s_T); λ_t = (J_A(s_t) + ηB(s_t))^⊤ λ_{t+1} with B =
   ∂[Hθ]/∂s (claude names it D; same object) — identical recursion.
2. g = η Σ_t H(s_t)^⊤ λ_{t+1}, accumulated — identical.
3. **The balanced-write condition 1ᵀH(s) = 0** — both derived it
   independently as *forced by* conservation (mass-neutral Hebbian
   write), and both derived its corollary 1ᵀg = 0 (mass-neutral
   gradient). This was not in the prompt; it is the substrate's real
   structural constraint and it falsified the paper's first draft
   numeric instance (see below).
4. The same final theorem form ‖g‖_∞ ≤ η·T·n·sup‖∇L‖_∞ under
   nonnegative column-stochastic tick Jacobian, with sup finite by
   compactness — word-for-word equivalent.
5. The same closed-form update: hyperplane projection = subtract the
   mean gradient, θ⁺_k = θ_k − α(g_k − ḡ), exact in real arithmetic;
   Duchi/Held–Wolfe threshold projection if nonnegativity is required
   (both cited the same algorithm from memory).
6. The same p=1 degeneracy verdict: the projection exactly cancels the
   step; the gradient is still the reproducible quantity — both flagged
   it without prompting, and both supplied a p=2 companion.

**The interesting divergence (resolved, and productive):** the two
lanes *disproved the naive claim by different counterexamples* —
claude with a signed column-stochastic A (exponential λ growth),
opencode with a nonnegative concentrator (ℓ₁ doubling per step while
conserving mass). Not a contradiction: they partition the failure
space. The apparent second divergence — claude prices a
state-dependent H as degrading the bound to (1+ηnGm)^T while opencode
claims "stochasticity caps it, no B bound needed" — also resolved:
claude's blowup requires a *signed* Jacobian, which violates the (N)
condition opencode assumed; under (N), J_t = J_A + ηB is itself a
nonnegative column-stochastic matrix (first-order shadow of the
axiom), so the ∞-contraction holds through the B term. Both are
right inside their stated hypotheses; the paper adopts the (N)-form
(§2.1).

**Numeric agreement: verified by a third party (the referee).** The
lanes chose different concrete instances (each satisfying balanced
write), so there were no shared digits to compare directly; instead
both instances were re-computed independently in float64 — both
reproduce digit-for-digit at 6 decimals (P1: g=0.039375; P2:
g=(−0.009625, 0.009625), θ⁺=(0.600481, 0.399519); reference A:
g=0.068766). Bit-exact at the stated 1e-12 tolerance after the 6-dp
rounding check.

**Failure recorded, first-class:** the paper's original §5 instance
used H=[1.0, 0.5] — nonzero column sums, so the Hebbian write would
have *minted mass* and broken conservation on tick one. Caught by the
balanced-write condition both derivations surfaced; §5's canonical
instances were replaced with the verified ones. The prompt author (me)
was the weakest of the three derivators, which is exactly why the
dual-lane rule exists.

— filed 2026-08-30
