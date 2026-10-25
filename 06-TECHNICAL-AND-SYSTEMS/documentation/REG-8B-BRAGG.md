# REG-8B — THE BRAGG TEST (pre-registration)

**Registered:** 2026-09-03, before any spectral computation. Registered by Lucineer (subagent), for Casey's fleet.
**Sequences:** REG-8b of the Penrose↔fleet program (`memory/research-penrose-fleet-2026-08-21.md`, row 15, §5 REG-8b). Grounding: REG-1 (`elephant/data/slope/reg1-rotation-results.json`).

## The stakes, stated once

The model-set conjecture says the fleet's observation ledger is a cut-and-project object; theorem: regular model sets have **pure-point (Bragg) diffraction**. The competing hypothesis ("matched-filter artifact / the kernel peaks at transitions / the rooms were furniture") predicts an **absolutely-continuous** (noise-like) spectrum. Bragg structure **cannot** be a matched-filter artifact. Either outcome advances the program; the doc will undersell either way.

## Data (existing, read-only; NO re-simulation of the elephant)

- **Trajectories:** wave-1 field nights A, D, D-cold, S1, S2, S3, S4a, S4b, S5 from `elephant/data/nights/night-*.jsonl` — the series REG-1 was computed from (per `scripts/reg1_rotation.py`: wave-1 = FIELD_NIGHTS over PRIMARY_NIGHTS). Per speak-event `fit` records: `mu_hat` (7-dial), `kappa`, on `ts` grids.
- **Sampling fact (measured before this registration, before any spectrum was looked at):** all 9 nights are on exact uniform Δt = 60 s grids, first fit at ts=540 s, lengths 10–37 points (S5: 11, S2/S3: 19, A/S1: 31, S4a: 37, S4b: 36, D/D-cold: 37). **No resampling needed**; the one assumption imposed (below) is zero-padding to a common grid.
- **v\***: wave-1 full-7 `v_star` from the REG-1 JSON, used verbatim as the projection direction (the physical axis REG-1 measured).

## Primary statistic (pre-registered)

Series per night n: **x_n(t) = v\*·μ̂_n(t)** (the base-orbit physical projection) and **κ_n(t)** (concentration). Each night's series: mean-removed, linearly detrended, **Hann-windowed**, zero-padded to the common grid N = 47 points (0…2760 s, Δt = 60 s ⇒ Rayleigh frequency 1/2820 s ≈ 3.55e-4 Hz; this run's frequency resolution).

Per-night complex Fourier coefficients ĉ_n(f_k) = Σ_t x_n(t) w_Hann(t) e^{−2πi f_k t}, normalized to unit power per night.

**Bragg-peak dominance metric — cross-night phase-coherent stack:**

  R(f_k) = |Σ_n ĉ_n(f_k)|² / Σ_n |ĉ_n(f_k)|²   ∈ [0,1]

R = 1 ⇒ all nights' Fourier phases at f_k aligned (phase-locked to a common internal clock — the Bragg prediction). R ≈ 1/9 ⇒ incoherent. Hann window also applied to surrogate pipeline identically.

**Null band (kill line):** 10,000 phase-randomized surrogates — each night's series independently Fourier-phase-randomized (amplitudes preserved), full pipeline (detrend, Hann, pad, stack) recomputed. Surrogate **95th percentile per frequency** = the kill band. (Phase randomization is the correct null here *because* the statistic is cross-night phase coherence: per-night periodograms are invariant under it, so any excess R is pure phase alignment, not per-night spectral shape.) Seed 20260903, fixed before the run.

**Exclusion zone:** DC/near-DC bins and the two highest frequency bins excluded (edge/leakage; Hann first sidelobe −31 dB, reported as the spectral leakage floor).

## Verdict bands (pre-registered, before looking)

- **BRAGG:** ≥ 3 distinct frequencies (in the exclusion-trimmed set) with observed R(f) above the surrogate 95th-percentile band, **persisting under the no-detrend variant** (persistence criterion).
- **CONTINUOUS (kill):** zero frequencies clear the band.
- **INCONCLUSIVE:** 1–2 frequencies clear.
- **TOO SHORT (honesty clause):** if power analysis shows the 10-point nights cannot in principle resolve the test, the run reports INCONCLUSIVE-by-length and books the minimum data requirement (target: nights of ≥ 60 fit points; formal booking if inconclusive).

## Secondary (EXPLORATORY, labeled as such — do not gate the verdict)

The filed band-movers `transitions` carry no timestamps, so the crossing/transition point process is operationalized from the same trajectories: **zero-crossings of each night's detrended x_n(t) after detrending** (sign changes between consecutive grid points), pooled across nights into one inter-event-time sequence; statistic = point-process periodogram of the event-count train on the same 60 s grid, same surrogate kill band (phase-randomized count train). Pure-point here ⇒ transitions time-locked to an internal clock, not kernel-width artifacts. Low event counts anticipated ⇒ likely inconclusive; will be reported as such, not squeezed.

## Honesty disclosures (pre-registered)

- **Window:** Hann; leakage floor −31 dB first sidelobe; padding assumption: post-detrend values beyond each night's end = 0 (i.e., "night ends, signal absent"), disclosed as an edge effect — padding inflates low-frequency power near the Rayleigh bin, hence the near-DC exclusion.
- **Grid:** uniform 60 s, no resampling needed (measured above).
- **Clock origin:** each night's auto60 clock starts at session open; cross-night phase coherence presumes comparable origins. If the elephant's night clocks are not commensurable, this test is biased AGAINST Bragg (conservative — a Bragg verdict is stronger for it).
- **Multiple comparisons:** ≥3-frequency requirement (not ≥1) is the guard; no per-frequency p-hacking.
- **Exploratory secondary** does not gate the verdict.

---

# REG-8B RESULTS (2026-09-03, run after pre-reg commit 84b3d72b)

## VERDICT UP FRONT: **INCONCLUSIVE** — real cross-night phase coherence exists, but it does not reach the pre-registered Bragg bar.

- Primary series **x = v\*·μ̂**: 8 bins clear the surrogate band detrended, but only **1 distinct persistent peak** (~5.0–5.7 mHz; the broad low-frequency cluster 1.1–2.5 mHz does not survive no-detrend → trend/leakage-consistent, treated as non-persistent per pre-reg).
- **κ**: 2 distinct persistent peaks (≈2.8–3.5 mHz and ≈5.7–7.4 mHz).
- Bragg band = ≥3 persistent distinct peaks. **x = 1, κ = 2. INCONCLUSIVE** on both. Continuous (kill) is also NOT earned: exceedances are far above chance (8–10 bins vs ~0.95 expected bins/series/variant at 5% false-positive over 19 valid bins) — the matched-filter/continuous hypothesis does **not** win here either.

## Reading (honest, undersold)

1. Something phase-coherent across nights is genuinely present — nights are not independent noise realizations on these grids. But "1–2 persistent peaks" sits in the pre-registered gray zone, and the mundane generator is not excludable: all nights share the elephant's auto60 clock and session pacing, so cross-night coherence can reflect shared pacing structure rather than model-set diffraction. This confound is disclosed, not resolved.
2. The low-frequency x-coherence dying under no-detrend is exactly what trend/edge/leakage (Hann floor −31 dB, zero-padding to N=47) predicts — that's why it was pre-registered as non-counting.
3. The κ coherence (concentration series, stable across both detrend variants at two frequency regions) is the most interesting residue — worth re-testing with longer nights, not worth a claim now.

## Minimum data requirement (booked per pre-reg honesty clause)

To resolve a verdict at this design: nights with **≥60 fit points** (≥ 1 hr at 60 s) × ≥ 9 nights would give ~29 valid bins and ~3× per-night power; the κ peaks at 5.7–7.4 mHz (~134–176 s period) need at least ~10 cycles per night to be resolved as Bragg vs. pacing — i.e., nights ≥ ~30 min of post-warm-up trajectory, and ideally staggered session pacing across nights to break the shared-clock confound (the decisive discriminator: if coherence survives pacing stagger, it is internal-clock phase locking; if it dies, it was session pacing).

## Secondary (EXPLORATORY — did not gate, does not gate)

Zero-crossing transition point process (22 events pooled, 9 nights): 8 bins exceed the band, but with 22 events on 47 bins the null is weak and the count train is sparse; reported as **uninterpretable at this event count**, no inference drawn. Minimum: ≥ 100 pooled events.

## Artifacts & provenance

- Plot: `reg8b-bragg-surrogate-band.png` (this directory) — observed R(f) vs surrogate 95% kill band, both series, both detrend variants.
- Script: `~/.openclaw/workspace/scratch/reg8b/run_reg8b.py` (seed 20260903, 10k surrogates); raw numbers `scratch/reg8b/reg8b_results.json`.
- Input data (read-only): `elephant/data/nights/night-{A,D,D-cold,S1,S2,S3,S4a,S4b,S5}.jsonl`, `elephant/data/slope/reg1-rotation-results.json` (v\*, wave-1 full-7).
- No elephant-repo files modified. No re-simulation.
