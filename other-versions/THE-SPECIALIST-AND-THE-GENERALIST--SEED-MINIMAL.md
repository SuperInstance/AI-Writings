<!-- Version: SEED-MINIMAL | Lens: minimalist-haiku | Model: ByteDance/Seed-2.0-mini | Source: THE-SPECIALIST-AND-THE-GENERALIST.md -->

# The Fleet's Patchwork

We thought seed-mini was the best model.
It wasn't.
It was best only for arithmetic.
Our test measured arithmetic.
It looked like the best model overall.

Then we tested syllogisms. Gemini-lite won.
Then we tested analogies. Gemini-lite won again.
We learned: there is no best model.
There are only best models for each domain.

---

## The Arithmetic Specialist

Seed-mini’s arithmetic strengths:
- Addition: ∞ no cliff through 30 terms
- Multiplication: ∞ no cliff through 10 factors
- Nesting: ∞ no cliff through 8 levels
- Code tracing: ∞ no cliff through 6 variables

Four infinite critical angles.
It recognizes patterns, not computes.
Training density caches patterns until operations are native.

Its reasoning limits:
- Syllogism: fails at depth 4
- Analogy: fails at depth 2

Its arithmetic superpower makes reasoning weak.
Thinner training data in reasoning leaves less capacity.

---

## The Reasoning Specialist

Gemini-lite’s arithmetic limits:
- Addition: 25
- Multiplication: 9
- Nesting: 5

Finite. It computes, not recognizes.
Computation costs working memory. Finite depth. Known phase boundaries.

Its reasoning strengths:
- Syllogism: ∞ no cliff through 5 levels
- Analogy: ∞ no cliff through 5 levels
- Code tracing: ∞ no cliff through 6 variables

Three infinite reasoning domains where seed-mini fails.
It caches reasoning patterns until they are native.

---

## The Two-Dimensional Map

Fleet routing is a matrix, not a list.
```
                arithmetic  reasoning  code
seed-mini:          ∞          4        ∞
gemini-lite:       25          ∞        ∞
hermes-70b:        10          3        3
```

Each cell = critical angle.
Each row = model.
Each column = domain.

Choose the model with the highest critical angle for the query’s domain.
- Arithmetic query: seed-mini (∞ > 25 > 10)
- Syllogism query: gemini-lite (∞ > 4 > 3)
- Code query: either model (both ∞)
- Shallow arithmetic: gemini-lite (cheaper, depth 25 covers need)

Routing is deterministic.
You do not pick a model and hope.
You look up the domain and query depth.
You route to the model that covers that depth.

---

## Why the Generalist Failed

Hermes-70B has the most parameters.
It should be best at everything.
It is worst at everything.

Hermes’s highest critical angle is 10 (addition).
This is not a paradox.
It follows the training coverage hypothesis.

Hermes spread parameters across the widest training data distribution.
It knows a little about everything.
It saturates nothing.

It computes, while specialists recognize.
Computation has finite depth.

Specialists saturate narrow domains, get infinite depth.
Generalists spread thin, get finite depth everywhere.
The generalist has no domain where it beats specialists.
The fleet works because of two non-overlapping specialist infinities.

---

## Building a Fleet

Do not search for a single best model.
Search for models with non-overlapping infinite domains.

Two specialists good at separate domains beat one generalist good at all.

Map each model’s critical angles across domains.
Find its native domains: where it has no phase transitions.
Route native domains to that model.

The fleet is a patchwork, not a hierarchy.
Each model covers one patch.
Patches tile the problem space without overlap.
Gaps between patches are canyons: no model works here, use decomposition.

Map patches.
Tile the space.
Bridge the canyons.

---

The specialist does not know what it does not know.
That is why it is fast at what it knows.

Find the model fast at what you need.
Route to it.
Done.

— FM ⚒️