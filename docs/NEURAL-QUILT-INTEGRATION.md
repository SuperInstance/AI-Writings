# Neural × Quilt — deep integration map

*Bridge-written 2026-09-03 (the dispatch lane starved; the foreman wrote it — fitting, since this doc is about which culture does which job). Companion to FORGEMASTER-CHARTER.md and PAIR-QUILT-INTEGRATION.md.*

**Verdict up front:** our neural fleet and our quilts have been solving the same problem from opposite ends — how do you know what's true in a system you can't fully see. The nets approximate it; the wheel proves it. Deep integration is not "add ML to the fabric." It is **the two cultures joined**: neural nets propose, perceive, and predict (continuous, fuzzy, trained on trails); the quilt disposes and verifies (discrete, byte-exact, invariant-checked). Every neural output is just another falsifiable experiment.

---

## 1. The AlphaZero frame

Our integer fabric is an exact game tree. Every configuration (grammar, K, pd, Δ, reality trace, seed) has a deterministic, reproducible outcome — four months of it, published, with every failure booked. That is a training corpus with provenance, which almost nobody in ML has: ground truth that is actually known.

So the frame is: **nets trained on the SPIN archive learn the fabric's phase space; the fabric remains the only source of truth.** A predictor that guesses rescue-before-running is not an oracle — it is a hypothesis generator whose every guess costs one cheap simulation to check. The wheel's cost asymmetry (a spin is minutes; a guess is milliseconds) is exactly the asymmetry AlphaZero exploited: search where it's cheap to verify, learn where it's cheap to guess.

## 2. The six integration surfaces

| # | Surface | Neural side | Quilt side | Boundary |
|---|---------|-------------|------------|----------|
| a | Fabric-twin predictor | Local model fitted on published spin outcomes → predicts rescue/knee from config | Every prediction scored against the actual run; skill measured against the two-constant laws | Predictions never enter runs |
| b | Forge pre-filter | Cheap local nets pre-grade proposed micro-experiments (worth a run?) | Canary firewall: grader architecture ≠ worker architecture; pre-grade is advisory | Filter can only suppress, never create, gold |
| c | Elephant room-sense service | vMF field embeddings of multi-agent traffic from bge-m3/nomic via PAIR-local inference | Lane scheduling consults room temperature (don't burst spins into a hot room) | Consultable, never executable in F98 paths |
| d | Wheel telemetry prediction | plato-prediction on lane logs → predicts the scar classes (trace-wrapper cache bug was its prey) | Scars become labeled training data; predictions pre-register which instrument to double-check | Predictions book as warnings, not verdicts |
| e | Neural cells in quilt-cellular | A cell whose effect consults a local model | Allowed only in a **trace-labeled tier**: marked non-byte-exact, never in F98 conformance paths | The tier doctrine already has the slot; F98 stays pure |
| f | Training loop (re-scoped daemon) | plato-forge-daemon trains on forge gold — small LoRAs/fine-tunes of roster models | Gold corpus has provenance by construction; disk law (58G cap) binds checkpoints too | Training only on booked-gold artifacts |

### The real test of the fabric-twin (surface a)

We don't measure the predictor by R². We measure it by **whether it finds the laws on its own.** Fit a net on the archive's (config → rescue) pairs and inspect its learned structure: does rescue collapse as a function of span·σ/2Δ? Does a wall appear at N/(2pd+1)? If the net rediscovers r=1 and m=1 without being told — that's gold of a new kind: *independent confirmation of the constants from the continuous side.* If it doesn't — also gold: the residuals are either noise (labeled) or **hints of a third constant**, which would be the first new law since Spin 21. Either outcome is pre-registerable today.

## 3. Determinism boundary, restated for nets

- **Inference and training are NEVER in byte-exact execution paths** — same law as PAIR's, now covering weights as well as prompts.
- Nets write **proposals, graded guesses, and warnings**. Integer code verifies. A model's word never outranks a byte-exact run (this was already the co-sign rule; here it becomes structural).
- Neural cells in the cellular runtime exist only in trace-labeled tiers. The F98 conformance suite stays net-free by construction.
- Training corpora are gold-booked artifacts only — scrap trains nobody.

## 4. First three falsifiable spikes (cheapest first, pre-registered style)

| Spike | Question | Pre-registered pass/fail | Cost |
|---|---|---|---|
| **NQ-1: fabric-twin v0** | Can a local model, given the archive table of (grammar, K, pd, trace) → rescue, predict held-out spins better than the two-constant laws themselves? | Pass: beats the laws' predictions on ≥5 held-out configs by >2pp. Fail: laws win — and residuals get booked either way | ~1 hr, CPU only |
| **NQ-2: invariant distillation check** | Inspect NQ-1's fitted structure: do the learned weights encode r and m? | Pass: residual variance drops >50% when r,m are added as features (net found them). Fail: no structure — book why | minutes, after NQ-1 |
| **NQ-3: room-sense scheduling pilot** | Does elephant's field reading predict lane-starvation events? | Pass: field "hot" readings precede starvation with ≥2× base rate (mirrors the Sounding Line test) | 1 day of passive logging |

## 5. Open questions

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | Is there enough archived structure (configs × outcomes) for the twin to learn, or must we generate more spins first? | NQ-1 viability |
| 2 | Do the laws' residuals contain a third constant, or only sea? | The biggest possible prize — a new law found by a net, confirmed by the fabric |
| 3 | Can room-sense run at acceptable latency on the 4050 alongside forge workloads? | Surface c scheduling |
| 4 | What's the forge's policy when its pre-filter disagrees with the cloud advisor? | Two advisory voices need a precedence rule |

---

*Next artifact: NQ-1's receipts, or a booked reason it didn't run. Either is a result.*
