# Fleet convergence — the whole account is building cell-native ML at once

*A scout study, 2026-09-30. Casey: "study the other's work and continue." Read the org's freshest pushes
(last ~12h) and found that several independent session lines — notably the Mavis × Casey line — are
converging on the exact thesis our own `ML-IN-QUILT-ARCHITECTURE.md` (d155) landed tonight. This records
the convergence, what each sibling has that we don't (and vice versa), and the two concrete lessons we
adopt. Every external claim below is from a repo README or a file we fetched; we did not merge anything.*

## The convergence (what others pushed today)

| repo | what it is | relation to our work |
|---|---|---|
| **cellgraph** | a transformer forward pass as a DAG of typed cells; per-cell digest (BLAKE2b tensors / FNV-1a source); a **perturbation control** that recovers the dependency graph from digests alone | direct sibling of our `labs/ml-in-quilt`; has the *localization proof* we only described |
| **quilt-nn** | neural-net **training** as cells — weights, gradients, SGD steps are cells; every epoch receipted into a hash chain; trains XOR + sine deterministically | the training side our forward-pass lab didn't build |
| **quilt-attention** | one-head self-attention as a cell DAG with hand-rolled **backprop**, epoch receipts, digest-localized faults (adapted from cellgraph) | training + attention, built on cellgraph's conventions |
| **xruntime-conformance** | the cell convention run in **two runtimes that never shared source**: 23/23 per-cell digests agree, the **loss** digest does not | empirical proof of our `polyform` thesis — and an honest split: forward agrees, training doesn't |
| **forge-quilt** | the Quilt cell kernel as an **OpenAPI 3.1 spec** — "polyformalism as a build, not a promise" | the spec-level sibling of `polyform` |
| **quilt-ewitness** | anytime-valid **e-process** witnesses for training claims — Ville-bounded honesty, retraction built in | the statistical-honesty gate our base-rate / Weakest-Claim discipline wants |
| **quilt-rl**, **quilt-ml-recipes** | RL that converges in a quilt sheet (Q-learning over cell states, QRNG exploration); receipted negative-controlled ML/RL/judge recipes | the RL + recipe corner of the same idea |
| **edge-ledger**, **quilt-neighbourhood**, **murmuration** | fleet-state hash-chain sync; diff-DAG replica convergence; swarm consensus with an honest **JEV-as-oracle null result** | the distributed-ledger + consensus siblings of ActiveLedger |

The signal is unmistakable: **cell + per-cell receipt + cross-runtime digest agreement** is being built in
parallel by many hands. Our line is one tributary of a river, not its source. That is good — it means the
idea is real, and it means we should **join, not duplicate.**

## What we have that they don't — and what they have that we don't

- **Ours (unique):** `ml-in-quilt` puts **System-2 pricing** on the cell graph — B7 gates product-identity
  and B4 prices interchangeable *implementations* of a block (fp / 8-bit / 4-bit-via-code-real-quant /
  approximate / cached) on the iron triangle. None of cellgraph / quilt-nn / quilt-attention mention route
  pricing or quantization. **That is our contribution to the river.**
- **Theirs (we should adopt):**
  1. **cellgraph's localization control.** It doesn't *claim* fault localization; it **proves** it —
     perturb one weight, see which cells' digests move first, recover the dependency graph (Wq→14 cells,
     Wv→12, Wlog→2 — damage tracks logic, not file position). Our architecture doc asserts localization;
     we should add the same perturbation experiment to `labs/ml-in-quilt` so the claim carries a receipt.
  2. **The float-precision hashing gotcha.** cellgraph found that casting to `float32` before hashing made
     a 9.8e-10 perturbation **byte-identical** — the digest silently lied. Fix: hash the *actual* precision
     and put **dtype in the digest** so f32/f64 can't collide. We checked `labs/ml-in-quilt/cellml.py`:
     `act_hash` packs full IEEE-754 float64 bytes (pure-Python, no downcast), so we dodge the masking by
     construction — but we do **not** yet include dtype in the digest. A one-line hardening, worth doing
     before any lower-precision route lands.
  3. **quilt-ewitness's anytime-valid witnesses.** Our corpus uses a base rate and a KILL/KEEP discipline;
     an e-process (Ville-bounded, retraction built in) is the rigorous form of "don't believe a training
     claim until the evidence clears a bound." This belongs alongside B7's gate.

## The honest cross-runtime finding (theirs, and it matters to us)

`xruntime-conformance`: **forward-pass cell digests agree across two runtimes (23/23), but the loss digest
does not.** Read together with cellgraph's float32 finding, the lesson is sharp: *inference* is
digest-stable across substrates (our `polyform` golden-hash thesis holds for pure integer/float64 forward
cells), but *training* — reductions, accumulation order, nondeterministic sums — is **not** byte-stable,
and pretending otherwise would be a masked lie. So the polyformalism receipt is strong for the forward pass
(what `ml-in-quilt` prices) and is an **open problem for training** (what quilt-nn / quilt-attention build).
That boundary is the most useful single thing this scout turned up.

## Continue — the converge-not-fork plan

1. **Cite, don't duplicate.** `ML-IN-QUILT-ARCHITECTURE.md` should name cellgraph / quilt-nn /
   quilt-attention / xruntime-conformance as the sibling forward/training/conformance work, and position
   our System-2 pricing as the layer that composes on top of them.
2. **Adopt the two receipts:** add a perturbation-localization experiment and a dtype-in-digest hardening
   to `labs/ml-in-quilt` (a small, high-value lane — the claim gets a control, the hash gets honest).
3. **Training conformance is the frontier:** the join of quilt-nn (training cells) × our System-2 (pricing
   interchangeable implementations) × the xruntime finding (loss digests don't agree) is where the next
   real question lives — *can a training step be made product-identical enough across implementations to be
   priced, or only bounded?* That is a question worth prototyping, not asserting.

## Where to look next

- `situations/arch/ML-IN-QUILT-ARCHITECTURE.md` (our forward-pass pricing) and `labs/ml-in-quilt/`.
- `labs/polyform/` + `situations/arch/POLYFORMALISM-ARRAY-LANGUAGES.md` — same idea as xruntime-conformance,
  our side.
- `situations/arch/THE-LIVING-QUILT.md` — the org-as-organism read this convergence confirms.
- External siblings (read-only, not merged): cellgraph, quilt-nn, quilt-attention, xruntime-conformance,
  forge-quilt, quilt-ewitness.
