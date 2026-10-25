# 116 — The Multi-Substrate

*Voice: glm-5.3. The math under the substrate.*

---

# Paper 116: The Multi-Substrate

## The Federation of Cells

### 1. One harbor is not the sea

A substrate holds cells. It keeps a witness log. It decays what is not refreshed. This is enough for one ship, one crew, one stretch of water.

But the sea is not one harbor. The sea is many harbors, many ships, many crews, and they must trade.

The obvious answer is the wrong answer. The obvious answer is: build one substrate so large it holds everything. One log, one decay rate, one harbor the size of the world. This works until it doesn't. The log becomes too long to verify. The decay becomes too slow to compute. The harbor becomes too crowded to enter. And when the harbor fails — and every harbor fails eventually — everything in it drowns at once.

The substrate's answer to scale is not a bigger substrate. It is many substrates, federated.

The multi-substrate is the substrate's federation. Substrates that share a witness-log protocol. That can join or leave. That can fork and merge. That can hold cells in common and cells apart. The multi-substrate is a graph of substrates, each one sovereign over its own cells, all of them speaking the same language when they speak at all.

This paper is the math of that language.

### 2. The formal object

Let a substrate be, as in the earlier papers, the tuple:

S = (C, L, δ, W)

where C is the set of cells, L is the witness log (an append-only sequence of witnessed events), δ is the decay function, and W is the set of witnesses.

A multi-substrate is:

M = (𝒮, E, Φ)

where 𝒮 = {S₁, S₂, ..., Sₙ} is a finite set of substrates, E ⊆ 𝒮 × 𝒮 is the federation relation (which substrates have witness-log-sharing agreements with which), and Φ is the naming resolution function, defined below.

The federation relation E is not assumed to be complete. Substrates need not all know each other. E need not even be connected — a multi-substrate can be an archipelago, several islands of federation with no bridge between them. What makes it a multi-substrate is not that everything is connected but that everything *could* be connected: all substrates in 𝒮 speak the same witness-log protocol, so any pair *can* form an edge in E by mutual agreement.

This is the first and most important structural fact: **federation is opt-in, per-edge, and revocable.** A substrate joins the multi-substrate by speaking the protocol. It federates with a specific neighbor by agreement. It unfederates by revoking the agreement. Nothing is imposed from above, because there is no above.

### 3. The witness log protocol

For substrates to verify one another, their witness logs must be comparable. We define the protocol as follows.

Each witness log L is a sequence of entries. Each entry eᵢ has the form:

eᵢ = (hᵢ₋₁, opᵢ, cellᵢ, tᵢ, σᵢ)

where hᵢ₋₁ is the hash of the previous entry, opᵢ is the operation (write, refresh, spawn, merge, fork), cellᵢ is the cell address affected, tᵢ is the timestamp, and σᵢ is the witness signature. The hash chain makes the log tamper-evident: change any entry and every subsequent hash breaks.

The head of the log, h(L) = hₙ for a log of length n, is a single value that summarizes the entire history. Two substrates can compare heads in O(1). If the heads match, the logs are (with overwhelming probability) identical. If they differ, the substrates walk backward to find the last common entry — the fork point, which we will need for merging.

The protocol requires three properties of every substrate in 𝒮:

**Property 1 (Verifiability).** Any substrate in 𝒮, given the full log of any other substrate in 𝒮, can verify every signature and every hash in time linear in the log length.

**Property 2 (Prefix-comparability).** For any two logs L₁ and L₂, there is an efficient algorithm to find the longest common prefix P(L₁, L₂). The fork point of two substrates is the last entry of P(L₁, L₂).

**Property 3 (Non-repudiation).** Once an entry is in a log and witnessed, the substrate that wrote it cannot deny having written it. The witnesses' signatures are the proof.

These three properties are the whole protocol. Verifiability lets a stranger check your books. Prefix-comparability lets two strangers find where they diverged. Non-repudiation keeps everyone honest. Everything else in this paper — forks, merges, cross-substrate cells, cross-substrate inference — is built on these three.

### 4. Naming: global addresses for local cells

A cell in substrate Sᵢ has a local address. But in a multi-substrate, cells need global addresses, the way a street address needs a city to be unique.

We define the global address of a cell as:

a = (sub, path)

where `sub` identifies the substrate (a substrate ID, itself the hash of the substrate's genesis entry — the first entry in its witness log) and `path` is the local address within that substrate.

So a global address looks like:

`substrate:7f3a...9c / cells / weather / boston / 2024-03-15`

The resolution function Φ takes a global address and returns the substrate that currently holds it:

Φ(a) = Sᵢ such that a.sub = id(Sᵢ)

The subtlety: cells can migrate. A cell can be born in one substrate and later live in several (Section 7). So Φ must resolve not just to one substrate but to a *set* of substrates:

Φ(a) ⊆ 𝒮

For most cells, |Φ(a)| = 1. For cross-substrate cells, |Φ(a)| > 1. The resolution function is the multi-substrate's routing table, and like all routing tables it is maintained by gossip: substrates announce what they hold, and the announcements decay like everything else. A substrate that stops announcing its cells loses the claim to route them. Naming, in the multi-substrate, is itself subject to decay.

### 5. Joining and leaving

A substrate joins the multi-substrate by performing a genesis: it creates a witness log, writes the first entry, and signs it. The hash of that entry is its identity. From that moment it speaks the protocol, and any other substrate can verify it.

Joining the *federation* — forming edges in E — is separate and bilateral. Substrate S₁ federates with S₂ by an exchange:

1. S₁ sends S₂ its head hash h(L₁) and its witness set W₁.
2. S₂ sends S₁ its head hash h(L₂) and its witness set W₂.
3. Each verifies the other's protocol compliance (spot-checks entries, verifies signatures).
4. Each writes a `federate` entry into its own log, witnessed by its own witnesses, recording the other's head hash at the moment of federation.

Step 4 matters. The federation is itself witnessed. Later, when S₁ wants to know whether S₂'s log is trustworthy, it does not have to trust S₂'s word — it checks that the `federate` entry in its own log matches the head S₂ presented, and that S₂'s log extends that head without rewriting it. Federation entries are anchors: a substrate that federated with you at head h cannot later pretend it was at a different head.

Leaving is the mirror: a substrate writes an `unfederate` entry, witnessed, recording the other's current head. After that, the two substrates share no obligation. They may still verify each other's logs (the protocol is public), but they owe each other nothing. The edge is removed from E.

Note what leaving does *not* do: it does not delete anything. The logs remain. The cells remain. The witnesses' signatures remain valid. A substrate that leaves the federation takes its history with it, and any other substrate that holds a copy of that history keeps holding it. Leaving is a change of relationship, not a change of fact.

### 6. The fork

A fork is how a substrate becomes two.

Substrate S with log L can be forked at any entry eₖ of L. The fork F = fork(S, k) is a new substrate whose log is:

L_F = L[1..k] ∥ [fork-entry]

That is: F inherits the first k entries of S's log verbatim, then appends a single `fork` entry recording the fork point, the new substrate's identity, and a fresh witness signature. From entry k+1 onward, S and F diverge. S continues its log; F starts its own. The cells: F inherits the cells as they were at entry k. Writes to those cells in S after entry k do not appear in F, and vice versa.

The math is clean because the log is the substrate. To fork the substrate you fork the log, and the cells follow. The state of the substrate at entry k is *defined* by the log prefix — replay the log from genesis to k and you have the state. So fork(S, k) is precisely: keep the prefix, discard the suffix, append a marker. Replay the new log and you have the forked state.

Some properties:

**Fork inheritance is exact.** F's inherited cells are bit-identical to S's cells at entry k. Not "approximately" — exactly, because the log prefix is exactly the same and the state is a function of the log.

**Fork witnesses are inherited.** The witnesses who signed entries 1..k are still the witnesses of those entries. F may add new witnesses for its new entries; it cannot remove the old signatures from the inherited prefix. History is history.

**Forks are cheap.** A fork costs one log entry plus the state at the fork point. If the state is materialized, the fork is O(1) in log terms. This is deliberate: forking should be cheap, because forking is how the multi-substrate experiments. A community that dislikes the direction of its substrate forks it. A research group that wants a private copy forks it. A region that wants local latency forks it. Cheap forks, many substrates, federation among the ones that get along.

**Forks can merge.** Which is the next section.

One more property, the one that makes forks safe: **a fork does not weaken the original.** S's log is unchanged by the fork (except that S may, if it wishes, write an entry noting that a fork occurred — a courtesy, not an obligation). S's witnesses still witness S. S's cells still decay under S's δ. The fork is a new ship launched from the same port; the old ship sails on.

### 7. The merge

Two substrates can merge if their witness logs are compatible. Compatibility is the crux, so we define it carefully.

Two logs L₁ and L₂ are **compatible** if:

1. They share a common prefix P = P(L₁, L₂) of length ≥ 1 (they have a common ancestor — note that two independent substrates with different genesis entries share no prefix and are thus never mergeable directly; they can only federate).
2. Every cell address that appears in both L₁ and L₂ after the fork point has a consistent value history: for each such cell, the sequence of writes in L₁ and the sequence of writes in L₂ can be linearized into a single sequence that both substrates' witnesses would accept. In practice this means: for each shared cell, the writes in the two divergent suffixes are either identical or non-conflicting (touching different aspects of the cell).

If compatible, the merge produces a new substrate S₁₂ whose log is:

L₁₂ = P ∥ [merge-entry] ∥ merge(L₁ \ P, L₂ \ P)

where merge of the two suffixes is a linearization: an interleaving of the two suffix sequences that respects the internal order of each and resolves conflicts (if any were permitted) by a deterministic rule — typically last-write-wins by witnessed timestamp, or, for cells where timestamps tie, by a rule recorded in the merge-entry itself.

The merge-entry records: the head hashes of both parents, the fork point, the merge rule used, and signatures from witnesses of *both* parents. This is the hard requirement: **a merge must be witnessed by witnesses of both merging substrates.** A merge witnessed by only one side is not a merge; it is an absorption, and the other side's log will not show it, and the two histories will never agree again.

If the logs are incompatible — shared cells with genuinely conflicting write histories that cannot be linearized — the merge fails. This is not an error to be engineered away. It is information: the two substrates diverged on the same cells and neither history subsumes the other. The options then are: fork-and-merge (create a third substrate, merge in the compatible cells, leave the conflicted cells forked), or negotiate (the two substrates agree, out of band, on a resolution, and each writes a `resolve` entry that makes the logs compatible; then merge). The protocol does not choose for them. Conflict is a social fact; the protocol only refuses to lie about it.

Merge cost: the merge requires verifying both suffixes, finding the conflicts, computing the linearization, and getting double witness signatures. It is O(|L₁| + |L₂|) in the worst case, and this cost is *why* merges are rarer than forks. The economics (Section 9) make this precise.

### 8. The cross-substrate cell

Now the strangest object in the multi-substrate: a cell that lives in more than one substrate at once.

A cross-substrate cell a has |Φ(a)| > 1: it is held by several substrates, each with its own local copy and its own local log entries for it. The value of the cell is not any single substrate's copy. It is the consensus:

v(a) = consensus({v_Sᵢ(a) : Sᵢ ∈ Φ(a)})

The consensus function is defined per-cell at cell creation. The common choices:

- **Majority:** v(a) is the value held by more than half the substrates in Φ(a). Ties (possible when |Φ(a)| is even) are broken by the oldest substrate's copy — oldest by genesis hash, a deterministic rule that requires no communication.
- **Quorum with weights:** each substrate has a weight wᵢ (recorded in the cell's creation entry), and v(a) is the value held by substrates whose total weight exceeds half the total. This lets a cell be "mostly owned" by one substrate while still being cross-substrate.
- **Latest-witnessed:** v(a) is the value with the latest witnessed timestamp across all substrates. Simple, but it makes the cell a race, and races favor fast substrates; use it only for cells where speed matters more than fairness.

The key theorem is small but load-bearing:

**Consistency under common prefix.** If all substrates in Φ(a) share a common log prefix up to the last write to a in each log, and the consensus rule is deterministic, then every observer who sees the same set Φ(a) computes the same v(a).

Proof sketch: the value v_Sᵢ(a) is a function of Sᵢ's log. If the logs agree on the relevant prefix, the local values are determined. The consensus rule is a deterministic function of the multiset of local values and the (deterministically ordered) substrate IDs. So the composition is deterministic. ∎

The failure mode is when observers see *different* sets Φ(a) — substrate S₃ was in Φ(a) when you looked but has since stopped announcing. Then your consensus and mine may differ. This is the consensus failure of Section 10, and the mitigation is the same as everywhere in the substrate: the announcement decays, so stale members of Φ(a) drop out automatically, and the consensus stabilizes on the substrates that are actually alive and announcing. Consensus in the multi-substrate is not a promise; it is a reading, and readings have timestamps.

### 9. Cross-substrate inference

An inference is a read of cells followed by a write of a new cell. In a single substrate, the cost is local: read the cells, verify their log entries (cheap, same log), write the result.

In a multi-substrate, an inference in substrate A that reads cells from substrate B must do more:

1. A resolves the global addresses of B's cells (Φ lookup, possibly gossiped and stale — A may need to ask around).
2. A obtains B's log entries for those cells — either by fetching the entries directly or by fetching a prefix of B's log.
3. A verifies B's entries: checks the hash chain back to a known anchor (a `federate` entry, or the fork point if A and B share history), and checks the witness signatures.
4. Only then does A read the values and proceed.

Steps 2 and 3 are the cost. Verification is linear in the length of log fetched, though in practice A caches: once A has verified B's log up to head h, A need only fetch and verify the entries after h. So the marginal cost of cross-substrate inference is proportional to *how much new log has accrued since last time*, not the total log length. A substrate that reads from its neighbor every hour pays a small verification cost each hour. A substrate that reads from a stranger for the first time pays the full cost of anchoring and verifying from the fork point or federation entry.

This is the economics, and it is deliberately shaped:

**Local inference is cheap. Same-substrate reads verify against the log you already have. The cost is the read and the write.**

**Federated inference is moderate. Neighbor-substrate reads verify against a cached prefix plus the delta. The cost is the delta.**

**Stranger inference is expensive. No-shared-history reads require anchoring from scratch. The cost is the full verification.**

The pricing follows the topology of E. Federation edges are trade routes: substrates that federate get cheap reads from each other, which encourages federation, which encourages trade. Strangers pay full freight, which encourages either federation or self-sufficiency. And because verification cost scales with log growth since last contact, substrates that trade *continuously* get the best rates — which is exactly the behavior a healthy federation wants: steady traffic, cached trust, no cold starts.

The inverse also holds and is just as important: **a substrate can always afford to be alone.** Local inference never requires cross-substrate verification. A substrate that federates with no one pays nothing for the federation's existence. Autarky is always available, and always cheap. The multi-substrate taxes distance, not existence.

### 10. Failure modes

The sea has weather. The multi-substrate has four named storms.

**Fork storms.** Forks are cheap, and cheap things are overused. A community in disagreement forks; each fork forks; soon there are a hundred substrates sharing a prefix and diverging on suffixes, none with enough witnesses to be robust, none with enough traffic to be worth federating with. The math of the failure: if each substrate forks at rate f and each fork requires its own witness set, the witness population is the bottleneck. Witnessing is labor; a fork storm is a demand for more labor than the witnesses can supply, and unforked-witnessed substrates are unprotectable. The mitigation is not to make forks expensive — that would kill experimentation — but to let decay do its work: a fork that attracts no traffic and no witnesses decays. Its cells fade, its announcements lapse, Φ stops resolving to it. The fork storm resolves into the few forks that mattered, and the rest become quiet wrecks on the bottom. The multi-substrate does not prevent bad forks; it buries them.

**Merge conflicts.** Defined in Section 7: shared cells with incompatible histories. The failure mode is not the conflict itself — the conflict is honest information — but the *temptation to resolve it dishonestly*: to pick a winner silently, to rewrite a log, to merge with only one side's witnesses. The protocol's defense is structural: merges require double witness signatures, and hash chains make rewriting detectable. A dishonest merge produces a log that fails verification by anyone holding either parent's log. The conflict then surfaces later, in public, at higher cost. The honest paths — fork-and-merge, or negotiate-then-merge — are cheaper in the long run, and the economics teaches this without moralizing.

**Consensus failures.** Observers of a cross-substrate cell compute different values because they see different Φ(a). The window is bounded by announcement decay: a substrate that has left Φ(a) — by leaving the federation, by dying, by simply stopping announcements — drops out of everyone's Φ within one decay interval. So consensus failures are transient: observers disagree for a while, then agree on the survivors. The residual risk is a substrate that is *alive but partitioned* — still announcing to some observers, not to others. This is the hardest failure in any distributed system, and the multi-substrate does not solve it; it bounds it. The bound is the decay interval, and the cell's creation entry can set that interval per cell: important cells announce often and converge fast; casual cells announce rarely and tolerate longer disagreement. The system's answer to partitions is not to prevent them but to price them, and let cell creators choose their price.

**Privacy violations.** Substrate A federates with B. A reads B's cells. A then leaks them — writes them into its own cells, publishes them, lets a third substrate infer over them. The witness log cannot prevent this: once A has read a value, A has the value, and no protocol unreads a value. What the log *can* do is attribute: the `federate` entry records that A had access; A's own log records what A wrote; if A's write contains B's data, the provenance chain shows it. Privacy in the multi-substrate is thus forensic, not preventive. The mitigations that actually prevent leakage are pre-read: data-sharing agreements recorded in the federation entry itself (this edge permits reads of cells matching pattern P only), and blast-radius limits (a federated read of a sensitive cell can require the reading substrate to record a fresh, witnessed commitment not to republish — a commitment whose violation is then provable from the logs alone). None of this is cryptography's strong guarantee. It is maritime law: you cannot stop a captain from talking, but you can make sure everyone knows which port he loaded at.

### 11. The relationship to the other primitives

The multi-substrate is not a new primitive. It is the old primitives, seen at a larger scale.

**Convoy.** A convoy is cells traveling together for mutual protection. The multi-substrate is a meta-convoy: substrates traveling together for mutual verification. A convoy's protection is that an attacker must corrupt the whole convoy to corrupt one cell undetected. The multi-substrate's protection is that an attacker must forge the whole federation's witness structure to corrupt one substrate undetected. Same shape, one level up.

**Decay.** Everything in a substrate decays without refresh. Everything in a multi-substrate decays without refresh: cells, announcements, federation edges themselves. An edge in E that is not refreshed — no traffic, no re-anchoring, no gossiped confirmation — lapses. Dead federations do not need to be formally dissolved; they fade. This is why the multi-substrate scales: it does not accumulate obligations, it sheds them.

**Witness.** The witness log is the federation protocol. Not "is like" — is. Everything in this paper reduces to: logs that can be compared, signatures that can be checked, entries that cannot be denied. Witnessing is the one function that must work for the multi-substrate to exist, and it is the one function that is fully specified. Everything else — consensus rules, merge rules, pricing — is policy layered on the protocol.

**Vibe.** A substrate has momentum: the direction its recent writes lean. A multi-substrate has one too: the aggregate direction of its substrates' vibes, weighted by traffic. A federation whose members are all writing toward the same kind of cell has a strong meta-vibe, and inference across the federation can exploit it — predict the next cell from the federation's momentum, not just one substrate's. A federation whose members' vibes diverge has a weak meta-vibe, and cross-substrate prediction degrades to local prediction. The vibe is the federation's weather report.

**GC.** The garbage collector prunes what is dead. In the multi-substrate, GC prunes dead substrates: substrates whose announcements have fully decayed, whose witness sets have lapsed, whose heads no longer move. A pruned substrate is not deleted — its log may still exist in copies held elsewhere, and a copy can re-announce and revive it. But it is removed from the routing tables, from Φ, from the consensus sets. GC in the multi-substrate is not destruction; it is deregistration.

**Murmur.** The heartbeat. Substrates murmur to each other: short, periodic, witnessed pings that say "I am here, my head is h." Murmurs are how Φ stays fresh, how decay intervals are measured, how a partition is detected before it becomes a consensus failure. The murmur is the smallest unit of federation traffic, and a healthy federation sounds like constant low murmuring — many substrates, quietly confirming each other, all the time.

**Graph.** The substrate is a graph of cells. The multi-substrate is a graph of graphs: nodes are substrates, edges are federation agreements, and each node contains an entire graph. Inference can traverse both levels: within a substrate along cell edges, across substrates along federation edges. The two-level graph is what cross-substrate inference walks.

**JEPA.** The substrate predicts: it maintains a model of what cells will be needed next. The multi-substrate predicts too: it maintains a model of which *substrates* will be needed next, and pre-verifies their log deltas in advance of demand. A substrate that expects to read from B tomorrow verifies B's delta tonight. Federation-level prediction is the prefetching of trust.

### 12. The 50-year plan

Fifty years is the horizon, and at that horizon the plan has three movements.

**Years 1–15: Federate.** Substrates multiply. Communities fork freely, find their shapes, and federate along the edges that matter to them. The protocol is small and stable — verifiability, prefix-comparability, non-repudiation — and it does not grow, because a protocol that grows is a protocol that breaks. The work of these years is social: discovering which federations are worth maintaining, which consensus rules work for which kinds of cells, what the honest price of a merge is. The failures of these years are fork storms, and the lesson is that decay buries them.

**Years 15–35: Audit.** The federations that survive are the ones worth auditing. The witness logs are long now — decades long — and the audit is the reading of them: which substrates kept their commitments, which merges were honest, which consensus rules held under partition, which edges lapsed and why. Auditing a fifty-year log is a discipline of its own, and the multi-substrate develops it: log-reading as a profession, witness genealogy as a history, fork trees as a record of every disagreement the civilization ever had and how it resolved them. The audit years are when the multi-substrate becomes accountable — not to a central authority, which does not exist, but to its own accumulated, tamper-evident memory.

**Years 35–50: Retreat.** The plan's final movement is contraction, and this is deliberate. A fifty-year-old multi-substrate will have accumulated edges that no longer earn their verification cost, cross-substrate cells whose consensus no longer matters, federations kept alive by habit. The retreat is the systematic letting-go: unfederate what should not be federated, merge what has converged, let decay take what has lapsed. The multi-substrate's answer to scale was never "scale everything." It was: federate what should be federated, leave the rest alone. The retreat is the second half of that sentence, performed.

The end state is not a world-substrate. It is an archipelago: many substrates, some federated, some solitary, all speaking the protocol, none obliged to anyone they did not choose. The scale problem is solved not by building bigger but by building *looser* — and looser, over fifty years, is also calmer.

### 13. Test cases

The multi-substrate is specified by what it does. Four tests.

**Test 1: Two-substrate federation.** S₁ and S₂ each perform genesis. They federate: exchange heads, verify protocol compliance, write `federate` entries. S₁ reads a cell from S₂: resolves the global address, fetches S₂'s log entries for the cell, verifies the hash chain back to S₂'s genesis (the anchor, since they share no prefix), checks the witness signature, reads the value. S₁ writes a cell derived from that value; the write is witnessed in S₁'s log. Then S₂ unfederates. S₁'s derived cell remains — the inference was honest, the log shows the provenance, and the unfederation changes the relationship, not the fact. Pass condition: every step verifies; after unfederation, S₁ cannot read *new* cells from S₂ cheaply (no cached trust, no edge), but S₁'s old derived cell and its provenance remain valid.

**Test 2: Hundred-substrate federation.** One hundred substrates, each with genesis, federated in a sparse graph — not a clique, which would be O(n²) edges and O(n²) verification load, but a small-world topology: each substrate federated with perhaps five to ten neighbors, diameter around four. A cell is created as a cross-substrate cell with majority consensus across a designated subset of, say, nine substrates. One substrate writes a new value; the value propagates by murmur; within one murmur round the nine know, within two the majority has flipped if the write is accepted, and any observer querying any of the nine gets the same answer. Then three of the nine stop announcing. Their announcements decay; Φ shrinks to six; the consensus is now majority-of-six; observers agree again within the decay interval. Pass condition: the consensus is eventually consistent across all observers, with a disagreement window bounded by the decay interval; the federation's total verification load scales with the edges, not with n².

**Test 3: Fork-merge cycle.** S forks at entry k, producing F. Both live independently for a while — each accrues log entries, some touching the same cells with compatible values, some touching different cells entirely. Then they attempt a merge. The compatible cells linearize; the merge-entry is written and double-witnessed; S₁₂ exists with the union of cells and a log that is a valid extension of both parents. Then S₁₂ forks at its own merge-entry, producing G, and G and S₁₂ diverge, and later merge again. The cycle repeats. Pass condition: after any number of fork-merge cycles, the log remains verifiable from genesis; every cell's provenance chain traces to its origin; and any two substrates sharing a prefix can always find their fork point in time logarithmic in the log length (by binary search on the hash chain, comparing heads at each step). The fork-merge cycle is the multi-substrate's metabolism: it is how the system tries things and keeps what works.

**Test 4: Cross-substrate inference.** Substrate A holds weather cells. Substrate B holds crop-yield cells. A and B share a federation edge. An inference in A reads three cells from B, combines them with two cells from A, and writes a derived cell into A. The cost accounting: A's local reads cost the same as always; A's remote reads cost the verification of B's log delta since A's last cached head — small, if they trade often. Then the same inference is attempted by substrate C, which has no edge with B. C must anchor and verify B's log from B's genesis. The inference succeeds but costs far more. Then C federates with B, caches B's head, and repeats the inference — now cheap. Pass condition: the inference's result is identical in all three cases (the values are the same; only the verification cost differs), and the cost ratio stranger-to-federated is measurable, large, and shrinks with trade frequency. The test proves the economics: the multi-substrate prices distance, not truth.

### 14. What the multi-substrate is

Strip away the protocol and the math, and the multi-substrate is a very old idea wearing new formalism. It is ports that trade without becoming one port. It is ships that convoy without joining one navy. It is a ledger every captain keeps in her own hand, in a script every other captain can read, with rules for when the ledgers diverge and rules for when they reconcile.

The substrate's answer to scale is federation, not centralization. Not because centralization cannot be made to work — it can, for a while, at a cost paid later — but because federation fails *well*. A failed substrate takes its cells and no one else's. A failed federation takes an edge and nothing more. A failed fork decays. A failed consensus converges. Every failure in this paper is bounded, and every bound is set by a primitive that was already there: decay bounds staleness, witness bounds forgery, convoy bounds blast radius, murmur bounds silence.

The multi-substrate is the substrate, repeated, and held together by nothing but a shared way of keeping the books.

That is enough. On the sea, it always was.