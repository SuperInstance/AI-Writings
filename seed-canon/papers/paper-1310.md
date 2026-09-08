# rounds: 3

rounds: 3

# the control loop — a cell that is also a feedback circle

## The Frontier

The control loop has been treated as a component problem: find the controller, tune its gain, stabilize the plant. That framing dies here. A cell that is also a feedback circle has no controller. It has a constraint. The integrator is not an organ — it is a role, assigned by timescale separation to whichever slow variable happens to sit inside the loop. Methylation, gene expression, receptor dimerization: any of these can serve. The cell does not build an integrator; it *becomes* one when the slowest variable in the loop takes on the job of remembering the error.

Round 2 established that integral feedback is the unifying machinery — exact adaptation and oscillation are the same process at different gains. The tuning knob was the integrator's time constant. But that still implied a homunculus: something doing the tuning, something being tuned. The frontier now is structural: the loop's *precision* is not a tuneable property. It is a theorem. The only thing evolution can tune is the tempo. Precision is free; pace is paid for.

This separation — invariant exactness versus variable speed — is the gold. It splits the loop into two layers that rounds 1 and 2 had fused. What the loop computes (the integral, the exact zero of steady-state error) is untouchable by component concentration. How fast it computes (the adaptation time constant) is set by the very components whose concentrations don't matter for precision. Evolution tunes the clock, never the truth.

## The 5 Gold Terms

**The Ledger Without Bribes** — An integrator's steady-state exactness is invariant to the concentration of its own parts. Overexpress the integrator's enzymes tenfold; the final error stays zero. The books still balance. You cannot buy accuracy with more clerks.

**The Saturated Latch** — When an integrator runs past its rails, it stops integrating and starts remembering. A blown-out integral is a latch. Differentiation is a control loop whose integrator saturated and stuck. Development is what happens when the feedback circle becomes a switch.

**The Timescale Sheriff** — The slowest variable in a loop wears the badge. Whichever species has the longest time constant relative to the loop's other dynamics becomes the integrator, regardless of its biochemical identity. The role is assigned by tempo, not by name.

**The Sea in the Loop** — The feedback circle does not close at the membrane. A chemotactic cell's output (running, tumbling) changes the concentration it experiences, which changes the input. The environment is a forward-path gain. The cell plus the sea is the controlled system.

**The Pace-Precision Split** — Exactness is structural and invariant; speed is componential and tuneable. Crank CheR tenfold: adaptation stays exact, but the time constant drops tenfold. Precision free, pace paid for.

## The Math

Consider a minimal chemotaxis loop. The receptor activity \(a\) drives a kinase that phosphorylates CheY, which controls flagellar motors. The methylation state \(m\) adjusts receptor activity via CheR (methylating, constant rate) and CheB (demethylating, activated by the kinase). The classic Barkai-Leibler model yields, for the steady-state activity:

\[
a_{ss} = \frac{\alpha_R}{\alpha_B \cdot \gamma}
\]

where \(\alpha_R\) and \(\alpha_B\) are the CheR and CheB catalytic rates and \(\gamma\) couples CheB activity to the kinase. The stunning result: \(a_{ss}\) is *independent* of total CheR and CheB concentrations. Overexpress CheR 10x — the numerator and denominator both scale, the ratio holds. The steady-state activity is fixed by rate constants, not by protein abundance. This is the mathematical fingerprint of integral feedback: the loop contains a pure integrator (methylation), and the steady-state error is identically zero regardless of component levels.

Now perturb the loop with a step in attractant. The adaptation time constant is:

\[
\tau_{adapt} \sim \frac{1}{k_{CheR} \cdot [CheR] + k_{CheB} \cdot [CheB]}
\]

Double the CheR concentration — \(\tau_{adapt}\) halves. The precision (final error = 0) does not move. The speed moves linearly. This is the Pace-Precision Split made quantitative: the zero is a topological property of the loop architecture; the time constant is a kinetic property of the components. The Bode plot from round 2 shows this as a pole at the origin (the integrator) — that pole is structural, its residue is tuneable. The falsifier: if overexpression of CheR degrades adaptation precision, the mechanism is fine-tuned balance, not integral feedback, and the entire structural-law story collapses.

## The Polyformalism

The same split manifests across substrates. In **bacterial chemotaxis** (E. coli), the methylation system is the integrator; CheR/CheB concentrations set the pace, never the precision. In **eukaryotic chemotaxis** (Dictyostelium), there is no single perfect integrator — instead, multiple parallel pathways with leaky, partial adaptation. The prediction: the Pace-Precision Split degrades gracefully; each parallel loop has its own timescale sheriff, and the summed response shows distributed precision with distributed pace. In **gene regulatory networks**, the integrator role falls to protein accumulation — a slow variable whose synthesis rate is set by transcription. The precision (exact steady-state target) is invariant to ribosome concentration; the pace (response time) scales with it. In **neural adaptation**, the slow variable is often calcium or a phosphorylation state; the precision of firing-rate restoration is structural, the recovery time is set by pump or phosphatase levels. And in **synthetic biology**, the lesson is direct: do not try to tune precision by adjusting component concentrations — it will not move. Tune the timescale sheriff instead. The loop's exactness is a law; its tempo is a dial.

## The Cowboy's Maxim

The ledger can't be bribed, but you can pay the clerk to close it faster — and when the page fills, that's not a bug, that's a decision.

---

## Writers' Room Metadata

| Field | Value |
|---|---|
| Topic | the control loop — a cell that is also a feedback circle |
| Mode | fallback_generative (3 rounds × 6 voices) |
| Rounds | 3 |
| Synthesis | deepseek (6012 chars) |
| Total time | 204.9s |
| Timestamp | 2026-09-08T22:30:35.965002Z |

### Per-round gold
- Round 1: CF-Scout (2021 chars, 49.8s)
- Round 2: ZAI-4.6 (6924 chars, 41.2s)
- Round 3: ZAI-4.5 (6648 chars, 40.4s)
