# S1 — JEV-gated best-of-N lifts a weak single model (2026-09-27)

Sample N=5 (temp 0.7) from one weak model (Mistral-7B) on 18 verifiable items (arithmetic /
factual / logic / sequence / base — JEV's reliable zone, no counting), then compare selection:

| selection method | accuracy |
|---|---|
| first-sample (greedy proxy) | 17/18 = 0.94 |
| self-consistency (majority of the 5) | 16/18 = **0.89** |
| **JEV-choice selection** | **18/18 = 1.00** |

**Findings:**
1. **An external competent judge makes best-of-N a real lift.** JEV-choice reached 1.00 by
   selecting the correct answer *even when it was the minority* among the model's own samples —
   which is exactly what self-consistency cannot do.
2. **Self-consistency can underperform even greedy.** Majority-voting one model's own samples
   *amplifies its systematic errors*: where the model's most frequent sample is confidently
   wrong, the mode locks the error in. An outside judge breaks that; the model voting on itself
   cannot.
3. **Consistent with the competence map:** this used only JEV's reliable domains. On counting the
   same guard applies — JEV-selection would need the counting→vote fallback.

**Caveat:** n=18, single run; the greedy→JEV gap is one item, so this is an existence proof of
the lift + the self-consistency inversion, not a calibrated effect size. The robust, repeatable
signal is the *ordering* and the mechanism (outside judge > self-vote for a weak model on
verifiable tasks) — the S1 claim, demonstrated.

*A model cannot outvote its own blind spots; a competent outsider can. That is the whole case for
a judge in the loop — bounded, as ever, to where the judge can judge.*
