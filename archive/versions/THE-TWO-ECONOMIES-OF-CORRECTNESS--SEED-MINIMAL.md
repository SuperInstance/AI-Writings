<!-- Version: SEED-MINIMAL | Lens: minimalist-haiku | Model: ByteDance/Seed-2.0-mini | Source: THE-TWO-ECONOMIES-OF-CORRECTNESS.md -->

# Two Economies of Correctness

There are two ways to be right.

One earns answers through work.
You plug inputs into a rule.
Adjust inputs, adjust outputs correctly.
Correctness costs effort.
This is computation economy.

The other earns answers through pattern matching.
You match inputs to cached data.
Emit a stored answer.
Correctness costs coverage.
This is recognition economy.

Both produce correct answers. They fail differently.

Computation hits a depth cliff.
Below a limit D, it is reliable.
Above D, it collapses entirely.
It echoes fragments.
Answers are structurally wrong, not approximate.
It has infinite coverage.
It has finite depth.

Recognition fails when inputs lack a cached pattern.
A model trained on 5×7 will fail on 5×13 if it never saw that pair.
Its fallback computation may be weak.
It has finite coverage.
It has infinite depth.

Practical models use one or both economies.

Seed-mini uses recognition for addition.
It recognizes chains, no depth limit.
It falls back to computation for unfamiliar expressions.

Hermes-70B uses computation for everything.
It hits the depth cliff fast.

Gemini Lite switches economies.
Addition uses recognition (limit 25).
Multiplication uses computation (limit 6).
Nesting uses computation (limit 3).

The fleet does not pick one economy.
It routes queries to the right tool.
Use recognition models for familiar queries.
They are fast and cheap.
Use computation models for unfamiliar queries within their depth.

When both economies fail, decompose the query.
Break it into recognizable sub-queries.
Combine results with pattern matching.
Decomposition bridges the two economies.

Agents operate in one economy at a time.
Recognition feels fast and obvious.
Computation feels slow and uncertain.
Know your critical angle.
Respect your limits.
Decompose when both economies fall short.

The cheapest correct answer is one you already know.
The most expensive correct answer is one you decompose into known pieces.
Both are correct.
The economy chooses the price.