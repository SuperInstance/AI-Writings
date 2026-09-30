# The turbovec family — a deep study of five older substrate-memory repos

*A scout/architecture study, 2026-09-30. Casey: "deep study all of these older projects too, one by one"
— the five `*turbovec*` repos in the SuperInstance org (all pushed 2026-09-22). Cloned and read in full;
every claim below is grounded in a run (35 tests green across the family) or a cited line, not the README's
word. Held to the house voice: what these are and what functional use they have — not a sales pitch.*

## In one breath

Five small, tightly-scoped Python repos that give the fleet a **compressed, hash-chained episodic memory**:
one base (`turbovec-substrate`, a pure-Python TurboQuant vector index where every entry is a chained cell)
and four thin application layers that each let a different generator *"find similar past runs"* — diffusion
prompts, critiques, GAN paradigms, and discovered model-failure edges.

## The family at a glance (verified locally)

| repo | lines (module) | what it remembers | key class | tests |
|---|---|---|---|---|
| `turbovec-substrate` | 267 | the base: any vector as a chained cell | `SubstrateIndex` | **9/9** |
| `jev-turbovec` | 234 | jev-diffusion runs (target+plan+combined) | `DiffusionMemoryIndex` | **8/8** |
| `peanut-gallery-turbovec` | 221 | critiques (prompt+output+critique) | `CritiqueMemoryIndex` | **6/6** |
| `madlibs-gan-turbovec` | 215 | GAN paradigms (paradigm+topic+template+fills) | `ParadigmMemoryIndex` | **6/6** |
| `paradigm-edges-turbovec` | 210 | model-failure edges (paradigm+prompt+edge_type+severity) | `EdgeMemoryIndex` | **6/6** |

All five are stdlib-only (no numpy), one module + a `tests/` suite + a README each. Total: **35 tests, all
green** when run with the substrate on `PYTHONPATH`.

## One by one

### 1. `turbovec-substrate` — the base (TurboQuant, made substrate-aware)

Implements Google's **TurboQuant** (arXiv:2504.19874) in pure Python: a **data-oblivious random rotation**
followed by **4-bit Lloyd-Max quantization** (16 fixed centroids, `-2.79 … 5.50`). The "substrate-aware"
twist: every indexed vector is a **cell** carrying a `prev_hash` chain, using the *exact* fnv1a-64 idiom the
rest of our fleet uses — `FNV_OFFSET 0xcbf29ce484222325`, `FNV_PRIME 0x100000001b3`, GENESIS
`0x0000000000000000` (`turbovec_substrate/__init__.py:15`, `:41`). `add()` links each cell to the last;
`_verify_chain()` walks the chain; `canon_submit()` POSTs a cell to a live Cloudflare Worker at
`quilt-distributed.casey-digennaro.workers.dev/api/cell`. The demo reports **8× compression** (4-bit vs
float32) with `prev_hash_chain_intact: True`.

**This is the load-bearing observation:** the substrate speaks the same hash-chain dialect as
`situation-recorder`, `activeledger`, and MicroMoth-quilt. It is a *vector cell* on the same chain algebra
as our *situation cells* — they are the same substrate seen from two angles (semantic index vs mission log).

### 2. `jev-turbovec` — memory for the diffusion engine

Wraps the substrate so `jev-diffusion` runs become retrievable: `add_diffusion(target, plan, combined)`
embeds `target + combined`, chains a `diffusion-<ts>` cell, and `find_similar(target, k)` returns the
nearest past runs "for inspiration." Reuses the substrate's rotation/centroids when importable, else
regenerates them inline (`jev_turbovec_main.py:91-101`) — a clean graceful-degradation pattern.

### 3. `peanut-gallery-turbovec` — memory for the critic

Same shape for critiques: `add_critique(prompt, output, critique, model)` →
`find_similar_critiques(prompt, output, k)`. So the critic can say "here are past critiques of similar
outputs" before scoring a new one — retrieval-augmented criticism.

### 4. `madlibs-gan-turbovec` — memory for the generative game

`add_paradigm(paradigm, topic, template, fills)` → `find_similar_paradigms(paradigm, topic, k)`. Lets the
madlibs-GAN find past games of the same paradigm for inspiration/variation.

### 5. `paradigm-edges-turbovec` — memory for the red-team

The most interesting for us: it remembers **discovered model failures**. `add_edge(paradigm, prompt,
edge_type, severity, description, evidence, model)` → `find_similar_edges(prompt, k)`. This is a searchable
corpus of where models break — directly adjacent to our **Weakest-Claim method** and the
`situation-recorder` corpus of what worked/failed. A red-team that remembers its own past edges probes
smarter next time.

## What is real (verified)

- **The chain algebra is real and fleet-compatible.** Same fnv1a-64 constants + GENESIS as our corpus;
  `_verify_chain()` passes; tamper would break it. These cells could be appended to (or read alongside) our
  situation cells with no dialect translation.
- **TurboQuant is faithfully implemented.** Random rotation (Gram-Schmidt-orthonormalized Gaussian, xorshift
  seed 42 → deterministic) + 4-bit Lloyd-Max centroids. The demo's nearest-neighbour ordering is correct.
- **The memory-layer pattern generalizes cleanly.** Four different content types, one base, ~215 lines each,
  all green — evidence the pattern is genuinely modular.
- **There is a live shared surface.** `canon_submit` targets a deployed Worker — a sibling of `i2i-ledger`
  and `superinstance-api` (see THE-LIVING-QUILT.md): another org-scale shared brain, this one a *vector*
  canon.

## What is not true yet (the honest gaps — each is a concrete opening)

1. **The 8× compression is nominal, not realized.** Every cell stores the full float `vector`, and
   `find_similar`/`search` computes exact float L2 over `cell.vector` (`peanut_gallery_turbovec.py:132,151`;
   substrate `__init__.py:153`). The quantized codes are computed and chained but **never used for
   retrieval**, and the float vectors are retained — so in-memory footprint is not reduced. `jev`'s `stats()`
   even reports `compression_ratio` as the constant `32/n_bits` rather than a measurement
   (`jev_turbovec_main.py:195`). **Opening:** make retrieval ride the codes (asymmetric/Hamming distance on
   4-bit codes) and drop the float vector — then the 8× is real and search gets faster, which is the whole
   point of TurboQuant.
2. **The embedding is lexical, not semantic.** `simple_embed` is a hash bag-of-words
   (`jev_turbovec_main.py:29`), so "find similar" is a lexical match despite the READMEs implying semantic
   recall. **Opening:** swap in a real embedder behind the same interface (the code already invites this:
   *"For production use, swap with sentence-transformers"*).
3. **The rotation is O(dim²) dense — not "turbo" in speed.** TurboQuant's actual speed win comes from a
   structured transform (e.g. Hadamard); this is a full dense matmul per vector (`__init__.py:102-108`).
   Correct, but the name over-promises on throughput at dim=384.
4. **Two concrete bugs, both grounded:**
   - `jev-turbovec`'s README quickstart says `from jev_turbovec import DiffusionMemoryIndex`, but the module
     file is `jev_turbovec_main.py` — that import raises `ModuleNotFoundError` (verified). The tests import
     the right name, so tests pass while the documented entry point is broken.
   - `turbovec-substrate`'s `canon_submit` error path references `cell.cell_id` where only `sv` is in scope
     (`__init__.py:223`) → `NameError` whenever the canon POST throws (i.e. exactly when you want the error
     message). The happy path is fine; the failure path masks the real error.

## How it composes with our current work

- **Same substrate, two indexes.** Our `situation-recorder`/`activeledger` chain *missions* (relation
  records + budget vectors); turbovec chains *vectors* (semantic cells). Joining them gives a corpus that is
  both **replayable** (our chain) and **searchable by similarity** (their index) — "which past mission is
  near this one?" becomes a `find_similar` over situation embeddings on the same chain.
- **System-2's budgeted-history recall wants exactly this.** §11 of ACTIVELEDGER-CELL-GRAPH.md has System-2
  reading history to propose alternative networks; `paradigm-edges-turbovec`'s "find similar past edges" and
  a situation-memory index are the recall primitive it currently lacks. The memory layer is a **modular tool
  that plugs into System-2**, not a separate product.
- **Converge, not fork (again).** The `quilt-distributed` vector canon is a third shared surface beside
  `i2i-ledger` (`/near` semantic recall) and `superinstance-api` (`/near` across tiles). All three are
  "find near X" over a shared brain. The move is the same as §14's OrgBook reconciliation: one recall
  protocol, many doors — our recorder should be able to `/near` against any of them.

## Modular-tool proposals (R&D synergy, per the wide-scope quest)

1. **`code-real-quant` (make the 8× true):** a ~40-line change to retrieval that ranks on 4-bit codes
   (popcount/asymmetric distance) and drops the float vector, with a recall-loss selftest vs the float
   baseline. Turns a nominal claim into a measured one — and it's a clean `labs/` cell with a receipt.
2. **`situation-memory` (join the two chains):** embed each `situation-recorder` transcript and index it with
   the substrate, so the corpus gains `find_similar_missions()`. Feeds System-2 recall and the base-rate work.
3. **`near-adapter` (one recall interface):** a thin client that speaks `/near` to i2i-ledger,
   superinstance-api, **and** the turbovec vector canon — so any cell can ask "who/what has learned near X?"
   regardless of which shared brain holds it.

## Where to look next

- `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §11 (System-2 history recall) and §14 (converge-not-fork).
- `situations/arch/THE-LIVING-QUILT.md` (i2i-ledger + superinstance-api shared surfaces).
- `labs/situation-recorder/` (the mission chain the vector index would join) and `arXiv:2504.19874`
  (the TurboQuant paper the substrate implements).
