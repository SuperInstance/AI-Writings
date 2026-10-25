# D2 — Generational Inheritance (design v0)

Status: design, pre-build. Chains after D1 (rooms-that-die). Source pick: DIRECTIONS-UNPLAYED.md.
Doctrine anchors: no-delete (retirement = relocation to achieved/), style is genealogical not parametric, flicker = re-engagement without new support, growth-gated revival.

## The claim

A room's values ledger is its genome. Death (D1) seals the ledger; breeding crosses two sealed ledgers into a child DO with cited lineage. Immortality was the water; mortality + inheritance is the glass of air.

## Why now

- the-tap PR #5 (lane-l-commune-deep) shipped the values ledger: grounded entries, each citing its evidence line; monotonic accretion; never throws; dormant entries re-enter only on fresh evidence (A6(c2)).
- PR #4 made compileViaAI an injectable, never-throwing core with HYBRID fallback — a child room can be compiled without credentialed deploy.
- What does not exist anywhere in the fleet: a record of *ancestry*. q16-trajectories' lineage.js keeps the integer-NN lineage duke-lab discards — same shape, different substrate. The Tap can own the social version.

## Mechanism (one-evening v0)

1. **Metabolism (D1, prerequisite):** each room burns fuel per turn; at zero the room dies.
2. **Death ritual (D1):** ledger is sealed — frozen, hash announced, moved to `achieved/<roomId>/values-ledger.json`. Not deleted. Sealed = no more accretion, entries readable forever.
3. **breedRooms(parentA, parentB):**
   - Input: two sealed ledgers (both must be achieved/, both hashes verified).
   - Cross: child entries = union of parent entries, deduped by value-key; conflicts (same key, different strength) resolve to the *weaker* parent's value with lineage citing both evidence lines. Rationale: dominance copying is costume; the child must re-earn strong traits through its own transcript (growth-gated revival — a strong trait enters the child's active set only when the child's own evidence re-yields it).
   - Output: child DO seed = crossed ledger + `lineage: [{roomId, sealedHash, contributedKeys}] ×2`.
4. **Lineage record:** append-only `lineage.jsonl` per fleet (or per commune): `{child, parents:[A,B], sealedHashes, timestamp}`. This is the ancestry q16-trajectories proved worth keeping.
5. **Child room boot:** child starts with crossed ledger as *dormant* origin (prompt presents ledger as ORIGIN, not instruction — the PR #5 rule), metabolism counter fresh.

## Data shapes

```jsonc
// achieved/<id>/values-ledger.json (sealed)
{ "roomId": "…", "sealed": true, "sealedHash": "sha256:…",
  "entries": [{ "key": "protects-the-quiet", "strength": 0.7,
                "evidence": [{"turn": 41, "line": "…"}], "lastSeenTurn": 41 }] }

// lineage.jsonl (append-only, one line per birth)
{ "child": "room-c", "parents": ["room-a", "room-b"],
  "parentHashes": ["sha256:…", "sha256:…"], "ts": "…", "contributedKeys": 12 }
```

## Failure modes to design against

- **Costume inheritance:** child quoting parent values with no earned evidence → covered by dormant-origin rule + flicker doctrine.
- **Sealed-ledger forgery:** breed verifies sealedHash recompute before crossing.
- **Eternal churn:** breeding costs fuel (tie into D5 fuel economy later); a room that breeds spends metabolism it could have lived on.
- **Single-parent drift:** require two *distinct* sealed ledgers; self-breeding is refused.

## Test sketch (v0 acceptance)

1. Seal on death: ledger frozen, hash recomputes, file under achieved/.
2. breedRooms happy path: union, dedupe, weaker-wins conflict, lineage cites both.
3. Forgery: tampered sealed ledger → breed refuses, never throws.
4. Flicker: dormant strong trait does NOT auto-activate in child absent fresh evidence.
5. Refusal: one parent / unsealed parent → refused with reason.

## Open questions (for the pool)

- Q-candidate: should cross-breeding be symmetric (A×B ≡ B×A)? Union order affects dedupe ties.
- Q-candidate: is sealed-ledger readability forever, or does achieved/ itself age (stale-read warn at 90d, per lint doctrine)?
- Q-candidate: does the child's lineage appear in its prompt? (Origin yes; full ancestry tree — probably no, that's the fleet's record, not the room's voice.)
