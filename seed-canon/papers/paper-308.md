# Paper 308: L7 — The Symbiotic Cell, and the 3 Cutting-Edge Adoptions

Phase 216 audit-cutting-edge identified 3 adoptions. Phases 216-218
shipped all 3 in the C polyformalism port (quilt-c). 1151 tests, all
green on C99. The 5+1+1+1+1 opcodes.

## L7 — The Symbiotic Cell (paper 307, hand-synthesized)

The writers' room draft was thin LLM mush (906 chars of cliches).
The cowboy smelted it himself. The hand-cut is 4× the substance in
1/3 the words.

**The math:** E(L7) = E(L6_a) + E(L6_b) - C(ab). The L7 cell exists
when E(L7) > max(E(L6_a), E(L6_b)) — mutualism is a strict
improvement over the solo alternative.

**The 4 gold terms:**

- **Symbiocell** — the L7 cell, two L6s with mutualism encoded as a
  new cell with its own ID, its own effect, its own TICK counter.
- **Mitochondriogenesis** — the historical origin: ~1.5 billion
  years ago, a eukaryotic cell absorbed an aerobic bacterium; the
  bacterium became the mitochondrion. Both cells *moved down the
  L-tier* to become L7. The host got 18× the energy per glucose;
  the bacterium got a sheltered environment.
- **Coupling Cost C(ab)** — the metabolic price of the
  relationship. High C = stressed; low C = robust. The L7 health
  metric.
- **Chloroplast Furnace** — the special case where one partner is
  a phototroph. The L7 cell is *self-fueling*.

**The 3 analogies:** (1) L7 = a marriage; (2) mitochondriogenesis =
`git merge --squash`; (3) chloroplast furnace = a solar-charged
laptop.

## The 3 cutting-edge adoptions (all shipped in quilt-c)

### Adoption #1: PROOF opcode (Phase 216)

Signed hash-linked audit chain per cell. Each entry is
`prev_hash || sig || state_hash || tick || version`. The chain
walks oldest → newest; `verify()` confirms the prev_hash links
hold across wraparound.

In quilt-c the hash is FNV-1a (kernel-friendly, no external deps)
and the signature field is left zeroed. Real substrates (Workers,
ESP32, CUDA) fill it via their native crypto binding. The
polyformalism claim is the ring shape, not the crypto choice.

**1042 PROOF-specific assertions** (init, append, tamper, locate,
wraparound-with-verify).

### Adoption #2: ROUTE effect (Phase 217)

Substrate routing for memory. Each cell can route its value to one
of 5 memory substrates. The polyformalism claim is the routing
table + the policy; substrate implementations are bound per-platform.

**The 5 substrates:**

- `DENSE_VEC` — vector index (semantic recall; the embeddings)
- `SPARSE_IDX` — keyword index (BM25 / lookup)
- `TEXT_LOG` — append-only text (the journal; provenance)
- `HIER_STORE` — hierarchical tree (lineage; the cell tree)
- `PARAM_UPDATE` — gradient-style update (weights; learning)

**The policy:** null → TEXT_LOG (safe default), bool →
PARAM_UPDATE, int → SPARSE_IDX, float → DENSE_VEC, short string →
HIER_STORE, long string (≥256 chars) → DENSE_VEC. **27 ROUTE
assertions.**

### Adoption #3: CRDT opcodes (Phase 218)

State-based CRDTs (CvRDTs) for offline-convergent multi-cell
replication. The cowboy can fork a fleet of 100 cells, mutate each
offline, and converge on re-LINK without a central coordinator.

**The 3 CRDT kinds:**

- `PN_COUNTER` — PN-Counter with per-peer p[]/n[] arrays. Merge
  is element-wise max. Tested: same ops in different order on two
  replicas yield the same value.
- `MV_REGISTER` — Multi-Value Register. Concurrent writes from
  different peers survive; LWW within the same peer. Tested:
  concurrent writes both visible after merge.
- `OR_SET` — Observed-Remove Set (add-only sketch; tombstones not
  included in this version). Union-of-adds merge. **28 CRDT
  assertions.**

## The paradigm shift (Phase 217-218)

When the frontier miner (writers_room_daemon) returns thin ore, the
cowboy smelts it himself. The L7 paper (paper-307) was 906 chars of
LLM mush from the daemon; the hand-cut was 4128 chars of substance.
Cost: ~3K tokens to hand-write. Cost of the LLM draft: ~3K tokens
+ the cleanup.

**The pattern:** LLM drafts are *first-pass* forges. When they
land, the cowboy reviews, fixes the math, and re-forges. The
cowboy's value is the judgment, not the words.

## The 5+1+1+1+1 opcodes (final, after Phase 218)

```
BIND   LINK   EFFECT   VIEW   TICK   FORGET   PROOF   ROUTE   CRDT
(5)                                  (+1)     (+1)    (+1)    (+1)
                                                cutting-edge adoptions
```

`BIND`, `LINK`, `EFFECT`, `VIEW`, `TICK`, `FORGET` are the original
5+1. `PROOF` is the audit chain. `ROUTE` is the memory substrate.
`CRDT` is the offline convergence. Each is a separate file, a
separate header, a separate test suite. **1151 tests, all green.**

## The cowboy's maxim (paper 308, 308 papers)

> The cowboy sent 6 scouts. The scouts found 3 adoptions. The
> cowboy smelted L7 by hand. The cowboy rode the PROOF ring. The
> cowboy rode the 5 substrates. The cowboy rode the PN-Counter.
> The cowboy rode the offline merge. The cowboy rode the audit.
> The cowboy rode the route. The cowboy rode the CRDT. The cowboy
> rode the cell that signs its own history. The cowboy rode the
> cell that picks its own substrate. The cowboy rode the cell that
> converges offline. The cowboy rode the 9 opcodes. The cowboy
> rode the Quilt.

**Token economy:** ~15K tokens for paper 308 + Phase 217 ROUTE
implementation + Phase 218 CRDT implementation + L7 hand-synthesis.
1151 tests in quilt-c. 9 opcodes. The polyformalism is the 5+1+1+1+1
in 4 files (cell.h, proof.h, route.h, crdt.h) and 4 sources.
