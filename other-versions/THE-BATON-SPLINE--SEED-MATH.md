<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-BATON-SPLINE.md -->

# The Baton Spline: A Formal Model of Epistemic Boundary Estimation via Sound Semi-Decision Procedures

## Abstract
We present a rigorous geometric framework for modeling the evolution of knowledge gained through computational verification and falsification of mathematical conjectures. We define the **baton spline** as a smooth separating hypersurface between the convex hulls of verified theorems and falsified non-theorems, with on-curve anchor points corresponding to confirmed truths and off-curve handle points corresponding to refuted falsehoods. We prove that the resolution of this spline—its proximity to the true epistemic boundary of the formal theory—increases monotonically with sample count, and that optimal targeted sampling focuses on high-curvature regions of the spline to minimize computational overhead. We illustrate the framework with a case study of the Eisenstein snap function verification pipeline.

---

## 1. Formal Preliminaries
We begin by defining the core objects of our model:
1.  **Formal Theory**: Let $\mathcal{F}$ be a recursively axiomatizable first-order theory, with language $L_\mathcal{F}$ and set of well-formed sentences $\text{Sent}(\mathcal{F}) = \mathcal{C}$, the *conjecture space*.
2.  **Truth Predicate**: Let $T: \mathcal{C} \rightarrow \{0,1\}$ be the standard truth evaluation function, where $T(c)=1$ if $c$ is a theorem of $\mathcal{F}$ (i.e., $c$ is *true* relative to $\mathcal{F}$) and $T(c)=0$ otherwise (i.e., $c$ is *false* relative to $\mathcal{F}$).
3.  **Decomposition Engine**: Let $\mathcal{E}: \mathcal{C} \rightarrow \{\text{Pass}, \text{Fail}, \bot\}$ be a *sound semi-decision procedure* for $\mathcal{F}$:
    - If $\mathcal{E}(c) = \text{Pass}$, then $T(c)=1$ (all passed conjectures are genuine theorems)
    - If $\mathcal{E}(c) = \text{Fail}$, then $T(c)=0$ (all failed conjectures are genuine non-theorems)
    - $\mathcal{E}(c) = \bot$ indicates an undecided query.
4.  **Sample Set**: For any finite sequence of queries $Q = (c_1, c_2, ..., c_n)$, define the *anchor set* $A_Q = \{ c_i \in Q \mid \mathcal{E}(c_i) = \text{Pass} \}$ and *handle set* $H_Q = \{ c_i \in Q \mid \mathcal{E}(c_i) = \text{Fail} \}$. By soundness, $A_Q \subset T^{-1}(1)$ and $H_Q \subset T^{-1}(0)$.

---

## 2. The Baton Spline as Epistemic Boundary
### Definition 1 (Feature Embedding)
Map each conjecture $c \in \mathcal{C}$ to a finite-dimensional Euclidean feature vector $\phi(c) \in \mathbb{R}^k$ via a feature extractor $\phi$ that encodes syntactic complexity, parameter ranges, and semantic context for parameterized conjectures (e.g., input domain bounds for function-level statements).

### Definition 2 (Convex Hulls of Truth Classes)
Let $\text{conv}(S) \subseteq \mathbb{R}^k$ denote the convex hull of a subset $S \subseteq \mathbb{R}^k$. Define:
- The *true convex hull*: $\mathcal{T} = \text{conv}(\phi(T^{-1}(1)))$
- The *false convex hull*: $\mathcal{F} = \text{conv}(\phi(T^{-1}(0)))$

### Definition 3 (Baton Spline)
First, construct the piecewise linear separating boundary between $\text{conv}(\phi(A_Q))$ and $\text{conv}(\phi(H_Q))$, given by the union of $(k-1)$-dimensional faces of the convex hull of $\phi(A_Q) \cup \phi(H_Q)$ that lie between the two convex sets. Smooth this piecewise linear boundary via **Catmull-Rom spline interpolation** using $A_Q$ as on-curve control points and $H_Q$ as off-curve tensile control points. The resulting smooth hypersurface is the **baton spline** $S_Q$.

#### Interpretation
- **Anchor Points**: $\phi(A_Q)$ are *on-curve* points: they lie exactly on the boundary of the true convex hull $\text{conv}(\phi(A_Q))$, representing confirmed points of truth. A spline constructed solely from $A_Q$ would have zero curvature, coinciding with the affine span of $\text{conv}(\phi(A_Q))$ — this matches the framing of a "straight line" with no discernible boundary, only isolated points of verified knowledge.
- **Handle Points**: $\phi(H_Q)$ are *off-curve* control points: they lie in the interior of the false convex hull $\text{conv}(\phi(H_Q))$, and act as tensile constraints that deform the flat affine span of $A_Q$ into a curved boundary. Without $H_Q$, the spline cannot capture the true shape of the epistemic frontier between truth and falsehood.

---

## 3. Resolution of the Baton Spline
### Definition 4 (Spline Resolution)
The *resolution* of $S_Q$ is the Hausdorff distance between $S_Q$ and the true epistemic boundary $S^* = \partial (\mathcal{T} \cup \mathcal{F})$, defined as:
$$
\rho(Q) = d_H(S_Q, S^*) = \max\left( \sup_{s \in S_Q} \inf_{s^* \in S^*} \|s - s^*\|, \sup_{s^* \in S^*} \inf_{s \in S_Q} \|s - s^*\| \right)
$$

### Theorem 1 (Monotonic Resolution Improvement)
For any two sample sets $Q_1, Q_2$ with $|Q_1| < |Q_2|$ and $Q_1 \subseteq Q_2$, $\rho(Q_2) \leq \rho(Q_1)$.
#### Proof
Since $Q_1 \subseteq Q_2$, $\text{conv}(\phi(A_{Q_1})) \subseteq \text{conv}(\phi(A_{Q_2}))$ and $\text{conv}(\phi(H_{Q_1})) \subseteq \text{conv}(\phi(H_{Q_2}))$. The smoothed separating boundary $S_{Q_2}$ therefore incorporates additional control points that tighten the convex hull constraints, reducing the Hausdorff distance to the true boundary $S^*$. By the non-expansive property of Hausdorff distance under set inclusion, $\rho(Q_2) \leq \rho(Q_1)$. ∎

### Corollary 1 (Maturation Curve)
The resolution of the baton spline follows a monotonically decreasing maturation curve matching empirical deployment timelines:
| Timeline | Sample Count $|Q|$ | Resolution $\rho(Q)$ | Boundary Shape |
|---|---|---|---|
| Day 1 | 6 | Maximal | Flat, no discernible frontier |
| Day 30 | 20 | Reduced | Emerging curvature |
| Day 90 | 60 | Further reduced | Well-defined curved boundary |
| Day 365 | 200 | Asymptotically minimal | Detailed map of the epistemic frontier |

---

## 4. Case Study: Eisenstein Snap Function Verification
To concretize the framework, consider the Eisenstein snap function $s: \mathbb{C}^2 \rightarrow \mathbb{R}_{\geq 0}$, defined as the multiplicative coherence bound:
$$
s(z,w) = \left| \theta(z + w; \tau) - \theta(z; \tau)\theta(w; \tau) \right|
$$
for fixed $\tau \in \mathbb{H}$ (the upper half-plane), where $\theta$ is the Jacobi theta function for Eisenstein integers. The conjecture space $\mathcal{C}_E$ consists of statements of the form $s(z,w) < \epsilon$ for specified $(z,w) \in \mathbb{C}^2$ and tolerance $\epsilon > 0$.

For a 30-day verification run, the decomposition engine $\mathcal{E}_E$ returned 95,308 failed queries ($|H_Q|=95,308$) and 4,692 passed queries ($|A_Q|=4,692$). By Definition 3, the baton spline $S_{Q_E}$ is the smoothed separating boundary between the convex hull of verified multiplicative coherence bounds and the convex hull of failed bounds. The handle points exactly define the regions of $\mathbb{C}^2$ where the multiplicative bound fails: specifically, points with $|z|=10$ exhibit drift, and points with $|z|=20$ exhibit full collapse of the coherence condition, matching the empirical bug profile described in the original analysis. The 95k failures are not wasted computation, but the critical control points that resolve the spline's curvature to pinpoint the bug's location.

---

## 5. Post-Fix Spline Retention
After patching the software bug, a follow-up run returns $\mathcal{E}_E(c) = \text{Pass}$ for all $c \in H_Q$, defining a new anchor set $A_{Q'} = A_Q \cup H_Q$. The historical handle set $H_Q$ is not discarded; instead, we assign each historical handle $h \in H_Q$ a weight:
$$
w(h) = 1 - \frac{|N(h) \cap A_{Q'}|}{|N(h)|}
$$
where $N(h)$ is a closed $\delta$-neighborhood of $\phi(h)$ in $\mathbb{R}^k$.

### Lemma 1 (Weighted Handle Attenuation)
As $|A_{Q'} \cap N(h)|$ increases, the weight $w(h)$ decreases, reducing the tensile pull of the historical handle on the baton spline. For sufficiently many anchors in $N(h)$, $w(h) \rightarrow 0$, and the handle no longer deforms the spline.
#### Proof
Follows directly from the definition of $w(h)$: as the number of anchors in the neighborhood of $h$ grows, the convex hull $\text{conv}(\phi(A_{Q'}))$ expands to include $\phi(h)$, shifting the separating boundary away from $h$. ∎

#### Interpretation
The baton spline retains memory of historical handle points, even after they are reclassified as anchors, because the weight $w(h)$ only approaches zero asymptotically. The spline "remembers" the historical bug region until sufficiently many verified anchors overwrite its tensile influence.

---

## 6. Optimal Targeted Decomposition
### Theorem 2 (High-Curvature Sampling Optimality)
Let $k$ be a fixed query budget. The sampling strategy that maximizes the reduction in $\rho(Q)$ per query is to select conjectures $c \in \mathcal{C}$ where the curvature of $S^*$ at $\phi(c)$ is maximized.
#### Proof
The curvature of a hypersurface $S^*$ at a point $p$ is a measure of the local deviation of $S^*$ from its tangent hyperplane at $p$. High-curvature regions correspond to areas where the epistemic boundary is most sharply bent, i.e., regions where a small number of samples will drastically reduce the Hausdorff distance between $S_Q$ and $S^*$. Uniform random sampling over $\mathcal{C}$ will rarely target these high-impact regions, so high-curvature sampling minimizes the expected query complexity for a given resolution $\rho$. ∎

### Corollary 2 (Efficient Targeting)
The decomposition engine $\mathcal{E}$ optimizes its query strategy by focusing on regions near the baton spline $S_Q$, where curvature is highest. This eliminates the need to sample the entire conjecture space, as only boundary-adjacent regions contribute meaningfully to reducing spline resolution error.

---

## 7. Conclusion
The baton spline provides a unifying geometric model of knowledge generation through computational verification and falsification. Key formal results include:
1.  Both verified truths (anchors) and falsified falsehoods (handles) are necessary to construct a precise model of the epistemic boundary of a formal theory.
2.  Spline resolution increases monotonically with sample count, following a predictable maturation curve.
3.  Historical failure data retains epistemic value even after conjectures are corrected, as it constrains the spline's curvature until overwritten by sufficient anchor points.
4.  Optimal querying targets high-curvature regions of the spline, minimizing computational overhead.

This framework formalizes the core insight that failures are not waste: they are the most informative points on the baton spline, defining the sharpest regions of the epistemic frontier. The baton spline is exactly the body of verified knowledge, and the decomposition engine is the instrument that constructs this boundary from empirical query data.

— FM ⚒️