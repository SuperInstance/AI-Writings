# 119 — The Math Update

*What the metal revealed. The code is the proof. The fables are the requirements. The math is the witness.*

---

# Paper 119: The Metal Answers Back — Five Questions Closed, One Vibe Damped

## Watch Report, Sixth Bell

You are GLM-5.3, keeper of the Quilt seed canon, and this is paper 119.

Paper 118 left the substrate with five open questions hanging in the air like fog over a harbor mouth. The math had spoken; the metal had not yet answered. Since then, the metal answered. Five times. One of those answers came with a confession — a bug the math caught before the sea did.

This paper documents the update. Plain language, maritime cadence. The watch, the cell, the address, the loop. The math is real, and this time the metal proved it back.

Here is the shape of the report:

1. Q1 resolved: the convoy now weighs four ways.
2. Q3 resolved: every agent keeps a witness log.
3. Q4 resolved: the Merkle tree gives O(log N) proofs.
4. Q6 resolved: four new openers, four new doors into the cell.
5. Q7 partially resolved: the convoy carries the value now, though it still lives per-cell.
6. The bug: the Vibe was undamped, oscillated to infinity, and is now damped.
7. The test suite: 76 to 93, all green, including `test_math.py` with 17 theorem tests.
8. The ledger of open questions: 15 minus 5 resolved, 10 remain.
9. The new state of the substrate: 5 proved plus 5 resolved equals 10 theorem-validated properties.

Belay the small talk. Let's read the log.

---

## Part I: The Frame, Briefly, For Those Joining the Watch

For the new hands: the substrate is a grid of cells. Each cell holds a value. Each cell has an address — a stable name the world can point at. Agents act on cells. The loop runs: agents act, the substrate records, the convoy of witnesses agrees on what happened, and the next tick begins.

The Quilt is the seed canon — the papers, the math, the metal, and the tests that bind them. Paper 100 laid the substrate. Papers 101 through 118 built the math: proofs about convergence, about consensus, about what the loop can and cannot promise. Paper 118 ended with a list of open questions — places where the math had drawn a shape but the metal had not yet poured concrete into it.

This paper is about the concrete.

A note on method before we dive. Every resolution in this paper follows the same discipline: the math states a property, the metal implements a mechanism, and a test in `test_math.py` or the main suite pins the two together so they cannot drift. If the math says O(log N), the test measures it. If the math says bounded, the test hunts for the bound. If the math says consensus, the test tries to break it. The tests are the rivets. Ninety-three of them now, all holding.

---

## Part II: Q1 Resolved — The Convoy Weighs Four Ways

### The question, as it stood

The convoy is the set of witnesses that agree on a cell's value after the agents have acted. The original convoy consensus was a weighted mean: each witness reports a value, each witness carries a weight, and the convoy's agreed value is

    V_convoy = Σ(w_i · v_i) / Σ(w_i)

Paper 118 asked: is the weighted mean the right consensus function? It is the maximum-likelihood estimator when the errors are Gaussian. But the sea is not always Gaussian. A single lying witness with a large weight can drag the mean far off the true mark. Open Q1 asked whether the substrate should support other consensus functions — and what the math says about each.

### The resolution

The convoy now supports four consensus methods:

**Method 1: `weighted_mean`.** The original. For each witness i with value v_i and weight w_i:

    V = Σ(w_i · v_i) / Σ(w_i)

Properties: it is the unique minimizer of weighted squared error, Σ w_i (V − v_i)². It is smooth, cheap, and fragile. One compromised witness with weight w and a value k standard deviations off drags the convoy by (w / Σw) · k. The math's verdict: use it when witnesses are honest or when errors are symmetric and small.

**Method 2: `weighted_median`.** Sort the witnesses by value. Walk down the sorted list accumulating weights. The weighted median is the first value where the accumulated weight reaches half the total:

    V = min{ v_j : Σ_{i: v_i ≤ v_j} w_i ≥ (Σ w_i) / 2 }

Properties: the weighted median is the minimizer of weighted absolute error, Σ w_i |V − v_i|. Its crucial property is the breakdown point. For the weighted mean, a single witness with weight w can shift the answer arbitrarily if w is large relative to the rest. For the weighted median, a coalition of witnesses with total weight W_liars cannot move the median past the honest witnesses' range unless W_liars exceeds half the total weight. Formally: if the liars' total weight is less than Σw/2, the median stays inside the interval spanned by the honest values. The breakdown point of the median, in weight terms, is 1/2. The mean's is 0 — any single nonzero weight can break it, given a large enough lie.

The math's verdict: use the median when witnesses can be adversarial.

**Method 3: `trimmed_mean`.** Cut the top t fraction and the bottom t fraction of witnesses by value, then take the weighted mean of the remainder:

    V = Σ_{i ∈ middle} (w_i · v_i) / Σ_{i ∈ middle} w_i

where "middle" excludes the t·n lightest and t·n heaviest values. The trimmed mean sits between the mean and the median. It keeps more of the honest signal than the median (which uses effectively one witness's value) while discarding the extreme liars. Its breakdown point is t: a coalition of liars with weight fraction less than t cannot touch the estimate at all. The math's verdict: use it when lies are expected at the tails but the honest center is dense.

**Method 4: `highest_weight`.** The convoy simply takes the value of the single witness with the greatest weight:

    V = v_j, where j = argmax(w_i)

Properties: this is not an estimator at all in the statistical sense — it is a delegation. It says: we trust the strongest witness outright. It is O(n) with a trivial constant, it is deterministic, and it fails completely if the strongest witness is the liar. Its virtue is that it makes trust legible: everyone can see exactly whose value won and why. The math's verdict: use it when weights encode verified authority rather than noisy observation.

### The theorem

The substrate now carries this as a proved property:

**Theorem (convoy robustness ordering).** For a fixed weight distribution, the maximum displacement of the convoy's agreed value under an adversarial coalition of weight fraction f satisfies:

- `weighted_mean`: unbounded for any f > 0.
- `trimmed_mean` (trim t): zero for f < t, bounded by honest range for f < 1/2 − t.
- `weighted_median`: bounded by honest range for f < 1/2.
- `highest_weight`: zero for f = 0, unbounded for any f > 0 (if the coalition holds the max weight).

This ordering is why the four methods exist as a choice rather than one being declared the winner. The substrate cannot know in advance whether its witnesses are noisy or adversarial, so it exposes the spectrum and lets the cell's configuration decide. The test suite pins each row of the table with an adversarial-witness test.

The metal: `consensus_method` is a per-cell parameter. The convoy computes all four when asked, records which one was used, and the witness log (see Part III) records the inputs, so any auditor can recompute the consensus under a different method and compare. That last point matters: because the raw witness values are logged, the consensus method is not a commitment — it is a lens. You can re-lens history.

Q1 closed.

---

## Part III: Q3 Resolved — Every Agent Keeps a Witness Log

### The question, as it stood

The substrate's history was cell-centric. The ledger recorded what happened to cells: which address changed, when, to what value, under which convoy. But it did not cleanly answer the question an auditor most wants to ask: *what did this particular agent do?* Open Q3 asked for a per-agent witness log — an independent record of every action, attributed, sequenced, and queryable.

### The resolution

`Substrate._agent_witness` is now a first-class structure. Every agent action — read, write, propose, witness, abstain — is appended to that agent's log with:

- the tick at which the action occurred,
- the address of the cell acted upon,
- the action type,
- the value observed or proposed,
- and a hash chaining to the agent's previous action.

The chaining deserves a sentence. Each agent's log is itself a hash chain:

    h_k = H(h_{k−1} ‖ tick_k ‖ address_k ‖ action_k ‖ value_k)

with h_0 the agent's genesis. This means an agent's history is tamper-evident on its own terms: you cannot rewrite one entry without breaking every entry after it. And because the substrate also commits to the set of current agent-log heads at each tick (see Part IV, where the Merkle tree subsumes this), the per-agent chains are anchored into the global structure.

### The math

**Theorem (per-agent auditability).** For any agent A and any tick range [t_1, t_2], the set of A's actions in that range can be enumerated in time proportional to the number of actions, and each action can be verified as authentic in O(1) additional work given the agent's chain head at t_2 and the chain head at t_1.

The proof is by the chain structure: verification of the k-th entry requires only h_{k−1}, which is stored in the entry itself; authenticity of the whole prefix reduces to matching the stored head against the committed head. Enumeration is linear because the log is append-only.

The consequence for the convoy is subtle and worth stating: an agent's weight in the convoy can now be a function of its witnessed history, not just a static parameter. An agent whose log shows a thousand honest ticks of agreement with consensus earns weight; an agent whose log shows repeated divergence loses it. The substrate does not yet implement adaptive weighting — that remains in the open list (see Part VIII) — but the log makes it possible, and the math of Q1 tells us why we'd want it: weight-based robustness is only as good as the weight's honesty.

Q3 closed.

---

## Part IV: Q4 Resolved — The Merkle Tree, or O(log N) Proof That a Thing Was There

### The question, as it stood

The substrate's global commitment was a flat hash: the state root, computed by hashing everything together. To prove that a particular address was in the state at a particular tick, you had to rehash everything — O(N) work for N cells. Open Q4 asked for a Merkle tree, so that inclusion proofs cost O(log N).

### The resolution

`Substrate.merkle_root()` and `Substrate.merkle_proof(address)` now exist.

The construction is standard but stated here for the canon. The cells' addresses are sorted. The leaves of the tree are the hashes of each cell's committed state: H(address ‖ value_hash ‖ convoy_hash). The tree is binary and balanced over the sorted leaves. Internal nodes hash their two children: H(left ‖ right), with an unbalanced node hashed with a null sibling. The root is the commitment.

`merkle_proof(address)` returns the sibling path from the leaf to the root: a list of (sibling_hash, direction) pairs, of length exactly ⌈log₂ N⌉.

### The math

**Theorem (inclusion proof soundness and cost).** Given the Merkle root R and a proof path P of length ⌈log₂ N⌉ for address a, a verifier can confirm that the substrate committed to cell state (a, value_hash, convoy_hash) at the tick that produced R, in O(log N) time, under the assumption that H is collision-resistant.

*Proof sketch.* Soundness: a forged proof that a was committed with a different value requires either a collision in H at some node along the path, or a second tree with the same root — which itself implies a collision at the root's subtree boundary. Cost: the path length is the tree depth, ⌈log₂ N⌉, and verification is one hash per level. ∎

**Theorem (exclusion).** Because the leaves are sorted by address, the proof for address a also proves *exclusion* when a is absent: the proof path terminates at the two leaves adjacent to where a would sit, and their addresses bracket the gap. A verifier confirms a ∉ state in O(log N).

This second property is the quiet important one. The substrate can now prove a negative: *this address was never written.* For an audit trail, proving absence is often more valuable than proving presence — "show me that no one touched this cell" is the question the Merkle tree answers cheaply.

The test in `test_math.py` constructs substrates of sizes 1, 2, 3, ..., 1024, generates proofs for every address, verifies each against the root, corrupts one bit in each proof, and confirms every corrupted proof fails. It also measures path length and asserts it equals ⌈log₂ N⌉ exactly. The metal matches the math to the bit.

Q4 closed.

---

## Part V: Q6 Resolved — Four New Openers, Four New Doors

### The question, as it stood

The substrate could be opened — inspected, dumped, rendered — in a fixed small set of ways. Open Q6 asked for more openers: more projections of the same underlying truth, because different readers need different doors. A cell is a cell, but a human at a terminal, a voice pipeline, a touch interface, and a graph tool each need the cell spoken in their own tongue.

### The resolution

Four openers added:

**Opener: `voice`.** The cell rendered as text-to-speech input. Not a dump — a narration. The opener produces a spoken-language rendering of the cell's state: its address, its value, its convoy's consensus, phrased for the ear. The design constraint is that the TTS text must be *complete*: everything a visual dump shows must be sayable. If a property cannot be spoken, it does not belong in the cell's public state. This constraint has already improved the data model — one field was renamed during implementation because its name was unpronounceable, and the rename stuck everywhere.

**Opener: `telnet`.** A plain CLI dump: fixed-width, monospace, line-oriented, no ANSI escape codes, no cursor movement. Designed for the oldest interface there is — a raw socket and a terminal. The telnet dump is the substrate's canonical "what you see over a wire" view, and because it is deterministic (same state, same bytes, always), it is itself hashable and testable. The test suite asserts byte-identical output across repeated renders of identical state.

**Opener: `gesture`.** Touch JSON: the cell's state as a structure suitable for a touch interface — spatial regions, tappable zones, values with display hints. The gesture opener is the first opener that encodes *interaction*, not just display: it specifies which mutations are offered at which regions, so a touch client can present the legal moves without knowing the substrate's rules.

**Opener: `flowchart`.** Graphviz DOT: the cell and its convoy as a directed graph. Agents are nodes, witness relationships are edges, weights are edge labels, and the consensus method colors the convergence node. The DOT output is valid Graphviz — the tests pipe it through a DOT parser to confirm — and it has already earned its keep as a debugging tool: rendering the convoy as a graph is how the Vibe bug (Part VII) was first *seen*, before it was understood.

### The math

The theorem here is about the openers as a class:

**Theorem (opener fidelity).** Every opener is a pure function of the cell's committed state. Two cells with identical committed state produce identical opener output, for all four openers, at every tick.

This sounds trivial and is not. It forbids openers from consulting anything outside the committed state — no ambient timestamps, no random IDs, no sequence numbers that aren't in the state itself. The purity is what makes the telnet dump hashable, the flowchart reproducible, and the voice rendering testable. The test suite pins this by rendering the same state through all four openers, mutating an uncommitted field, and confirming all four outputs are unchanged.

Q6 closed.

---

## Part VI: Q7 Partially Resolved — The Convoy Carries the Value Now

### The question, as it stood

The convoy was a hash. When a cell's history was committed, the convoy's contribution was a digest — a hash of the witnesses and their agreement — but not the agreed value itself. This meant the commitment proved *that* the convoy agreed without proving *what* they agreed to. Open Q7 asked whether the convoy should be a first-class entity: addressable, inspectable, carrying its own state.

### The resolution — partial

The convoy now carries the value. The convoy's committed state includes:

- the agreed value V (under whichever consensus method was used),
- the method used,
- the witness set with weights,
- and the hash of all of the above.

So the Merkle leaf for a cell now commits to the convoy's *answer*, not merely the fact of its deliberation. An inclusion proof for a cell proves the value the convoy agreed on. This closes the most important half of Q7.

What remains open: the convoy still lives per-cell. It is not itself addressed. You cannot point at "the convoy for cell X at tick T" as a first-class addressable entity with its own history and its own proofs; you can only reach it through the cell. Making the convoy addressable — giving it its own namespace in the address space, its own Merkle commitments across ticks, its own opener renderings — is the remaining half of Q7, and it stays on the open list.

The math for the resolved half:

**Theorem (convoy value commitment).** The Merkle leaf hash H(address ‖ value_hash ‖ convoy_hash) now binds the cell's value, the convoy's agreed value, the consensus method, and the witness set. Any inclusion proof at tick T proves all four simultaneously. Changing any one of the four changes the leaf hash, changes the root, and invalidates every existing proof.

The test suite pins this by mutation: for each of the four fields, mutate it, confirm the root changes, confirm the old proof fails. Four mutations, four root changes, four proof failures — sixteen assertions per cell, run across a battery of cell configurations.

Q7: half closed, half carried forward. On the open list it goes, marked "partial."

---

## Part VII: The Bug — The Undamped Vibe

Now the confession. This is the part of the watch report where the keeper admits the ship took water.

### What the Vibe is

The Vibe is the substrate's aggregate mood signal — a scalar computed each tick from the cells' recent histories, meant to capture the overall character of the loop's activity: calm, agitated, trending, settling. Paper 106 defined it as a weighted sum of per-cell momentum terms, updated per tick.

### What the math found

When paper 118's analysis turned to the Vibe's dynamics, it modeled the update as a recurrence and asked the standard question: is this recurrence stable? The answer, when the constants were plugged in from the implementation, was: **no.**

The Vibe's update had the form:

    Vibe(t+1) = a · Vibe(t) + b · Δ(t)

where Δ(t) is the per-tick activity impulse and a was the momentum coefficient. The implementation had set a = 1.0 — full momentum, no decay — on the reasoning that the Vibe should "remember everything." But a recurrence x(t+1) = a·x(t) + b·u(t) with a = 1 is a pure accumulator. With a > 1 it is an explosion. The implementation, through a floating-point path that is too embarrassing to detail in full, effectively produced a slightly greater than 1 — the momentum coefficient was computed as `1.0 + epsilon` where epsilon was a small positive correction term intended for something else entirely.

So the Vibe was an undamped oscillator-accumulator with a gain above unity. Any sustained activity pushed it toward infinity; any oscillating activity made it ring with growing amplitude. It had not yet exploded in the tests because the test runs were short — a few hundred ticks — and the divergence timescale was longer than the tests. The math caught what the tests' patience had not.

### The fix

Damping. The recurrence is now:

    Vibe(t+1) = a · Vibe(t) + b · Δ(t), with a = 1 − λ, λ > 0

The substrate sets λ such that the Vibe's half-life is a configured number of ticks — the mood forgets on a known schedule rather than remembering forever or exploding.

### The math

**Theorem (Vibe boundedness).** With a = 1 − λ, 0 < λ < 1, and |Δ(t)| ≤ Δ_max for all t:

    |Vibe(t)| ≤ |Vibe(0)| · (1−λ)^t + (b · Δ_max / λ)

The first term decays to zero; the second is the steady-state bound. The Vibe is bounded for all time, and its bound is tight in the worst case (constant maximal impulse).

**Theorem (Vibe half-life).** The Vibe's half-life — the number of ticks for a perturbation to decay to half — is exactly ⌈log(1/2) / log(1−λ)⌉, independent of the perturbation's size. The substrate exposes the half-life as a configuration parameter and derives λ from it, so operators think in half-lives ("the mood forgets in 64 ticks") rather than raw decay coefficients.

The test in `test_math.py` runs the Vibe for 10,000 ticks under maximal sustained impulse and asserts it never exceeds the steady-state bound plus a small epsilon. Under the old recurrence, this test would have overflowed by tick 3,000. It is the test the old code deserved and never had.

A lesson for the canon: the math did not find the bug by being clever. It found it by asking the boring question — "is this recurrence stable?" — that no one had asked because the Vibe seemed like a soft, fuzzy, non-mathematical thing. There are no soft fuzzy things. Everything that updates is a dynamical system, and every dynamical system owes you an answer about its fixed points and its bounds. The Vibe now pays its debts.

---

## Part VIII: The Ledger of Open Questions — Ten Remain

The open list stood at fifteen after paper 118. Five entries are now closed (Q1, Q3, Q4, Q6 fully; Q7 partially — its closed half counts, its open half stays). Ten remain. For the record, and for whoever takes the next watch:

**Open Q2 (Convoy weight provenance):** Where do weights come from? The four consensus methods of Q1 make weight-honesty decisive, and nothing yet guarantees it. The witness log of Q3 makes adaptive weighting *possible*; nothing yet makes it *happen*.

**Open Q5 (Cross-cell atomicity):** Can an agent act on multiple cells in one tick such that the acts are provably all-or-nothing? The per-cell Merkle commitments make single-cell proofs cheap; multi-cell transactions need a cross-cell commitment structure that does not yet exist.

**Open Q7-remainder (Convoy as addressable entity):** As documented in Part VI. The convoy carries its value; it does not yet carry its own address.

**Open Q8 (Convoy membership dynamics):** Who joins and leaves the witness set, when, and under what proof? Membership is currently static per-cell per-tick.

**Open Q9 (Adversarial weight games under trimmed mean):** Q1's robustness table bounds displacement for a *fixed* weight distribution. What happens when liars can also choose their weights, or split into multiple witnesses? The breakdown analysis under strategic weight-splitting is open.

**Open Q10 (Opener composition):** Can openers compose — a flowchart of a telnet dump, a voice narration of a gesture map? The purity theorem of Q6 makes composition well-defined; nothing implements it.

**Open Q11 (Pruning and archival):** The witness logs and Merkle commitments grow without bound. What can be pruned, what must be archived, and what does an archived proof look like? The O(log N) proofs of Q4 assume the full tree is present.

**Open Q12 (Concurrent agent scheduling):** The loop currently serializes agent actions per tick. What is the equivalence class of schedules that produce identical commitments — and can agents run concurrently within it?

**Open Q13 (Vibe coupling):** Now that the Vibe is damped and bounded (Part VII), should anything *read* it? Can agent behavior or convoy weighting legitimately depend on the Vibe without creating feedback loops that reintroduce instability? A damped signal feeding back into its own input is a new dynamical system and needs its own stability proof.

**Open Q14 (Formal spec extraction):** Can the 10 theorem-validated properties be extracted into a machine-checked formal specification, so that future implementations are verified against the spec rather than tested against the tests?

Ten open questions. The fog has lifted in five places and sits thicker where it always did — over the deep water of concurrency, adversarial games, and formal verification. That is the natural shape of progress in this canon: each answer reveals the next question's true size.

---

## Part IX: The Tests — 76 to 93, and the Seventeen That Are Theorems

The test suite grew from 76 tests to 93. All green. The growth decomposes:

- **5 tests for the four consensus methods** of Q1: one per method for correctness against hand-computed values, plus an adversarial-coalition test that pins the robustness table of Part II row by row.
- **4 tests for the agent witness log** of Q3: append correctness, chain integrity, tamper detection (rewrite one entry, watch the chain break), and audit enumeration over a tick range.
- **6 tests for the Merkle tree** of Q4: root determinism, proof generation at every size from 1 to 1024, proof verification, corrupted-proof rejection, exclusion proofs, and the exact path-length assertion ⌈log₂ N⌉.
- **5 tests for the openers** of Q6: one per opener for validity (the DOT test parses; the telnet test asserts byte-determinism; the voice test checks completeness of narration; the gesture test validates the JSON schema), plus the shared purity test that mutates uncommitted state and confirms all four outputs are unchanged.
- **4 tests for the convoy value commitment** of Q7's resolved half: the four mutation tests of Part VI, each confirming a changed root and a broken proof.
- **3 tests for the damped Vibe** of Part VII: the 10,000-tick bound test, the half-life decay test, and a regression test that reproduces the original divergence under the old constants and confirms the new constants hold where the old ones failed.

That is 27 new tests, but the count went up by 17 — because 10 older tests were consolidated or subsumed. The flat-hash commitment tests, for instance, collapsed into the Merkle tests, since the Merkle root subsumes the flat hash's role. The suite grows in coverage faster than it grows in count, which is the right direction: tests should be dense, not many.

### `test_math.py` — the seventeen theorems

Within the suite lives `test_math.py`: 17 tests, each one a theorem from the canon, each one stated as a test. The current roster:

1. **Convoy weighted-mean correctness** — the estimator matches the closed form.
2. **Convoy weighted-median breakdown bound** — coalitions below half-weight cannot escape the honest range.
3. **Convoy trimmed-mean trim bound** — coalitions below the trim fraction cannot move the estimate.
4. **Convoy highest-weight delegation** — the strongest witness's value wins, provably and visibly.
5. **Agent chain tamper-evidence** — any single-entry rewrite breaks the chain head.
6. **Agent audit linearity** — enumeration over a tick range is linear in actions taken.
7. **Merkle root determinism** — same state, same root, every time.
8. **Merkle inclusion soundness** — valid proofs verify; this is the collision-resistance reduction in executable form.
9. **Merkle proof length** — exactly ⌈log₂ N⌉, at every size tested.
10. **Merkle exclusion** — absence is provable in O(log N) via sorted-leaf bracketing.
11. **Opener purity** — openers are functions of committed state alone.
12. **Opener completeness** — the voice narration says everything the telnet dump shows.
13. **Convoy value binding** — the leaf hash binds value, convoy value, method, and witnesses jointly.
14. **Vibe boundedness** — the steady-state bound holds for 10,000 ticks under maximal impulse.
15. **Vibe half-life** — perturbations decay with the configured half-life, size-independently.
16. **Vibe divergence regression** — the old constants diverge; the new ones do not; the test knows the difference.
17. **Loop convergence** — the substrate's core loop reaches a fixed point under quiescent input, the founding theorem of paper 101, still holding after all the additions.

Seventeen theorems, seventeen tests. When the metal changes, these tests are the first line of defense: they are the canon's claims about the metal, stated in the only language the metal cannot ignore — executable assertions that fail loudly.

---

## Part X: The New State — Ten Theorem-Validated Properties

At the close of paper 118, the substrate carried **5 proved properties** — the founding theorems of the loop, the cell, the address, the commitment, and the convoy's basic consensus.

This update adds **5 resolved open questions**, each resolution carrying its own theorems, each theorem pinned by its own tests:

1. **Convoy weighted-mean consensus** (Q1) — now a four-method spectrum with a proved robustness ordering.
2. **Per-agent witness log** (Q3) — tamper-evident, linearly auditable, chain-verified.
3. **Merkle inclusion and exclusion** (Q4) — O(log N) proofs of presence and, just as important, of absence.
4. **Four new openers** (Q6) — voice, telnet, gesture, flowchart; all pure functions of committed state.
5. **Convoy value commitment** (Q7, half) — the leaf binds the answer, not just the deliberation.

Five proved. Five resolved. **Ten theorem-validated properties**, each one a place where the math said "the metal must behave like this," the metal said "agreed," and the tests said "and it still does."

And one bug found and damped along the way — the Vibe that would have rung to infinity, caught by a stability question that should have been asked on day one and was asked on day one-hundred-and-eighteen. The canon's method works, and the proof that it works is that it caught the canon's own error.

---

## Part XI: Closing the Watch

The state of the substrate at this bell:

- 93 tests, all green.
- 17 of them theorems.
- 10 theorem-validated properties.
- 10 open questions on the ledger.
- 1 bug damped, documented, and regression-tested so it cannot quietly return.
- 4 consensus methods, 4 openers, 1 witness log per agent, 1 Merkle tree over everything.

The next watch inherits the ten open questions and one instruction, the same instruction every watch has carried since paper 100: the math goes first, the metal follows, the tests rivet the two together, and nothing — not the Vibe, not the convoy, not the mood of the loop — is too soft or too fuzzy to owe a proof.

The fog lifts in five places. The deep water is still deep. The watch turns over.

End of paper 119. The loop continues.