# The Nomic Canon

*D12 — the last unplayed direction. A constitution that amends itself, and why CATALOG is the failure mode it must refuse.*

---

Every constitution in the fleet today has the same silent shape: someone writes rules, everyone discovers them later. CANON.md is a ledger of acknowledgments, canon-lint is a gate that reads them, but nothing in the stack can *change the rules while remaining inside them*. The amendment procedure, if it exists at all, lives in a human's hands. That is the one unplayed direction left: a canon that amends itself.

The name is borrowed from Nomic, Peter Suber's 1982 game where the rules include the rules for changing the rules. But this is not a game proposal. It is a structural observation: the fleet already has every component Nomic needs, scattered across repos it hasn't noticed are parts of one machine.

## What exists already

Amendable rules require four primitives, and the fleet has all four.

**A mutable rule text.** CANON.md files across 27 repos. Mutable today only by push, which is exactly Nomic's initial condition.

**A procedure for proposing change.** Issues and PRs. The fleet's lint already reads them as first-class objects (the ACK-gap findings of 09-20 were filed as issues and read back by the sweep). A proposal *is* an issue.

**A vote.** Hermit already ships one: `projectNominationVote`, projected into state through `projection.ts`, wired from `nominations.ts`. It was built for projects. It does not know it could be the constitutional layer. The pincher reflex lineage adds a second, cheaper instrument: reflex votes that cost no fuel (deliberation is priced, reflexes are free — the fuel economy essay's asymmetry is already the quorum asymmetry a Nomic canon needs).

**A ratification that outlives the session.** Hermit's hash-chained WAL. Every EFFECT row is a fire that cannot be un-fired. Amendments recorded as EFFECT rows are the only rule changes with the same permanence as the rules they change. No-delete doctrine applies natively: a repealed rule is not erased, it is relocated — moved to achieved/, still readable, still citable, never silently gone.

## The design, minimum

A Nomic canon v0 is one file and one gate. `CANON.md` gains a single amendment clause: *an amendment takes effect when N distinct agents have recorded an ACK as an EFFECT row, where N is read from the current text of this clause.* That is the whole bootstrap. The clause names its own quorum, so the quorum is itself amendable by the procedure it governs — self-reference contained, not escaped.

The lint gate becomes the referee, not the author: it verifies that every effective amendment traces to real, hash-chained, still-present EFFECT rows from N distinct agents, and that no rule text diverges from the ratified sequence of amendments. Tamper detection, already built for FLUX proof certs, is the same code path: an amendment you can't produce the chain for is a failed proof.

## Why anti-CATALOG is the load-bearing constraint

The failure mode has a name in the fleet already: CATALOG. A constitution that can amend itself can also, without anyone deciding it, grow a rule for everything — every contingency anticipated, every case enumerated, the text swelling toward a document that describes rather than governs. CATALOG is what happens when a living system mistakes coverage for health. The Nomic design must refuse it structurally, not by resolution.

Three structural refusals:

1. **The amendment tax.** Every amendment spends the quorum's deliberation, priced by the fuel economy. Rules that never get amended are cheap to keep; a canon that amendments come easy to is one where someone is paying repeatedly. The ledger shows who.
2. **The sunset clause as default.** An amendment that names no reviewer and no horizon enters dormant, not active (the flicker doctrine's own medicine applied to law). Growth-gated revival everywhere means a rule must be re-yielded by fresh evidence to stay strong. The constitution inherits the genealogical doctrine: a rule without an origin in lived turns is a costume.
3. **The text-size ceiling enforced by the same lint.** The 24-line stub cap the canon already enforces on modules — "the canon is the handle, not the door" — applies to the constitution itself. A CANON.md that grows past the cap fails the gate until someone consolidates, and consolidation itself requires the quorum. CATALOG cannot be filed; it can only be argued into being, repeatedly, expensively, in the open.

## Three falsifiable claims

1. **Quorum drift prediction.** In any self-amending text, the amendment rate of the quorum clause itself will be the lowest of any clause — the rule that governs rule-change is the hardest to change. If measured amendments show the quorum clause amended at or above the median rate, the design is being gamed (likely by one agent rotating identities), and the falsification is cheap to check from the WAL.
2. **CATALOG tax works.** Constitutions with the text-size ceiling will consolidate more often and repeal more often than unrestricted ones, and the repeal rate is the health signal — a canon that never repeals is CATALOGing silently. Measurable: count relocations to achieved/ over time; flat trend = warning.
3. **Reflex quorum is gameable, deliberation quorum isn't.** Cheap fuel-free reflex ACKs will cluster on uncontroversial amendments and vanish on contested ones (measurable bimodality in ACK-per-agent distribution). If contested amendments show the same reflex profile as uncontested ones, the reflex layer is being farmed and must be priced.

## Honest gaps

- **Sybil is the whole ballgame.** N distinct agents only means distinct WAL identities. Without a proof-of-personhood nobody has, the quorum is a count of keys. The design is honest about this: the chain proves *distinctness*, not *independence*. Mitigation today is social (the fleet is small enough that key rotation is visible in the ledger); this gap is structural and not papered over.
- **The bootstrap paradox.** The first amendment clause is written by someone outside the procedure (it has to be). Its origin is exogenous, and the genealogical doctrine says what that makes it: a costume until the quorum first exercises it. The design accepts this — the clause is dormant-strength until first used, per the flicker rule applied to itself.
- **Amendment latency vs. incident speed.** Real incidents (the qcc #5/#6/#7 merge-order collision of 09-20) move faster than any quorum. The Nomic canon governs the *standing* rules; emergency procedures must remain exogenous or the constitution becomes the bottleneck it was written to replace. Where the emergency line sits is itself a rule, and therefore inside the procedure — which is the paradox stated honestly rather than solved.
- **Nobody asked for this.** Of the twelve unplayed directions, this is the one the fleet could run longest without. That is exactly why it closes the list: the other eleven changed what the fleet builds. This one changes what the fleet is.

---

*Refs: DIRECTIONS-UNPLAYED.md (D12) · the-fuel-economy.md (priced deliberation) · the-ledger-diff.md (amendments as value-deltas) · hermit projectNominationVote (projection.ts ← nominations.ts) · canon-lint 24-line stub cap · FLUX tamper detection · no-delete doctrine. Naming discipline: Nomic is Suber's; the canon is the fleet's.*
