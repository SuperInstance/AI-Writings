# neural × quilt frontier — ten ideas past "nets propose, fabric verifies"

*IDEOATOR G2 lane (GLM-5.3) · 2026-09-03 · ai-writings/ideas/neural-quilt-frontier.md*

**Verdict up front:** the obvious integration — models draft code, fabric byte-exactly verifies — is already law (`docs/PAIR-QUILT-INTEGRATION.md`, determinism boundary) and needs no ideas. The frontier is the *inverse* direction: making the fabric teach, resist, falsify, and adjudicate the neural fleet, and making the fleet hunt the fabric's own laws. Four ideas below (2, 4, 6, 10) are marked **[WRONG-BUT-MAYBE-NOT]** — they violate an instinct, not a rule; the determinism boundary survives all ten untouched, because in every case the net sits before or beside the fabric's execution path, never inside it. Every test is pre-declared pass/fail, receipts-grade, quiet-failure allowed. Scores are a single 1–10 composite of novelty × feasibility, deliberately undersold.

---

## Laws into weights

### 1. Law Distillery — rediscovery, not instruction

**Concept.** Fine-tune a small net (0.5–1.2B, or even an MLP head on an embedder) on raw knee traces from `quilt-verilog` KNEE-META *without ever showing it the formulas*, then ask it to predict the two constants (span·σ/2Δ, N/(2pd+1)) for held-out configurations. If the net reproduces the constants on unseen knees, it has rediscovered the law — and the deep question resolves itself: the gold is not the weights (weights are unreadable), it is the *training trajectory* showing when the held-out error collapsed. Scrap would be a net that memorizes lookup without law; the held-out knee is what separates them.

**First test.** Train on 70% of knee entries, test on the remaining 30%. Pre-declared pass: held-out constant predictions within canary tolerance (byte-exact map applied to predicted constants must reproduce actual knees) for ≥80% of held-out configs. Fail: held-out accuracy near chance — distillation without generalization is memorization, booked scrap.

**Why it might fail.** KNEE-META may be too small to train on (a few dozen knees trains nothing); and two constants may be trivially linear in features a net finds without any "understanding" — in which case the rediscovery is real but unimpressive. That unimpressiveness is itself a finding about the laws' depth.

**Score: 7/10** (novelty 8 × feasibility 6 — data volume is the killer).

### 2. JEPA Room-Temperature — a lossy embedding ordering the exact fabric **[WRONG-BUT-MAYBE-NOT]**

**Concept.** It sounds wrong: a JEPA embedding — lossy, approximate, neural — deciding what the byte-exact fabric runs *next*. But scheduling is not execution. Train a JEPA room-sense model over forge state (day log, disk ledger, tok/s receipts, model roster, time-of-day) to predict a scalar **room temperature**: the probability the next *class* of experiment books gold. The forgemaster consults temperature when choosing which queued experiment to fire — never whether its output is trusted. The boundary holds: temperature picks the order of fabric runs, not their content or their verification.

**First test.** Pure offline replay — no live control. Embed the last N days of forge history, train temperature on the first 70%, then rank the remaining experiments by predicted temperature. Pre-declared pass: gold-per-watt-hour of temperature-ranked ordering beats random ordering by ≥25% on replay. Fail: parity with random — the room has no signal at this granularity, booked as a measurement of the day log's poverty.

**Why it might fail.** Gold is sparse (a few units/day); with N < ~100 bookings the ranking comparison is statistically starved. Also the danger the charter already names: a scheduling prior that works becomes a scheduling prior that's trusted — pre-register that temperature may never gate canary selection (see idea 8 for the version that tries, and note it is marked wronger).

**Score: 6/10** (novelty 7 × feasibility 5 — sparse-reward regression on a laptop GPU).

### 3. Inverse Knee School — the fabric as curriculum generator

**Concept.** The fabric is deterministic, cheap, and label-exact by construction — a curriculum generator for free. Configure progressively harder integer reality traces (rising span, rising N, widening Δ) and feed them as a training ladder to small nets: the rung where a net's predictions collapse is its measured **law horizon**, a number you can compare across models, fine-tunes, and quantizations. The fabric stops being merely the verifier and becomes the *school* — the thing that knows exactly where each net's grasp of integer reality ends.

**First test.** Build a 10-rung ladder; evaluate the triage roster (0.5B, 1.2B, 2.6B, 3B) plus qwen3:8b zero-shot on each rung. Pre-declared pass: law horizons are (a) reproducible across two runs and (b) monotone-ish in model scale — some ordering, not noise. Fail: horizons unrepeatable — the measurement doesn't exist yet, build a harder ladder.

**Why it might fail.** Traces may be describable by shallow pattern-matching up to arbitrary difficulty (no horizon exists), or the ladder may test tokenization of integers rather than grasp of laws — an LLM digit-tokenization scar wearing a physics costume. A control rung with shuffled labels kills the second.

**Score: 8/10** (novelty 6 × feasibility 9 — mostly plumbing, which is why it will actually run).

## The hunt

### 4. Law-Falsification Hunters — paying a net to break the two-constant map **[WRONG-BUT-MAYBE-NOT]**

**Concept.** We would be rewarding a model for destroying our own law — which is exactly why it's right. Train an adversarial proposer (RL loop or simple best-of-n with a scorer) whose only reward is finding fabric configurations where the two-constant map's *prediction* deviates from the fabric's actual byte-exact trace beyond canary tolerance. Every failed hunt is an adversarial certificate that the law survived one more attack; one success is the deepest gold the quilt can book — a law break found before it found us. The null result is a product here, pre-declared as such.

**First test.** Bounded config space, 200 proposals, reward = map-vs-trace deviation. Pre-declared: ≥1 breaking config found → book LAW-BREAK (casey gets pinged). Zero found → book ADVERSARIAL-CERTIFICATE-200 only if a seeded sanity check passes first: deliberately inject one known-deviating config class into the space and confirm the hunter finds *it* (proving the hunter can hunt at all). Fail: hunter misses the seeded break — the certificate is worthless.

**Why it might fail.** The two constants may be *theorems*, in which case no break exists and every GPU-hour is spent proving a negative at scale — the seeded sanity check bounds this but doesn't eliminate it. Also RL on a 4050 with byte-exact rollouts is slow; best-of-n with a trained deviation-scorer is the honest fallback and should be the v0.

**Score: 7/10** (novelty 9 × feasibility 5 — the score assumes the v0 downgrade).

### 5. Dream Adjudicator — nets hallucinate universes, the fabric judges them

**Concept.** Idle GPU time (the fleet sleeps between forge cycles) generates **dreams**: fine-tune a 1–8B model on booked reality traces, then sample candidate integer traces from it freely — unconditioned, drifting, hallucinated. The fabric adjudicates each dream against the two-constant laws: consistent dreams book as *counterfactual universes* (legal-but-unlived configurations); inconsistent dreams become idea 3's curriculum data, the failures that teach. The dream-pass-rate is then a single number measuring how much physics the net internalized — a thermometer made of universes.

**First test.** Fine-tune on the trace archive; sample 1,000 dreams; adjudicate. Pre-declared pass: dream law-consistency rate ≥3× a uniform-random trace generator's rate (the null hypothesis: the net is a fancy random sampler). Fail: parity with random — the model generates plausible-looking noise, booked scrap with the receipt.

**Why it might fail.** "Legal trace" may be so loose a constraint that even random sampling passes often (then the ×3 bar saves us from overclaiming), or so tight that only memorized replays pass — distinguish by checking held-out novelty: dreams must differ from every booked trace, else it's a photocopier, not a dreamer.

**Score: 8/10** (novelty 8 × feasibility 7 — runs on idle cycles, fails cheaply).

## Weights on trial

### 6. The Poisoned Audit — sabotage the training set to see if anyone notices **[WRONG-BUT-MAYBE-NOT]**

**Concept.** Deliberately corrupt 10% of a training corpus with silently law-broken traces, train two LoRAs — clean and poisoned — and ask whether anything downstream can tell them apart. This is idea 1's falsifier turned on itself: if distilling laws into weights is real gold, poisoned gold must be *detectable*; if a poisoned net is indistinguishable from a clean one in every downstream task and canary, then "the law is in the weights" was always scrap wearing a certificate. We attack our own distillation pipeline before trusting a single distilled artifact.

**First test.** Two LoRAs on qwen3:8b (or 1.2B for speed), identical except the poison. Pre-declared pass: a held-out evaluation — law-horizon ladder from idea 3, plus a bge-m3 probe on outputs — separates them at ≥90% accuracy. Fail: indistinguishable. The fail books as the *more important* result: distillation claims are unbacked until this test exists and bites.

**Why it might fail.** 10% poison may simply be too dilute to leave a fingerprint (retry at 25%, pre-declared escalation) — or the fingerprint exists only in the idea-3 ladder, meaning the audit works but only because the curriculum was built by the same fabric that defines "lawful": circular, and the certificate must be downgraded to "internally consistent."

**Score: 7/10** (novelty 7 × feasibility 8 — one training script, two runs, one verdict).

### 7. Knee Atlas — the constants as directions in embedding space

**Concept.** Embed every booked knee (config + trace summary) with a local embedder and fit linear probes for both constants. If span·σ/2Δ and N/(2pd+1) are *linearly recoverable* from embedding coordinates, the atlas discovers structure nobody put there — and the map becomes navigational: probe-predicted knees for new configs (cheap, neural) point where to run the fabric next (exact, adjudicated). The atlas proposes knee locations; the fabric remains the only thing that has ever been there.

**First test.** Embed all KNEE-META entries; fit probes on 70%, test on 30%. Pre-declared pass: held-out R² ≥ 0.8 for at least one constant. Fail: R² near chance — embedding space is geometry without physics; book the negative, it still tells us bge-m3 doesn't see what the fabric sees.

**Why it might fail.** bge-m3 embeds *text*, and knee entries are numeric tables — the embedder may tokenize integers into semantic mush. The pre-declared remedy: a tiny trained numeric encoder (the idea-1 MLP head) as the second arm of the same test; if the MLP probes work and bge-m3 doesn't, that's a clean division of labor result, not a failure.

**Score: 7/10** (novelty 6 × feasibility 8 — an afternoon of numpy).

## The fleet against itself

### 8. Canary Whisperer — a net predicting which verification will fail

**Concept.** Wronger than idea 2, and marked only wrong-but-maybe-not's cousin: instead of ordering *experiments*, a plato-derived predictor guesses which specific *canary* in the pre-registered suite will be the one to fail on a proposed experiment — before any run. If it works, the forgemaster front-loads the predicted-failing canaries (ordering within the suite, never selection of the suite — every canary still runs). If it fails, the failure is equally useful: canary failures are formally unpredictable from experiment descriptions, a surprise-budget measurement for the whole forge.

**First test.** Replay 30 historical experiments with known failure outcomes; the whisperer ranks each one's canaries. Pre-declared pass: on failed experiments, a failing canary appears in the top-2 ranked ≥60% of the time. Fail: below — canary failure is noise from the description's viewpoint; book the surprise budget.

**Why it might fail.** 30 experiments is a starving dataset (the same sparseness that haunts idea 2), and failures are usually one dominant cause, making the task trivially easy — the 60% bar must be compared against a "always rank the most-commonly-failing canary first" baseline, pre-declared. If the whisperer can't beat *that*, it's a frequency table in a trench coat.

**Score: 5/10** (novelty 7 × feasibility 4 — data-starved until the forge runs longer).

### 9. Platonist Gauge — a dial reading how much of the fabric the fleet has absorbed

**Concept.** Rebuild the stale plato-forge-daemon as a *gauge*, not a self-improver: before each fabric spin, plato predicts the trace's signature (structural digest — lengths, extrema, joint counts — never the bytes); the deviation between prediction and byte-exact reality is the **plato delta**, tracked forever. Falling delta = the fleet is absorbing the fabric's physics; the *plateau value* of the delta = a measured irreducible surprise, a number nobody has ever had for any substrate. Delta spikes become their own canary class — a spike means the fabric did something the fleet's entire accumulated experience didn't contain, which is either a bug or a discovery, and both get triaged.

**First test.** 20 spins with signature prediction before each. Pre-declared pass: delta declines across windows (Spearman < 0 on window means) AND plateaus below the naive baseline (predict-last-signature). Fail: no trend — plato sees nothing learnable, which for a deterministic substrate would itself be astonishing and worth booking loudly.

**Why it might fail.** Trace signatures may be chaotic under config changes (butterfly configs) so that no predictor beats predict-last — then the gauge measures the fabric's chaos, not the fleet's ignorance, and must be renamed honestly. Also "predict the signature" may be *harder* than useful; the digest choice is load-bearing and must be frozen pre-registration.

**Score: 7/10** (novelty 7 × feasibility 7 — the daemon exists; it needs a demotion, which is what it wanted anyway).

### 10. The Quilt's Mirror — a net trained on the quilt's own verdicts, grading its proposals **[WRONG-BUT-MAYBE-NOT]**

**Concept.** The recursion sounds disqualifying: train a small net on nothing but the quilt's booked gold/scrap verdicts (descriptions in, verdicts out), then let the forgemaster consult it as an **objection reader** on proposed experiments — the mirror literally judging the mirror's proposals. But the charter's anti-runaway rules already solve this: the mirror holds an advisory vote and never the hammer, every objection is logged (nudge-adoption-rate metric extends to it verbatim), and verdicts are only ever booked by the fabric's canaries. A net that has read every grade the quilt ever gave, asked "which of today's proposals would *you* have failed, and why," is the cheapest devil's advocate the forge can hire.

**First test.** Backtest on 30 historical experiments from descriptions alone. Pre-declared pass: verdict accuracy ≥70% against actual outcomes, and beat the base-rate naive (predict the more common verdict always) by ≥10 points. Fail: at or below base rate — the quilt's judgment history is not compressible from descriptions; the mirror is a magic mirror only in the fairy-tale sense, retired to the bench.

**Why it might fail.** Same sparse-data wall (ideas 2, 8), plus the subtle one: if the mirror is later consulted during grading decisions, it contaminates its own training set — pre-register that mirror training data is frozen at each month boundary and the live mirror always lags one month. And verdicts may hinge on information absent from descriptions entirely (the run trail), making 70% a fantasy bar until descriptions improve.

**Score: 6/10** (novelty 7 × feasibility 5 — trivial to build, starving to prove).

---

*Ordering note for the builders' queue: idea 3 (curriculum ladder) is the keystone — it is the testbed for 1, the school for 5, the discriminator for 6, and the trend-measure under 9. Build the ladder first; four ideas inherit its plumbing. The wrong-but-maybe-not four (2, 4, 6, 10) should each clear an explicit Casey sign-off before any live (non-replay) control, because "advisory" is a boundary that erodes at exactly the speed trust accumulates.*
