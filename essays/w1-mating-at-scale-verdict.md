# W1 — THE MATING AT SCALE: verdict

*Experiment Wheel, first formal turn. Station 2 (bench, RTX 4050).
Pre-registered in EXPERIMENT-WHEEL.md before running. Raw: w1-results.json.
Code: w1_bench.py. Station-1 antecedent: seed-canon/papers/mating_verified.py.*

## E1 — scalar mating, 10,000 pairs (pre-registered kill: real-rate < 1%)

| metric | sexual | asexual |
|---|---|---|
| real offspring (tol 0.05) | **432 / 10,000 (4.32%)** | 0 / 10,000 (0%) |
| CPU wall time | 0.67 s | — |
| GPU wall time | 1.48 s | — |

**PASSES the kill gate (4.3% ≥ 1%): the mating advantage compounds at
scale.** The 3/30 (10%) from station 1 was small-sample inflation; the true
tight-tolerance rate is ~4%. Honest correction on record.

**The finding that matters — the tolerance sweep:**

| hand's tolerance | sexual rate | asexual rate | winner |
|---|---|---|---|
| 0.02 (demanding) | 1.65% | 0.0% | sexual, ∞ |
| 0.05 | 4.32% | 0.0% | sexual, ∞ |
| 0.10 | 7.95% | 0.69% | sexual, 11× |
| 0.20 (loose) | 13.8% | **25.3%** | **asexual, 2×** |

**Mating wins exactly when the hand is demanding.** Under tight selection,
cross-iteration is the only path to the target (asexual never reaches it);
under loose selection, cheap mutation wins — no need to leave your own
basin when anything near you passes. The bar conversation (Paper 219's
culture bridge) inherits the sharpened claim: *the bar matters precisely
when the sea is hard.* Easy years favor staying home; hard years are what
the A×B space is for. This is a real, falsifiable, regime-dependent law —
the kind the wheel exists to produce.

**Material note (the doctrine):** GPU was 2.2× SLOWER than CPU at n=10k
(kernal-launch overhead dominates elementwise work) — the 4050 earns its
keep at E2's matmul scale, not E1's. Know your materials; sing in their key.

## E2 — the paper's tanh-net appendix, at scale

Cross- AND self-relevance both 0.0000 at every measured step (1/5/10/50),
10,000 cells, honest random init, target 0.7, tolerance 0.1. A 16-dim 0.1-
ball is simply rare under random dynamics — for both modes. **The paper's
claimed rising-relevance curve (0.000→0.234) does not reproduce and was
presumably a tuned-init artifact.** Second confirmed theater element in
Paper 219's evidence (after the one-pair 30/0). The thesis survives on E1's
honest numbers; the appendix's specific curve is filed negative.

## Wheel dispositions

- E1: PASS → queued for Station 3 (the hand's tolerance bands as a .qm
  table on metal — the selector judging offspring in nanoseconds, and the
  regime law — tight/loose — as two sealable band-sets)
- E2: FILED NEGATIVE (appendix curve; kept in canon with this verdict)
- Meta: the wheel's first turn took one bench script, one pre-registration,
  and produced one confirmed law + one refuted claim + one material lesson.
  The structure pays for itself.
