# The Weakest-Claim Method — an un-gameable audit instrument

*Built by playing situation S17 live against three tools (2026-09-28, ledger d098/d100/d101).
This is the reusable tool the experiments produced: point it at any tool's advertised guarantee
and it returns the guarantee's weakest claim + whether an adversary nobody could steer breaks it.
Runnable: `situations/play/weakest-leaf.mjs` (swap the `AUDIT_TARGET` block).*

## What it does
Projects the live JEV oracle around a tool's headline guarantee in an **increasingly decomposing**
way, then fires an **un-gameable quantum-drawn adversary** at the located weak point:

1. **Decompose.** Split the compound guarantee into leaf-claims. JEV `noul` each
   (`P(this is a sound absolute guarantee, no plausible bypass)`). The tree of nouls is the
   visual logic; the whole verdict is a shadow, the fold is a map.
2. **Localize.** `argmin` over the leaves = the weakest claim. Decompose *it* again to an atom.
3. **Confirm.** Moth `comet-qrng` draws (Bell-witnessed, S>2) *which* concrete bypass-hypotheses
   fire at the located leaf — the auditor cannot stack the deck. JEV `choice` adjudicates each.
4. **Answer.** The located leaf + the adversary hit-rate + the provenance (quantum seed, Bell S).

## The calibration finding (why this is the honest shape)
Across three tools the **absolute noul level is nearly uninformative** — JEV rates *any* "absolute
guarantee, no plausible bypass" at ~0.1–0.35, because almost every absolute claim hides an
unstated assumption. So **never use JEV as a grader here.** The real signals are relative:

| signal | what it is | what it tells you |
|---|---|---|
| **ranking** (argmin) | the weakest leaf *within* the tool | where to harden first (the *localizer*) |
| **adversary hit-rate** | of quantum-drawn bypasses, how many defeat the leaf | concrete-and-real vs abstract-and-hard (the *confirmer*) |
| **divergence** (whole − fold_min) | how much the compound verdict hid | uniform overclaim (low) vs one buried soft-spot (high) |

## The three results (the 2×2 taking shape)
| tool | weakest leaf (noul) | divergence | adversary | reading |
|---|---|---|---|---|
| **rate-component** | KV budget-bucket *atomicity* (0.12) | 0.03 | **3/3 land** | uniform overclaim hiding a **concrete confirmed bug** → fix the code (done, d099) |
| **exoj** | identity-fragment *inclusion-only* (0.10) | 0.15 | **0/3 land** | a **located but abstract** soft-spot → sharpen decomposition / make the bypass pool leaf-specific |
| **qthe-verify** | tamper-tick *localization* (0.17) | 0.06 | **2/3 land** | a modest tool still has a **real** hole: canonical-serialization determinism (conf 0.84) → harden |

Low-divergence + high-hit = concrete bug. High-divergence + low-hit = abstract soft-spot (or the
adversary pool missed the leaf — draw leaf-specific bypasses next). This is the audit typology.

## Real weaknesses it found (making better tools, for real)
- **rate-component** — KV eventual-consistency budget race → hardened to an honest soft-guard + DO path (d099).
- **exoj** — the inclusion-only identity rule is the charter's soft spot (and `L7-jev-soft` is shaky
  *because* exoj's JEV is a mock — the live-fold wiring, branch `claude/live-fold`, fixes exactly that).
- **qthe-verify** — byte-identical PASS depends on canonical serialization; a platform/float-format
  difference could flip a verdict. *Next: pin the serialization + document the runtime assumption.*

## How to run it on any tool
`node situations/play/weakest-leaf.mjs` (needs `TYPESAFEAI_KEY`, `MOTHQUANTUM_KEY`,
`MOTHQUANTUM_BASE`; `--no-moth` for a cents-cheap JEV-only pass). Swap the `AUDIT_TARGET` block:
`whole` (the headline guarantee), `leaves` (its decomposition), `subleaves` (level-2 for the
likely-weakest), `bypass_pool` (concrete failure hypotheses; **make them leaf-specific** for a
sharper confirm). Cost: ~11 JEV + 1 Moth run (5 credits). Book every play in the ledger.

## Next rungs
- **Leaf-specific adversary draw** (S17.1): generate the bypass pool *from the located leaf* so the
  0/3 abstract cases (exoj) become a real test.
- **S18 "The Deadband Is Lying"** — audit pincher's 0.80 confidence gate (does self-confidence track correctness?).
- **S19 "The Un-gameable Curriculum"** — steering detector (hand-picked vs Moth-drawn test set).

## Scout-confirmed limits & upgrades (2026-09-29, SOTA verified)

Three findings from the SOTA scout (SCOUT-FINDINGS-2026-09-29.md, wave 2) correct and sharpen this method:

- **The fold catches a WRONG leaf, not a MISSING one.** "Rethinking Atomic Decomposition" (2603.28005)
  found holistic judging beats self-decomposing atomic judging on completeness by +14.5–33.0pp:
  decomposition "fragments completeness reasoning, making global omission detection harder." So a
  located-weakest verdict is only as trustworthy as the claim graph — **an omitted branch is invisible
  to leaf-scoring.** *Upgrade:* run one cheap **holistic completeness pass in parallel** to the leaf
  fold and flag disagreement; a low whole-verdict with all leaves high is the omission signature.
- **Independent reach pays ONLY at the margin.** "Blind to the Pivotal Vote" (2608.06940): a tool-backed
  independent signal gives +10–23pp on one-vote-margin queries and **exactly zero elsewhere**; and
  "Nine Judges, Two Effective Votes" (2605.29800) shows a 9-model panel is ~2 independent votes
  (correlation, not aggregation, is the wall). *Upgrade:* **margin-gate** the adversary/tool escalation
  — spend independent reach only on the leaves where the sub-judges are within one vote. Averaging a
  tool score into confident leaves buys nothing (and costs credits). This is Law 7 made operational.
- **Never anchor a leaf on the whole verdict.** Showing a judge a prior score destroys its independence
  (anchoring, 2608.25869). Score each leaf cold; compute the whole–fold gap afterward.
- **Known blind spots stay routed to code:** counting, letter-level spelling, arithmetic (tokenization),
  plus verbosity/position/self-preference bias (self-preference is model-specific — Claude Sonnet 4.5
  measured *anti*-self, β=−0.229 — so don't assume a universal correction).
