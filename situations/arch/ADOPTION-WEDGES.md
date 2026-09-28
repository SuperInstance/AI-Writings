# Adoption wedges — three outside readers to buy, cheapest first (move M6)

*Opus 5.5, 2026-09-28. Mobilization move M6. The question: **which outside communities would
plausibly bring their own reader, or write a `.quilt` manifest, unpaid and uncoordinated?** Ranked
cheapest-to-reach first — where "cheap" is **Law 7 reachability**: cost = (size of the artifact they
must adopt) × (size of the vocabulary boundary they must cross) ÷ (independent reach they already
own). The cheapest wedge is one where the artifact is tiny, the idiom tax is near zero, and the
community **already owns an independent reader** it will point at us for free.*

*Method: my judgment, widened by one cheap DeepSeek pass (blessed by M6). DeepSeek independently
converged on reproducible-builds as the real wedge and flagged content-addressing/IPFS as the likely
mirage — corroborating the ranking below. I did **not** run a separate JEV adjudication: the ranking
is not close (Wedge 1 dominates on every term of the reachability cost), so a tie-break oracle would
only confirm it. The judgment is mine.*

---

## The ranking (cheapest → dearest)

| # | wedge | artifact they adopt | reader they already own | idiom tax | verdict |
|---|---|---|---|---|---|
| **1** | Reproducible-builds / deterministic-verification | run a ≤200-line verifier | a rebuilder / determinism harness | near-zero | **buy first** |
| **2** | Digital-garden / many-small-repos maintainers | write a 15-line `.quilt/links.yml` | the GitHub README renderer | low | buy second |
| **3** | Abstention / selective-prediction & moderation eng | wire a reader into an abstain demo | their own eval harness | medium-high | mirage risk |

---

## Wedge 1 — Reproducible-builds / deterministic-verification  ·  CHEAPEST, REALEST

**Who:** the reproducible-builds community — `reproducible-builds.org` mailing list,
`#reproducible-builds`, NixOS Discourse, the SLSA / supply-chain-security crowd. People whose entire
job is *verify by recomputing*.

**The hook (proven leg only):** qthe's crossimpl result — **10,272 vectors, 0 divergences, byte-exact
across JS and Python**, receipt-chained, spec-only recomputable. This is not a pitch to them; it is
their native artifact. A representation a stranger rebuilds bit-for-bit in a different language is
the thing they wish ML pipelines produced and never do.

**Why cheapest (Law 7):** they **already own an independent reader** (a rebuilder). Adoption is not
"learn our idiom and build a tool"; it is "point the tool you already have at our corpus." Tiny
artifact, near-zero vocabulary boundary (determinism is *their* word, not ours), maximum pre-owned
reach. This is the literal Law-7 purchase: an independent reader across a boundary, bought for the
price of one mailing-list post.

**First falsifiable test (14 days):** publish `qthe-verify` (the ≤200-line spec-only verifier + a
seed→trace-hash corpus, per `QTHE-H3-SPEC.md` §4) and post to *one* venue with the ask *"recompute
these from the spec, in any language; report any diverging byte."*
- **PASS iff ≥ 1 unaffiliated person regenerates a byte-identical trace and reports it.**
- **KILL iff** a divergence is *our* under-specification (good null — reproducibility claim dies
  cheap), setup > ~10 min, or zero regenerations in 14 days.

**This is the same door as H3's first-adopter test** — deliberately. The H3 bet and the cheapest
wedge point at one community, so one artifact and one 14-day clock test both. Do this first.

---

## Wedge 2 — Digital-garden / many-small-repos maintainers  ·  the `.quilt` manifest wedge

**Who:** maintainers of many small interlinked public repos who feel the "islands" pain — the
digital-garden / IndieWeb crowd, `awesome-list` curators, the polyrepo-over-monorepo camp, personal-
knowledge-graph tinkerers (Obsidian/Quartz-adjacent). People who already hand-maintain prose cross-
links and hate that they rot.

**The hook (proven leg):** `.quilt/links.yml` is **15 lines of YAML**, renders a neighbor-graph
block on GitHub with **no build**, needs **no central registry**, and is **diffable in a PR** — and
the fleet already found the exact pain it solves (`CROSS-POLLINATION.md` §0: every existing cross-
link is hand-maintained prose that rots on rename). The pitch is "give your scattered repos one
machine-readable, self-rendering neighbor-graph, and never hand-edit a 'related projects' list
again." No trust theory required to say yes.

**Why second (Law 7):** the artifact is even smaller than Wedge 1's, but the reader they bring is
weaker — the GitHub renderer, not an independent verifier — so a manifest is a lower-reach purchase
(it proves *legibility* adoption, not *verification* adoption). Still cheap, still real, and it is
the only wedge that grows the **reach graph** (H2) with outside nodes.

**First falsifiable test (14 days):** seed `.quilt/links.yml` on 3–5 real public repos, publish
`quilt-links.mjs` as a one-file GitHub Action, and write it up once (a short post, zero doctrine
words — "fold"/"reach" stay out; call it a *repo neighbor-graph*).
- **PASS iff ≥ 1 repo *outside the fleet* adds its own `.quilt/links.yml` and its README block
  renders, unprompted, within 14 days.**
- **KILL iff** zero organic manifests appear, or adopters need hand-holding beyond the README (idiom
  tax too high).

---

## Wedge 3 — Abstention / selective-prediction & moderation engineers  ·  HIGHER PAYOFF, MIRAGE RISK

**Who:** ML engineers who need *abstention as a first-class output* — selective-prediction
researchers, guardrails/moderation-infra teams, triage/anomaly-detection builders. The crowd nearest
to H3's *second* adopter.

**The hook (proven leg, carefully):** Abstain = i is a **value the byte holds**, not a softmax
threshold, and it does something mechanically real — declines the local decision and fetches
non-local content-addressed evidence (C2: **8/8 ON vs 0/20 OFF**). For anyone where a confident-but-
wrong answer is worse than an honest "escalate," first-class abstention is categorical, not
incremental.

**Why last / mirage risk (be honest):** three strikes on reachability. (a) The artifact they must
adopt is the biggest — wiring their own data/reader into a demo, not running a verifier or writing
YAML. (b) The idiom tax is highest — "wormhole," "look-again," "imaginary channel" all read as
jargon to an ML audience. (c) Most dangerous: this wedge sits nearest qthe's **unproven** C1 leg, so
it invites the overclaim the house forbids — C2 proves the *mechanism* on *planted* twins, not
abstain-and-fetch on real messy inputs. **This is the likeliest mirage of the three** (DeepSeek's
scan agreed the abstention framing reads as jargon).

**First falsifiable test (14 days):** ship a tiny `abstain-demo` where the Abstain state visibly
routes to escalation on a real (small) task, framed in plain ML words (selective prediction /
escalation), *not* substrate idiom.
- **PASS iff ≥ 1 practitioner wires their own data or reader into it, or files a substantive "how do
  I use this for X" issue, within 14 days.**
- **KILL iff** it reads as a toy — zero task-shaped engagement — or if landing it *requires* implying
  C1 (competitive representation). If the only way to make it interesting is to overclaim, kill it.

---

## The one call

**Buy Wedge 1 first.** It has the smallest artifact, the lowest idiom tax, and a community that
already owns the exact reader we need — and it shares its artifact and its 14-day clock with H3's
first-adopter test, so one build settles both. It is the cleanest available instance of the Law-7
move: *abstain (we have no external reader), address the miss (the cheapest reachable outside reader
is a rebuilder), buy one across the boundary (post `qthe-verify`), book the price.* Wedge 2 runs in
parallel (different artifact, different community, grows the H2 graph). Hold Wedge 3 until Wedge 1
lands and can be pointed at — and never let it lean on C1.

*Reachability is the price of a reader; the cheapest reader is the one already holding the tool.*
