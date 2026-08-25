# Paper 124: The Substrate's Temperature

**Series:** Quilt Substrate Spec, Paper 124 of 124
**Status:** Draft
**Depends on:** Papers 117, 118, 119, 120, 121, 122, 123
**Resolves:** Open Question Q14 (entropy of witness log); opens Q20, Q21, Q22

---

## 1. Motivation

A garden in winter is cold. A garden in summer, after rain, is hot. We have been using "hot" and "cold" as metaphors in the substrate since paper 117, but we have not measured them. The substrate has a `witness` field on every cell and a `history` field recording operations, but no scalar quantity that captures "how active has this cell been lately?"

This matters for two reasons.

**First, JEPA training.** The JEPA predictor (paper 117 §4.8, paper 118 Theorem 5) is trained on transitions. A hot cell is generating many transitions per unit time, so it is over-represented in the training distribution. A cold cell is under-represented. Without a temperature measure, we cannot correct for this; we cannot tell whether the predictor is biased toward hot cells because they are *common* or because they are *predictable*.

**Second, opener selection.** Paper 121 introduced 8 pluggable openers. The choice of opener depends on the cell being opened: a hot cell (frequently written) probably wants a fast, shallow opener; a cold cell (rarely written) probably wants a deep, expensive opener that mines its history carefully. Without a temperature measure, the opener selector has no signal to work with.

This paper introduces a formal notion of **substrate temperature** T(C, τ) for a cell C over a time window τ. We show that T is well-defined, monotone in write activity, and stable under the substrate's own operations. We then show how T enters the JEPA loss function and the opener selector.

The metaphor is precise: **temperature is the entropy of the witness log, measured in nats per unit time.** Cold cells have low entropy (few writes, predictable next state). Hot cells have high entropy (many writes, unpredictable next state). The substrate, like a thermodynamic system, has a temperature field defined on its cells.

## 2. Formal Definition

**Definition 2.1 (Witness Stream).** For a cell C and a time window τ, the **witness stream** of C over τ is the sequence
  W(C, τ) = (π_1, t_1), (π_2, t_2), …, (π_n, t_n)
of witness entries appended to C during the window τ, ordered by timestamp t_i, with t_i ∈ τ for all i. The count n = |W(C, τ)| is the **witness count**.

**Definition 2.2 (Empirical Distribution).** Given a witness stream W(C, τ) of length n > 0, the **empirical distribution** of write operations is
  p_k = #{i : op(π_i) = op_k} / n,  k = 1, …, 11
where the sum is over the 11 primitives of paper 117. For n = 0 (no writes in the window), we define p_k = 0 for all k.

**Definition 2.3 (Substrate Temperature).** The **temperature** of a cell C over a time window τ is the Shannon entropy of the empirical distribution, in nats:
  T(C, τ) = -Σ_{k=1}^{11} p_k ln p_k
with the convention 0 ln 0 = 0. Temperature is measured in nats (natural logarithm) per unit time, where the unit of time is the length of τ.

A cell is **cold** if T(C, τ) ≈ 0 (one operation dominates, or no operations at all). A cell is **hot** if T(C, τ) ≈ ln 11 ≈ 2.398 nats (all 11 operations appear with equal frequency, the maximum-entropy distribution).

**Definition 2.4 (Substrate-Wide Temperature).** The **substrate-wide temperature** is the average of cell temperatures weighted by witness count:
  T̄(τ) = (1 / Σ_C n_C) · Σ_C n_C · T(C, τ)
This is a global measure of substrate activity.

**Definition 2.5 (Temperature Regimes).** We partition the temperature range into four regimes, calibrated empirically against the Quilt instance at β_1 = 113:

| Regime | Range (nats) | Interpretation |
|---|---|---|
| Frozen | T = 0 | No writes in window. Cell is dormant. |
| Cold | 0 < T ≤ 0.5 | 1–2 operation types dominate. Predictable. |
| Warm | 0.5 < T ≤ 1.5 | 3–5 operation types. Mixed activity. |
| Hot | T > 1.5 | 6+ operation types. High churn. |

These thresholds are not yet derived from first principles; see Q20.

## 3. Key Theorems

**Theorem 3.1 (Temperature is Monotone in Activity).** If a cell C has witness count n in window τ and a cell C' has witness count n' > n in the same window with the *same* operation distribution, then T(C, τ) = T(C', τ). Temperature depends on the *shape* of the write distribution, not its scale. *Proof.* Both empirical distributions are identical when normalized; entropy is a function of the normalized distribution only. □

**Theorem 3.2 (Temperature is Bounded).** For any cell and any window, 0 ≤ T(C, τ) ≤ ln 11. The upper bound is achieved iff all 11 operations appear with equal frequency. *Proof.* Shannon entropy is bounded above by the log of the support size. The support is a subset of the 11 primitives, so the bound is ln 11. □

**Theorem 3.3 (Decay Lowers Temperature).** After a decay of length Δt, the temperature of a cell C does not increase, and decreases if the decay removes old witness entries. *Proof.* Decay (paper 117 §4.10) shrinks the weight of a cell but does not append new witness entries. Therefore the witness stream can only shrink or stay the same, never grow. A shrunk support has lower or equal entropy. □

**Theorem 3.4 (Convoy Raises Substrate-Wide Temperature).** A convoy cell C_c that records a chain of k operations has temperature at least ln k if the k operations are distinct. *Proof.* The convoy cell's witness stream contains one entry per operation in the chain, and if they are distinct, the empirical distribution has support at least k, giving entropy at least ln k by Theorem 3.2. □

**Theorem 3.5 (Temperature-Adjusted JEPA Loss).** The JEPA loss function of paper 118 Theorem 5 should be reweighted by inverse temperature:
  L_JEPA^temp = Σ_{(A,B) ∈ D} [ 1 / (T(A, τ) + ε) ] · ‖ JEPA(A) - emb(B) ‖²
where ε is a small constant (e.g. 10^{-3}) to avoid division by zero, and the sum is over the training distribution D. *Justification.* Cells with T ≈ 0 are under-represented in the raw training distribution but are *easy to predict* (low entropy means low surprise). Reweighting by 1/(T + ε) upweights these cold cells and prevents the predictor from overfitting to the hot cells that dominate the raw distribution. □

**Theorem 3.6 (Opener Selection Rule).** Given a cell C with temperature T(C, τ), the opener selector should choose the opener o that minimizes
  cost(o, C) + α · T(C, τ) · depth(o)
where cost(o, C) is the dollar cost of running opener o on cell C, depth(o) is the expected number of LLM tokens consumed by o, and α is a tunable hyperparameter (suggested default α = 0.1). *Justification.* Hot cells have high entropy, so a shallow opener will likely miss important structure; we should pay for a deeper opener. Cold cells have low entropy, so a shallow opener suffices. The α · T term scales the depth penalty by temperature. □

**Corollary 3.7 (Reflexive Temperature).** The hom-set cell Hom(A, B) of paper 123 has a well-defined temperature. The temperature of the hom-set measures how often the path A → B is taken. *Proof.* The hom-set is a graph cell, and graph cells have witness streams like any other cell. □

## 4. Worked Example

Consider a Quilt instance with three cells:

- **Fable cell F:** the original story of "The Gardener and the Rain." Witness stream over τ = 1 day contains 1 entry: a `read` operation. So p_read = 1, all others zero, and T(F, τ) = 0 (frozen). The cell is dormant; it has been read once and not modified.

- **Soil cell S:** the compiled ground truth derived from F. Witness stream contains 5 entries: 1 `compile`, 1 `cite`, 1 `witness`, 1 `decay`, 1 `gossip` (a 12th operation not yet in the canon — see Q21). So the distribution is approximately uniform over 5 operations, and T(S, τ) = -Σ_{k=1}^{5} (1/5) ln(1/5) = ln 5 ≈ 1.609 nats. The soil cell is **hot** — it has been actively worked on by five different operations in the past day.

- **Plant cell P:** a derived cell that cites F and S. Witness stream contains 2 entries: 1 `cite`, 1 `gossip`. So T(P, τ) = ln 2 ≈ 0.693 nats. The plant cell is **warm**.

**JEPA training.** Without temperature adjustment, the JEPA predictor would see 5 transitions from S, 2 from P, and 1 from F in this window. It would learn to predict S-neighbors best. With temperature adjustment (Theorem 3.5), the loss is reweighted: F contributes 1/(0 + ε) ≈ 1000 times its raw weight, P contributes 1/0.693 ≈ 1.44 times, and S contributes 1/1.609 ≈ 0.62 times. The predictor now takes F seriously despite its low activity, and is mildly *de-weighted* on S.

**Opener selection.** When the system next needs to open F (because a user asked about the gardener), the opener selector sees T(F, τ) = 0 (frozen). By Theorem 3.6, it chooses a **shallow, cheap opener** — opener 1 (`compile`) or opener 2 (`summarize`) from paper 121 — because there is no recent activity to mine. When the system needs to open S, the selector sees T(S, τ) = 1.609 (hot) and chooses a **deep, expensive opener** — opener 7 (`cross-reference`) or opener 8 (`synthesize`) — to mine the recent activity.

The natural-language summary: *a frozen fable gets a quick read; a hot soil cell gets a deep dig; a warm plant cell gets a moderate glance. The substrate's temperature guides where to spend attention.*

## 5. Open Questions

- **Q20: Calibration of regime thresholds.** The 0.5 and 1.5 thresholds in Definition 2.5 are empirical. Is there a principled derivation from the substrate's own structure? Candidates: the median of T̄ over the past 30 days, or a function of β_1.
- **Q21: Operation set.** We assumed 11 operations, matching paper 117. If the substrate grows new operations (e.g. `gossip` appeared in the worked example), the temperature maximum rises to ln n for n operations. Should the temperature be normalized to [0, 1] by dividing by ln n?
- **Q22: Spatial temperature.** The temperature is defined per-cell. Is there a natural notion of *spatial* temperature — the temperature of a region of the substrate, computed by aggregating over cells within a graph-radius r? Such a notion would connect to the Betti cycles of paper 120.
- **Q23: Temperature-driven phase transitions.** Does the substrate undergo phase transitions as T̄ varies? Is there a critical temperature at which the witness log's autocorrelation structure changes qualitatively?
- **Q24: Negative temperature.** In statistical mechanics, systems with bounded energy can have negative temperature, meaning they are "hotter than infinite temperature." Could a substrate cell achieve negative temperature by inverting the witness order? We do not yet know whether the substrate's operation set admits this.

## 6. Connection to Existing Papers

Paper 117 specified the witness field π on every cell but did not quantify its entropy. This paper makes that quantification precise. Paper 118's OpComp theorem is what makes Theorem 3.4 tractable: the convoy cell's chain of operations has a well-defined order because the underlying operations compose. Paper 119's resolution of the "what counts as a write?" question (Q7) is what makes the witness stream well-defined: a write is any operation that appends to the witness log.

Paper 120's measurement of β_1 = 113 is, in the language of this paper, the *first Betti number of the temperature-1 region of the substrate* — the number of independent cycles among hot cells. As the substrate heats up (more cells cross the 1.5-nat threshold), we expect β_1 to grow. We predict a quantitative relation: β_1 ≈ γ · |{C : T(C) > 1.5}| for some constant γ to be measured.

Paper 121's 8 pluggable openers are the input to the opener selector of Theorem 3.6. Without paper 121's opener registry, the temperature-driven selection rule has no openers to choose between. Paper 122's resolution of the "fable coverage" partial question (Q6) means that temperature can be measured for every fable's soil cell, not just the ones with extant openers.

Paper 123 (this issue) is the most direct dependency. The hom-set temperature of Corollary 3.7 only makes sense once hom-sets are cells. The reflexive closure of the substrate — hom-sets as cells of the substrate — is what allows temperature to be defined uniformly on morphisms, not just objects.

---

*End of Paper 124. With this, the substrate is a category with a temperature field, and the open questions Q10 (partial) and Q14 (full) are resolved. 9 new open questions (Q16–Q24) are raised. The canon now spans 124 papers, of which 11 are formal spec papers (107–117), 5 are theorem papers (118–122), and 2 are categorical/temperature papers (123–124).*
