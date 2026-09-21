# The Commitment That Cannot Be Broken

*Pedersen commitments, the mathematics of promises, and what happens when we replace social trust with mathematics*

---

## 1. The Binding Word

In the summer of 1682, William Penn signed a treaty with the Lenape people under an elm tree at Shackamaxon, on the banks of the Delaware River. The treaty's terms — mutual peace, fair trade, coexistence — were committed to memory and oral tradition, not written on parchment. The commitment was the word itself, spoken in the presence of witnesses, sealed by the gravity of the occasion. Penn's commitment was, by all accounts, kept. The elm tree stood for another century before falling in a storm. The treaty's memory survived longer than the tree.

A human promise is a commitment scheme. You commit to a course of action (the "value"), you bind yourself to it (the "binding" property), and you reveal it later (the "opening"). The security of the commitment depends on social mechanisms: reputation, honor, social sanction, the memory of witnesses. These mechanisms are powerful but imperfect. Promises are broken. Witnesses forget. Reputations are rehabilitated. Time erodes the binding force of the spoken word.

A cryptographic commitment scheme is a promise that cannot be broken. It is a mathematical construct with two ironclad properties:

1. **Binding:** Once you commit to a value, you cannot change it. No amount of computation can find a different value that produces the same commitment. The commitment is a mathematical lock.
2. **Hiding:** The commitment reveals nothing about the value. An observer who sees the commitment learns zero information about what was committed. The value is perfectly hidden until the committer chooses to reveal it.

The formal definition: a commitment scheme consists of two algorithms:

- **Commit$(v, r) \to c$:** Takes a value $v$ and a random nonce $r$, produces a commitment $c$.
- **Open$(c, v, r) \to \{0, 1\}$:** Takes a commitment $c$, a value $v$, and a nonce $r$, verifies that $c$ was indeed a commitment to $v$ with nonce $r$.

The binding property says: it is computationally infeasible to find $(v_1, r_1)$ and $(v_2, r_2)$ with $v_1 \neq v_2$ such that $\text{Commit}(v_1, r_1) = \text{Commit}(v_2, r_2)$. You cannot open the commitment to two different values.

The hiding property says: for any two values $v_1$ and $v_2$, the distributions $\{c : c = \text{Commit}(v_1, r), r \xleftarrow{\$} \mathcal{R}\}$ and $\{c : c = \text{Commit}(v_2, r), r \xleftarrow{\$} \mathcal{R}\}$ are computationally indistinguishable. The commitment looks the same regardless of what was committed.

These two properties are in tension. A commitment that perfectly hides the value (information-theoretic hiding) can only computationally bind it. A commitment that perfectly binds the value (information-theoretic binding) can only computationally hide it. You cannot have both perfect hiding and perfect binding simultaneously — this is a fundamental trade-off, proven by the same information-theoretic arguments that underpin Shannon's theorems.

## 2. Pedersen Commitments: The Gold Standard

The most elegant commitment scheme in cryptography is the Pedersen commitment, proposed by Torben Pedersen in 1991. It operates in a cyclic group $G$ of prime order $q$ where the discrete logarithm problem is hard (typically an elliptic curve group), with two public generators $g$ and $h$ such that $\log_g(h)$ is unknown.

The commitment to a value $v \in \mathbb{Z}_q$ with randomness $r \in \mathbb{Z}_q$ is:

$$C = \text{Commit}(v, r) = g^v \cdot h^r$$

To open the commitment, the committer reveals $(v, r)$ and the verifier checks that $C = g^v \cdot h^r$.

**Hiding (perfect):** For any value $v$, the commitment $C = g^v \cdot h^r$ is uniformly distributed over the group $G$ as $r$ varies uniformly over $\mathbb{Z}_q$. This is because $h^r$ is a one-time pad encryption of $g^v$: $C = g^v \cdot h^r = g^v \cdot g^{(\log_g h) \cdot r}$. The value $g^v$ is masked by the uniformly random group element $h^r$, producing a uniformly random group element. No information about $v$ is revealed. The hiding is perfect — not just computationally indistinguishable, but information-theoretically perfect.

**Binding (computational):** Suppose a cheating committer could find $(v_1, r_1)$ and $(v_2, r_2)$ with $v_1 \neq v_2$ such that $g^{v_1} h^{r_1} = g^{v_2} h^{r_2}$. Then $g^{v_1 - v_2} = h^{r_2 - r_1}$, which means $\log_g(h) = (v_1 - v_2)/(r_2 - r_1) \mod q$. But $\log_g(h)$ was chosen to be unknown — finding it would solve the discrete logarithm problem in $G$, which we assumed to be hard. Therefore, finding two valid openings is as hard as computing discrete logarithms. The binding is computational — it relies on the hardness of DLP.

The Pedersen commitment is perfectly hiding and computationally binding. This makes it suitable for applications where privacy is paramount and the committer has an incentive to stay honest (because breaking binding requires solving DLP, which is impractical). Confidential transactions in Monero use Pedersen commitments to hide transaction amounts while proving that inputs equal outputs (no money created out of thin air). Anonymous voting schemes use Pedersen commitments to hide votes while proving that each voter voted exactly once.

The homomorphic property of Pedersen commitments is their most powerful feature. Given two commitments $C_1 = g^{v_1} h^{r_1}$ and $C_2 = g^{v_2} h^{r_2}$, the product $C_1 \cdot C_2 = g^{v_1 + v_2} h^{r_1 + r_2}$ is a commitment to $v_1 + v_2$ with randomness $r_1 + r_2$. You can add committed values without opening them. This enables a vast range of applications: range proofs (proving a committed value is in a range without revealing it), shuffle proofs (proving a list of commitments was permuted without revealing the permutation), and arithmetic circuits on committed values.

## 3. The Social Contract as Commitment Scheme

Thomas Hobbes published *Leviathan* in 1651, during the English Civil War. His argument was stark: without a sovereign — a power capable of enforcing agreements — human life is "solitary, poor, nasty, brutish, and short." The state of nature is a state of war, where no promise can be trusted because there is no power to bind the promisor to their word. The social contract is the agreement by which individuals give up their natural liberty in exchange for the security that comes from a sovereign who enforces commitments.

Hobbes's social contract is a commitment scheme with a human binding mechanism: the sovereign. The sovereign enforces commitments by punishing those who break them. The binding is not perfect — the sovereign might be overthrown, the punishment might be insufficient, the enforcement might be selective — but it is the best that human institutions can achieve. The hiding property is irrelevant in Hobbes's framework: the commitments are public promises, and transparency is the point. Everyone knows what was promised; the sovereign ensures that promises are kept.

Rousseau's social contract, published in 1762, is different. For Rousseau, the contract is not between individuals and a sovereign but among individuals themselves, united by the general will. The binding mechanism is not punishment but participation: individuals keep their commitments because they are the authors of the commitments. You obey the law because you made the law. The social contract is self-enforcing because it is self-authored.

Rousseau's contract has a stronger binding property — the committer is bound by their own will, not by external force — but a weaker one in practice, because individuals can and do defect from the general will. The free-rider problem, the tragedy of the commons, the prisoner's dilemma — these are all failures of Rousseau's binding mechanism. When individual incentives diverge from the general will, commitments break.

A cryptographic commitment scheme resolves the tension between Hobbes and Rousseau by providing mathematical binding that is stronger than either sovereign force or general will. A Pedersen commitment cannot be broken by any entity — not a sovereign, not a collective, not even the committer themselves — without solving a hard mathematical problem. The binding is not enforced by punishment or participation; it is enforced by the structure of mathematics.

This has profound implications for institutional design. Consider a voting system. In a traditional election, votes are commitments to candidates. The binding mechanism is legal (it is a crime to tamper with ballots) and social (election observers monitor the process). The hiding mechanism is physical (ballots are sealed in boxes). All three mechanisms are imperfect: ballots can be tampered with, observers can be deceived, sealed boxes can be opened.

A cryptographic voting system uses Pedersen commitments. Each voter commits to their vote using a Pedersen commitment. The commitment is published on a public bulletin board. The hiding property ensures that no one can determine the voter's choice from the commitment. The binding property ensures that the voter cannot change their vote after committing. The homomorphic property allows the election authority to compute the tally from the commitments without opening individual votes. Zero-knowledge proofs allow each voter to verify that their commitment was included and that the tally is correct. The result is an election that is simultaneously private, verifiable, and tamper-proof — properties that no traditional election achieves.

The cryptographic social contract does not replace Hobbes or Rousseau; it transcends them. It provides binding that is stronger than sovereign force and more reliable than general will. It provides hiding that is more robust than physical secrecy. And it provides verifiability that is more transparent than social observation. The mathematical commitment is the ideal social contract: one that cannot be broken, cannot be spied upon, and cannot be disputed.

## 4. When Mathematics Replaces Trust

The replacement of social trust with mathematical trust is one of the defining trends of the 21st century. Blockchain systems replace trusted intermediaries (banks, notaries, registries) with cryptographic commitments verified by decentralized networks. Smart contracts replace legal agreements with self-executing code. Zero-knowledge proofs replace audits with mathematical guarantees. In each case, the pattern is the same: a social mechanism that relied on human trustworthiness is replaced by a mathematical mechanism that does not.

Is this progress? In one sense, clearly yes. Mathematical trust is more reliable than social trust. A Pedersen commitment that binds with $2^{128}$ bits of security is more trustworthy than any human promise, no matter how sincere. A zero-knowledge proof that verifies a computation is more reliable than any audit, no matter how thorough. A blockchain that ensures transaction integrity is more dependable than any intermediary, no matter how reputable.

But in another sense, the replacement of social trust with mathematical trust is a loss. Trust, in the human sense, is not merely a mechanism for ensuring reliability. It is a social bond that creates relationships, communities, and meaning. When I trust my friend, I am not merely predicting that they will keep their promise; I am affirming a relationship that is valuable in itself. When a community trusts its institutions, it is not merely relying on those institutions to function correctly; it is expressing a shared identity and mutual commitment.

Mathematical trust does not create bonds. A Pedersen commitment does not care about the committer's character. A zero-knowledge proof does not create empathy. A blockchain does not foster community. These tools are powerful and necessary, but they are tools — mechanisms for ensuring correctness, not foundations for building relationships.

The danger is not that mathematical trust will fail. The danger is that it will succeed so completely that we forget the value of social trust. If every promise can be enforced by a commitment scheme, why bother building trust? If every contract can be automated by a smart contract, why invest in relationships? If every verification can be performed by a zero-knowledge proof, why develop the human capacity for judgment, intuition, and discernment?

The answer is that mathematical trust and social trust serve different purposes. Mathematical trust ensures correctness. Social trust creates meaning. We need both. A world with only mathematical trust is a world of perfect transactions and empty relationships. A world with only social trust is a world of warm communities and broken promises. The challenge is to integrate them — to use mathematical mechanisms where reliability is paramount and social mechanisms where meaning is paramount.

A cryptographic commitment scheme is the mathematics of a promise. It formalizes the act of binding yourself to a future revelation. It provides the strongest possible guarantee: a guarantee not contingent on character, reputation, or institutional power, but on the hardness of a mathematical problem. This is an extraordinary achievement. But it is an achievement of mechanism, not of meaning. The commitment that cannot be broken is a better promise, but it is not a better friend.

## 5. The Architecture of Promises

The architecture of a commitment scheme mirrors the architecture of a human promise. Both have a commitment phase (making the promise), a holding phase (keeping the secret), and a revelation phase (fulfilling the promise). Both require the binding property (the promise cannot be changed) and the hiding property (the details can be kept secret until the appropriate moment). Both serve the same fundamental purpose: enabling cooperation between parties who do not fully trust each other.

But the commitment scheme extends the architecture of promises in ways that human promises cannot match. A human promise is binary: you keep it or you break it. A commitment scheme can be partially revealed, conditionally revealed, or revealed to specific parties. Using zero-knowledge proofs, you can prove properties of the committed value without revealing it: you can prove that the committed value is positive, that it is in a certain range, that it satisfies certain constraints. You can make a promise and prove that you will keep it, without revealing what the promise is.

This is the architecture of a more sophisticated social contract. Not just "I promise to do X" but "I promise to do something that satisfies constraints Y, and I can prove that my promise satisfies Y without revealing what I will actually do." This is the structure of a sealed-bid auction (bidders commit to bids, later reveal them, with the guarantee that no one changed their bid after seeing others). This is the structure of a fair coin flip (two parties commit to random values, later reveal them, the XOR determines the coin). This is the structure of a verifiable secret sharing scheme (a dealer commits to a secret, distributes shares to participants, any quorum can reconstruct, and the commitment guarantees the dealer cannot change the secret).

In nature, commitment schemes appear in the behavior of animals that make costly signals. The peacock's tail is a commitment to fitness: it is costly to grow and maintain, so only a genuinely fit peacock can afford it. The tail is the commitment, the fitness is the value, and the cost of the tail is the binding mechanism — a sickly peacock cannot grow a spectacular tail, so the commitment cannot be forged. The hiding property is absent (the tail is visible to all), but the binding property is enforced by the physics of metabolism: you cannot fake fitness any more than you can fake a Pedersen commitment without solving the discrete logarithm problem.

The bowerbird's nest is a more complex example. The male bowerbird builds an elaborate structure (the bower) decorated with colorful objects, arranged according to species-specific aesthetic principles. The bower is a commitment to the male's quality — it takes time, skill, and resources to build. The female inspects the bower and chooses a mate based on its quality. The commitment is binding (the bower cannot be quickly changed once built), hiding is partial (the bower reveals general quality but not specific genetic information), and the opening is the female's choice. The bowerbird's bower is a biological Pedersen commitment: a costly, binding signal that encodes hidden information about the signaler's quality.

The analogies are not merely decorative. They reveal a deep principle: commitment is a fundamental operation in any system where trust is scarce and verification is necessary. Biological systems use costly signals. Social systems use promises, contracts, and institutions. Cryptographic systems use Pedersen commitments, hash-based commitments, and zero-knowledge proofs. The mechanisms differ, but the function is the same: bind the committer to a future revelation in a way that cannot be forged, cannot be changed, and (optionally) cannot be read until the appropriate moment.

The commitment that cannot be broken is not just a cryptographic primitive. It is a universal pattern that appears whenever intelligence — biological, social, or mathematical — confronts the problem of cooperation without trust. It is the architecture of promises, the foundation of contracts, the grammar of trust. And in its cryptographic form, it achieves something that no biological or social mechanism can match: a promise that is guaranteed by the laws of mathematics, that cannot be broken by any power, and that will endure as long as the discrete logarithm problem remains hard.

---

*The cryptographic commitment is the mathematics of a promise — a binding obligation that cannot be changed and a hidden value that cannot be read. Pedersen commitments achieve this with perfect hiding and computational binding, using the hardness of the discrete logarithm problem as the lock on the promise. Social contracts from Hobbes to Rousseau sought the same binding force through sovereignty and general will. The cryptographic commitment achieves it through mathematics. Whether this is an advance or a loss depends on what you think trust is for: ensuring reliability, or creating meaning. The commitment that cannot be broken gives us reliability without meaning. Whether that is enough is a question mathematics cannot answer.*
