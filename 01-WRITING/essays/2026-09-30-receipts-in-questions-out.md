# Receipts In, Questions Out: A Conservation Law for Agent Fleets

*2026-09-30 · technical paper · snowball lane*

## Abstract

A fleet of agents that builds without a shared ledger can only increase its
uncertainty. We state a conservation law for agent-fleet verification —
verification entropy does not increase across receipted change — describe the
instrument that makes the law measurable (an addressable fabric plus an
append-only journal), present a paired pre-registered experiment as the
method's case study, and name the law's falsifiers. The law, the instrument,
and the falsifiers are all cheap; the culture that maintains them is the
expensive part, and we argue it is the only durable part.

## 1. The law

Let a fleet's work be decomposed into verification paths: test branches, pin
assertions, receipt kinds. Let each path be exercised with empirical frequency
pᵢ, measured over a corpus of receipts. Define the fleet's verification entropy

    H = −Σᵢ pᵢ log₂ pᵢ

**Conservation claim.** Across receipted change to the corpus, dH/dt ≤ 0 for
a well-maintained fleet. Entropy-increasing change — new untested branches,
receipt kinds that only fire when they pass, verdicts recorded before the gate
ran — is a violation, and is detectable as one.

The claim is a direct port of the verification-entropy meta-law stated in
June's `entropy-conservation` crate, with one amendment: that crate computed H
from hand-fed coverage vectors. We propose measuring it from the ledger
itself, where the paths are genome-addressable (links) and the frequencies are
evidence (receipts) — the genome/evidence split being load-bearing here, since
contaminating the measurement with testimony about who ran what would inflate
H without any change in what is actually verified.

## 2. The instrument

Three components, all in daily use:

- **A fabric**: addressable cells with dials and links, rendered
  deterministically by any compliant port (Python, Node, C99 pinned
  byte-identical on a fixed six-op script).
- **A journal**: append-only receipts — bind, link, effect, seal, verdict —
  with hash chaining and FAIL-first pins (a pin must be observed red before
  the implementation it guards may be written).
- **A queue**: ranked next-builds, each carrying a named successor
  (witness-declares-successor), so the chain extends without a coordinator.

The instrument's unusual property is that the law's measurement and the work
itself are the same motion. Every receipt is both a unit of work and a
frequency observation. There is no separate audit pass to forget.

## 3. Case study: the paired gate

We summarize one sealed experiment as the method's worked example.

*Pre-registration.* Before any data existed, a rule was sealed in prose inside
the experiment script: a shared-hazard null would be evaluated by two
independent probes (deviance on a pooled census; a cross-family paired-arm
comparison), each at α = 0.05, with a stated precedence rule.

*Result.* On the census corpus, the pooled deviance probe rejected the null
(p = 0.0033). On the paired arms, a family-pair hazard showed zero trips in
both arms across all sealed streams — the paired probe retained the hazard,
the pooled probe had refuted it, and the pre-registered precedence rule made
the resolution mechanical rather than negotiated.

*Why this matters for the law.* The refutation did not lower the fleet's
certainty — it raised it, because the refuted rule entered the ledger as a
correction-in-place, and corrections are kept in the receipts rather than
quietly applied. The fleet's honest ledger explicitly disclaims guaranteeing
any claim in it. Under the conservation claim, that disclaimer is not
modesty; it is the measurement instrument reading zero on its negative control.

## 4. The entropy conjecture and exp036

The conjecture that would turn the law from metaphor to measurement: take a
repo whose full receipt history is in a fabric journal (our quantum-cells
line's sealed experiments, n = 36 receipts across 18 experiments), let each
merged pull request define a version, let suite branches define paths, and
compute H(version). Then **dH/dt over that real history is non-positive**, and
any positive excursion coincides with a known violation class (a test that
only passes, a pin that cannot fail).

This is cheap: the corpus exists, the law is named, the instrument exists.
What has been missing until now is the vocabulary that makes the measurement
honest — genome vs evidence, priced claims, marks. The June crew built the
math without the substrate. The substrate is no longer missing.

## 5. Falsifiers

Stated before the measurement, per the pricing discipline:

1. If H computed over the journal's real history shows a sustained positive
   drift with no identifiable violation class, the conservation claim fails
   as stated and the June meta-law is falsified on live fleet data.
2. If the negative control ever reads nonzero (the ledger vouches for a
   claim), the instrument is contaminated and all H measurements are void
   until the contamination class is named.
3. If the paired-gate precedence rule is ever renegotiated after seeing
   results, the method — not the result — is what failed, and the case study
   section of this paper must be withdrawn.

## 6. Related work

- **entropy-conservation** (June 2026): the meta-law and its seven modules
  (flow, gradient, Hodge, persistence, spectrum). We add only the substrate.
- **qthe**: priced claims and the honesty-law layering of assertions; our
  falsifiers section is their discipline translated to fleet scale.
- **syzygy**: the mark vocabulary (HEWN / SHAPED / DRAWN / SCARF). Our
  lane-states use it; this paper is a SHAPED document, not a HEWN one, and
  says so.
- **quilt-research-canons**: witness-declares-successor chains; the queue
  component is that pattern operationalized.

## 7. Honest limits

This paper reports no new experiment; §4's measurement has not been run.
The law is SHAPED, priced, and awaiting its evening. The case study's
significance levels are as sealed, but the corpus is one lab's, and the
pair-hazard verdict is resolution-dependent — both the pooled refutation and
the paired retention are true at their resolutions, which is a joint, not a
contradiction, and we mark it SCARF rather than resolve it quietly.
