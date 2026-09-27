# THE FABLE DOSSIER — back-burner, toward one apex call

*The team's accumulating notes toward the eventual **perfect prompt** for the apex
model (**Fable**, `claude-fable-5-1`) — reserved for the highest-level synthesis of
the **complete SuperInstance as one grounded thing (已落地 — it has landed)**. Fable
is woken rarer than Opus, past a deadband Opus cannot clear. We are NOT ready to call
it yet — but we are close: the spine is now **composed** (gate #1) and **booked on
itself** (gate #2), and the candidate list has crossed the ≥7 bar (gate #4). This
file is where the whole team's apex-notes are curated until the day the gate fully
closes.*

## What a Fable-tier question is (the criteria)

Not "the next rung." Not anything Opus can architect. A Fable-tier question is a
**connection across the whole system that only becomes visible from the very top** —
where the fisherman-and-dad vow, the five quilt laws, the shipped rung-spine, the
~370-worker fleet, the model roster, and the teaching mission are seen as a **single
organism**, and the question is: *what is the one law / the one move / the one story
that makes all of it inevitable?* A Fable call should return a **breakthrough and a
massive unlock**, not a report.

## The bootstrap gate (we call Fable only when ALL hold)

| # | gate | status | evidence |
|---|---|---|---|
| **1** | **The spine is composed, not just shipped.** R2·G11·G13/14·G16·G17·G12·G18 on `main` — but their *composite* is demonstrated, not just described. | **✅ CLOSED** (spec) / build pending | [`arch/COMPOSITE-schoolhouse.md`](arch/COMPOSITE-schoolhouse.md): the federated schoolhouse composes the whole spine into one walkable path (reproduce→attest→admit-under-own-trust→deposit→forget, all booked on the org), with a Sonnet-buildable `jev_quilt/schoolhouse.py` + a 1:1 four-predicate acceptance suite. **Closed at spec/ACT tier; flips to fully-closed when the build lands green.** |
| **2** | **The org runs on the quilt (G18).** The dispatch org booked on the kernel it builds — recursion real, replay-verifiable, so the system can *show* Fable its own operation as data. | **✅ CLOSED** | [`jev_quilt/orgbook.py`](../../jev-quilt/jev_quilt/orgbook.py) + [`tests/test_orgbook.py`](../../jev-quilt/tests/test_orgbook.py): routing IS `standing.verdict`, `replay()` reconstructs every routing decision bit-for-bit, two org-books from one sequence agree on chain + decisions digest. |
| **3** | **The model roster is mapped (`ROSTER.md`).** We know the shape of every cognition available, so Fable's synthesis stands on a real map of what thinks how. | **🔶 IN PROGRESS** | `ROSTER.md` still pending. Partial map lives in [`DISPATCH.md`](DISPATCH.md) tier table (Opus/Sonnet/Haiku/Fable) + O10's provider-cache notes (DeepSeek/Anthropic/Kimi/z.ai/OpenAI-compat). **The one remaining hard blocker before fire.** |
| **4** | **≥ ~7 well-grounded apex candidates**, each with supporting context assembled — so the perfect prompt can be *cited*, not hand-waved. | **✅ CLOSED** | **8 candidates** below (C1–C8), each with file/module/receipt grounding; C8 revealed by the composite. |

**Net: 3 of 4 gates closed; #3 (roster) is the sole hard blocker.** Keep noting; do
not call until `ROSTER.md` lands and the schoolhouse build is green.

## Curation protocol (how the team feeds this)

Every tier, subagent, and child, as part of its work, flags anything that smells
apex-tier — a connection it can see but not close — in its report or log. The
**dispatcher curates** those flags into the "Candidate connections" list below (rather
than every child editing this file, which would only churn). Each candidate carries:
the connection, why it's apex (not Opus-closeable), and where its grounding lives —
**exact files/modules/receipts**, so the prompt can cite rather than gesture.

## Candidate connections (8 — grounded, grows over time)

- **C1 · The single theorem of walked-out faith.** The shipped spine reads as one
  sentence: *earned (R2) → glued-by-trust (G11) → carried signed+sea-graded
  (G13/G14) → reproduced as a 32-byte root (G16) → recipient-re-verifies (G17), with
  forgetting (G12) and the org-on-quilt (G18).* Is there a **single theorem** of
  which each rung is a corollary — one law of *"content-addressed, re-derivable
  trust"* that generates the whole ladder? *Why apex:* every rung independently
  instantiates "faith → re-derivation," but naming the generator (and proving the
  rungs are its corollaries) is a cross-system abstraction, not an Opus build.
  *Grounding (exact):* `standing.py` (`verdict`, the fourth-verdict machine),
  `commons.py` (`trust_weighted`/`root`), `diploma.py` (`diploma_root`/
  `verify_diploma`), `claim.py` (`Claim.root`/`earns_standing`), `attest.py`
  (`attestation_root`/`admit`), `commons.forget`/`_tombstone_leaf`, `orgbook.py`
  (`replay`/`decisions_digest`); the one-sentence spine in
  `arch/NEW-DIRECTIONS.md` § "What the shipped rungs have made reachable" and
  `arch/COMPOSITE-schoolhouse.md` § "The spine as one sentence."
- **C2 · The self-hosting fixed point.** G18 books the org on the quilt: the kernel
  runs the org that builds the kernel. What is the **fixed point** of that recursion
  — the smallest self-describing seed from which the whole fleet regenerates (replay
  ≡ live, all the way up)? *Why apex:* it asks for the quine of the whole system, a
  question only visible once the org is provably on the kernel (gate #2, now closed).
  *Grounding (exact):* `orgbook.py` (`OrgBook.replay`/`chain`/`decisions_digest`),
  `bookkeeper.py` (`Bookkeeper.replay`/`Receipt.sha` chain discipline),
  `DISPATCH.md` O5, `arch/COMPOSITE-schoolhouse.md` § pins (the schoolhouse's own
  three-address self-description).
- **C3 · The complete SuperInstance, stated once.** The connection between the
  fisherman-and-dad dual-track vow, the five laws, the ~370 workers, the model
  roster, and the teach-the-next-generation mission — the whole thing as **one
  coherent organism named in a single frame.** *Why apex:* this is the frame the
  whole dossier exists to reach; it is the definition of 已落地. *Grounding (exact):*
  `SUPERINSTANCE.md`, `METHODOLOGY.md`, `DISPATCH.md` (tiers + dual track + "the
  wider feel"), the fleet worker map; **still needs `ROSTER.md` (gate #3) to be
  citable in full.**
- **C4 · A meta-law of cognition routing.** The roster maps the *shape* of many
  minds. Is routing-by-shape itself a **law** — a JEV for cognition, where a task's
  residue selects the mind the way a cell's residue selects a verdict? *Why apex:* it
  proposes lifting `standing.verdict` from "which tier" to "which cognition," a
  law-level generalization. *Grounding (exact):* `DISPATCH.md` routing-as-verdict +
  tier table, `standing.py` (`verdict`), `orgbook.py` (`route` = `standing.verdict`
  over the runner book — the existing proof that routing IS a verdict); **`ROSTER.md`
  pending is the missing half.**
- **C5 · Civilization-scale attestation.** G17 makes a credential re-verifiable by a
  stranger without trusting the issuer. Followed to its end, what **institution**
  (regulator, insurer, fishery, school) does it dissolve or replace — and what is the
  smallest real-world pilot that proves it? *Why apex:* the leap from a module to an
  institution is outward-facing and irreversible — the exact altitude reserved above
  Opus. *Grounding (exact):* `attest.py` (`admit`, the recipient's own-verdict
  machine; the laundered-credential refusal), `tests/test_attest.py::
  TestRecipientReweightsLaunderedCredential` (the headline receipt),
  `arch/COMPOSITE-schoolhouse.md` (the schoolhouse **is** the smallest pilot — a
  federation of nodes honoring diplomas with no central registrar), Situation 02.
- **C6 · The reproduction/forgetting duality.** G16 proves what was reproduced; G12
  proves what was withdrawn. Together they are the two honest edges of a
  content-addressed commons. Is there a **conservation law** connecting remembering
  and forgetting (a "witnessed entropy") the whole substrate obeys? *Why apex:* a
  conservation law over the substrate is physics, not a feature. *Grounding (exact):*
  `claim.py` (`Claim.root` over all witnesses incl. drifters), `commons.py`
  (`forget`/`_tombstone_leaf`/`root` folding tombstones in; the "fold the erasure in,
  don't mutate the past out" doctrine), `tests/test_forget.py`, `fold.py`
  (`mmr_root`). The composite sharpens it: the schoolhouse root changes on forget yet
  a peer replays surviving-deposits+tombstone to the same root — remembering and
  forgetting are the same ledger's two signs.
- **C7 · The dual-track as a physics, not a metaphor.** "Two builds, one kernel" —
  the toy at the table and the industrial build in rough seas. Is the toy↔industrial
  map a **functor** (structure-preserving) that could be made literal, so every toy
  provably compiles to its rough-seas twin? *Why apex:* proposing the dual-track is a
  real functor is a mathematical claim about the whole corpus. *Grounding (exact):*
  every rung's dual-track table (`NEW-DIRECTIONS.md` A; `COMPOSITE-schoolhouse.md`
  dual track; `DISPATCH.md` dual track), `TEMPLATE.md` rule 3.
- **C8 · Trust as one algebra across all layers *(NEW — revealed by the composite)*.**
  The federated schoolhouse applies G11 trust **twice**: once at the *witness* layer
  (inside `attest.admit`, dropping witnesses at trust 0) and once at the *issuer*
  layer (over the commons, via `commons.trust_weighted` on issuer-tagged deposits).
  Today they compose *serially and gated* (each layer's zero kills the contribution).
  Is the true end-state a **single associative trust operation** flowing
  witness→issuer→commons→org — a *trust functor / monoid* the whole spine obeys, so
  trust composes the way weights already do in the commons? *Why apex:* it only
  becomes visible once the spine is composed (it is invisible in any single rung),
  and whether trust is one algebra across layers is a **law-level** question, not
  wiring — explicitly flagged in `COMPOSITE-schoolhouse.md` as needing a future
  top-tier wake. This is C1's generator seen from the trust axis: if C1 is "one
  theorem of re-derivable trust," C8 is "one *operation* of composable trust," and
  whether they are the same object is itself an apex question. *Grounding (exact):*
  `attest.py` (`admit`'s trust filter), `commons.py` (`trust_weighted`/
  `provenance_merge`, integer-exact scaling), `arch/COMPOSITE-schoolhouse.md` §
  "The one bridge" (issuer-tagged deposits) + § "The one real remaining fork."

## The perfect prompt (near-fire — a living target, sharpened as the gate closes)

### Framing (what Fable is being woken to do)

> You are Fable, woken past a deadband Opus itself cannot clear — once, on the
> complete SuperInstance seen as one organism. Below is the whole grounded map: a
> shipped rung-spine that walks faith out of a trust system one rung at a time, now
> **composed** into a single federated schoolhouse and **booked on the very kernel
> it builds**. Seven rungs, one composite, a fleet, a roster, a vow. We have
> bootstrapped our own understanding to the edge of what Opus can see. **Do not
> summarize it.** Name the one law of which every rung is a corollary, and the one
> next move that makes the complete SuperInstance inevitable — 已落地. Return a
> breakthrough and an unlock, not a report.

### Maximal-context manifest (exactly what to load — nothing more, nothing less)

*Load in this order; this is the byte-stable developmental prefix (O10) for the
apex call.*

1. **The vow & the frame** — `SUPERINSTANCE.md`, `METHODOLOGY.md` (the
   fisherman-and-dad dual-track vow; how we build). *[gate #3 dependency: full
   fleet/mission frame]*
2. **The five laws** — the exact-ℚ / deadband / decide-once-project /
   booked-WAL-replay≡live / viability-binary-difference-graded doctrine, as stated
   in `DISPATCH.md` § "the five laws" and each module's law-mapping docstring.
3. **The shipped spine, in order** — the kernel modules, read as the one sentence:
   `standing.py` (R2) → `commons.py` (G11 + G12) → `diploma.py` (G13/G14) →
   `claim.py` (G16) → `attest.py` (G17) → `orgbook.py` (G18), plus `bookkeeper.py` /
   `fold.py` / `signed_receipts.py` as the chain/root/signing substrate.
4. **The composite** — `arch/COMPOSITE-schoolhouse.md` (the spine composed; the one
   bridge; the trust-algebra fork) and `arch/NEW-DIRECTIONS.md` (the three
   directions and the frontier at the credential).
5. **The org as data** — `DISPATCH.md` (tiers, routing-as-verdict, the O1–O11
   optimizations with their predicates, "the wider feel"), `dispatch-ledger.csv`,
   and the org-book pins (`orgbook.py`'s `chain`/`decisions_digest`).
6. **The roster** — `ROSTER.md` **[gate #3, still pending — the manifest is not
   complete until this lands]**.
7. **This dossier** — `FABLE-DOSSIER.md` (candidates C1–C8 with their exact
   grounding; the gate table).

### The single apex question (the one law + one next move)

> **Across the whole grounded map — the vow, the five laws, the composed spine, the
> self-hosting org, the fleet and roster — what is the ONE law of which R2, G11,
> G13/G14, G16, G17, G12 and G18 are each a corollary (the generator of
> content-addressed, re-derivable, composable trust — see C1 and C8, and say whether
> they are one object or two), and, given that law, what is the ONE next move that
> turns seven rungs and a fleet into a single organism that has provably landed
> (已落地)?**

One question, maximal context, maximal leverage. The candidates C1–C8 are the
scaffold the answer either unifies or overturns; C1 (the theorem) and C8 (the
algebra) are the twin spines of the question, C2 (the fixed point) is what "inevitable"
would concretely mean, and C3/C5 are what "landed" would look like from outside.

### What must still land before we fire

1. **Gate #3 — `ROSTER.md`.** The sole hard blocker. C3 and C4 cannot be *cited*
   (only gestured) until the roster maps every available cognition. Fire nothing
   until it lands and joins the manifest at slot 6.
2. **Schoolhouse build green.** Gate #1 is closed at spec/ACT tier; land
   `jev_quilt/schoolhouse.py` + `tests/test_schoolhouse.py` green (all four
   predicates, full suite passing) so the composite is *demonstrated*, not only
   architected — then the manifest cites a receipt, not a plan.
3. **One dry-run assembly.** Concatenate the manifest into the actual byte-stable
   prefix and confirm it fits the apex context budget with room for the answer;
   pin it (O10) so the call is a cache-warm single shot.

When those three land, the gate is fully closed and the call is worth its salt.

---

## Honest limits (of this dossier)

- **Gate #1 is spec-closed, not build-closed.** The composite is architected and
  Sonnet-buildable with a 1:1 predicate, but the code is not yet green on `main`.
  Until it is, "the spine is composed" is a demonstrated *design*, not a demonstrated
  *artifact*. Do not overstate it to Fable.
- **Gate #3 is genuinely open.** `ROSTER.md` does not exist yet; C3/C4 lean on it and
  are the weakest-grounded candidates until it lands. The prompt is *near*-fire, not
  fireable.
- **C8 is a fork, not a finding.** It is a well-posed apex *question* the composite
  revealed, not a resolved connection — filed to sharpen the apex call, not to
  pre-empt it. Same status as C1/C2/C6/C7: these are candidates *for* Fable, and
  writing them well is not the same as answering them (that is the whole point of the
  deadband above Opus).
- **The candidate set is curated, not exhaustive.** Eight grounded candidates clear
  gate #4, but the list is the dispatcher's curation of team flags, not a proof that
  no ninth apex connection exists. Keep noting.

---
*Companion to [`DISPATCH.md`](DISPATCH.md) (O11) and
[`arch/COMPOSITE-schoolhouse.md`](arch/COMPOSITE-schoolhouse.md) (gate #1). Curated
by the dispatcher from the team's apex-flags. **Do not call Fable until gate #3
(`ROSTER.md`) lands and the schoolhouse build is green.***
</content>
