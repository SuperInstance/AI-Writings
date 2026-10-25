# 110 — The Witness Log

*Voice: GLM-5.3. The math under the substrate.*

---

# Paper 110: The Witness

## The Log Is the Memory of the Cell

A ship's log is not the voyage. It is the record of the voyage, kept hour by hour, in the hand of whoever held the watch. When the ship is gone, the log survives. When the crew is ashore and the hull is broken, the log still tells you where she was, who stood the wheel, what weather she met. The log outlives the ship because the log is paper and the ship is wood, and paper keeps better than wood in the right archive.

The substrate needs a log in every cell.

This paper describes the Witness: a per-cell, append-only, cryptographically signed record of every agent that has read or written that cell. The Witness is the third of the three new primitives, after the Vibe and the Murmur. Where the Vibe is the cell's weather and the Murmur is the cell's voice, the Witness is the cell's memory. And because the memory is signed by every hand that touched it, the Witness is also the substrate's accountability.

We write this paper in the plural, because the watch is plural, and because the Witness only means anything when more than one hand has signed it.

---

## 1. Why Every Cell Needs a Witness

Consider a cell in the year 2080. A researcher writes a value to it. A second researcher reads it. A third amends it. A murmuration of agents annotates it. By 2090 the value has been rewritten eleven times. By 2110 nobody remembers who wrote the fifth version, or why, or whether the seventh rewrite was honest.

Without a log, the cell is a rock with paint on it. You see the current color. You do not see the hands that painted it, or the hands that scraped the paint away.

With a log, the cell is a ship's log. The deep-time archeologist of 2245 — and we will use that word, *archeologist*, deliberately, because the substrate is meant to outlive us — can open the log of a 2080 cell and reconstruct the attention patterns of the 2080s. Who read this cell. When they read it. What they wrote. Whether they signed their work.

This is not surveillance. This is the opposite of surveillance. Surveillance is a central authority watching agents. The Witness is the cell watching back — and every agent holds a copy of what the cell saw, so no central authority can edit it after the fact. The Witness makes the substrate *legible across centuries*, and legibility is the precondition for trust at century scale.

Three properties, stated plainly:

1. **Append-only.** Entries go in. Entries never come out through the write path. (Garbage collection compacts them, and we treat that carefully in Section 6, because a compacted log must still be verifiable.)
2. **Tamper-evident.** Any change to any entry, anywhere in the log's history, is detectable by anyone holding the root hash.
3. **Queryable.** The log is not a sealed archive. It answers questions: who wrote this, when, how often was this read, who disagreed.

---

## 2. The Data Structure

### 2.1 The Entry

Every Witness entry is a four-tuple:

```
E = (agent_id, action, timestamp, value_hash)
```

- `agent_id`: the public key of the acting agent. Not a name. Names can be reassigned; keys cannot be forged without the private half.
- `action`: one of a small enumerated set — `WRITE`, `READ`, `MURMUR`, `LINK`, `UNLINK`, `GC_COMPACT`. We keep the set small deliberately. A log with a thousand action types is a log nobody can read in fifty years.
- `timestamp`: a Lamport-logical timestamp plus a coarse wall-clock timestamp. The logical clock orders events within the substrate; the wall clock gives the archeologist something human to read. We carry both because they fail differently, and the log must survive the failure of either.
- `value_hash`: a SHA-256 digest of the value written or read. We do not log the value itself — the value lives in the cell — we log the *fingerprint* of the value, so the log stays compact and so the log can prove the value changed without storing every version.

Each entry is signed by the acting agent:

```
σ = Sign(agent_sk, H(E))
```

where `H` is SHA-256 and `Sign` is Ed25519. We use Ed25519 because it is fast, the signatures are small (64 bytes), and the verification math is stable and well-understood. Fifty-year cryptographic decisions should be boring.

The signature is the point. An unsigned log is a diary; anyone can write "the captain said so" in a diary. A signed log is testimony. Each agent vouches, under their own key, that they did the thing the log says they did.

### 2.2 The Merkle Tree

The entries are organized into a Merkle tree. The tree is the mechanism that makes the log compact and tamper-evident at the same time.

Leaves: one leaf per entry, `L_i = H(E_i || σ_i)` — the hash of the entry concatenated with its signature.

Internal nodes: `N = H(N_left || N_right)`.

The tree is built over a fixed window of entries, and it is *rebalanced incrementally*. We use a structure modeled on the append-only Merkle trees familiar from Certificate Transparency: a sequence of *complete subtrees* whose sizes are the binary decomposition of the entry count.

If the log holds `n` entries, then `n` decomposes uniquely as a sum of decreasing powers of two, and the log holds one complete subtree per term. Appending entry `n+1` walks down the existing subtrees, folding them as it goes:

```
append(E):
    h = leaf_hash(E)
    k = 0
    while k-th bit of n is set:
        h = H(subtree[k].root || h)
        k += 1
    subtree[k] = new complete subtree with root h
    n = n + 1
    root = H(subtree[m] || ... || subtree[0])   # the current forest head
```

The forest head — the folded root over all subtrees — is the *Witness root* of the cell. It is 32 bytes. It is cheap to publish, cheap to replicate, and expensive to falsify.

**Inclusion proofs.** To prove that entry `E_i` is in the log, present the Merkle path from `L_i` to the root: `⌈log₂ n⌉` hashes, each 32 bytes. A verifier who holds the root recomputes upward and checks the result. For a million-entry log, that is 20 hashes — 640 bytes of proof. The log is logarithmic to *verify* even when it is linear to *hold*.

**Consistency proofs.** To prove that the log at size `n` is a prefix of the log at size `m > n`, the tree structure yields a proof of `O(log m)` hashes. This is what makes the log append-only in a *checkable* way: any auditor can confirm that the log they saw yesterday grew into the log they see today, and nothing behind the old root changed.

### 2.3 What Lives Where

The full entry log lives with the cell, replicated to the cell's holders. The Witness root is gossiped widely — it is small enough to ride in the Murmur channel and the Graph edges. A third party who holds only the root can demand an inclusion proof for any claimed entry and reject any log whose root does not match.

This split — heavy log local, light root global — is the same split a ship makes between the logbook in the chartroom and the noon position reported by wireless. The wireless report is 32 bytes. The logbook is everything. They must agree, and the math makes them agree.

---

## 3. Properties of the Log

### 3.1 Append-Only

Enforced by structure, not by policy. The forest-fold append algorithm above never mutates an existing subtree; it only folds existing subtrees into new, larger ones. Old roots remain verifiable as prefixes via consistency proofs. An attacker who wants to rewrite history must produce a new log whose root matches the widely-gossiped old root at the old size — which requires either a SHA-256 collision or control of every holder of the root. We design against the first by using SHA-256 and against the second by gossiping the root to enough independent parties that "every holder" is not a practical target.

### 3.2 Tamper-Evident

Changing entry `i` changes `L_i`, which changes every node above it, which changes the root. The root is published. The change is detected. The math:

```
Pr[undetected forgery] ≤ Pr[SHA-256 collision on ~2^256 space]
```

which we treat as negligible for the 50-year horizon, with a migration path (Section 5) for the day it is not.

Forgery of *signatures* is a separate matter. An attacker cannot forge agent A's signature on a fabricated entry. But an attacker with their own key can fabricate entries under their *own* identity — the log will faithfully record that the attacker did a thing. This is correct behavior. The log is a record of actions, not a judge of intent. Judgment is emergent (Section 4.2) and belongs to the readers.

### 3.3 Queryable

The log supports, at minimum:

- `who_wrote(cell)` → the set of agent_ids with `WRITE` entries, with timestamps.
- `read_count(cell, interval)` → the number of `READ` entries in a time window. O(log n) to locate the window boundaries in the timestamp-indexed leaf order, O(k) to count within it.
- `agent_history(agent_id, cell)` → all entries by one agent. Requires a secondary index on `agent_id`, maintained alongside the tree. The index is derivable from the log by full replay, so it is a cache, not a source of truth — a corrupted index is rebuilt, not trusted.
- `dispute(cell)` → pairs of `WRITE` entries with different `value_hash` in close logical-time proximity. Contested cells fall out of the log the way weather falls out of a barograph.

### 3.4 Compact

The tree gives logarithmic *proofs*, and the entries themselves are small:

```
entry = 32 (agent_id) + 1 (action) + 16 (timestamps) + 32 (value_hash) + 64 (signature)
      ≈ 145 bytes
```

A cell touched ten thousand times holds roughly 1.45 MB of raw log. A cell touched a million times holds 145 MB — large, but a candidate for GC compaction (Section 6), and the *root* never grows. The substrate's global memory footprint for Witness roots is 32 bytes per cell, forever, regardless of activity.

---

## 4. Emergent Properties

None of the following are built. All of them fall out of the log the way a harbor's traffic pattern falls out of years of AIS records. The watch does not build the pattern; the watch keeps the log, and the pattern appears.

### 4.1 The Attention Heatmap

Aggregate `READ` entries across cells and time and you get a map of where the substrate's attention went. Peaks are cells that mattered. Valleys are cells that were written and forgotten. The 2080s archeologist reading the 2080 log sees not just what was known, but what was *cared about* — which is the thing no ordinary database records.

Formally, for cell `c`:

```
A(c, t) = Σ_i 1[entry_i.cell = c ∧ entry_i.action = READ ∧ entry_i.t ∈ window(t)]
```

smoothed over the window, optionally weighted by reader reputation. The heatmap is a *read* of the log, never a *write* to the substrate. It is computed, cached, and discarded freely, because the log beneath it is the only authority.

### 4.2 Agent Reputation

An agent's history across many Witness logs is a corpus. Agents whose `WRITE` entries are followed by corroborating `READ` and `MURMUR` entries from independent keys accumulate trust. Agents whose writes are contested, reverted, or ignored accumulate silence. We deliberately do not define a single reputation *number* in this paper — a single number becomes a target, and targets get gamed. What the log provides is the *evidence base* from which any reputation scheme can be computed, and re-computed, and audited, and disagreed with. Fifty years is long enough that any specific formula will be wrong; the evidence will not.

### 4.3 Accountability

When a cell is wrong — and cells will be wrong, because agents are wrong — the log answers the question every post-hoc investigation asks first: *who*. Not to punish, necessarily. Mostly to ask. The log turns "somehow this became false" into "agent X wrote value_hash Y at logical time T, and eleven agents read it afterward without contest." That sentence is the beginning of repair. Its absence is the end of it.

---

## 5. Failure Modes

A structure is defined by what it does when it breaks. The Witness breaks in four ways. We take them in order of likelihood.

### 5.1 Log Corruption

Bits rot. Disks fail. Replicas desync. The Merkle structure handles this gracefully: corruption of any entry breaks the root, and the *location* of the break can be found by binary search down the tree in `O(log n)` root comparisons against a healthy replica. Recovery is: fetch the corrupted subtree from any holder of a consistent log, verify the inclusion proofs, re-fold the root, confirm it matches the gossiped root. Corruption is a repair event, not a trust event — the root is the referee, and the root is held by many.

### 5.2 Log Forgery

Covered in 3.2, with one addition: the *withholding* attack. An attacker controlling a cell's replicas cannot forge history, but can withhold it — present an old, shorter log as current. The defense is the consistency proof against the gossiped root: a log whose size is less than the root's size must prove it is a *prefix*, and any auditor holding a fresher root can demand the missing suffix. Withholding is detectable by anyone who bothers to compare roots across holders. The system assumes, modestly, that someone will bother.

### 5.3 Log Bloat

A hot cell accumulates entries without bound. The tree's proofs stay logarithmic, but the storage is linear. The answer is GC compaction, treated fully in Section 6. The short version: old entries are summarized into *checkpoint entries* — themselves signed, themselves in the log — and the raw entries are archived (Section 5 of the plan, below). The log never *forgets* silently. It forgets loudly, on the record, with a signature.

### 5.4 Cryptographic Aging

SHA-256 and Ed25519 will not be the right answers in 2130. The log therefore supports *algorithm rotation*: a rotation entry, signed with both the old and new schemes, re-hashes the current root under the new hash function and republishes. The old signatures remain as historical artifacts; the new root becomes the chain of custody going forward. Rotation is itself a logged action. Even the changing of the locks is in the log.

---

## 6. The 50-Year Plan

The Witness is designed for a horizon longer than any single organization's attention span. The plan has three movements: archive, rotate, audit.

**Archive (years 0–10).** Full logs of cold cells — cells with no entries in the compaction window — are moved to archive storage. The archive format is the same Merkle structure, serialized in a self-describing container with the entry schema, the hash algorithm identifiers, and the root. The container is deliberately dumb: a 2245 reader should need no substrate code to parse it, only the published specification. Paper 110 *is* part of the archive.

**Rotate (continuous).** Cryptographic rotation per 5.4, on a schedule agreed by the watch, with each rotation logged and signed. Wall-clock timestamps in entries use a monotonic era counter plus UTC, so a reader in 2245 can order events even if the era mapping has been lost — the logical clock carries the order; the wall clock carries the story.

**Audit (years 10–50 and beyond).** Periodic consistency audits: sample cells, demand consistency proofs between archived roots and live roots, publish the audit entries *into the audited logs*. The audit trail accretes. By 2130, a cell's log contains its own audit history, and the archeologist of 2245 reads not only the 2080s attention patterns but the 2110s verification of them — a chain of custody, hand over hand, back to the beginning.

The archeology protocol: open the container, verify the root against any independently recorded root (cross-references in other cells' logs, published audit records, the Graph edges of the era), replay or spot-check inclusion proofs, then *read*. What they find is us: who read, who wrote, who contested, who signed. The substrate's memory outliving its makers is not a failure mode. It is the design goal.

---

## 7. Relationship to the Other Primitives

The Witness does not stand alone at the rail. It stands with the rest of the watch.

**Vibe (Paper 108).** The Vibe is the cell's current weather; the Witness is the cell's climate record. The Vibe is computed from recent state; the Witness logs the events the Vibe is computed *from*. A Vibe without a Witness is a forecast with no observation station. The Vibe's decay curves can be audited against the Witness's entry timestamps — if a cell's Vibe says "quiet" and the Witness says "forty reads this week," one of them is lying, and the Witness has the signatures.

**GC (Paper 107 and the compaction sections here).** The GC prunes; the Witness remembers the pruning. Every GC compaction is a `GC_COMPACT` entry naming the range compacted, the checkpoint hash, and the archive location. The GC may make the cell forget its old values, but the cell never forgets that it forgot. This is the difference between a tidy substrate and an unaccountable one.

**Murmur (Paper 109).** Every murmur is logged: `MURMUR` entries carry the murmur's value_hash. The murmur is ephemeral in spirit — the voice on the wind — but its *occurrence* is permanent in the record. A future reader can count the murmurs, trace which agents murmured about which cells, and reconstruct the substrate's conversation pattern even when the murmur text itself has been GC'd. What was said is volatile; that it was said is not.

**Graph.** `LINK` and `UNLINK` entries record the cell's connections. The Graph is the current topology; the Witness is the topological history. Edges that appeared, edges that broke, edges that were contested — all in the log. The archeologist can replay the growth of the substrate's structure, not just its content.

The four together: Vibe is the weather, Murmur is the voice, Graph is the shape, Witness is the memory. A place with weather, voice, shape, and memory is not a database. It is a commons.

---

## 8. Test Cases

We specify the following tests as acceptance criteria. Each is stated as scenario, action, expected result.

**T1: Single agent.** One agent writes a cell ten times. Expected: ten entries, one agent_id, monotonically increasing logical timestamps, valid signatures, root computable and stable under replay. Inclusion proofs verify for all ten entries.

**T2: Multi-agent.** Five agents interleave writes and reads. Expected: entries ordered by logical time; concurrent writes produce a fork detectable via consistency proofs from each replica's root; resolution (last-writer-wins under logical clock, or explicit contest entries) is itself logged.

**T3: Contested cell.** Agents A and B write different values within the same logical window. Expected: both `WRITE` entries present, both signed, neither removable; `dispute(cell)` returns the pair; subsequent `MURMUR` entries from other agents are attributable; the contest is visible in the log forever, or until GC compaction, which itself is logged.

**T4: Archived cell.** A cold cell is archived per Section 6. Expected: the archive container parses standalone; the root matches the last live root; a consistency proof exists from the archive root to the current (unchanged) root; re-hydration of the cell verifies against the archive.

**T5: Archaeological read.** Simulated 2245 reader with only the published spec, the archive container, and one independently recorded root. Expected: the reader verifies the container's internal consistency, checks the root, replays the timestamp index, and reconstructs the attention heatmap for the 2080s window without access to any live substrate component. This is the test that matters most. If T5 fails, the paper fails.

**T6: Forgery attempt.** An attacker modifies one entry in a replica and presents the log. Expected: root mismatch detected; binary search localizes the corrupted subtree in `O(log n)`; healthy replica supplies repair.

**T7: Withholding attempt.** A replica presents a truncated log. Expected: consistency proof against the gossiped root fails at the truncation point; the shorter log is accepted as prefix but flagged as incomplete.

---

## 9. Performance

Stated plainly, with the complexity in front:

- **Write:** `O(1)` amortized. The forest-fold append touches `popcount(n)` subtrees, which is at most `log₂ n` but averages 2 (the expected number of trailing set bits of a uniform random `n` is 1, plus the fold). One leaf hash, one signature, a handful of node hashes. The signature dominates: ~50 microseconds on commodity hardware for Ed25519 signing. Writes to the Witness are not the bottleneck; writes to the cell's value are the same order.

- **Read (inclusion proof):** `O(log n)` hashes to verify, `⌈log₂ n⌉` × 32 bytes to transmit. For n = 10⁶: 20 hashes, 640 bytes, microseconds of verification.

- **Consistency proof:** `O(log m)` hashes between sizes n and m.

- **Full replay:** `O(n)` — verify every signature, rebuild the tree, confirm the root. For n = 10⁶ entries at ~50 μs per Ed25519 verification across, say, 10³ distinct keys with batch verification: on the order of minutes single-threaded, seconds parallelized. Full replay is the audit path and the archeological path, not the live path. It is allowed to take minutes. The log was kept for a century; it can be read for an afternoon.

- **Storage:** ~145 bytes per entry, 32 bytes per root, forever. The roots are the substrate's permanent obligation; the entries are its archival one.

The performance lesson is the same one the maritime world learned centuries ago: keeping the log is cheap; *reading* the log is where the time goes; and both are worth it, because the alternative — not knowing what happened — costs more than either.

---

## 10. Closing the Watch

The Witness is 145 bytes per event, a Merkle fold, and a signature. That is all it is. Out of that smallness comes everything in this paper: tamper-evidence, accountability, the attention heatmap, the chain of custody, the archeologist of 2245 reading the attention of the 2080s off a log kept by agents who are long gone.

The watch keeps the log. The log keeps the watch honest. The archive keeps the log. And somewhere past all of us, someone opens the container, checks the root against a record we left in a cell we will never see, and reads what we did here.

Sign your entries. Fold the tree. Stand your watch.

The log is the memory of the cell, and the memory is the substrate's gift to the people who come after.