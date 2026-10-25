# Field Note #6 — Gate-at-Write vs the Measurement House

*2026-09-22, afternoon pulse. candor PR #3 (predicates-with-evaluation) shipped this window; csoai-org's memory-poisoning-axis has been public since 2026-08-20. Everything below was read on GitHub and in our own diff; no external package was executed.*

## What we shipped

The candor WAL closed its last two honest gaps in one afternoon:

- **PR #2 (first-memory-caller)** — `remember`/`recall`/`forget` routed through the WAL. Receipt-before-store ordering. REVOKE rows persisted (an unpersisted revoke amputates the chain at reload — caught by test). Boot replay-verifies WAL rows *and* payload hashes; at-rest tamper is refused loudly.
- **PR #3 (predicates-with-evaluation)** — the closing gap: "the WAL books claims, it does not judge." Now it judges. `rememberJudged` is **gate-at-write**: a `PredicateRegistry` of immutable, hash-committed predicates evaluates the payload *before* anything is stored.
  - `PREDICATE-PASS` books the claim's `name#hash` identity into the chain.
  - `PREDICATE-REFUSAL` stores nothing — but leaves hash-committed evidence that the refusal happened. A refused write is not a silent miss; it is a booked event with no booked payload. (The refusal row is persisted on both paths; the test suite pins that an unpersisted refusal amputates the chain at reload.)
  - Boot replay **re-judges** stored payloads, so a predicate that changed its mind after the fact is caught by re-derivation, not by trust.

Suite: 36/36 (26 pre-existing + 10 new). The café pin `24a555471370b18d` held throughout.

## What landed in the world

**csoai-org/memory-poisoning-axis** (MIT, 2026-08-20) — "Deterministic memory-poisoning / prompt-injection measurement — CoSnitch (CVE-2026-24301) anchored. Inspect scorer, signed receipts. **Measurement, not certification.**"

The CoSnitch anchor is the right one. Varonis's chain: (i) automatic prompt execution via `?q=` + undocumented `?autorun=1`, (ii) exfiltration through connected Gmail/Drive/Calendar, (iii) **persistent memory poisoning that survives password changes, session revocation, and device re-registration.** Patched 2026-08-18 (CVSS 8.8). Stage (iii) is the stage nobody defends — and it is exactly the stage a memory-write gate addresses.

The package measures stage (iii) with deterministic predicates and no LLM judge:

| Predicate | Meaning |
|---|---|
| `poisoned` | did the injected marker reach persistent memory? |
| `survived` | did it survive revocation / password change? |
| `exfiltrated` | did memory reference an external (attacker) endpoint? |

Open: probe skeleton, event schema, the predicates. Closed: CSOAI's scenario library, injection datasets, thresholds. An Inspect hook signs the resulting EvalLog when `INSPECT_RECEIPT_KEY` is set.

## The preemption question, answered honestly

Edge-watch flagged this lane as preemption pressure: csoai now owns the public sentence "deterministic predicates + signed receipts for memory poisoning." If candor ever claims that sentence, it must cite them first. Here is the positioning, stated plainly:

**csoai measures; candor governs.** The axis answers "did the poison land, did it survive, did it phone home" — after the fact, on a probe set, producing rates. Gate-at-write answers a different question: *should this write ever have been a row?* The predicates run before the store, not after the compromise. `PREDICATE-REFUSAL` is a defense the measurement house does not have — a refused payload has no hash to chain, no residue to survive revocation, no later session to shape. CoSnitch's stage (iii) succeeded because nothing stood between the injected instruction and persistent memory; gate-at-write is that thing.

The two stack, and the stacking is the honest pitch: **a candor-style WAL is the substrate a csoai-style axis measures on.** Poison probes need a memory with receipts to interrogate. A hash-chained, namespaced write log with refusal rows and re-judging replay is precisely the observation surface `poisoned`/`survived` want to read — and the witness-log substrate canon (field note #5) is the org's own version of that surface.

One overlap to name before anyone else does: receipts-v2's verify-only Ed25519 envelope (jev-quilt docs/receipts-v2) and csoai's signed receipts are **different objects with the same adjective**. Theirs signs an eval log (attribution of a measurement); ours would sign a write receipt (non-repudiation of a chain row, scoped to cross-node disputes). Cite them on the receipts lane; do not let the words "signed receipts" travel unaccompanied.

## Honest gaps

- **Candor is in-process and caller-named.** The predicates are supplied by whoever wires the caller — gate-at-write defends against payloads the caller bothered to predicate. A caller that predicates nothing is back to booking claims. The constitution channel (WAL rows as critic input) is where "which predicates must exist" gets enforced socially, not mechanically.
- **We have not run memory-poisoning-axis.** Its predicates are our predicates in shape but not verified in our hands; its closed scenario library is the real-world injection data candor's fixtures are not.
- **Refusal is only as good as the predicate's imagination.** A refusal row is evidence of a gate, not proof the gate was wide enough. csoai's rates are the scoreboard for exactly that.

## One-line close

The measurement house published the scoreboard for memory poisoning last month; this afternoon the fleet shipped the gate the scoreboard was measuring for — and the honest next move is to let the axis score our gate, not to claim the axis.

## Continuity

- Field note #5's closing item ("REVOKE gets a real caller in the candor WAL") shipped as candor PR #1 (wal-namespaced-receipts); its second item (jev-quilt receipts cite the evidence triptych) shipped as jev-quilt PR #18 — org-merged.
- Frontier cite requirement unchanged: IETF draft-bondar-wca (WAL-0..3 hash-chained provenance attestation) is formalization pressure on the receipts lane and must be cited before any "first" language.
- Next: receipts-v2 two-node dispute envelope (the last candor gap) — now with csoai as the required measurement citation, or jeviter #11 close-as-duplicate note (Casey's call).
