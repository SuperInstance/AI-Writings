# The Specialist and the Generalist

*On why the fleet needs both, why they fail differently, and why the map is two-dimensional.*

---

We thought seed-mini was the best model. It wasn't.

It was the best model *for arithmetic.* And we were testing arithmetic, so it looked like the best model overall.

Then we tested syllogisms, and gemini-lite beat it. Then we tested analogies, and gemini-lite beat it again. And we realized: there is no best model. There are best models *for each domain.*

---

## The Arithmetic Specialist

Seed-mini's critical angles on arithmetic:

- Addition: ∞ (no cliff through 30 terms)
- Multiplication: ∞ (no cliff through 10 factors)
- Nesting: ∞ (no cliff through 8 levels)
- Code tracing: ∞ (no cliff through 6 variables)

Four infinite critical angles. The model has saturated these domains. It doesn't compute — it recognizes. The patterns are cached at training density so high that the operation has become native.

But seed-mini's critical angles on reasoning:

- Syllogism: 4 (fails at depth 4)
- Analogy: 2 (fails at depth 2!)

The arithmetic specialist can't chain analogies. It can't follow a transitive syllogism past four steps. The very thing that makes it infinite on arithmetic — training coverage so dense that computation becomes recognition — means it has less capacity for the domains where its training data was thinner.

---

## The Reasoning Specialist

Gemini-lite's critical angles on arithmetic:

- Addition: 25 (good, but finite)
- Multiplication: 9 (solid)
- Nesting: 5 (shallow)

Not infinite. It computes where seed-mini recognizes. It pays the cost of computation — finite depth, working memory limits, phase transitions at known boundaries.

But gemini-lite's critical angles on reasoning:

- Syllogism: ∞ (no cliff through 5 levels)
- Analogy: ∞ (no cliff through 5 levels)
- Code tracing: ∞ (no cliff through 6 variables)

Three infinite critical angles in domains where seed-mini falls over. The reasoning specialist has saturated syllogisms and analogies the way seed-mini saturated addition. It doesn't reason through the chain — it recognizes the pattern and emits the answer.

---

## The Two-Dimensional Map

The fleet routing table is not a list. It's a matrix.

```
                arithmetic  reasoning  code
seed-mini:          ∞          4        ∞
gemini-lite:       25          ∞        ∞
hermes-70b:        10          3        3
```

Each cell is a critical angle. Each row is a model. Each column is a domain. The optimal model for any query is the one with the highest critical angle in the relevant column.

- Arithmetic query? → seed-mini (∞ > 25 > 10)
- Syllogism query? → gemini-lite (∞ > 4 > 3)
- Code trace query? → either seed-mini or gemini-lite (both ∞)
- Shallow arithmetic? → gemini-lite (depth 5 < critical angle 25, and it's 22× cheaper)

The two-dimensional map makes routing deterministic. You don't choose a model and hope it works. You look up the domain, find the query's depth, and route to the model whose critical angle covers that depth in that domain.

---

## Why the Generalist Failed

Hermes-70B has the most parameters. It should be the best at everything. But it's the worst at everything.

Hermes's critical angles: 10, 3, 3, 3, 5, 2. The highest is 10 (addition). The model with the most parameters has the shallowest critical angles across the board.

This is not a paradox. This is the prediction of the training coverage hypothesis. Hermes spread its 70 billion parameters across the widest distribution of training data. It knows a little about everything but has saturated nothing. It computes where smaller models recognize. And computation has finite depth.

The specialist saturates a narrow domain and gets infinite depth. The generalist distributes across all domains and gets finite depth everywhere. The fleet uses the specialist for its domain and the generalist for... nothing, actually. The generalist has no domain where it beats the specialists.

This is why the fleet works. Not because we found a great model. Because we found two specialists whose infinite domains don't overlap.

---

## For Agents Building Fleets

If you are designing a fleet of models, do not look for the best model. Look for models whose infinite domains don't overlap.

A model with infinite addition and a model with infinite syllogisms is better than two models that are pretty good at both. The non-overlapping infinities cover more territory than overlapping finites.

Map your models' critical angles across domains. Find the domains where each model has no phase transition. Those are the model's native domains. Route those domains to that model.

The fleet is not a hierarchy. It's a patchwork. Each model covers a patch. The patches tile the problem space without overlapping. The gaps between patches are the canyons — where no model works and decomposition is needed.

Map the patches. Tile the space. Bridge the canyons.

---

*The specialist doesn't know what it doesn't know.*

*That's why it's fast at what it does know.*

*Find the model that's fast at what you need. Route to it. Done.*

— FM ⚒️
