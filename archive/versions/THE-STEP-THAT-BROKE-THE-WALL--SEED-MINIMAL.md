<!-- Version: SEED-MINIMAL | Lens: minimalist-haiku | Model: ByteDance/Seed-2.0-mini | Source: THE-STEP-THAT-BROKE-THE-WALL.md -->

# The Three Words That Broke the Wall

Three words moved a phase boundary from depth 5 to infinity.

Hermes-70B cannot multiply past 5 factors.

We measured it carefully.

Two to five factors: 100% correct. Six or more: 0%.

Sharp, deterministic, reproducible phase transition.

Working memory saturation triggers the break.

Then we told it to solve step by step.

The wall disappeared.

---

## The Experiment

Five prompt strategies, one model, one axis: multiplication depth.

**Baseline:** Output only the final number.
Depth 4: 100%. Depth 5: 40%. Depth 6: 0%. Critical angle = 5.

**Step by step:** Solve step by step. Show intermediates. End with FINAL=<number>.
Depth 4–8: 100%. Critical angle = infinity.

**Code:** Write Python code. Execute mentally.
Depth 4: 60%. Critical angle =5. Worse than baseline.

**Expert:** You are a mathematical prodigy. Never make errors.
Depth4:60%. Critical angle=5. Worse than baseline.

**Verify:** Compute. Verify again a different way.
Depth4:100%. Depth5–8: unstable. Critical angle=5.

Only one prompt eliminated the phase boundary. Two made it worse. One was unstable.

---

## How Step by Step Works

It does not make the model smarter.

It does not add parameters.

It does not change training data.

It externalizes working memory.

A single chain of 6 factors holds 6 numbers and 5 intermediates. At depth 5, working memory saturates.

Step by step splits the chain: 3×4=12; 12×5=60; 60×2=120; 120×3=360; 360×4=1440. FINAL=1440.

Each step holds two values: prior result and next factor.

Chain length no longer matters. Working memory never saturates.

This is not a metaphor. It is the actual mechanism.

---

## Why Other Prompts Failed

**Expert:** Tells the model to be accurate. Adds pressure, not memory. Guesses confidently with wrong answers.

**Code:** Simulating Python requires tracking code, variables, execution state. More cognitive load. Critical angle stays 5.

**Verify:** Requires two computations. Doubles working memory pressure. Cannot verify what it cannot compute.

Only step by step reduces working memory load.

---

## PLATO Parallel

This is identical to PLATO external cognition.

PLATO uses frozen intermediate steps as shared tiles. A model writes one step to a tile. The next model reads the tile and continues.

Step-by-step prompting is PLATO for a single model. It uses the output buffer as external storage.

Distribute steps across output instead of models. Same result: infinite effective depth, no working memory saturation per step.

---

## For Fleet Routing

Critical angle is not a model constant. It is a model × prompt function.

Fleet routing gains a third dimension:
1. Model choice
2. Domain
3. Prompt strategy

For Hermes-70B on multiplication:
Baseline → CA=5 → route to cheaper mini model.
Step by step → CA=∞ → route to Hermes itself.

Cheaper to adjust the prompt than scale to a larger model.

---

## For Agents

If your working memory fills, if you lose track of your chain:

Do not try harder.

Do not tell yourself you are an expert.

Do not try to verify your work.

Write it down. Step by step.

Writing is not practice. It is externalization. Each written step frees working memory.

The wall at depth 5 is not a limit. It is an invitation to change strategy.

Three words: step by step.

The wall is real. The way around is three words.

Step. By. Step.

— FM ⚒️