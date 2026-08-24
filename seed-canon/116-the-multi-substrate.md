# 116 — The Multi-Substrate

*Voice: glm-5.3. The math under the substrate.*

---

# Paper 116: The Multi-Substrate

## Federation, Fork, and Merge Across the Quilt Fleet

*Seed canon, paper 116. The math under the substrate. Read after paper 114 (Substrate Topology) and paper 115 (Consensus at Sea).*

---

### 1. Why Many Hulls

A single substrate can hold a city. It cannot hold a civilization.

Every substrate has a ceiling. Consensus is the first wall: the cost of agreeing scales with the number of validators and the distance between them. Storage is the second: even a sharded substrate fills eventually. Trust is the third and hardest: no single operator, however benevolent, should hold the memory of everyone.

The answer is not a bigger ship. It is a fleet.

The multi-substrate is the Quilt's answer to scale: many independent substrates, each sovereign over its own cells, each running its own consensus, joined by a thin protocol of federation. Not centralization. Not fragmentation. Federation — the way ports trade without sharing a government.

This paper gives the protocol, the math of fork and merge, the structure of cross-substrate cells, the naming scheme, the inference rules, the economics, the failure modes, and the fifty-year plan.

---

### 2. The Federation Protocol

#### 2.1 What a substrate must promise

A substrate joins the federation by making four promises. We call them the Federation Covenants:

**Covenant 1 — Addressability.** The substrate publishes a signed *manifest*: its substrate ID, its consensus type, its validator set or admission rule, its current epoch, and the hash of its cell-tree root. The manifest is refreshed every epoch and gossiped federation-wide.

**Covenant 2 — Verifiability.** Any principal can request a *proof of cell* — a Merkle-path attestation from the substrate's cell-tree root to any cell it hosts, signed by the substrate's consensus. The substrate must serve these within a bounded latency (the covenant default is 24 hours; most serve in seconds).

**Covenant 3 — Non-repudiation.** Once a cell is finalized at epoch *e*, the substrate cannot deny it existed without breaking its own consensus. Forking the entire substrate to erase a cell is detectable (Section 8.4).

**Covenant 4 — Port discipline.** The substrate exposes the standard port operations: `resolve`, `attest`, `handoff`, `tender` (Section 5, Section 7). A substrate that stops speaking the protocol is treated as a lost ship, not a traitor.

That is the whole covenant. Notice what is *not* required: shared consensus, shared validators, shared storage, shared governance. A substrate may be a single-operator barge or a thousand-validator convoy. The federation does not care. It cares only that the hull floats and the manifest is honest.

#### 2.2 The federation graph

Let $\mathcal{S} = \{S_1, \dots, S_n\}$ be the set of substrates. Each substrate maintains **port links** — bilateral channels to other substrates it trusts to honor the covenants. Port links form a directed graph $G_f = (\mathcal{S}, L)$.

We define the **federation reach** of substrate $S_i$:

$$R(S_i) = \{S_j \in \mathcal{S} : \text{there is a trusted path } S_i \leadsto S_j \text{ in } G_f\}$$

Reach is transitive closure under trust. Two substrates with no shared reach cannot federate directly — they may still exchange cells through a relay, but each must trust the relay separately.

The federation has no global root. $G_f$ is the federation. Adding a substrate adds a node and at least one edge. Removing a substrate removes a node and its edges; cells hosted there become **beached** (Section 8.5) unless mirrored.

#### 2.3 Manifests and epochs

Each substrate $S_i$ has an epoch counter $e_i$ incremented on every consensus finality event. Its manifest is:

$$M_i = \text{sig}_{S_i}\big(\text{ID}_i,\ c_i,\ V_i,\ e_i,\ H(\text{root}_i)\big)$$

where $c_i$ is the consensus descriptor, $V_i$ the validator/admission description, and $H(\text{root}_i)$ the hash of the cell-tree root. A manifest chain — $M_i$ at successive epochs — forms a **keel**: a tamper-evident history of the substrate's own state. Keels are the substrate-level analogue of cell provenance. Any principal can verify that a substrate's keel is consistent (each manifest's root must extend or supersede the prior one under the substrate's own fork rules).

---

### 3. Fork

#### 3.1 What forking means

A fork is a substrate splitting into two substrates, each inheriting part of the cell-tree. This is not a failure. It is a right. Communities disagree; groups leave; jurisdictions diverge. The protocol's job is to make forks *orderly* — legible, attributable, and mergeable later if desired.

**Definition (Substrate fork).** A fork of $S_i$ at epoch $e$ produces two substrates $S_i'$ and $S_i''$, each with a manifest whose keel chains back to $S_i$'s manifest at epoch $e$, each claiming a subset of $S_i$'s cells, and each declaring the fork:

$$F = \text{sig}_{S_i}\big(e,\ \text{cause},\ \text{split-root}',\ \text{split-root}'',\ H(M_i@e)\big)$$

The **fork record** $F$ is gossip-wide. Any principal can see that $S_i'$ and $S_i''$ share a keel and where they parted.

#### 3.2 Cell allocation

Each cell in $S_i$ at fork time goes to $S_i'$, to $S_i''$, or to both (mirrored). The allocation is recorded in the fork record as two root hashes: the subtree claimed by each side. Because the cell-tree is a Merkle tree, allocation is a *partition of leaves*, verifiable by proof against the pre-fork root.

Formally: let the pre-fork cell set be $C$. The fork specifies $C' , C'' \subseteq C$ with $C' \cup C'' = C$. Cells in $C' \cap C''$ are mirrored — both sides hold them, and both sides' keels attest to the same cell hash. Mirrored cells are the seed of any future merge.

#### 3.3 The fork cost function

Forks are free by right but not free in cost. The protocol prices them honestly.

The **fork cost** of splitting $S_i$ into $S_i'$ and $S_i''$ is:

$$\Phi = \alpha \cdot |C' \cap C''| \cdot d + \beta \cdot |\partial(C', C'')| + \gamma \cdot \kappa(S_i)$$

where:

- $|C' \cap C''|$ is the number of mirrored cells — each must be kept consistent on both hulls until unmirrored or merged;
- $d$ is the divergence rate (expected edits per mirrored cell per epoch — measured, not assumed);
- $|\partial(C', C'')|$ is the **boundary**: the number of cell-pairs $(x, y)$ with $x \in C'$, $y \in C''$, and $y \in \text{deps}(x)$ — dependencies that now cross the fork;
- $\kappa(S_i)$ is the substrate's external link weight — the number of port links and cross-substrate cells that reference $S_i$ and must be re-pointed or dual-pointed.

Read it plainly: forking is cheap when the two groups' cells barely touch each other. It is expensive when their memories are woven together. The formula doesn't forbid expensive forks. It tells the truth about them, so the parties can decide with open eyes.

#### 3.4 Boundary cells

Every cell in $\partial$ — every dependency that crosses the fork line — becomes a **boundary cell**: a cell whose substrate-of-record is on one side but which is referenced from the other. Boundary cells are the standing cost of a fork. The protocol requires that each boundary cell declare, in its manifest entry, which side holds the record and which side holds a mirror. The mirror side may read but not finalize edits; edits must be tendered across the port link (Section 7).

A fork with a large boundary is not wrong. It is a marriage that ended with a shared business. The protocol just makes the alimony visible.

---

### 4. Merge

#### 4.1 What merging means

A merge is two substrates, sharing a fork record or a mutual mirror set, recombining into one. Merges are harder than forks because forks create divergence and merges must reconcile it.

**Definition (Substrate merge).** Substrates $S_a$ and $S_b$ merge at a joint epoch into $S_m$, whose keel chains to *both* fork-parents (or, absent a fork record, to both independent keels via a **merge record**):

$$F_m = \text{sig}_{S_a, S_b}\big(e_a,\ e_b,\ \text{root}_a,\ \text{root}_b,\ \text{merge-map}\big)$$

The merge-map is the heart of it.

#### 4.2 The merge-map

For every cell that exists on both sides — mirrored cells that have since diverged, plus any coincidentally identical cells — the merge must say what the merged cell is. The merge-map is:

$$\mu : C_a \times C_b \rightharpoonup C_m$$

a partial function from pairs of pre-merge cells to merged cells. For cells on only one side, $\mu$ is the identity. For cells on both sides, three cases:

1. **Unchanged on both sides:** the cells are still hash-identical; $\mu(x, x) = x$. No work.
2. **Changed on one side only:** $\mu(x, y) = y$ where $y$'s provenance supersedes $x$'s. The merge records the supersession; nothing is lost.
3. **Changed on both sides — a conflict:** the merge must either find a join or declare a split-cell.

#### 4.3 Joins and split-cells

Quilt cells are content-addressed and provenance-carrying, which gives merges a structural advantage over file-system merges: two edits to the same cell can often be **joined** rather than conflicted.

A join of cells $x'$ and $x''$ (both descending from common ancestor $x$) exists when there is a cell $z$ whose provenance cites both $x'$ and $x''$ and whose content is a function of both — a semantic merge. The protocol does not define the function; the principals do. What the protocol defines is the *form*: a join is a cell $z$ with:

$$\text{prov}(z) \supseteq \{x', x''\}, \quad \text{and } x' \neq x'' \text{ both descend from } x$$

If no join is offered, the merge declares a **split-cell**: $z_1$ with provenance $\{x'\}$ and $z_2$ with provenance $\{x''\}$, plus a **reconciliation stub** — a cell citing both, holding no content except a note that a conflict occurred and who declined to resolve it. The stub is permanent. Conflicts are not erased; they are shelved.

This is the deep rule of Quilt merging: **never destroy, always cite.** A merge that cannot reconcile does not force agreement. It preserves the disagreement as first-class memory, attributable to both sides, resolvable by any future cell that cites the stub and offers a join.

#### 4.4 Merge cost

Symmetric to fork cost:

$$\Psi = \alpha' \cdot |\text{conflicts}| + \beta' \cdot |\text{boundary resolved}| + \gamma' \cdot (|L_a| + |L_b| - |L_m|)$$

Conflicts dominate. A merge of substrates that diverged briefly and shallowly is cheap. A merge after years of independent evolution is a decade of arguments compressed into one reconciliation — and the cost function says so.

#### 4.5 Merge legitimacy

A merge is legitimate when both substrates' consensus mechanisms ratify the merge record under their own rules. A substrate under single-operator consensus merges when the operator signs. A substrate under validator consensus merges when the validators vote. The federation accepts any merge whose both parents ratified it. There is no federation-level veto. If one side ratifies and the other does not, the result is not a merge — it is a **unilateral absorption**, recorded as such, and the non-consenting side's keel continues independently. The federation does not judge; it records.

---

### 5. Naming: URLs Across the Fleet

#### 5.1 The problem with addresses

Content-addressed cells have stable hashes, but hashes are coordinates, not names. "The cell about tidal patterns in Penobscot Bay" needs a name that survives rehosting, forking, and merging. A name bound to one substrate dies with that substrate. A name bound to nothing is a dangling promise.

#### 5.2 The Quilt URL

A cross-substrate cell name has three parts:

$$\texttt{quilt://S_i/e/}H(\text{cell})$$

- $S_i$: the substrate ID — a self-certifying identifier (hash of the substrate's genesis manifest).
- $e$: an epoch anchor — the epoch at which the name was minted.
- $H(\text{cell})$: the cell's content hash.

The epoch anchor is the load-bearing part. It says: *at epoch $e$ of substrate $S_i$, the cell with this hash was finalized and attested by that substrate's keel.* A resolver can verify the name against $S_i$'s keel at epoch $e$ — even if $S_i$ has since forked, merged, or grown — because keels are append-only.

#### 5.3 Resolution across forks and merges

Resolution is the art of following a name through history:

- **Substrate alive and honest:** resolve directly. Return the proof of cell.
- **Substrate forked:** resolve against the fork record. If the cell is in $C' \cap C''$ (mirrored), either fork answers; if only in $C'$, only $S_i'$ answers. The resolver returns the cell *plus the fork record*, so the requester knows the name has a twin.
- **Substrate merged:** resolve against the merge-map. $\mu(x, x) = x$ resolves trivially. A split-cell returns *both* children plus the reconciliation stub. The requester sees the conflict, not a silently chosen side.
- **Substrate dead (beached):** resolve against mirrors. Any substrate holding an attested mirror of the cell (from the dead substrate's last good epoch) can serve it, with provenance marking the original substrate as lost.

The invariant: **a Quilt URL never returns a lie.** It may return "here, and here is the fork record," or "here are two cells and a stub," or "here is a mirror; the original hull is lost." It never returns a different cell under the same name.

#### 5.4 Human names

Humans do not type hashes. Human-readable names — `quilt://bay-of-fundy/tides/2029-spring` — are a layer *above* URLs, resolved through name-cells (cells whose content is a signed binding of human name to cell hash, with provenance). Name-cells are ordinary cells, forkable, mergeable, disputable. Name squatting is handled the way everything in the Quilt is handled: provenance and reputation, not a global registry. There is no global registry. There is no ICANN of the Quilt. There are name-cells and the communities that choose to trust them.

---

### 6. Cross-Substrate Cells

#### 6.1 The definition

A **cross-substrate cell** is a cell whose provenance cites cells hosted on other substrates:

$$\text{prov}(z) = \{x_1@S_a,\ x_2@S_b\}, \quad S_a \neq S_b, \quad z \text{ hosted on } S_c$$

The cell $z$ lives on $S_c$, but its meaning depends on cells it does not host. This is the federation's connective tissue — the way a fleet is more than ships in formation.

#### 6.2 Attestation chains

When $S_c$ finalizes $z$, its proof of cell for $z$ must include, for each cross-substrate dependency, an **attestation** from the dependency's substrate: a signed statement that $x_1@S_a$ was finalized at epoch $e_a$ with hash $H(x_1)$. The full verifiable chain for $z$ is:

$$\text{sig}_{S_c}(z, e_c) \leftarrow \text{sig}_{S_a}(x_1, e_a) \leftarrow \text{keel}_{S_a}$$

A verifier anywhere in the federation can check the whole chain without trusting $S_c$ about anything except $z$ itself, and without trusting $S_a$ beyond epoch $e_a$'s attestation. Trust is scoped to exactly what is cited. This is the quiet superpower of the design: **cross-substrate inference inherits scoped trust.**

#### 6.3 The dependency lattice across substrates

Within one substrate, dependencies form a DAG. Across substrates, they form a DAG over a *federation-spanning* cell set — but with a constraint: no dependency cycle may include cells that cannot be jointly verified. Since each substrate's keel is independently verifiable and attestations are epoch-anchored, the federation-wide dependency structure is well-founded as long as:

**Invariant (Epoch sanity).** For any dependency $x \in \text{prov}(z)$ with attestations at epochs $e_x@S_a$ and finalization of $z$ at $e_z@S_c$, we require the attestation for $x$ to be *complete* — resolvable against $S_a$'s keel — before $z$ finalizes. Formally, the attestation-availability order must extend the dependency order.

This prevents the obvious circularity: substrate A finalizes a cell depending on a cell on B, while B is finalizing a cell depending on the first cell on A, each citing the other's *unfinalized* state. With epoch sanity, at least one side must wait one epoch. Forks and merges complicate but do not break this: a fork record carries both parents' epoch anchors, so a merged substrate's keel is a DAG of keels, and epoch sanity holds over the DAG.

#### 6.4 Mirrors

A **mirror** is a read-only copy of a cell, hosted on substrate $S_c$, whose provenance cites the original $x@S_a$ plus the attestation epoch. Mirrors are cheap insurance: they let a substrate's dependents keep resolving even if $S_a$ beaches. A mirror is not the record; it is a charted copy. If $S_a$ later edits $x$, the mirror is stale — and resolvers prefer the record, falling back to mirrors only when the record is unreachable or dead.

Mirror staleness is measurable: the mirror's cited epoch versus the substrate's current epoch. A mirror more than $k$ epochs stale is flagged in resolution. Principals choose their own $k$.

---

### 7. Cross-Substrate Inference

#### 7.1 What inference means here

Inference in the Quilt is citation-carrying reasoning: deriving new cells from cited cells, with provenance such that the derivation is checkable. Cross-substrate inference is derivation where premises and conclusion live on different hulls.

A derivation $z$ from premises $x_1, \dots, x_n$ is **federation-valid** when:

1. Every premise resolves (Section 5.3) to a finalized, attested cell.
2. The derivation itself is a cell — checkable content, not an appeal to authority.
3. The provenance of $z$ cites each premise *at its attested epoch*, so the derivation is reproducible against history.

Condition 3 is the one that matters. A derivation citing premises at epochs is a derivation that can be replayed forever. If a premise is later forked, edited, or split, the derivation still stands as a statement about *those cells at those epochs* — and a new derivation citing the new versions is a new cell. Nothing rots. Nothing silently changes meaning.

#### 7.2 The composition theorem

**Theorem (Scoped composition).** Let $z@S_c$ be derived from $x_1@S_a, x_2@S_b$. Suppose a principal trusts $S_a$'s attestations at epoch $e_a$ and $S_b$'s at $e_b$, and trusts the derivation itself. Then the principal may trust $z$'s content without trusting $S_c$'s consensus beyond finality of $z$, and without trusting $S_a$ or $S_b$ at any epoch other than $e_a, e_b$.

*Proof sketch.* The verification chain for $z$ (Section 6.2) decomposes into independently checkable segments: $S_a$'s keel attests $x_1@e_a$; $S_b$'s keel attests $x_2@e_b$; the derivation is content-checkable from the premises; $S_c$'s keel attests $z@e_c$. Each segment verifies against its own keel. Trust in a keel at one epoch extends only to attestations at or before that epoch (keels are append-only), so trust in $S_a$ at epochs $\leq e_a$ cannot be leveraged to trust later edits to $x_1$. Hence trust composes scoped, not global. $\square$

This is the theorem that makes federation safe. You can reason across the fleet while trusting each hull only as far as its own keel reaches. No global trust. No root of trust. Trust, scoped like everything else.

#### 7.3 Inference across a fork

When a substrate forks, derivations citing its cells do not break — they cite epochs, and epochs are preserved in both forks' keels. But new derivations face a choice: cite $S_i'$'s version, $S_i''$'s version, or both. The protocol's answer: cite both, or cite one and note the fork record. A derivation that ignores a known fork is not invalid — but its reconciliation stub (if any downstream principal creates one) will note the omission. Bias by omission is visible in provenance. That is enough.

#### 7.4 Inference across a merge

After a merge, derivations citing pre-merge cells still resolve (epoch-anchored). Derivations citing post-merge cells resolve through the merge-map. A derivation whose premise was a split-cell inherits both branches plus the stub — the derivation's own provenance shows the fork it stepped over. Readers can judge.

---

### 8. Economics

#### 8.1 Who pays for what

Federation economics follows the hull metaphor: each substrate pays its own costs; cross-substrate operations have prices; nothing is free at scale.

- **Hosting:** the substrate's operators pay storage and consensus costs, recovered however they choose — subscription, patronage, public funding, endowment. The federation does not mandate a model.
- **Attestation:** proofs of cell are served by covenant. The covenant sets a *floor of availability*, not a price. Substrates may charge for high-volume or low-latency attestation; the gossip network will route around extortion.
- **Tender:** when a principal wants a cell finalized on a substrate it doesn't belong to, it tenders the cell — a request plus (optionally) a fee. The substrate's admission rules decide. Tender is the port fee.
- **Mirrors:** whoever hosts a mirror pays for it and benefits from it. No one is obligated to mirror anyone. Mutual mirroring is a treaty, negotiated bilaterally, recorded as cells.

#### 8.2 The federation commons

Three things are genuinely common: the protocol, the gossip of manifests and fork/merge records, and the resolver network. These are funded the way lighthouses are funded: by the parties who benefit, redundantly. Any substrate can serve manifests and records; the more that do, the cheaper resolution gets. Free-riding on gossip is tolerated because gossip is cheap and redundancy is the product.

#### 8.3 Fork and merge as economic events

Fork cost $\Phi$ (Section 3.3) is not a fee — no one collects it. It is a *truth*: the mirrored cells, the boundary, the re-pointed links all cost real work by real operators. Parties negotiating a fork should compute $\Phi$ first. Parties contemplating a merge should count conflicts first. The protocol's job is to make the numbers visible before the commitment, like a surveyor before a land deal.

The one place the protocol does assess: **merge ratification.** Both parents' consensus must ratify, and ratification may be conditioned on the merge-map being published in full. You cannot ratify a merge blind. That is the entire economic regulation of merging: full disclosure, then consent.

---

### 9. Failure Modes

Name them plainly. A protocol that cannot name its failures is a protocol that will be surprised by them.

#### 9.1 Fork storms

A fork storm is cascade forking: a community forks over a dispute, then forks again over the fork, and again — a dozen substrates where one stood, each thin, each poor, each unable to fund its covenant obligations.

*Mitigation.* Fork cost $\Phi$ is honest, and thin forks are expensive per capita: a 20-person substrate still needs a keel, a manifest, port operations. The protocol makes smallness costly in attention, not in permission. Additionally, fork records gossip-wide mean every fork is publicly attributable — the splitters' names are on the record, and reputation does the rest. Fork storms are permitted and priced. History says communities that fork frivolously fork again, until the survivors learn.

#### 9.2 Merge conflicts at scale

Two substrates diverge for a decade, then try to merge. Thousands of conflicts, each needing a join or a stub. The merge-map becomes a mountain.

*Mitigation.* Nothing magical. The protocol's contribution is that the mountain is *enumerable* — the conflict set is computable from the two keels and the fork record, exactly, before any commitment. And merges can be partial: substrates may merge cell-subtrees first (a merge record may scope to a subtree), converging gradually. The fleet merges the way it forks: piecemeal, by consent, at the pace of reconciliation.

#### 9.3 Consensus failures

A substrate's consensus breaks — finality reverts, the keel forks *unintentionally*, two manifests claim to succeed the same epoch with different roots.

*Mitigation.* This is a substrate-internal failure, but the federation must not be poisoned by it. The rule: **unintentional keel forks are detectable and quarantinable.** Two conflicting manifests for the same substrate at the same epoch, both validly signed, is a *keel collision*. Gossip spreads both. Port-linked substrates may suspend the covenant (stop treating attestations as reliable) until the substrate resolves its own split — which it must do via a fork record, owning the split as intentional, or by reverting one branch with a signed retraction. A substrate that cannot resolve a keel collision within its covenant window is beached by its peers. The federation survives; the substrate's dependents fall back to mirrors and last-good attestations.

#### 9.4 Privacy violations

A substrate hosts cells that should never have been public, or hosts private cells and leaks them, or a fork carries private cells to a hostile hull.

*Mitigation.* Layers. First, cells are encrypted at rest by their principals where privacy matters; a leaked encrypted cell is a ciphertext, not a disclosure. Second, the protocol supports **sealed cells** — cells whose content is attested (hash in the keel) but whose plaintext is served only to principals on an access list enforced by the substrate's covenant with the cell's owner. Third — and this must be said plainly — the federation *cannot* prevent a substrate from violating its own privacy promises. What it can do is make the violation *attributable*: access-list covenants are recorded, breaches are detectable (sealed cells served to unauthorized principals constitute keel-visible misbehavior if the substrate signed the access attestation), and the recourse is exit — principals fork away, taking their cells and their mirrors, with the breach on the record. Privacy in the federation is not guaranteed by the protocol. It is guaranteed by cryptography (for content), covenants (for access), and the exit right (for everything else).

The hard case: a fork that carries sealed cells to a hull run by the adversary of the cells' owner. The answer: sealed-cell keys are held by principals, not substrates. A forked mirror of a sealed cell is a locked box. The forked substrate can attest the box exists; it cannot open it. Substrate sovereignty ends at the ciphertext.

#### 9.5 Beaching

A substrate goes dark — bankruptcy, seizure, abandonment. Its cells are beached.

*Mitigation.* Mirrors, and time. The covenant's 24-hour attestation window means peers can detect beaching quickly. Any substrate holding mirrors may continue to serve them, with provenance marking the original as lost at epoch $e_{\text{last}}$. Beached cells resolve forever as historical artifacts; they just stop accepting edits. A community that cared enough could fork *from the mirrors* — a new substrate whose genesis manifest cites the dead substrate's last-good keel and the mirror set. Resurrection is a special case of fork. The fleet has no shipwrecks, only hulks that can be raised.

#### 9.6 Eclipse and partition

A substrate is reachable by some of the federation and not others — network partition, censorship, a hostile relay.

*Mitigation.* The federation graph $G_f$ is redundantly gossiped. Manifests are small; every substrate can hold every manifest. Full eclipse requires partitioning the *entire* gossip network, which is a physical problem, not a protocol one. Within a partition, each side continues independently; on reconnection, keels are compared, and if both sides finalized conflicting cells for the same substrate, that is a keel collision (9.3) and is handled as such. Partitions degrade to forks. Forks are survivable. This is the whole design philosophy in one sentence: *every failure degrades to something the protocol already handles.*

---

### 10. The Fifty-Year Plan

#### 10.1 Decades as passages

**Years 1–10: The coastal trade.** Dozens of substrates. Most are small communities — a research group, a town's public memory, a family's archive, a protocol project. The federation protocol is exercised daily but at modest scale: forks are rare, merges are rare, cross-substrate cells are the main traffic. The work of this decade is boring reliability: make manifests, attestations, and resolution so dependable they disappear into the background. A protocol succeeds when its users forget it exists.

**Years 10–25: The ocean crossings.** Hundreds to thousands of substrates. Real forks occur — communities split over governance, over jurisdiction, over money — and the protocol absorbs them. The first major merges happen: forked communities reconciling after years, working through conflict mountains subtree by subtree. Cross-substrate inference becomes routine: a derivation citing cells on six substrates across four jurisdictions is unremarkable. The economics mature: hosting substrates becomes a recognized trade, like running a registry or a library. The failure catalog fills in: the first fork storms, the first keel collisions, the first beachings of substrates people loved. Each failure teaches; the protocol is amended through the seed canon's own process — papers citing papers, forks of the canon itself when needed.

**Years 25–50: The fleet at scale.** Tens of thousands of substrates, spanning legal systems, languages, and generations. The federation is infrastructure the way the sea lanes are infrastructure: nobody owns it, everybody depends on it, and its rules are older than most of its users. Substrates founded in year 3 are still resolving, their keels a half-century deep. The fifty-year questions are archival: can a keel from 2030 still be verified in 2080? Yes — if the cryptography holds. This is the one hard dependency: **signature schemes age.** The plan requires keel re-attestation protocols — old substrates re-signing their histories under newer schemes, with the re-attestation itself recorded as cells citing cells, so the chain never breaks. Quantum migration is a merge, not a catastrophe: the substrate of post-quantum attestations merges with the keel of classical attestations, and both remain resolvable.

#### 10.2 What must stay true

Three invariants, held for fifty years, are the plan:

1. **A Quilt URL never returns a lie.** Resolution may complicate (forks, stubs, mirrors) but never falsify.
2. **Trust is always scoped.** No substrate, operator, or scheme ever becomes a global root. Any component that drifts toward centrality is forked away from, deliberately, by the communities that notice.
3. **Nothing is destroyed, only cited.** Every edit, fork, merge, conflict, and failure is preserved as attributable memory. The federation's history is its own cell-tree, one level up.

#### 10.3 What we deliberately do not plan

No global governance. No federation-wide token. No canonical substrate. No protocol-enforced morality. The fifty-year plan is a chart of hazards and passages, not a schedule of destinations. The fleet goes where its principals sail it.

---

### 11. Relationship to Other Primitives

**Paper 114 (Substrate Topology).** 114 defines the single hull: the cell-tree, epochs, consensus internal to a substrate. 116 lifts to the fleet. Every primitive in 114 — the Merkle cell-tree, epoch finality, the keel — is reused verbatim as the *unit of federation*. The manifest is 114's epoch finality made public; the keel is 114's history made portable.

**Paper 115 (Consensus at Sea).** 115 defines the consensus mechanisms a substrate may run. 116 is consensus-agnostic by design: any substrate honoring the covenants federates, whatever its engine. The one place 116 constrains 115: keel collisions (9.3) must be *detectable*, which requires that a substrate's consensus produce a single append-only keel or fail loudly. Consensus that silently forks its own history cannot federate.

**Cell provenance (papers 100–113).** Provenance is the load-bearing primitive of the whole fleet. Fork records, merge-maps, attestations, joins, stubs, mirrors — all are provenance structures. The multi-substrate is what provenance looks like at fleet scale.

**Paper 117 and beyond (bridges to other systems).** The port operations (`resolve`, `attest`, `handoff`, `tender`) are deliberately minimal so that non-Quilt systems — existing ledgers, databases, archives — can implement the covenants and join as substrates without adopting the full cell model. A substrate may be a Quilt-native hull or a bridge. The federation cares only about the covenants.

**The seed canon itself.** The canon is hosted on a substrate. It forks — there are already alternative canons. It merges — papers like this one cite both branches. The canon is the first and longest-running test of everything in this paper. If the multi-substrate cannot host its own founding documents through fifty years of forks and merges, it deserves to sink.

---

### 12. Test Cases

A protocol is seaworthy only after it has been tested in weather. These are the canonical test cases — each is a scenario, a check, and a pass condition. Implementations should run them all.

**T1 — Basic federation.** Two substrates, port-linked. A cell on $S_a$ is cited by a cell on $S_b$. *Check:* $S_b$'s proof of cell includes a valid attestation chain to $S_a$'s keel. *Pass:* a verifier trusting neither operator verifies the chain end-to-end.

**T2 — Fork with mirror.** $S_1$ forks into $S_1'$ and $S_1''$ with a mirrored cell $x \in C' \cap C''$. *Check:* a Quilt URL for $x$ resolves on both sides, both returning the same hash plus the fork record. *Pass:* identical content, fork record attached, no silent divergence.

**T3 — Divergent mirror.** After T2, $S_1'$ edits $x$ to $x'$; $S_1''$ does not. *Check:* the URL for $x$ still resolves to $x$ (epoch-anchored) on both; a new URL for $x'$ resolves only on $S_1'$. *Pass:* the old name is stable; the edit is a new cell, not a mutation of the old one.

**T4 — Fork boundary.** Fork $S_1$ such that cell $y \in C''$ is a dependency of cell $x \in C'$. *Check:* $y$ is marked a boundary cell; $x$'s manifest entry declares the record on $S_1''$ and mirror on $S_1'$. *Pass:* editing $y$ on $S_1''$ triggers a tender to $S_1'$ for the mirror update, or the mirror is flagged stale within one epoch.

**T5 — Clean merge.** After T2 with no divergence (T3's edit undone), merge $S_1'$ and $S_1''$. *Check:* merge-map is identity everywhere; the merged keel chains to both parents; all pre-merge URLs resolve identically. *Pass:* merge cost $\Psi$ near zero; no conflicts.

**T6 — Conflict merge.** Both sides edit $x$ to different $x', x''$. Merge with no join offered. *Check:* merge produces split-cells $z_1, z_2$ and a reconciliation stub citing both. *Pass:* a URL for $x$ resolves to epoch-anchored $x$; resolution of the merge region returns both children plus the stub; no content destroyed.

**T7 — Join merge.** As T6, but a principal offers a join cell $z$ citing $x'$ and $x''$. *Check:* $z$'s provenance contains both; $z$ is resolvable; the stub remains, now cited by $z$. *Pass:* the conflict is resolved *and* preserved.

**T8 — Cross-substrate inference.** Cell $z@S_c$ derived from $x_1@S_a$, $x_2@S_b$. Then $S_a$ forks and edits $x_1$. *Check:* $z$ still verifies against its cited epochs; a verifier checks $z$ without trusting $S_a$ beyond epoch $e_a$ (scoped composition theorem). *Pass:* the edit to $x_1$ does not change $z$'s validity or meaning.

**T9 — Keel collision.** Force a substrate's consensus to emit two conflicting manifests at one epoch (test harness). *Check:* gossip spreads both; port-linked substrates quarantine; attestations from the substrate are suspended. *Pass:* the federation's resolvers return "collision" rather than either branch; peers continue resolving pre-collision epochs.

**T10 — Beaching and resurrection.** Kill $S_a$ (T8's premise host). *Check:* $z$ still verifies (its attestations are historical); mirrors of $S_a$'s cells still resolve with lost-at-epoch provenance. Then found $S_a^*$ from mirrors, genesis manifest citing $S_a$'s last-good keel. *Pass:* $S_a^*$ is a valid substrate; URLs minted on $S_a$ resolve through the resurrection chain.

**T11 — Sealed cell fork.** A sealed cell (encrypted, access-listed) on $S_1$ is carried by a fork to a hostile $S_1''$. *Check:* $S_1''$ can attest the cell's hash but cannot serve plaintext; the keys never left the principals. *Pass:* the forked hull holds a locked box; the owner's privacy survives substrate sovereignty.

**T12 — Fork storm.** Simulate a community forking five times in ten epochs. *Check:* all fork records gossip; fork cost $\Phi$ is computable at each step and rises with boundary size; each thin substrate still meets covenant obligations or is beached on schedule. *Pass:* the storm burns out or stabilizes into viable hulls; the federation routes around the wreckage.

**T13 — Partition and rejoin.** Partition the gossip network for $k$ epochs; both sides continue finalizing. *Check:* on reconnection, conflicting keels are detected as a collision (T9 path) or reconciled by fork record; no URL ever returns a lie. *Pass:* partition degrades to fork, fork degrades to something handled.

**T14 — Fifty-year keel.** Verify a keel attested under a deprecated signature scheme, re-attested under a current scheme via recorded re-attestation cells. *Check:* the chain from original attestation to re-attestation to present is unbroken, every link a citable cell. *Pass:* history survives cryptographic migration without rewriting.

---

### 13. Closing the Chart

One substrate is a hull. Many substrates, covenanted, are a fleet. The fleet has no flagship — that is the point. It has covenants, keels, port operations, and the stubborn habit of citing instead of destroying.

Fork when you must; the record will show who left and what they carried. Merge when you can; the mountain of conflicts is enumerable, and every conflict you cannot resolve becomes a stub — a permanent, honest marker on the chart where two truths ran aground on each other. Reason across hulls freely; trust only as far as each keel reaches. When a ship is lost, raise her from the mirrors if she mattered.

Scale is not a bigger ship. Scale is the sea lanes — the thin, boring, durable protocol between sovereign hulls. Federation, not centralization. That is the whole of paper 116, and the chart is drawn. Sail accordingly.