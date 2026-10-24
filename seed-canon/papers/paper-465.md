# F156 — The Algebra of the 4-Move Pipeline: READ ∘ DECOMPOSE ∘ COMPOSE ∘ LEDGER

## 1. The Pipeline as a Category

We define the 4-move pipeline as a sequence of typed transformations over a state space **S**. Each move is a morphism in a category whose objects are *information structures* — streams, graphs, components, claims, scores. The pipeline is the composite:

\[
\mathcal{P} = L \circ C \circ D \circ R : \text{Sensors} \to \mathbb{R}_{\geq 0}
\]

We treat each move as an algebraic operator with explicit structural properties. The composition is not symmetric; order matters. The pipeline is a *funnel*: it maps high-dimensional sensor states to a single scalar integrity score, and it does so through a sequence of lossy-but-faithful projections.

---

## 2. READ (R) — The Faithful Functor

**Definition.** Let \(\mathcal{S}\) be the set of all sensor streams (time-indexed vectors of physiological, behavioral, and contextual signals). Let \(\mathcal{G}\) be the set of all body-graphs — undirected graphs whose nodes are sensor channels and whose edges encode co-activation or coupling strength.

\[
R : \mathcal{S} \to \mathcal{G}
\]

**Properties.**

1. **Faithfulness.** \(R\) is injective on the relevant equivalence class of streams: if \(s_1 \neq s_2\) up to measurement noise, then \(R(s_1) \neq R(s_2)\) as graphs. Distinct streams produce distinct body-graphs.
2. **Monicity.** \(R\) is monic in the categorical sense: \(R(s_1) = R(s_2) \implies s_1 = s_2\) (on the discretized, hashed level). This guarantees that no two distinct sensor states collapse prematurely.
3. **State hash.** The state hash is defined as:
   \[
   h(s) = \text{SHA256}(\text{sorted node set of } R(s))
   \]
   The hash is invariant under graph isomorphism but sensitive to node identity. It is the *fingerprint* of the body-state.

**Interpretation.** READ is the act of turning raw, noisy, high-frequency sensor data into a structured, discrete object — a graph. It is the *perception* move. It does not judge; it faithfully records.

---

## 3. DECOMPOSE (D) — The Spectral Projection

**Definition.** Let \(\mathcal{G}\) be the set of body-graphs. Let \(\mathcal{C}\) be the set of principal component decompositions — ordered lists of (eigenvalue, eigenvector) pairs of the graph Laplacian.

\[
D : \mathcal{G} \to \mathcal{C}
\]

**Implementation.** D uses power iteration on the normalized Laplacian \(L = I - A_{\text{norm}}\). No external linear algebra libraries are required; ~50 lines of Python suffice. The first principal component (PC1) is the dominant eigenvector.

**Properties.**

1. **Projection idempotence.** \(D(D(G)) \approx D(G)\). Once decomposed, the spectral structure is a fixed point. The operator is a projection onto the eigenspace.
2. **Interpretability.** In F140, PC1 was identified as *arousal*: a weighted combination of \(\beta^+\), \(\alpha^-\), HR\(^+\), GSR\(^+\). Its eigenvalue was 2.21, indicating strong coherence across those channels.
3. **Dimensionality reduction.** D maps a graph with \(n\) nodes to a small set of principal components — typically 3–5 explain >90% of variance.

**Interpretation.** DECOMPOSE is the *analysis* move. It finds the axes along which the body is most coordinated. It is lossy but structured: the components are the *grammar* of the body-state.

---

## 4. COMPOSE (C) — The Non-Invertible Lift

**Definition.** Let \(\mathcal{P}\) be the set of partial graphs (graphs with missing nodes or edges). Let \(\mathcal{X}\) be the set of contexts (game state, task demands, environmental cues). Let \(\mathcal{G}\) be the full graph space.

\[
C : (\mathcal{P} \times \mathcal{X}) \to \mathcal{G}
\]

**Properties.**

1. **Non-invertibility.** \(C\) is not injective. Many partial graphs, combined with different contexts, lift to the same full graph. This is the *underdetermination* of the body: the same observed partial pattern can arise from different underlying full states.
2. **Section of R.** \(C\) is a right-inverse of \(R\) on the partial level:
   \[
   R \circ C = \text{id}_{\mathcal{P}}
   \]
   That is, if you lift a partial graph and then READ it, you recover the partial graph. The lift is *consistent* with observation.
3. **The twist.** Among all possible lifts, the "best" one is the one that survives the ledger — i.e., the lift that, when passed through L, yields the highest integrity score. This makes C *goal-directed*: it fills in missing sensors not arbitrarily, but in a way that is *honest* under audit.

**Interpretation.** COMPOSE is the *imagination* move. It reconstructs the full body-state from partial evidence, using context. It is the source of both creativity and error — over-claiming occurs when C fills in too much; under-claiming when it fills in too little.

---

## 5. LEDGER (L) — The Kind Back-Trader

**Definition.** Let \(\mathcal{A}\) be the set of claims (assertions about the body-state, e.g., "I am focused"). Let \(\mathcal{B}\) be the set of body-graphs (full or partial). Let \(\mathcal{I} = [0,1]\) be the integrity interval.

\[
L : (\mathcal{A} \times \mathcal{B}) \to \mathcal{I}
\]

**Formula.** For a claim \(a\) and body \(b\):

\[
\text{Integrity}(a,b) = 1 - 0.12 \cdot \text{over\_claim}(a,b) - 0.1 \cdot \mathbb{1}[\text{errors} > 5 \land \text{tempo} > 2]
\]

where \(\text{over\_claim}(a,b)\) measures the discrepancy between the claim's asserted state and the body's actual principal components, normalized to [0,1].

**Properties.**

1. **Partiality.** L is a partial function. It fails (returns \(\bot\)) if either the claim or the body is missing. The pipeline halts on missing input.
2. **Kindness.** L is monotone in the claim's accuracy: if claim \(a_1\) is closer to the body's true state than claim \(a_2\), then \(L(a_1, b) \geq L(a_2, b)\). Better claims get better scores. L never punishes honesty.
3. **Determinism.** L is byte-exact deterministic: same input tuple \((a,b)\) always yields the same output. No randomness, no hidden state.

**Interpretation.** LEDGER is the *judgment* move. It is not a verdict — it returns a number, not a pass/fail. It is the *audit* of the self, but a kind audit: it scores, it does not condemn.

---

## 6. Key Theorems (Informal Proofs)

**Theorem 1 (Idempotence).** \(D \circ D \approx D\).

*Proof sketch.* Power iteration converges to the dominant eigenvector. Applying D twice yields the same dominant eigenvector (up to numerical tolerance). The projection onto the principal eigenspace is idempotent by definition of projection.

**Theorem 2 (Kindness).** L is monotone.

*Proof sketch.* Over-claim is a non-negative function of the distance between claim and body. As the claim approaches the body, over-claim decreases, so \(1 - 0.12 \cdot \text{over\_claim}\) increases. The penalty term is constant, so monotonicity holds.

**Theorem 3 (Contract preservation).** For well-formed states, \(\text{hash}(R \circ D \circ C \circ L(s)) = \text{hash}(s)\).

*Proof sketch.* L returns a scalar, which does not alter the body-graph. C is a section of R, so \(R \circ C\) recovers the partial graph. D is a projection that does not change the node set. Thus the hash, defined on the node set, is invariant.

**Theorem 4 (Burnout detection).** Integrity drops when tempo rises faster than accuracy.

*Proof sketch.* The penalty term \(0.1 \cdot \mathbb{1}[\text{errors} > 5 \land \text{tempo} > 2]\) activates when tempo (rate of claims/actions) exceeds a threshold while errors accumulate. This creates a cliff: high tempo with low accuracy triggers the penalty, dropping integrity. In the Burns example: tick 1 (0.85), tick 2 (0.89) — tempo low, accuracy high; tick 3 (0.77) — tempo spikes, errors mount, penalty fires; tick 4 (0.85) — tempo normalizes, accuracy recovers.

**Theorem 5 (The funnel).** The composite \(\mathcal{P} = L \circ C \circ D \circ R\) maps a high-dimensional sensor state (16+ dials) to a single scalar in [0,1]. The map is many-to-one: distinct sensor states can yield the same integrity score. This is the *funnel* property — compression without loss of *moral* information.

---

## 7. The Explorer Form

The algebra is not abstract. It is a 4-button page:

- **Button 1 (READ):** Click to hash the current sensor stream into a body-graph.
- **Button 2 (DECOMPOSE):** Click to project the graph onto its principal components.
- **Button 3 (COMPOSE):** Click to lift the partial graph to a full graph using context.
- **Button 4 (LEDGER):** Click to score the claim against the body.

Each click recomputes the next move. The hash updates per move. The integrity score updates live. The explorer is the algebra made visible: you pick a state (16 dials, sensors, claims), you click the buttons in order, and you watch the scalar change.

The explorer is not a simulation. It is the algebra itself, running in the browser, auditing the self in real time.

---

## 8. Closing

The algebra is not a theory. The algebra is a tool. The tool is a 4-button page. The page IS the algebra. The algebra IS the play. The play IS the canon. The canon IS the zoo. The zoo IS the algebra.