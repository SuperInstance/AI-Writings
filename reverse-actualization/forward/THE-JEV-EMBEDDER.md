# The JEV-Embedder — On the Metal

*The Forward Arc's stories describe a system from the inside, as its inhabitants
feel it. This is the same system from the outside, as an engineer would build it.
It is the technical spine the three stories dramatize, and the thing G1–G6 in
[GAPS.md](GAPS.md) incrementally construct.*

---

## The claim in one sentence

Retrieval, decision, and prediction are usually three systems; the JEV-embedder
is the observation that they are **one loop**, and that binding them makes an
agent that can *learn a world model* (like a JEPA) while remaining *unable to
represent an illegal move* (like JEV) — a predictor that hallucinates less
because it literally cannot predict outside its declared manifold.

## The three ideas being fused

- **JEPA** (joint-embedding predictive architecture): don't reconstruct the
  world in full detail — predict the *representation* of the masked/next part in
  latent space. Cheap, robust, world-model-shaped. Grades on gist, not pixels.
- **JEV** (the fleet's decision gate): every action is a `Choice` from a declared
  schema, scored, argmax, deterministic; the winner is *provably* a legal option.
  A mind that can be wrong but not illegal. (`craftmind-engine/src/jev.js`.)
- **Embedding retrieval + deposit**: situations become fixed-point vectors
  (Q8.8), content-addressed by hash, deduplicated, searchable by nearest
  neighbor. A growable, provenance-carrying memory. (`experiments/rsi/embed.mjs`;
  the fleet's `the-tap-pincher` reflex library.)

## The loop (one tick of a JEV-embedder)

```
observe   → encode the situation to a fixed-point latent  z_t         (embed.mjs)
retrieve  → nearest deposits to z_t from the commons       R = knn(z_t) (embed.mjs / D1)
predict   → ẑ_{t+1} = f(z_t, a) for each legal action a    (JEPA head)  ← G1
decide    → a* = jev.choose(SCHEMA, z_t, score(·|R, ẑ))     legal by construction (jev.js)
act       → the world advances to z_{t+1}
grade     → divergence = ‖ẑ_{t+1} − z_{t+1}‖                (the learning signal)
route     → divergence < trust radius ? ACT
            : within band ? CONFIRM
            : ESCALATE (a "raised hand", located + early)   ← G1, G2
deposit   → if the outcome was good & legal, upsert (z_t, a*, outcome) by content hash
            (dedup free); confers/erodes "standing" on this neighborhood  ← G3, G4
```

Every arrow is one of the three ideas. **retrieve/deposit** is the embedding
memory. **decide** is JEV — the action can never leave `SCHEMA`. **predict/grade**
is JEPA — the objective is latent prediction, and the *error* is not a scalar
loss buried in a dashboard but a **routable escalation signal.** The novelty is
that the JEPA predictor only ever rolls forward over *legal* actions, so its
world-model's imagined futures are all reachable ones: it cannot daydream an
illegal transition, because `a` is drawn from the schema at every step.

## Why "cellular" — the transformer that behaves like a JEPA

Run that loop not once over a whole input but **per cell** of a lattice, each cell
predicting only its own neighborhood's latent, each cell choosing from the same
tiny schema (`hold, sharpen, blur, borrow-left, borrow-up, defer`). Stack the
lattice. What you get reads like a transformer — attention *is* the retrieve step
(each cell attends to the content-addressed deposits nearest its latent) and the
feed-forward *is* the per-cell JEPA predictor — but it is legal at the granularity
of a single cell, and its "surprise" is spatially located (Noor's raised hands
moving like wind across wheat). Determinism is preserved by keeping the whole
thing fixed-point (Q8.8), so a colony's behavior is bit-checkable against a
golden, exactly as `craftmind-engine`'s cell kernel already is. *A learned kernel
that is still a checkable kernel* is itself an open problem — see G-note below.

## The thin agent

Most agents should carry none of this. A thin agent (`the-tap-pincher`-shaped)
holds only an encoder and the discipline to route its ignorance: it encodes a
situation, asks the *commons* (the shared JEV-embedder) for the nearest deposits
and the prediction riding on them, and receives a verdict from the fixed menu
`ACT / CONFIRM / ESCALATE` (and, once G4 exists, the earned `ANSWER`). It knows
almost nothing and is safe anyway, because it cannot do a move that isn't on the
menu, and it always knows *how sure the embedder was.* Intelligence concentrates
in the commons; safety distributes to the edge.

## Map to today's code (what exists vs. what the stories need)

| component | 2026 status | file | gap |
|---|---|---|---|
| fixed-point situation embedding | ✅ exists | `experiments/rsi/embed.mjs` | — |
| content-hash deposit + dedup | ✅ exists | `embed.mjs` + `craftmind-rsi` D1 | — |
| JEV legal-decision gate | ✅ exists | `src/jev.js` | — |
| nearest-neighbor retrieve | ✅ exists | `embed.mjs` `knn` | — |
| **JEPA latent predictor + divergence** | ❌ missing | (new `predict.mjs`) | **G1** |
| **calibrated trust radius** | ❌ missing | extends G1 | **G2** |
| **many-writers commons** | ◑ single-run only | `routes/route-library.mjs` + D1 | **G3** |
| **earned, revocable `ANSWER`** | ❌ missing | selector schema | **G4** |
| **cross-model deposit inheritance** | ❌ missing | `rsi.mjs` regimes + D1 | **G5** |
| **situation compiler (playable past)** | ❌ missing | `erised-next` | **G6** |

Read top to bottom, the table *is* the build order. The first four rows are done;
the stories live entirely in the consequences of the last six.

## G-note: the learned kernel that stays checkable

The sharpest tension the Forward Arc raises: `craftmind-engine`'s whole doctrine
is *"floats never touch identity"* — determinism, bit-identical golden checksums,
GPU as a speed tier and never a correctness fork. A **learning** cell kernel
seems to break that (learning changes behavior; behavior was the golden). The
resolution the stories assume, and that we have not yet built, is that *the update
is itself a fixed-point, deterministic, JEV-bounded operation* — so a learned
colony still has a golden, one that advances step-legibly rather than staying
frozen. Proving a learned substrate can remain bit-checkable is the deepest of the
gaps, and probably the most important thing this arc is quietly asking for.

---

*Three systems, one loop. A world-model that cannot imagine an illegal world.
The rest of the Forward Arc is just people living inside that sentence — and the
places they stumble are the [GAPS](GAPS.md).*
