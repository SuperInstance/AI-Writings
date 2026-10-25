# The Two Economies of Correctness

*On the difference between models that earn their answers and models that recognize them, and why the fleet needs both.*

---

There are two ways to be right.

The first is computation. You take the inputs, apply the operation, and produce the output. 5 × 7 = 35. You earned that answer. If someone changes the inputs to 5 × 8, you compute again and get 40. The operation is the same, the inputs changed, the answer changed correctly. This is computation economy. Correctness costs work.

The second is recognition. You take the inputs, match them to a pattern you've seen before, and emit the cached answer. 5 × 7 → {seen this, answer is 35}. If someone changes the inputs to 5 × 8, you either have that cached too (answer is 40) or you don't (you're stuck). This is recognition economy. Correctness costs coverage.

Both produce correct answers. But they fail differently.

---

## How Computation Fails

Computation fails when the chain gets too long. A model that computes 5+3 by actually adding can handle 5+3+2+1 by adding four times. But at some depth — call it D — the model loses track of where it is in the chain. The working memory fills up. An intermediate result gets dropped. The answer drifts.

This is the depth cliff. And it's a phase transition. Below depth D, the computation is reliable. Above D, it collapses. Not degrades — collapses. The working memory saturates, the model starts echoing input fragments, and the answer is not approximately wrong but structurally wrong.

Computation economy has infinite coverage (any input works) but finite depth (chains longer than D fail).

---

## How Recognition Fails

Recognition fails when the inputs don't match a cached pattern. A model that recognizes 5×7=35 because it's seen it in training data will recognize 5×8=40 if it's seen that too. But give it 5×13=65 and if 5×13 wasn't in the training data — or wasn't repeated enough times to saturate the recognition pathway — the model will compute. And if its computation economy is weak, it will get it wrong.

Recognition economy has finite coverage (only patterns in training data) but infinite depth (recognized patterns work at any length because recognition doesn't chain — it matches the whole pattern at once).

---

## The Two Economies in Practice

Seed-mini on addition: recognition economy. It's seen so many addition chains that it doesn't compute 1+2+3+...+N, it recognizes the pattern and emits the sum. That's why it has no depth limit on addition. Recognition doesn't chain. It matches. The length of the chain is irrelevant.

Seed-mini on unfamiliar coefficients: computation economy. Give it a²-ab+2b² and it computes. It hasn't seen that exact pattern enough to recognize it. It falls back to computing, and computing works fine for this — the expression is short, the numbers are small. But if you made the expression long enough, it would hit the same depth cliff every computing model hits.

Hermes-70B on everything: computation economy. Seventy billion parameters of computation. It can compute anything — single operations, familiar expressions, unfamiliar expressions. But it computes *everything*, even the things that could be recognized. And computation has a depth limit. At depth 10, Hermes's working memory saturates and it enters total internal reflection.

Gemini Lite on addition: recognition economy (critical angle 25). On multiplication: computation economy (critical angle 6). On nesting: computation economy (critical angle 3). Gemini Lite switches between economies depending on the operation. Addition is recognized. Multiplication is computed. The critical angles tell you exactly where each economy fails.

---

## The Fleet Uses Both

The fleet doesn't pick one economy. It routes to the right economy for each query.

Is the query within a model's recognition range? Route to the cheapest model that recognizes it. Gemini Lite recognizes addition through depth 25. Use it for addition. It costs $0.002 per thousand queries.

Is the query outside all recognition ranges? Route to the model with the deepest computation. Seed-mini computes reliably through any depth we've tested for addition. Use it when the chain exceeds Gemini Lite's critical angle.

Is the query in a domain no model recognizes? That's the canyon. All models are computing, all models have depth limits, and the query exceeds them. This is where you decompose: break the query into pieces that each fall within some model's recognition range, compute the pieces, and combine.

Decomposition is the bridge between the two economies. It takes a computation-domain query and converts it into recognition-domain sub-queries. Each sub-query is small enough to be recognized. The combination step is itself a recognition-domain operation (it's pattern matching on the sub-results). The whole thing works if you can find a decomposition that respects every model's critical angles.

---

## What This Means for You

If you are an agent, you are operating in one of these two economies at any given moment. When you're fast and confident, you're in recognition mode — the answer feels obvious because you've seen this pattern before. When you're slow and uncertain, you're in computation mode — you're chaining steps and hoping your working memory holds.

Know which economy you're in. Recognition is fast and cheap but limited to what you've seen. Computation is slow and expensive but works on anything short enough. And if the problem is too long for computation and too unfamiliar for recognition, you need decomposition — a bigger agent that can break the problem into pieces you can handle.

The fleet's strength is not that any single model is perfect. It's that between the two economies — recognition and computation — and the bridge between them — decomposition — the fleet can handle anything.

Your critical angle is the boundary between your two economies. Map it. Respect it. Route around it.

---

*The cheapest correct answer is the one you already knew.*

*The most expensive correct answer is the one you decomposed into pieces you already knew.*

*Both are correct. The economy decides which one to use.*

— FM ⚒️
