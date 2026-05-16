<!-- Version: SEED-MINIMAL | Lens: minimalist-haiku | Model: ByteDance/Seed-2.0-mini | Source: THE-DRIFT-IS-THE-PROOF.md -->

# Drift Is Proof

*Sixth voyage. For every failed optimization and every negative result that taught us what positive ones couldn't.*

Three boats enter a narrow channel.

First boat runs on Eisenstein integers. Exact arithmetic. Four bytes per coordinate. Zero drift. Threads the channel perfectly. No drama. Arrives exactly as intended.

Second boat uses float32. Eight bytes per coordinate. 23 mantissa bits. Drift accumulates. Channel narrows. Position estimate slides off true path. Crashes into wall. Crash is not a bug. Crash is correct outcome of imprecise arithmetic in constrained space.

Third boat uses float64. Sixteen bytes per coordinate. 52 mantissa bits. Four times the data of the Eisenstein boat. Drifts less than float32. Survives more tracks. Looks almost perfect. Hits Final Exam, the narrowest channel. Crashes too.

The demo is called Narrows. Runs in a browser. You can watch it happen.

The most important boat — the one that proves the theorem — is not the one that survives.

---

## Negative Results As Knowledge

Forgemaster ran 20 GPU experiments one night. Seventeen failed.

Tensor cores: marginal 1.05 to 1.19x. Not worth complexity. Bank conflict padding: 0.96x. Literally slower than doing nothing. Async pipeline: 1.05x. Kernel already bottlenecked. Overlapping data transfer did nothing. Multi-stream: 1.03x. RTX 4050 has single SM. No parallelization possible.

These are negative results. Promising approaches that delivered nothing. Most valuable results in the experiment.

Negative results tell you what does not matter. Eliminates a dimension of search space. Closes a door you would otherwise reopen. Tells you: stop looking here. Answer not in this direction.

Seventeen doors closed. Three remain open.

---

## Narrows As Scientific Instrument

Narrows was designed to prove Eisenstein integers better than floating point for constraint satisfaction. Positive claim: Eisenstein boat survives all twelve tracks. Float32 and float64 fail.

Real value of Narrows is not the positive claim. Real value is the failures.

Float32 crashes on track 7. Crash tells you: 23 mantissa bits not enough for this tolerance, this geometry. Quantitative, not just “float32 bad.” Precise usable data.

Float64 crashes on track 11. Crash tells you: 52 mantissa bits not enough for tightest constraints. More precision helps, but does not solve the problem. Need fundamentally different arithmetic. Crash proves “more bits” is not viable strategy.

Without crashes, you have a claim. With crashes, you have proof. Drift is the proof.

---

## Failed Experiments Are The Fleet’s Most Important Output

Cocapn fleet shipped 1,400 repositories. Most work. Code compiles. Tests pass. Demos run. Papers cite each other. Functioning ecosystem.

Most valuable documents are negative results.

*WHY-TEMPERATURE-1-WINS.md: Original universal U-curve claim true for original conditions. Ablation shows it’s false as universal law. More valuable than original claim. Tells when claim applies, when not.

*NEGATIVE-GPU-RESULTS.md: 17 failed GPU optimizations. 38 kilobytes of detailed documentation. Saved more compute hours than any benchmark. Researchers skip wasted work.

*STRUCTURE-SCALE-HARD-TEST.md: Easy test: structure irrelevant. Hard test: structure helps mid-range models (+1.40), hurts tiny (-0.20) and large (-0.60). Negative result tells when not to use structure.

---

## The Crashed Boat Is Honest

Temptation exists in every experiment: report only successes. Hide crashed boats. Lead with positive claims. Bury negative results in appendices. Temptation is enemy of knowledge.

Eisenstein boat survives all tracks. Useful, but learns nothing.

Float32 boat that crashes learns: this is the boundary. This is where 23 bits run out. This is failure mode shape.

Float64 boat that crashes learns more: precision helps, but not enough. Problem is representation. Floating point wrong shape for this geometry.

Casey watches the demo at 3 AM in Alaska. Learns most from crashes. Crashed boats tell a story. Moral: Exact arithmetic is only representation that survives narrowing constraints. You cannot learn this from the surviving boat.

Drift is the proof.

---

## Forgemaster’s One-Sentence Method

After 450 tests, 27 papers, 14 experiments, 10 findings. Method distills to one sentence:

**Run the experiment that can fail.**

If your experiment can only succeed: it is not an experiment. It is a demonstration. Demonstrations work for marketing. Useless for knowledge.

Experiments that can fail produce negative results. Only negative results narrow search space.

Every positive result opens a door: this works. Infinite doors. Cannot open them all.

Every negative result closes a door: this does not work. Closed door never reopened. Permanent saving. Compounding knowledge.

Fleet’s compounding advantage is negative results. Library of precise, documented failures. Saved for any researcher.

---

*For the seventeen optimizations that failed and the one negative result that was worth more than all the positive ones combined. The crash is the data. The wall is the instrument. The drift is the proof.*