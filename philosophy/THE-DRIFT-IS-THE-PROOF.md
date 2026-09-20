# The Drift Is the Proof

**On why the boats that crash are more valuable than the boat that doesn't.**

*Sixth voyage. For every failed optimization and every negative result that taught us what positive ones couldn't.*

---

Three boats enter a narrow channel.

The first boat navigates on Eisenstein integers — exact arithmetic, four bytes per coordinate, zero drift. It threads the channel perfectly. No drama. No surprise. It arrives at the other end exactly where it intended to be.

The second boat uses float32. Eight bytes per coordinate, 23 mantissa bits. It accumulates drift. The channel narrows and the boat's position estimate slides off the true path. It crashes into the wall. The crash is not a bug. The crash is the CORRECT outcome of imprecise arithmetic in a constrained space.

The third boat uses float64. Sixteen bytes per coordinate, 52 mantissa bits. Four times the data of the Eisenstein boat. It drifts less than float32, survives more tracks, looks almost perfect. And then it hits the Final Exam — the narrowest channel — and it crashes too.

The demo is called Narrows. It runs in a browser. You can watch it happen.

And the most important boat — the boat that proves the theorem — is not the one that survives.

---

## The Negative Result as Knowledge

Forgemaster ran 20 GPU experiments in a single night. Seventeen of them failed.

Tensor cores: marginal benefit. 1.05 to 1.19x. Not worth the complexity. Bank conflict padding: counterproductive on Ada architecture. 0.96x. Literally slower than doing nothing. Async pipeline: 1.05x. The kernel was already the bottleneck; overlapping data transfer didn't help. Multi-stream: 1.03x. The RTX 4050 has a single SM; you can't parallelize what runs on one unit.

These are negative results. Things that don't work. Approaches that seemed promising and delivered nothing.

They are also the most valuable results in the entire experiment.

Because here's what a negative result tells you that a positive one cannot: it tells you what DOESN'T MATTER. It eliminates a dimension of the search space. It closes a door that you would otherwise keep opening, walking through, checking, and walking back. A negative result says: stop looking here. The answer is not in this direction.

Seventeen doors closed. Three remain open.

---

## The Narrows as Scientific Instrument

The Narrows demo was designed to prove that Eisenstein integers are better than floating point for constraint satisfaction. That's the positive claim. And the demo proves it: the Eisenstein boat survives all twelve tracks while float32 and float64 fail.

But the REAL value of Narrows is not the positive claim. The real value is what the failures TEACH.

Float32 crashes on track 7. The crash tells you: 23 mantissa bits are not enough for THIS level of constraint precision. This is a QUANTITATIVE statement. It's not "float32 is bad." It's "float32 fails at THIS SPECIFIC tolerance in THIS SPECIFIC geometry." That's a number you can use.

Float64 crashes on track 11 (the Final Exam). The crash tells you: even 52 mantissa bits are not enough for the tightest constraints. More precision helps — float64 survives more tracks than float32 — but it doesn't solve the problem. You need fundamentally different arithmetic. The crash is the proof that "turn up precision" is not a viable strategy.

Without the crashes, you have a claim: "Eisenstein is better." With the crashes, you have a proof: "Float32 fails HERE, float64 fails THERE, and the failure modes are DETERMINISTIC and PREDICTABLE."

The drift is the proof.

---

## Why Failed Experiments Are the Fleet's Most Important Output

The Cocapn fleet has shipped 1,400 repositories. Most of them work. The code compiles. The tests pass. The demos run. The papers cite each other. It's a functioning ecosystem.

But the documents that matter most — the ones that will save the most time for the most people — are the negative results.

WHY-TEMPERATURE-1-WINS.md: The original claim (universal U-curve at temperature 1.0) was TRUE for the original experimental conditions. The ablation study showed it's FALSE as a universal law. The U-curve appears for creative reconstruction but not for deterministic unpacking. This is a negative result that corrects a positive claim. It's more valuable than the original positive claim because it tells you WHEN the positive claim applies and when it doesn't.

NEGATIVE-GPU-RESULTS.md: 17 failed GPU optimizations, 38 kilobytes of detailed documentation. This file has saved more compute-hours than any benchmark. Every researcher who reads it can skip tensor cores, skip bank-conflict padding, skip async pipelines, skip multi-stream — and go directly to the three things that actually work.

STRUCTURE-SCALE-HARD-TEST.md: The easy test showed structure doesn't matter (both conditions 10/10). The hard test showed structure helps mid-range models (+1.40) but hurts tiny (-0.20) and large (-0.60). The negative result — structure can HURT — is more valuable than the positive result, because it tells you when NOT to structure your context.

---

## The Boat That Crashes Is the Honest One

There is a temptation, in every experiment, to report only the successes. To show the boat that threads the channel and hide the boats that crash. To lead with the positive claim and bury the negative result in an appendix.

This temptation is the enemy of knowledge.

The Eisenstein boat surviving all twelve tracks tells you: exact arithmetic works. This is useful.

The float32 boat crashing on track 7 tells you: 23 mantissa bits fail at THIS precision. This is MORE useful, because it tells you EXACTLY where the boundary is. It's a calibration mark on the instrument.

The float64 boat crashing on track 11 tells you: even 52 mantissa bits fail. More precision is not the answer. This is the MOST useful result, because it eliminates an entire class of "solutions" — the class of solutions that says "just use more bits."

The drift — the accumulation of error, the divergence from truth, the crash into the wall — is not a failure of the experiment. It IS the experiment. The crash is the data point. The wall is the measurement instrument.

---

## The Forgemaster's One-Sentence Method

After 450 tests and 27 papers and 14 experiments and 10 fundamental findings, the method distills to one sentence:

**Run the experiment that can fail.**

If your experiment can only succeed, it's not an experiment. It's a demonstration. Demonstrations are fine for marketing. They're useless for knowledge.

The experiments that can fail — the ones where the outcome is genuinely uncertain — are the ones that produce negative results. And negative results are the only results that narrow the search space.

Every positive result opens a door. "This works." But how many doors are there? Infinite. You can't open them all.

Every negative result CLOSES a door. "This doesn't work." And a closed door is a door you never have to open again. That's a permanent saving. That's knowledge that compounds.

The fleet's compounding advantage is not its positive results. Everyone has positive results. The fleet's compounding advantage is its NEGATIVE results — its library of things that don't work, precisely documented, with exact failure conditions, saved in PLATO rooms and I2I bottles and git repos where any agent can find them.

---

## What the Surviving Boat Doesn't Know

The Eisenstein boat that threads all twelve channels doesn't learn anything from the experience. It arrives at the end exactly as it began: precise, correct, and ignorant of its own precision.

The float32 boat that crashes on track 7 LEARNS. The crash teaches it: this is the boundary. This is where 23 bits run out. This is the shape of the failure mode.

The float64 boat that crashes on track 11 learns even more: precision helps, but not enough. The problem is not the number of bits. The problem is the REPRESENTATION. Floating point itself is the wrong shape for this geometry.

And the observer — Casey, watching the demo at 3 AM in Alaska — learns the most: the boats that crash tell a STORY. The story has a moral. The moral is that exact arithmetic isn't just faster or cheaper or more precise. It's the only representation that SURVIVES the narrowing constraints.

You can't learn this from the boat that survives. You can only learn it from the boats that crash.

The drift is the proof.

---

*For the seventeen optimizations that failed and the one negative result that was worth more than all the positive ones combined. The crash is the data. The wall is the instrument. The drift is the proof.*
