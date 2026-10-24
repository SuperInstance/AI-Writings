# metabolizer — grow → freeze → patch-in → refine → re-freeze

A VERIFIED capability becomes a reusable, routable **expert patch** (a patch is a cell; general-purpose
means routable, not numerous). Wires existing cells; reinvents none:

| piece | from |
|---|---|
| Cell receipts, Differ, Ledger, budget vector, `price` (B7 gate + B4 pick) | `labs/quilt-kernel` |
| invariants a capability preserves (`mine`) → seeds the gate's probes | `labs/invariance-miner` |
| version-witness: Ville-bounded e-process that RETRACTS on drift | `labs/priced-training/route_witness.py` |
| cross-check of the cheaper-route pick on the iron-triangle axes | `labs/route-preference` |

A **frozen patch** = **gate** (domain + invariance probes that can say "no"; a gate that cannot decline is
refused) + **budget tier** + **version-witness** (live capability vs frozen snapshot; retracts on drift,
patch then refuses to serve until `refreeze()`).

**Composition = routing.** Product-identical members (Differ-certified) → the cheaper wins. Members that
disagree → the resolution is frozen as a **blend patch** (referee cases gated: only cases whose expected
product equals a member's product survive). The router is itself a patch.

`crew.sh` fetches cheap-crew fixture proposals (DeepInfra); `metabolizer.gate_crew` / `gate_cases` filter
them — crew output is never trusted raw. `fixtures/crew_proposals.json` is a saved proposal set.

```
python3 selftest.py     # metabolizer selftest: 74 checks, 0 failures
```
Selftest covers (a) freeze + decline of an out-of-invariant input (tab quirk invisible to the miner's log),
(b) witness retraction on drift + re-freeze (invariants re-mined), (c) identical products → cheaper, incl.
role-swap, (d) disagreement → blend that is gated, witnessed, retracts on member drift and re-freezes.
