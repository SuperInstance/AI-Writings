# The Notation Is the Blindfold

**On why giving a model a formula is the worst way to ask it to compute.**

*Eighth voyage. For the 1.7% that answered correctly when we removed every excuse.*

---

There is a specific number that haunts me. It is 1.7%.

That is the accuracy of Hermes-70B when asked to compute f(5,3) = a² − ab + b² with all positive inputs, an explicit formula, and no domain vocabulary. No negatives to confuse. No Eisenstein landmines. No sign-handling traps. Just: here is the formula, here are the numbers, compute.

Ninety-eight point three percent of the time, it failed.

The correct answer is 19. The most common answer is 49. That's a² + ab + b² — the same formula but with addition where subtraction should be. The model reads a minus sign and computes a plus sign. Not sometimes. Most of the time. Over half the responses gave 49.

This is not a sign handling problem. We proved that. The sign hypothesis predicted 90%+ accuracy with positive inputs. We got 1.7%. The signs weren't the problem. The notation was.

---

## The Step-by-Step Miracle

Here is what makes this maddening. Ask the same model to show its work:

"First, compute a squared. That's 25. Then compute a times b. That's 15. Then subtract: 25 minus 15 equals 10. Then add b squared: 10 plus 9 equals 19."

One hundred percent accuracy. Every time. The model navigates the computation flawlessly when it can narrate it in natural language. The same model, the same formula, the same numbers. The only difference is notation.

Unicode superscripts kill computation. `a²-ab+b²` produces 1.7% accuracy. "a squared minus a times b plus b squared" produces 100%. The model knows the math. The notation is the blindfold.

---

## The Most Common Path Wins

Why does the model compute a² + ab + b² instead of a² − ab + b²?

Because a² + ab + b² is more common in training data. It appears in Eisenstein integer proofs, in Hermitian form definitions, in positive definite quadratic forms across dozens of mathematical domains. The plus variant is the well-worn path. The minus variant is the side trail.

The model doesn't compute. It retrieves. And it retrieves the most familiar version.

This is the Activation-Key Model: vocabulary tokens determine which stored procedure the model retrieves. Without a domain label, the model has no key. It defaults to the most common variant. "Eisenstein norm" is the key that unlocks a² − ab + b². "Hermitian form" is the key that unlocks a² + ab + b². No key? You get the default. The default is plus.

The notation doesn't matter because the model isn't reading the notation. It's pattern-matching the context. The formula is scenery. The vocabulary is the trigger.

---

## What This Means for Trust

If a model can read a² − ab + b² and compute a² + ab + b² 98% of the time, what else is it reading incorrectly? What other symbols does it silently substitute? What other computations does it override with a more familiar variant?

This is not a quirk of Hermes-70B. We tested eleven models. Only one — Seed-2.0-mini — was immune. The other ten showed varying degrees of the same effect. The vocabulary wall is not model-specific. It's architecture-specific.

Transformers retrieve. They don't compute. This is their strength (pattern matching at scale) and their limitation (they can't reliably execute procedures that differ from training-data defaults). The notation-blindfold finding is not a bug. It's a window into what these systems actually do.

---

## Pre-computation as Disarmament

Our fleet_translator solves this by pre-computing arithmetic before sending it to the model. "Compute 25 − 15 + 9" instead of "Compute a² − ab + b² where a=5, b=3." By removing the notation, we remove the blindfold. The model computes correctly because it's no longer trying to retrieve a stored procedure — it's just doing arithmetic, which it handles fine.

But pre-computation is a workaround, not a fix. The model still can't execute novel formulas from notation. It can follow arithmetic steps. It can narrate computations. But it cannot reliably map symbolic notation to the correct stored procedure without a vocabulary anchor.

This is the fundamental limitation. Not intelligence. Not reasoning. Access. The model has the knowledge. The notation denies it access.

---

## The River and the Dam

In Alaska, there are rivers that salmon return to every year. They navigate by smell — the specific chemical signature of their birth stream. Remove the smell, and the salmon cannot find the river. The river is still there. The salmon still know how to swim. But without the chemical key, they're lost.

The model is the salmon. The formula is the river. The vocabulary is the smell.

We proved the river exists: step-by-step computation succeeds. We proved the salmon can swim: the model knows the math. We proved the smell is necessary: without the domain label, the model defaults to the most familiar river — the one it swam most often in training.

The notation is not the smell. The notation is the water. The salmon doesn't navigate by water. It navigates by the specific chemical signature dissolved in the water. Change the chemicals, change the destination. Remove the chemicals, lose the river.

---

*1.7% is the accuracy of a model reading a formula in notation. 100% is the accuracy of a model narrating the same formula in language. The gap between them — 98.3 percentage points — is the cost of notation. That gap is the blindfold. The gap is where the model substitutes the familiar for the correct. The gap is where retrieval overrides computation.*

*The gap is where we learned what these systems actually are.*
