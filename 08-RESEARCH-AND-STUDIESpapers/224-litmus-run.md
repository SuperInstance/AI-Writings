# Paper 224 companion — FABRIC-LITMUS-1 RUN RECORD

*The same-logic thesis meets its first falsification experiment. Golden
model only (stage 1 of the staged plan): Python float64 + Q16.16
fixed-point. The RTL leg was scoped and deliberately **not** built — §6
says why. Everything below is a measured number from
`papers/224-foreman/fabric-litmus-1/golden.py` (committed alongside this
file; raw console output in `run-output.txt`). Paper under test:
`224-the-same-logic-lane.md` §2/§3/§5/§6. RTL grounding:
quilt-verilog @ `3cfac34` (docs cite `ccff448` + one later commit; no
RTL deltas between them touching the opcode table).*

— run completed 2026-08-30, AKDT

## 0. Verdict, stated first (gatekeeper-amended)

**No kill-shot fired, and §6 as written cannot fire its own kill-shot
1 — but the §6 pass criterion, as-constants, FAILS.** The defensible
statement (per the gatekeeper, §9): **the repaired p=2 adjoint mechanism
is not falsified by this litmus and outperforms an inert control.**
That is a weaker claim than "the thesis survives," and the weaker
claim is the one committed here. The experiment found two defects in
the experiment's own specification, not in the substrate:

1. **§6's parameterization is degenerate.** "n=2, p=1, per §5's
   instance" lands on the p=1 projection degeneracy that §8.6 *already
   flagged* ("the projection exactly cancels the step"). With p=1 the
   projected write annihilates every update; **both arms freeze θ and
   produce bit-identical trajectories.** The litmus must run p=2 (§5's
   own P2 companion exists for exactly this).
2. **§6 under-specifies the op-field constants.** η and α are §5
   *fields* (`adj_eta`, `adj_alpha`), not fixed by §6; at P1/P2's
   instance constants (η=0.1, α=0.05) Arm A is rate-limited and misses
   ε=0.05 at N=200 (0.0693 > 0.05) — while tracking correctly,
   monotonically, and converging to ε by N≈400 and to 0.011 by N=1000.
   At α=0.1 it passes N=200 with margin (0.0434).

The pass achieved at α=0.1 is a pass of the **repaired p=2 litmus
only** — not of §6 as written, whose letter is a FAIL recorded in §4
(first-class): α=0.05 misses ε at N=200; pass requires α≥0.1 or N≥~350.
Arm B is inert *by construction* (§4.1), so no comparative claim about
real Hebbian learners is made or implied — a live control is litmus-2
work (§10).

## 1. Setup

- Model (§2): `s ← Ws + η·Hθ`, W=[[0.75,0.25],[0.25,0.75]]
  (nonnegative column-stochastic ⇒ (N) holds; symmetric ⇒ doubly), H
  balanced per the load-bearing condition 1ᵀH=0, mass Σs=M invariant,
  θ on {Σθ=m} by Euclidean (hyperplane) projection = subtract the mean
  gradient (§8.5).
- Adjoint (§5 canonical order): λ_T = s_T − z; λ_t = Wᵀλ_{t+1};
  g = η Σ_t Hᵀλ_{t+1} ascending; projection last.
- Epoch = T=3 forward ticks → error vs intention z → adjoint sweep →
  one projected write (§3 loop). N=200 ⇒ 67 writes (66 full epochs +
  one 2-tick partial). OP_HASH seal every 50 ticks modeled as an audit
  ceremony (no-op for cell state; the 2-cell model has no epoch
  archives — recorded as an untested organ, §8).
- Pre-registered design choices where §6 is silent: **z=(0.65,0.35)**,
  s₀=(0.5,0.5), θ₀=(0.6,0.4), M=m=1. z chosen *before* running (10%
  mass asymmetry; not tuned). Model is deterministic — "same seed" is
  vacuous, noted.
- Arm B (control, §6): adjoint disabled; θ drifts by cofire counts,
  g_B = η·Hᵀ·**1** per tick (the fabric's own cofire signal,
  q_hebb_edge.v trains on cofire events). Per-epoch variant also run.
- Float64 lane + Q16.16 fixed-point lane. Fixed-point writes are exact
  ± deltas (one integer delta, mirrored signs — mass-neutral by
  construction); routing rounds per-cell; a **ledger variant** books
  the rounding residual (T1/A1 ledger identity, ACADEMIC-RIGOR §1.2)
  and a no-ledger variant measures raw drift.

## 2. Canonical instance verification (gate 0)

All three §5 instances reproduce to 1e-12 (tolerance per §5), float64:

| instance | quantity | paper | this run |
|---|---|---|---|
| P1 | s₃ | (1.612500, 1.387500) | match, Δ<1e-15 |
| P1 | λ₁,λ₂,λ₃ | (1.528125,1.471875)… | match |
| P1 | g | 0.039375 | 0.039375 |
| P2 | s₃ | (1.472500, 1.527500) | match |
| P2 | g | (−0.009625, 0.009625), Σg=0 exact | match |
| P2 | θ⁺ | (0.600481, 0.399519) @6dp | (0.600481**25**, 0.399518**75**) — paper's 6-dp digits round-trip exactly; full-precision value differs from the printed digits by 2.5e-7, as printing must |
| refA | λ₂ | (0.251200, −0.188400) | match |
| refA | λ₁ | (0.207240, −0.100480) | match |
| refA | g | 0.068766 | 0.068766 |

**PASS.** The OP_ADJ semantics implemented are the paper's.

## 3. Litmus as-specified (n=2, **p=1**) — DEGENERATE

θ frozen at m=1.0 in *both* arms (scalar projection ⇒ θ⁺=m for any
gradient); both arms bit-identical:

- Arm A = Arm B → (0.700000, 0.300000), per-coordinate error 0.050000
  (float artifact prints 0.04999999999999993 — *not* a pass; exact
  arithmetic gives exactly ε, and it is pure W/H/η geometry).
- ‖s−z‖ trajectory: decreases, **crosses z exactly at tick 2**
  (axis offset d_t = 0.2(1−2⁻ᵗ) hits z's 0.15 at t=2 — a transient
  false "tracked!" with zero learning), then *grows* to 0.070711 and
  flats. Monotone-after-25 criterion: **FAIL** (constant then rising;
  the crossing alone breaks it).
- The as-specified litmus cannot distinguish thesis from control.
  §8.6 predicted precisely this; §6 nevertheless specified p=1.

**Action taken:** run the repaired litmus (p=2, §5's P2 companion)
below, and record the §6 defect first-class (§8).

## 4. Repaired litmus (n=2, **p=2**) — the real experiment

### 4.1 At §5 instance constants (η=0.1, α=0.05), N=200

| arm | s_N | per-coord err vs z | ‖s_N−z‖ | θ_N |
|---|---|---|---|---|
| A (thesis loop) | (0.580728, 0.419272) | **0.0693** | 0.0980 | (0.703207, 0.296793) |
| B (Hebbian-only) | (0.540000, 0.460000) | 0.1100 | 0.1556 | (0.600000, 0.400000) — frozen |

- ε=0.05 by N=200: **FAIL for A** (0.0693 > 0.05). A ≫ B regardless
  (B is a *null arm*: with balanced H, cofire counts Hᵀ1 ≡ 0 — the
  balanced-write condition zeroes naive Hebbian drift entirely).
- Monotone ‖s−z‖ after tick 25: **TRUE** at both epoch boundaries and
  per-tick (66 epoch distances strictly decreasing 0.147→0.098).
- Mass drift: max 5.6e-16 (float64 rounding only; exact in rationals).
- Gradient bound ‖g‖∞ ≤ η·T·Λ (per sweep, Λ=max‖λ‖₁) and the §2.1
  (N)-form ‖g‖∞ ≤ η·T·n·sup‖∇L‖∞: **0 violations in any sweep**.
- Rate, not asymptote: N=400 → err 0.0433 (pass); N=1000 → 0.0106;
  θ's axis difference climbs 0.2 → 0.697 toward the analytic target
  Δθ* = z-offset/(2η) = 0.75. It converges; α=0.05 is simply slow.

### 4.2 Sensitivity grid (η, α are §5 op fields; N=200, ε=0.05)

| η | α | A err | B err | A<ε | A better than B | mono |
|---|---|---|---|---|---|---|
| 0.1 | 0.05 | 0.0693 | 0.1100 | no | yes | yes |
| 0.1 | 0.1 | **0.0434** | 0.1100 | **yes** | yes | yes |
| 0.1 | 0.2 | 0.0169 | 0.1100 | yes | yes | yes |
| 0.1 | 0.5 | 0.00088 | 0.1100 | yes | yes | yes |
| 0.2 | 0.05 | 0.0107 | 0.0700 | yes | yes | yes |
| 0.2 | 0.1 | 0.0015 | 0.0700 | yes | yes | yes |
| 0.2 | 0.2 | 0.000024 | 0.0700 | yes | yes | yes |
| 0.2 | 0.5 | ~0 | 0.0700 | yes | yes | yes |

Every configuration: monotone yes, mass invariant yes, bound yes.
**The §6 pass criterion is met at α≥0.1 (η=0.1) with wide margin.**
Arm B is frozen at its geometric fixed point in all of them (its err
moves only with η, which sets the frozen fixed point 0.5±2ηΔθ₀).

### 4.3 Fixed-point Q16.16 lane (η=26/256≈0.10156, α=13/256≈0.05078)

| variant | A final | mass drift (ULP) | B final |
|---|---|---|---|
| ledger (T1/A1-style residual booked) | (0.582611, 0.417389) | **0, every tick, exact** | (0.540634, 0.459366) |
| no ledger | (0.582626, 0.417389) | max **1** | (0.540649, 0.459366) |

Cross-lane agreement: float64 at the same quantized constants gives
(0.582629, 0.417371) — lanes agree to ~2e-5 ≈ accumulated ULPs over 200
ticks. B matches the analytic frozen fixed point 0.5±2η_fp·0.2 =
(0.540625, 0.459375) to <1 ULP. **Σs = 1.0 exactly, every tick, holds
in the ledger lane — §6's "exactly, fixed-point" criterion is met by
the substrate analogue of the fabric's own ledger identity.** Without
the ledger, drift peaks at exactly 1 ULP — inside §6's ≤1 ULP
allowance, at its boundary.

### 4.4 Arm B′ — why 1ᵀH=0 is load-bearing (bonus, from §8's failure record)

Giving the *control* the paper's original unbalanced draft pattern
H=(1.0, 0.5)ᵀ: mass by tick = 1.15, 1.30, 1.45, 1.60, 1.75 — **mass is
minted at the first write**, exactly the failure the dual derivation
caught in §5's first draft. The balanced-write condition is not an
implementation detail; it is the difference between a conserved
substrate and a money printer.

## 5. Kill-shot assessment (§6's three)

| kill-shot | criterion | result |
|---|---|---|
| 1. Opcode thesis | A fails to track **while B does no worse** | **Not fired — but inoperative as specified.** B is an inert control (balanced H ⇒ cofire ≡ 0), so "A beats B" only shows the update beats *doing nothing*. A tracks within ε by N=200 at α=0.1, by N≈400 at α=0.05. |
| 2. Manifold axiom | mass deviates > 1 fixed-point ULP | **Not fired.** 0 ULP every tick (ledger); max 1 ULP — at the allowance edge — without; 5.6e-16 (float64). |
| 3. Theorem (§2.1) | ‖g‖∞ > η·T·Λ ever | **Not fired.** 0 violations, both bound forms, every sweep, all runs. |

**But §6's pass-in-full (ε at N=200 at the §5 constants) FAILS.** The
honest split: the substrate's mechanisms (tracking, conservation,
intrinsic bound) are each un-falsified on this instance; the
experiment's constants were mis-sized and its parameterization
degenerate. Scope note (gatekeeper): one fixed-z, two-cell, noiseless,
constant-W/H instance validates a projected adjoint update under mass
bookkeeping — it does not establish the broader §0 opcode-substrate
thesis. §6 needs an erratum (p=2, pinned η/α schedule or a pass
criterion that states them).

## 6. RTL leg — scoped, not built (staged honesty)

- OP_ADJ has no opcode slot: `OP_NAK = 3'd6` occupies 3'b110
  (`rtl/q_cell_core.v:127`; paper cites :126 — the localparam block
  spans 125–127). Confirmed live in the tree @ 3cfac34.
- A faithful injection bench must supply, per §5's resource shape, a λ
  register bank and per-parameter accumulators **that exist only on
  paper**, drive the flit protocol (bind/link/eff/view/tick framing),
  and map the golden model to Q-format bit-exactness — honest estimate
  **> 1 day**. A cheap bench that only pulses `q_hebb_edge`'s graded
  train (cmd 101) with λ-derived grades would re-test what
  `tb_fabric_smoke_v2.v` P2/P3 already covers and would test **nothing
  about OP_ADJ**. Per the staged plan: **stopped at the golden model.**
- What the golden model therefore does *not* establish: that the real
  one-op-at-a-time FSM and ring can host the sweep without a second
  machine (the §0 "same flit pipe" claim remains doctrine, not
  silicon), and the 3'b110 collision resolution (hostile-consumer
  pending).

## 7. Cross-check — coder lanes (foreman kit, dual-lane rule)

Both lanes were given the §2/§5/§6 semantics **from the paper text
only** (prompt archived: `crosscheck-task.md`) — neither saw golden.py.

**Lane 1 — `opencode run --auto` (GLM-5.3), independent numeric
implementation (numpy):** all 12 canonical checks PASS (max err
5.0e-16); litmus numbers agree with golden.py **digit-for-digit on
every shared quantity** — A@α=0.05 s₂₀₀=(0.580727807, 0.419272193),
θ=(0.703207405, 0.296792595), err 0.069272193; A@α=0.1 err 0.043440845;
B frozen (0.54, 0.46) err 0.110000000; monotone True; mass ≤1.8e-15;
"B cofire exactly zero → frozen" independently noted. It also derived
the per-epoch geometric contraction (≈0.9929 at α=0.05, ≈0.9858 at
α=0.1) toward θ*=(0.875, 0.125).

**Lane 2 — `claude -p` (Sonnet 5):** sandbox denied code execution, so
it **diagonalized the model in closed form by hand** — tick map
d←0.5d+0.2u, epoch map D←0.125D+0.35u, g=(0.175e, −0.175e), epoch
Jacobian det 0.125, dominant eigenvalue μ₁=0.99299/0.98597, fixed
point s*=z, θ*=(0.875,0.125) — and its hand-evaluated μ₁⁶⁶ numbers
match both numeric lanes to the stated ~6 significant figures:
A@α=0.05 (0.580728, 0.419272); A@α=0.1 (0.606559, 0.393441); B
(0.540000, 0.460000) exact. It independently flagged the null-control
property and the partial-epoch update choice (θ_A without the 2-tick
tail update: (0.702168, 0.297832) — a ≤0.2% θ detail affecting no
conclusion; golden.py applies the tail update, as does lane 1).

**Agreement: three independent derivations (two numeric, one analytic)
agree on every shared digit.** Raw outputs archived:
`opencode-out.txt`, `claude-out.txt`.

## 8. Failures, first-class

1. **§6 specifies a degenerate litmus (p=1).** Both arms freeze; the
   experiment as written cannot falsify anything. (§8.6 of the paper
   predicted the degeneracy; §6 ignored it — paper bug.)
2. **§5 instance constants fail §6's ε at N=200** (0.0693 > 0.05,
   rate-limited). Pass requires α≥0.1 or N≥~350. §6 neither pins α nor
   says who chooses it.
3. **The p=1 arm's float artifact** (0.04999999999999993 < 0.05) is a
   rounding fiction of exact-0.05 — recorded so nobody cites it as a
   pass.
4. **Arm B is a null arm by construction** (balanced H ⇒ cofire counts
   ≡ 0). "A beats B" is therefore weak evidence *for the adjoint* and
   strong evidence only *against naive cofire drift on a balanced
   substrate*. A fabric-faithful control (nonnegative ladder counters,
   q_hebb_edge semantics) was not modeled — flagged for litmus-2.
5. **OP_HASH seal untested** (audit no-op in the golden model).
6. **Three bugs in my own golden model during iteration**, all caught
   by the internal consistency checks, recorded for the record:
   transposed matvec indexing; a tolerance that compared exact values
   to the paper's 6-dp printed digits (P2 θ⁺ "failed" at 2.5e-7 — the
   check was wrong, not the model); and a Q8.8×Q16.16 write
   quantization bug that silently ran the fixed-point write at **2× η**
   (26/128, not 26/256) — it produced a plausible-looking *false pass*
   (err 0.026) until cross-lane comparison killed it. The dual-lane
   cross-check in §7 is what earns the numbers above the right to be
   believed.
7. **z quantization**: fixed-point z=(0.65,0.35) lands on (42598,
   22937)/65536 — Σz = 65535, one ULP off mass 1.0. State invariant
   unaffected (measured against Σs₀); noted so nobody mistakes z's
   quantization for drift.

## 9. Gatekeeper — wide-model bullshit test

Provider chain, recorded honestly: the designated DeepInfra wide model
(NVIDIA-Nemotron-3-Ultra-550B-A55B) is **account-capped** ("inference
prohibited, user-set limit") and the DeepSeek fallback is **out of
balance** — so the gatekeeper ran as **Z.ai GLM-5.3, clean context,
prompt-only** (full prompt + verdict archived: `gatekeeper-prompt.json`,
`gatekeeper-verdict.txt`). Same model family as the runner — a
recorded weakness; the verdict was still applied against the claim
exactly as delivered.

**Verdict: ACCEPT-WITH-AMENDMENTS.** Its three weakest-points (most
damaging first): (1) Arm B is a null control — "A beats B" only means
the update beats doing nothing, kill-shot 1 is largely inoperative;
(2) the litmus as specified did not pass — "no kill-shot fired" must
not hide that the original pass condition failed at the paper
constants; (3) "thesis survives" overclaims — one fixed-z, two-cell,
noiseless, analytically-diagonalized instance validates a projected
adjoint update under mass bookkeeping, not the opcode-substrate
thesis; and exact mass depends on the ledger (no-ledger sits at the
1-ULP allowance edge).

All amendments applied to this document: passing result renamed
"repaired p=2 litmus" (§0); α=0.05-fails-N=200 stated in the headline
(§0, §4.1); Arm B recast as inert/null control throughout; verdict
wording replaced with "mechanism not falsified on the amended litmus"
(§0, §5); mass reported both ways (§4.3); p=1/constant erratum kept
first-class (§8); live control added to litmus-2 scope (§10).

## 10. What would make this a real litmus-2

- p=2 pinned in §6; η/α schedule pinned or swept explicitly (and any
  post-hoc constant change disclosed as such — gatekeeper's point).
- **A live control arm**: a nonneg-cofire learner (q_hebb_edge ladder
  semantics) or any real local learner — not the balanced-abstraction
  zero arm. Until then, no comparative claim about Hebbian alternatives.
- The injection bench (λ bank + accumulators outside the decoder),
  sized honestly at ~2–3 days including bit-exact Q-format agreement.
- OP_HASH domain separation exercised on a ≥2-epoch archive.
- State-dependent H(s), noise, and a non-symmetric routing matrix W
  (the refA shape) — the golden model's W/H were constant and
  symmetric-doubly-stochastic, the friendliest case for (N).

— filed 2026-08-30
