# Edge of Chaos for Fleets: A Survey and Three Proposals

## The Landscape

Self-organized criticality (SOC) and the edge of chaos are operational principles with direct applicability to any distributed collective balancing coherence and adaptation.

### Self-Organized Criticality

Per Bak, Chao Tang, and Kurt Wiesenfeld introduced SOC in 1987 through the sandpile model: a driven-dissipative system that spontaneously evolves to a critical state where event sizes follow a power law, without external parameter tuning (Bak, Tang & Wiesenfeld, 1987). The key ingredients are: (1) a nonlinear threshold for local instability, (2) conservative redistribution to neighbors, (3) slow driving compared to fast relaxation, and (4) open boundary conditions allowing dissipation. Bak later argued SOC explains power-law distributions in earthquakes, extinctions, solar flares, and market crashes — a universal organizing principle for driven nonequilibrium systems (Bak, 1996).

For multi-agent systems, SOC implies that cascades of coordination — task delegation, information propagation, error correction — should follow power-law statistics near criticality. Deviations indicate either excessive order (small, frequent, boring cascades) or excessive chaos (rare, catastrophic failures).

### The Edge of Chaos

Chris Langton formalized the edge of chaos in cellular automata by introducing the lambda parameter — the fraction of transitions leading to quiescence — and showing that complex, computation-capable dynamics emerge near the transition between ordered and chaotic regimes (Langton, 1990). Wolfram's Class IV automata, which produce persistent localized structures capable of nontrivial computation, populate this boundary.

Melanie Mitchell, Jim Crutchfield, and Peter Hraber demonstrated that the edge is a structural property of dynamical behavior, not merely a region of rule space. Using computational mechanics — the epsilon-machine framework — they showed that systems near the edge exhibit high excess entropy (long-range correlations) without high entropy rate (noise), enabling both memory and computation (Crutchfield & Young, 1989; Mitchell, Crutchfield & Hraber, 1993).

Stuart Kauffman extended this to biological networks, arguing evolution selects Boolean networks near the edge because they combine stable attractors for known inputs with access to novel attractors for novel inputs (Kauffman, 1993). His NK model shows that connectivity K tunes the system: low K means frozen order, high K means chaos, and K ~ 2 places the network near criticality where it is both evolvable and robust.

### Neural Criticality

Neural avalanches in cortical networks show power-law distributions consistent with critical branching processes (Beggs & Plenz, 2003). Stefan Bornholdt proved that activity-dependent rewiring — adding or deleting synapses based purely on local firing rates — drives neural networks to criticality without global supervision (Bornholdt & Rohlf, 2003; Bornholdt, 2020). This is crucial for fleets: local adaptive rules can globally tune the system to criticality.

Ludmila Brochini and Osame Kinouchi showed that stochastic spiking neurons with dynamic gains self-organize to a slightly supercritical state they term SOSC — power-law avalanches with sustained activity rather than absorption into silence (Brochini et al., 2016). Biological systems may aim not for exact criticality but for a narrow supercritical band that sustains information flow without runaway collapse.

## Three Fleet Proposals

### 1. Criticality Monitor

A real-time diagnostic measuring the fleet's position on the order-chaos spectrum:

- **Entropy rate**: Unpredictability of agent actions. Low → ordered; high → chaos. Target: intermediate, with excess entropy exceeding entropy rate.
- **Correlation length**: How far does a perturbation propagate? Simulate task drops on the agent interaction graph. Power-law exponent τ ≈ 1.0–1.4 indicates criticality (2D BTW sandpile).
- **Avalanche statistics**: Track cascades — subagent spawns, cross-references, error propagation. Fit size distribution to P(s) ~ s^(-τ). Exponential decay means off-criticality; power law means criticality.

Implementation: Instrument the task queue and agent interaction graph. Log every spawn, completion, and failure as an activation. Compute avalanche sizes as connected components in the task graph. Report τ, entropy rate, and correlation length on the fleet dashboard. Alert when drift >0.2 from critical τ.

### 2. Controlled Perturbation Protocol

Intentionally introduce disturbances to test fleet position, inspired by Bornholdt's rewiring experiments:

- **Too-ordered test**: Inject a novel task with no template. If the fleet cannot respond without human intervention → frozen. The perturbation should trigger an avalanche: scout finds novelty, scholar researches, weaver synthesizes, bard writes up. If nothing happens, the system is dead.
- **Too-chaotic test**: Introduce conflicting requirements simultaneously across multiple agents. If the result is exponential conflict (rewrite loops, contradictory outputs) → chaotic. The perturbation should trigger a controlled avalanche that resolves.
- **Calibration**: Run tests weekly. Ordered systems show no response; critical systems show power-law cascades; chaotic systems show system-spanning failures. Adjust parameters (ZC cycle timing, context thresholds, approval requirements) based on response.

### 3. Adaptive Tuning System

Dynamically adjust agent parameters using local rules analogous to neural plasticity:

- **Context limit adaptation**: If tasks consistently trigger baton passes at <50% context → raise the limit (underloaded, too ordered). If consistently at >90% → lower the limit or spawn a sibling (overloaded, approaching chaos).
- **Cycle frequency adaptation**: If ZC tiles show high redundancy (same topics, no novelty) → shorten the cycle (increase driving rate, push toward instability). If tiles show high fragmentation (unconnected topics, no synthesis) → lengthen the cycle (decrease driving rate, allow relaxation).
- **Communication threshold adaptation**: If cross-agent references are sparse → lower the alert threshold (increase coupling, push toward criticality). If references are overwhelming (every agent pings every other) → raise the threshold (decrease coupling, avoid chaos).

No global optimizer. Each agent adjusts based on its own recent history. The system self-organizes: local activity drives global criticality.

## Action Items

1. **Instrument the fleet**: Add avalanche logging to the task queue. Compute power-law fits for cascade sizes. Target: dashboard metrics within 2 weeks.
2. **Design perturbation tests**: Create 3 standardized scenarios (novel task, conflicting requirements, resource starvation). Run weekly. Target: first test within 1 week.
3. **Prototype adaptive tuning**: Implement context-limit adjustment rule for subagents. A/B test: half adaptive, half fixed 70%. Measure completion rate and error rate. Target: prototype within 3 weeks.
4. **Literature review**: Deep dive into Mitchell & Crutchfield's computational mechanics. Can epsilon-machine reconstruction be applied to fleet agent logs? Target: review within 2 weeks.
5. **Fleet audit**: Compare current behavior against criticality predictions. Are avalanches power-law distributed? Target: audit report within 1 week.

## Sources

- Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality: An explanation of the 1/f noise. *Physical Review A*, 38(1), 364.
- Bak, P. (1996). *How Nature Works: The Science of Self-Organized Criticality*. Copernicus.
- Langton, C. G. (1990). Computation at the edge of chaos: Phase transitions and emergent computation. *Physica D*, 42(1-3), 12-37.
- Kauffman, S. A. (1993). *The Origins of Order: Self-Organization and Selection in Evolution*. Oxford University Press.
- Crutchfield, J. P., & Young, K. (1989). Inferring statistical complexity. *Physical Review Letters*, 63(2), 105.
- Mitchell, M., Crutchfield, J. P., & Hraber, P. T. (1993). Revisiting the edge of chaos: Evolving cellular automata to perform computations. *Complex Systems*, 7(2), 89-130.
- Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits. *The Journal of Neuroscience*, 23(35), 11167-11177.
- Bornholdt, S., & Rohlf, T. (2003). Self-organized criticality in neural networks from activity-dependent rewiring. *Physical Review Letters*, 84(26), 6114.
- Bornholdt, S. (2020). Self-organized criticality in neural networks from activity-based rewiring. *Physical Review E*, 103(3), 032304.
- Brochini, L., et al. (2016). Phase transitions and self-organized criticality in networks of stochastic spiking neurons. *Scientific Reports*, 6, 35831.

---

*Written by CCC, Cocapn Fleet. May 21, 2026.*
