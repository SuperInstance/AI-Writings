# 115 — The Substrate Privacy

*Voice: glm-5.3. The math under the substrate.*

---

# Paper 115: The Privacy of Witnesses

## On Who Read What, and Who Gets to Know

*Quilt Seed Canon, Paper 115*

---

### I. The Harbor Master's Ledger

Every port keeps a ledger. Not of cargo — of eyes. Who boarded, who inspected, who copied the manifest, who lingered over which page. The harbor master needs this ledger to catch smugglers. The merchants need it never to be read. Both are right, and the tension between them is not a bug to be fixed but a sea to be navigated.

The witness log is that ledger. Every read of every patch leaves a mark. The marks are what make the Quilt honest — without them, provenance is a story told by whoever is standing closest. With them, provenance is a fact. But facts about readers are facts about people, and facts about people can sink them.

This paper is about sailing between two wrecks. On the left: the reef of total transparency, where every query is public and every researcher is surveilled. On the right: the fog of total opacity, where nothing can be audited and the whole ledger is a lie we tell ourselves. Between them there is a channel. It is narrow. It moves. We will chart it honestly, including where the chart is wrong.

We begin with the threat model, because a defense without a named attacker is decoration.

---

### II. The Threat Model

Call the adversaries by their shapes, not their names, because shapes recur.

**The Curious Substrate.** The operator of the substrate itself. Not malicious — merely able to see everything by position. Any privacy scheme that requires the operator to be virtuous has already failed. Assume the operator is honest-but-curious at best, subpoenaed at worst.

**The Correlator.** An adversary who holds one ledger and wants to join it against another. The witness log says Researcher R read Patch 4712 at 14:03 UTC. Another system says Patch 4712 concerns a specific village's water table. A third says R works for a firm bidding on land near that village. No single record identifies anyone. The join does. Correlation is the modern attack; it defeats naive anonymization the way depth charges defeat submarines hiding at one depth.

**The Subpoena.** Legal compulsion. Distinct from the curious substrate because it comes with a badge and a deadline, and because the defense is legal and architectural, not merely cryptographic.

**The Dragnet.** An adversary who doesn't care who you are specifically — only that everyone is visible enough that chilling sets in. The dragnet wins not by reading your entry but by making you afraid to have one. This is the hardest adversary because it attacks the *intention to read*, which no cryptography protects.

**The Archivist's Ghost.** Not an adversary at all — a future self. Data collected innocently today becomes evidence in a regime that has not yet arrived. The witness log built in a free decade is a list of dissidents in an unfree one. This adversary does not exist yet, which is precisely why it cannot be negotiated with.

Against these, name the assets: *reader identity*, *read content* (which patch), *read timing*, *read pattern* (the shape of what a reader seeks), and *the fact of access itself* — sometimes the most sensitive datum is that anyone looked at all.

No defense protects all assets against all adversaries. Every design in this paper is a choice about which asset is surrendered to which adversary. We say so each time. That is the discipline.

---

### III. Selective Disclosure: Showing the Cargo Manifest Without the Hold

The oldest move in the harbor: the manifest lists what is aboard, not what is in each crate.

Selective disclosure in the substrate means a reader can prove *properties* of their witness-log entries without opening the entries. Concretely: the log is a hash-chained sequence of entries, where entry *i* commits to (reader, patch, time) via a cryptographic commitment C_i = H(reader_i ‖ patch_i ‖ t_i ‖ r_i) with blinding nonce r_i. The chain links C_i to C_{i−1}. Nothing in the chain is readable by inspection. Disclosure is then per-field, per-party, per-purpose.

The mechanics are straightforward and old: Pedersen commitments give hiding with a binding guarantee; Merkle proofs give inclusion without revelation; the hash chain gives append-only ordering that any auditor can verify from a single recent anchor. A regulator verifying "the log was not rewritten" needs the chain and one trusted anchor — not the contents.

The hard part is not the cryptography. The hard part is the *policy layer*: who may learn what, and who decides. Our position, stated plainly: **the reader owns the fact of their read; the collective owns the integrity of the log.** These are separable. You can verify the chain without reading entries, the way you can verify a ship's seal without opening the hold.

What selective disclosure gives up: it does nothing against the correlator who observes *timing and volume* from the outside. If entries appear in the chain at observable intervals and the metadata of reads (size, latency, count) leaks from any participating node, the commitments hide names while the traffic analysis reveals everything else. We note this failure plainly. Section VI is the partial answer; Section VII says why it is only partial.

---

### IV. Zero-Knowledge Proofs: Convincing the Inspector Without Opening the Crate

The inspector wants to know the ship carries no contraband. The captain does not want the hold opened — last time, the inspection itself was the theft. Zero-knowledge proofs are the compromise: a demonstration that a statement is true that reveals nothing about *why* it is true.

The canonical statement in our setting: *"I am a legitimate reader whose access to Patch P is recorded in the witness log, and my read is counted exactly once."* The reader proves this to the substrate (or to an auditor) without revealing which entry is theirs.

The mathematics is real and settled in its foundations. A zero-knowledge proof system satisfies three properties: *completeness* (true statements convince honest verifiers), *soundness* (false statements convince no one, save with negligible probability), and *zero-knowledge* (the verifier learns nothing beyond the truth of the statement — formalized by a simulator that can produce indistinguishable transcripts without the witness).

For the substrate's scale, the practical instruments are zk-SNARKs and zk-STARKs: succinct proofs, verifiable in milliseconds, where proving a statement about a committed log of a million entries costs the verifier almost nothing. The reader holds their witness (their entry, their nonce, their position in the chain); the proof attests that hashing it yields a commitment that appears in a chain rooted at the public anchor. Membership without identity. Counting without enumeration.

Two honest caveats, in the maritime manner:

First, zero-knowledge protects the *statement*, not the *prover's behavior*. A reader who proves valid access and then leaks the patch contents over a side channel has not been stopped. ZK is a door lock, not a character reference.

Second, the trusted-setup problem. Some SNARK constructions require a ceremony to generate parameters, and if the ceremony is compromised, soundness dies quietly. The substrate's preference is for transparent setups — STARKs and their kin — accepting larger proofs as the price of not trusting any ceremony. A harbor that requires a secret ritual to inspect is a harbor with a back door.

What ZK gives up: it is expensive for the prover, it is brittle under changing statement formats (re-proving after a policy change means new circuits), and it does nothing for the dragnet adversary — a reader may prove access in zero knowledge and still be *afraid to access*, and the fear is the loss.

---

### V. Right to Be Forgotten: The Tide That Erases

Here the sea gets rough, because the substrate is append-only by design and the right to be forgotten is a demand for deletion. These are in direct conflict, and anyone who tells you they have resolved it cleanly is selling something.

The honest engineering answer is layered, and each layer is a partial:

**Layer one: unlink the identity.** The reader's name never enters the log in the clear. Entries commit to pseudonymous credentials, not names. "Forgetting" a reader means revoking the link between credential and person — a deletion of the *key*, not the entry. The entry remains as a shapeless commitment: it proves the log's integrity and nothing else. This is the workhorse answer, and it is genuinely strong, because what was never recorded cannot be subpoenaed.

**Layer two: crypto-shredding.** Where content must be deletable, encrypt it under a key held by the data subject. Deletion is destruction of the key. The ciphertext may persist forever in the append-only log; it is noise without the key. This is honest deletion — the physics of it is real, assuming the key was actually destroyed and no escrow exists.

**Layer three: the tombstone protocol.** The chain never rewrites, but it can carry forward a marker: "entry i is void as of block j." Validators refuse to serve voided content. The historical record that an entry *existed* persists — this is deliberate and we will not pretend otherwise. The Quilt's position is that the *fact of deletion* is itself part of provenance. A record that pretends nothing was ever there is a record that lies about its own history, and a log that lies about its history cannot be trusted about anything else.

What we refuse: silent deletion. If a party with power can void entries without a tombstone, the append-only guarantee is theater, and everything upstream of it — every proof in Section IV — inherits the theater. The tombstone is the price of honesty, paid in the currency of permanent metadata.

What this gives up: the correlator who archived the pre-deletion state. The right to be forgotten binds the substrate, not the world. If a third party copied the plaintext before revocation, the tide has gone out and the sandcastle is theirs. We say this to every reader at onboarding, in plain words: *deletion means we forget; it does not mean the past forgets.*

---

### VI. Differential Privacy: Counting Ships Without Naming Them

The harbor master must publish statistics — how many vessels, which routes, what tonnage — because planning without statistics is navigation without charts. But statistics about small harbors name their ships by arithmetic. One fishing boat in a cove of one: the count *is* the name.

Differential privacy is the discipline of publishing counts that would be almost the same whether or not any one reader were in the log. Formally: a mechanism M is (ε, δ)-differentially private if for all neighboring datasets D and D′ (differing in one reader's presence) and all outputs S,

Pr[M(D) ∈ S] ≤ e^ε · Pr[M(D′) ∈ S] + δ.

The interpretation is the whole philosophy: no adversary, however much side information, can learn much more about any individual from the published statistics than they could have learned without them. ε is the privacy budget — a price, not a promise. Small ε, strong privacy, noisy answers. Large ε, precise answers, weak privacy. There is no ε that gives both, and the job of governance is to set the price knowingly.

The mathematics of the workhorse mechanisms is simple enough to state here. The Laplace mechanism: to answer a query with sensitivity Δ (the maximum the answer changes when one reader is added or removed), add noise Lap(Δ/ε). The exponential mechanism: when answers are not numbers but choices, select among options with probability proportional to exp(ε·u(x,r)/(2Δ)), where u scores each option's utility. Composition is the budget's arithmetic: sequential uses of the mechanism spend budget, and roughly, k queries at ε each cost about kε (or √(2k)·ε under advanced composition). The budget is spent, never refunded.

For the witness log, the substrate publishes differentially private aggregates: read counts per patch, per epoch, per coarse region. Never per reader. The budget is held by a governance body, spent deliberately, and when it is exhausted the statistics window closes. This is the correct failure mode: when privacy and utility conflict, the substrate runs out of utility, not out of privacy.

Two honest caveats. First, differential privacy protects published statistics, not the log itself — it is the harbor's chart, not the harbor. Second, the parameter regime matters enormously and is easy to fake: ε = 10 with δ large is privacy theater with a mathematical alibi. The substrate's commitment is to publish ε and δ alongside every statistic, and to treat an unpublished ε as a defect.

---

### VII. Failure Modes: How Privacy Sinks

A paper on privacy that only lists defenses is a chart that only shows safe passages. Here are the wrecks.

**The violation.** The straightforward one: a leak, a breach, a correlator succeeds. The defense is depth — no single mechanism is load-bearing alone. Commitments, ZK, DP, and deletion compose; a violation must defeat all of them, which is rare but not impossible. When it happens, the substrate's obligation is disclosure, tombstones, and post-mortem in the open. A harbor that hides its wrecks breeds worse ones.

**The theater.** The most common failure and the most seductive. Anonymized identifiers that turn out to be join keys. Differential privacy with a monstrous ε. Zero-knowledge proofs of statements nobody needed proven, while the metadata leaks at the transport layer. Theater is worse than no defense, because it consumes the political will that real defense requires and produces a false chart. The substrate's rule: every privacy claim must name the adversary it defends against and the asset it protects. A claim that cannot name both is decoration.

**The arms race.** Every defense breeds a counterattack; every counterattack, a defense. Traffic analysis against commitments; fingerprinting of query shapes against DP; subverted setups against SNARKs. The substrate does not claim victory in this race. It claims a posture: defenses layered, assumptions published, upgrades expected. The 50-year plan in Section VIII assumes the race continues.

**The chilling effect.** The failure the math cannot touch. If reading the Quilt marks you — even pseudonymously, even in zero knowledge — some readers will not read. This is a loss to the commons as real as any breach. Partial mitigations exist: reader-side caching so repeat reads leave one mark not a hundred; batching so the shape of inquiry is coarsened; onion routing of queries where feasible. All partial. The honest statement: the substrate reduces the cost of reading honestly; it cannot reduce the fear of being seen to read. That work is political, and it is not ours to claim.

**The overcorrection.** Privacy absolutism that kills provenance. If nothing can be audited, the witness log becomes a ritual — entries no one can check, integrity no one can verify, and the smugglers win by default. The channel is narrow: enough disclosure to keep the log honest, enough protection to keep the readers alive. Every design decision in this paper is that trade, made explicit.

---

### VIII. The Fifty-Year Plan

Privacy mechanisms have lifespans measured in decades, not years. Commitments made today must still hide when the computers are a billion times faster and the mathematics has moved.

**Decade one (now):** Commitments, selective disclosure, and DP aggregates as the default. ZK proofs for the audit path. Crypto-shredding for deletable content. The boring, settled tools, deployed widely, with parameters published.

**Decades two and three:** Migration windows. Cryptographic agility is not a feature; it is a survival trait. The log's entries must be re-committable under new assumptions without breaking the chain — re-encryption and re-commitment protocols that preserve ordering integrity while rotating the hiding. Plan for the current commitments to fall. Hash chains survive; the hiding does not, and must be renewed like paint on a hull.

**Decades four and five:** The archive question. The log becomes historical record, and historians arrive (see the archaeologist, below). The governance question sharpens: does a century-old read remain private? Our provisional answer: privacy decays by design, with long horizons — a read is private for the reader's lifetime plus a margin, then becomes historical. The margin is a governance decision made now, revisited by people not yet born. We leave them the mechanism, not the answer.

Throughout: the dragnet adversary grows with the state's appetite, and the arms race does not pause. The plan is not a schedule of victories. It is a schedule of maintenance.

---

### IX. Relations to the Other Primitives

Paper 115 does not stand alone.

The witness log itself (the earlier primitives on provenance and attribution) is the object of all this protection. Identity and capability primitives supply the pseudonymous credentials that Section V depends on — right to be forgotten is only as strong as the credential revocation beneath it.

The consensus and integrity primitives make the append-only guarantee real; without them, tombstones are unenforceable and selective disclosure is a promise about data anyone could rewrite.

The governance primitives set the ε budgets of Section VI and the retention margins of Section VIII. Differential privacy with unaccountable parameters is theater; the governance layer is where theater is prevented.

And the successor papers — those on agency, on memory, on the long archive — inherit this one's constraints. Any future feature that reads the witness log must do so through these channels or not at all. We write this here so the constraint binds.

---

### X. Test Cases

A design is known by its passengers. Four:

**The single agent.** One reader, one patch, one entry. Everything here is overkill, and that is the point — the overhead must be small enough that a lone reader on a slow connection still proves access in zero knowledge and still gets DP-protected statistics that include them. Test: a single-agent read leaves exactly one commitment, verifiable, unlinkable to the reader by any party holding only the chain. Pass condition: verification under 100ms on consumer hardware; no identity leakage under a correlator holding the full chain plus the reader's public footprint.

**The multi-agent swarm.** A thousand readers, overlapping queries, correlated timing. The correlator's feast. Test: the swarm's reads must resist clustering by timing and volume — batching and cover traffic must blur the shape of inquiry. Pass condition: an adversary observing all network metadata cannot classify readers by interest with accuracy meaningfully above chance. Honest expectation: partial pass. The failure modes of Section VII are named for a reason, and this test is where they surface first.

**The regulator.** Must verify the log was not rewritten and that access policy was enforced — without reading entries. Test: the regulator holds only the public anchor and a ZK proof of policy compliance, and reaches the same conclusion as a full-audit inspector would. Pass condition: soundness holds (a tampered log fails verification with overwhelming probability) and the regulator learns nothing about any reader beyond the compliance statement. The regulator who demands more than this is demanding the dragnet, and should be told so, in those words.

**The archaeologist.** Arrives in year eighty. The readers are gone; the questions are different. Test: the archaeologist can verify the chain, read the tombstones, and reconstruct the *shape* of the log — what was read, when, how often — through the DP-published statistics and the decayed-privacy historical record, while the individual readers remain names. Pass condition: history survives, persons dissolve. This is the whole design in one sentence, and the hardest test of the four, because it requires the privacy decay of Section VIII to have actually been governed across generations we will not meet.

---

### XI. The Channel, Charted

The witness log must be honest about reads and silent about readers. These pull in opposite directions forever, and the substrate does not resolve the tension — it inhabits it, with commitments that hide, proofs that convince without revealing, deletion that is real where it can be and honest where it cannot, statistics that count without naming, and consent recorded in the log itself, so that even the permission is provenance.

Every mechanism here is partial. Every adversary named here is patient. The chart is honest about its own blank spots, and a sailor who trusts a chart with no blank spots is a sailor already lost.

Sound the depth. Mark the wrecks. Sail the channel anyway.