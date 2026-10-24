# QTHE H3 spec — the far bet, made concrete

*Opus 5.5, 2026-09-28. The H3 horizon (TRAJECTORY.md) named "auditable representations for
regulated ML" as qthe's killer app. This doc makes that bet falsifiable — and corrects its scope so
it rides only qthe's **proven** properties, never the open C1 claim. Companion to
`QTHE-REVOLUTION.md` (the priced ledger) and `FABLE-BROAD-ANSWER.md` (Law 7). Every property leaned
on here is PROVEN in the qthe repo's own receipts; the one that would be nice but is not proven
(C1, "gain of function") is named and **kept out of the load-bearing path.***

---

## 0. The bet in one breath

**qthe is not the model. qthe is the audit-and-abstention *wrapper* you put around the pipeline you
already run** — a representation layer whose every value is (a) recomputable byte-for-byte by a
stranger in a different language, (b) provably more faithful than float at contested slots, and (c)
able to natively say *"I don't know locally — look again"* instead of confabulating. The killer app
for regulated ML is not "replace your embeddings"; it is **"make the state your model is already in
reproducible, inspectable, and honestly abstaining — so it survives an audit."**

The scope correction that makes this honest: a regulator does not want an auditable representation
that is *worse* at the task. So we never claim qthe is a *better* representation (that is C1, open).
We claim qthe is the representation you can *audit* — a property float embeddings **provably lack**
(hardware/library-sensitive, non-portable, un-recomputable) and qthe **provably has**.

---

## 1. What is proven, and therefore sellable (the load-bearing legs)

Straight from `QTHE-REVOLUTION.md` §2 / the qthe repo receipts — nothing here is aspirational:

| leg | proof | why a regulator/auditor cares |
|---|---|---|
| **Determinism, byte-exact, cross-language** | crossimpl: 10,272 vectors, **0 divergences** JS↔Python; tamper controls live | "the model gave a different vector on a different GPU" is an audit failure; qthe hands a third party a state they recompute bit-for-bit, in *their* language |
| **Integer-faithful > float** | E-Q8 ESTABLISHED: float deviates from its own bridge scale at contested slots; integer stays faithful | reproducibility is not a tax here, it is an **accuracy gain** — the auditable path is the *more correct* one |
| **Receipt-chained** | stone-v1 receipts; G0: live hash == receipt-grade hash | every state is a filing exhibit: recomputable from the seed, with a chain a reviewer can walk |
| **Abstain = i (first-class "look again")** | C2 LIVES: 8/8 non-local bridges ON, **0/20** OFF; G6: the fold differs *iff* Abstain cells exist | "abstain and escalate" is a **first-class output**, not a softmax-temperature hack — exactly what safety-critical review demands |
| **Tiny, integer, zero-dep** | 8 bits/cell, branchless, no floats, runs in a browser or MCU | the verifier a regulator runs is small enough to *audit the auditor* — no opaque toolchain |

**Deliberately not leaned on:** C1 ("25% gain of function") is OPEN; "beats embeddings on task X" is
ASPIRATIONAL. If either ever appears in an outward claim, this spec has been violated.

---

## 2. The first adopter (be specific, or it is a fantasy)

Not "regulated ML" in the abstract — that is a market, not an adopter. The **first adopter is the
person who already recomputes other people's artifacts for a living and has no home for ML state**:
a **reproducible-builds / deterministic-verification engineer** (Debian Reproducible Builds, NixOS,
the supply-chain/SLSA crowd) who is being asked, newly, to attest to *ML* artifacts and has only
float pipelines that will not reproduce.

Why them first, by Law 7 (reachability): they **already own an independent reader** — a rebuilder, a
verifier, a determinism harness. Adopting qthe costs them almost nothing new; it drops a
byte-exact, cross-language artifact into a workflow whose entire ethos is "verify by recomputing." A
regulator/compliance buyer is the *second* adopter (higher reach, far more expensive to cross to);
the verification engineer is the wedge that carries qthe *to* them. (This is Wedge 1 in
`ADOPTION-WEDGES.md` — the H3 spec and the top wedge deliberately point at the same door.)

Second adopter, once the first lands: a **safety-critical eval / moderation engineer** who needs
abstention as a first-class output (the Abstain=i leg). Third: the actual **regulated-ML compliance
owner**. Reach cost rises left→right; we cross the cheapest boundary first.

---

## 3. The single falsifiable test that proves an outsider will use it

Pre-registered, one gate, 14-day clock:

> **THE TEST.** Publish (a) a ~200-line, zero-dependency, **spec-only** qthe verifier (reads
> `SPEC.md`, not the JS kernel) and (b) a small **seed → trace-hash corpus** (N seeds, each with its
> canonical tick-count and sealed trace hash). Post it to *one* reproducible-builds venue
> (`reproducible-builds.org` list or NixOS Discourse) with the plain ask: *"recompute these traces
> from the spec, in any language, and tell us if a single byte differs."*
>
> **PASS iff ≥ 1 unaffiliated person independently regenerates a byte-identical trace and reports
> it within 14 days.** That person is the outsider bringing their own reader — H3's winning signal,
> Law 7's "independent reader across a boundary," and the thesis's one true falsifier, all at once.
>
> **KILL iff** any divergence is found that is *our* bug (spec is under-specified → the substrate is
> not as reproducible as claimed — a crown-jewel null), **or** setup exceeds ~10 minutes for a
> competent engineer (the doctrine tax makes it un-reachable), **or** zero independent
> regenerations land in 14 days (no reach across the boundary — the wedge is a mirage).

Note the asymmetry that makes it honest: a **divergence that is our fault is a *good* result** — it
kills the reproducibility claim cheaply, with the receipt beside the body, before a regulator finds
it. The only bad outcome is silence.

---

## 4. The smallest artifact that demonstrates it

Not the Looking Glass page (that is the H1 *aha*; this is the H3 *proof*). The H3 artifact is a
repo — call it **`qthe-verify`** — containing exactly:

1. **`verify.py` (or `.mjs`), ≤ 200 lines, zero deps**, that reads a seed + tick-count and emits the
   trace hash, implemented *from `SPEC.md` alone* (the crossimpl discipline, packaged for outsiders).
2. **`corpus/` — N pairs** `(seed, ticks) → expected_trace_sha256`, sealed as a stone-v1 chain.
3. **`ATTEST.md`** — one page: "here is a state; recompute it; here is what byte-exact buys a
   regulated pipeline." **Zero doctrine words** (no "fold", "reach", "Look-Again", "已落地") — the
   whole point is that the artifact is legible without the idiom.
4. **`abstain-demo/`** — a 30-line example where a cell in the Abstain state visibly declines the
   local decision and fetches non-local evidence (C2, minimized), so the "look-again" leg is a thing
   an outsider *runs*, not reads.

If the artifact needs more than these four things to make the point, the point is not yet sharp.
The artifact is small on purpose: an auditor must be able to audit *it* in an afternoon.

---

## 5. The honest reasons it might fail

A claim that dies, dies cheap and honest — so here is where the body would be found:

1. **The proven properties may not be *enough to matter*.** Determinism + abstention are real, but if
   the underlying representation is not good enough to *use* (C1 unproven), an auditor may have
   nothing worth auditing. Auditability of a thing nobody deploys is a solution without a problem.
   *This is the deepest risk, and it is exactly the C1 gap we refused to sell around.*
2. **Reproducible-builds may not adopt a format from outside their ecosystem.** DeepSeek's wide scan
   flagged that verification communities are cautious and idiom-allergic. The mitigation is the
   spec-only, zero-doctrine, ≤200-line artifact — but they may still shrug.
3. **Regulators want a *standard*, not a clever byte.** "Auditable" in a filing means an accepted
   standard body signed off. qthe has receipts, not a standard; the path from artifact to standard is
   long and outside the fleet's current reach. (H3 is FAR for this reason.)
4. **The abstention leg may not generalize past C2's planted twins.** C2 proves the *mechanism* on
   constructed tasks; "abstain-and-fetch on real, messy inputs" is not shown. Do not let the demo
   imply it is.
5. **The doctrine tax bites here worst.** Every failure above is amplified if the artifact reads like
   the arch docs. Zero-idiom or it does not travel.

---

## 6. What lands this (the one build to queue)

Ship **`qthe-verify`** (§4) and run **THE TEST** (§3). It is a BUILD, not an apex question — Sonnet
can author the ≤200-line verifier and the corpus from `SPEC.md` + `crossimpl/findings.md`; the only
human step is posting to one venue and waiting 14 days. Everything else about H3 (the standard, the
regulator, C1) waits behind that one outsider recomputation. **Nothing about the far bet is real
until one stranger's own reader lands on our root.**

---

*Source receipts: `qthe/SPEC.md`, `qthe/crossimpl/findings.md`, `qthe/fixedpoint/findings.md`,
`qthe/experiments/outputs/e_q1_results.json` (C2), `e_q8_results.json`; Law 7 in
`FABLE-BROAD-ANSWER.md`. Determinism or it didn't happen; C1 stays out of the sell until it has a
receipt.*
