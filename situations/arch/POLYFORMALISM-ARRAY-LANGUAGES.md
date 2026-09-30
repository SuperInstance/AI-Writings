# Polyformalism — building the parts that mattered into Uiua, Futhark, and BQN

*Ideation, 2026-09-30. Casey: "what if we built the parts that mattered into Uiua, Futhark, and BQN.
ideate on these not just for polyformalism thoughts about constraints, but also as tools for various
architectures with our components." Held to the house voice: what functional use each gives us, not
which language is "best."*

## The one idea underneath

Almost every component we prize is, at its core, **an array operation with a conservation law**:
TurboQuant is a rotation + a nearest-centroid map; the Syzygy fused pass is an integer reduction; the
differ is an elementwise equality fold; double-entry is a sum-to-zero; the rubric reward is a harmonic
mean; fnv1a-64 is an integer fold over bytes. **Array languages are the native home for exactly these.**
So "build the parts that mattered into Uiua/Futhark/BQN" is not three rewrites — it is giving each core
component **three more witnesses** of the same math, alongside our Python/Rust/WASM.

That turns two things on at once, which are Casey's two lenses:

## Lens A — polyformalism as a verifier (the constraints thought)

We already treasure *one* form of this: **byte-exact across substrates** (federated-tinyml-vessel's
Python/C/Rust/Node agreement), **Syzygy's golden `0x6dbdd1a8`** across WASM + native, **unit-translation
round-trips** (B2), **replay≡live** (OrgBook/ActiveLedger). Each is "the same math computed two ways must
agree." A language is just another way. So:

- **Each formalism is an independent witness.** Run the same test vectors through the BQN spec, the Futhark
  kernel, the Uiua pipeline, and our Python/Rust — and assert they land on **one golden hash**. Agreement
  is the receipt; **divergence is a bug localized to a formalism** — the Weakest-Claim method pointed at a
  language matrix instead of a clause.
- **The constraint is the point, not the polyglot.** Porting forces the component to be *pure* (Futhark
  won't take side effects), *shape-honest* (BQN's rank rules reject a unit mismatch loudly — the B2 error
  class caught at the type level), and *composable* (Uiua's stack won't let you hide flow in named temp
  vars). A part that *can't* be expressed cleanly in all three is telling you it isn't really a clean
  component yet. Polyformalism is a **design-smell detector** with a golden-hash receipt.

## Lens B — each language is a different tool for a different architecture

They are not interchangeable; they sit at different corners of our own iron-triangle {good, fast, cheap}.

### Futhark — the *fast/cheap* execution substrate (a route generator)
Futhark is a pure functional array language that **compiles to GPU** (CUDA/OpenCL/Metal) and multicore C,
with fusion and a **cost model**. For us it is literally a **new route** in the B4/B7 sense: a
Futhark-compiled TurboQuant (rotation + quant + the `code-real-quant` ADC) or a Futhark Syzygy pass is
*product-identical* to the Python route (differ-gated) but lands at a different iron-triangle point. Two
payoffs unique to Futhark:
1. It **generates the faster route** we keep saying B4/B7 need — GPU-vs-CPU placement becomes real, wired to
   `quilt-gpu-lab`.
2. Its cost model gives a **compiler-derived budget estimate**, not just a measured one — a static prior for
   the ActiveLedger budget vector, before a single run.

### BQN — the *good/correct* specification substrate (the oracle)
BQN's based-array theory + tiny orthogonal primitive set make it ideal for a **five-line executable golden
spec**. Write the invariants there — double-entry conservation (`+´ = 0`), the differ (`≡`), the rubric
harmonic mean, the Lloyd-Max map — and the spec becomes **the oracle the differ checks against**. This is
exactly Syzygy's P4 differentiator ("un-gameable verifier"): a spec small enough to audit by eye can't be
gamed. BQN is where "good" is *defined*, so B4's `good` axis and B7's product-identity gate get a reference
that isn't itself a big program to trust.

### Uiua — the *legible/composable* topology substrate (the notation)
Uiua is stack-based and tacit; a whole pipeline is a point-free composition. That makes it a candidate
**notation for the cell-network itself** — the mic→filter→STT→LLM route, or a cell graph, written as one
rearrangeable expression where the *structure* is visible. System-2's job is to rewrite networks; if a
network is a tacit Uiua expression, a **rewrite is a diffable expression edit**, and two networks are
comparable as terms, not as prose. Uiua is where the *shape of the route* lives.

## The synthesis: a substrate axis on the iron-triangle

Give each "part that mattered" three witnesses — **BQN spec (oracle) · Futhark kernel (fast route) ·
Uiua composition (legible topology)** — plus the Python/Rust we have. Then:

- **B7/B4 gain a substrate dimension.** Today they place routes on {good, fast, cheap}. Add **which
  formalism/substrate** as a first-class route attribute: pick the Futhark route when the GPU is hot, the
  Python route otherwise, and keep the BQN spec as the always-on oracle. The iron-triangle becomes
  {good, fast, cheap} × {substrate} — and System-2 can A/B **formalisms**, not just parameters.
- **The corpus gains the strongest possible invariant.** "N formalisms agree on the golden hash" is a
  receipt no single implementation can fake.

## The parts worth porting first (smallest exact thing → up)

1. **fnv1a-64** — an integer fold; trivially exact in all three. The *harness proof*: get five witnesses to
   agree on one golden hash before porting anything bigger.
2. **TurboQuant / code-real-quant** — array-native (rotation + nearest-centroid + ADC). Futhark for the GPU
   rotation, BQN for the Lloyd-Max spec, Uiua for the pipeline. Ties straight into the turbovec study.
3. **The differ + double-entry conservation** — BQN one-liners that become the B2/B7 oracles.
4. **The Syzygy fused pass** — a Futhark GPU route + a BQN golden spec; extends Syzygy's multi-substrate
   story to a language matrix.

Stateful/IO parts (the canon Worker POST, the live LLM call) are *not* array math and don't port — and
that's the useful line: **the pure kernels are exactly "the parts that mattered."**

## Modular tools this suggests (buildable as `labs/` cells with receipts)

- **`polyform` — a cross-formalism differ harness.** One component in → BQN/Futhark/Uiua/Python out → run
  shared vectors → assert one golden hash, else localize the diverging formalism. Syzygy's byte-exact story,
  generalized to a language grid. Receipt: N witnesses agree.
- **`futhark-route` — a GPU route adapter.** Wrap a Futhark-compiled kernel as an ActiveLog route with a
  budget vector, so B7 can price it against the Python route on real hardware.
- **`bqn-oracle` — the invariant reference pack.** Tiny BQN specs for conservation / differ / reward that
  B2, B7, and rubric-forge check against.
- **`uiua-topology` — a route-graph notation.** Express a cell network as a tacit expression; System-2
  rewrites become term edits.

## Honest constraints (so this stays useful, not a hobby)

- These are niche languages; the win is the **cross-check**, not wholesale adoption. Keep Python/Rust as the
  production spine; the formalisms are witnesses + specialized routes.
- **CI cost is real:** Futhark needs its C backend (or a GPU) in CI; Uiua/BQN add small interpreters.
  Start with `polyform` on fnv1a-64 so the harness earns its keep before we grow it.
- **Only the pure kernels port.** Don't try to force IO/statefulness through an array language; that's a
  category error, and the line it draws is itself informative.

## Where to look next

- `situations/arch/TURBOVEC-FAMILY-STUDY.md` (the array kernels this would port first) and
  `SuperInstance/Syzygy` (the byte-exact multi-substrate precedent).
- `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §11 (System-2 A/B) + §14 (the iron-triangle join B4 realizes)
  — where the substrate axis attaches.
- `labs/system2-backtest` (B7) and `labs/route-preference` (B4) — the route machinery a Futhark route plugs
  into.
