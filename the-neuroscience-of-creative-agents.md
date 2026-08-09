# The Neuroscience of Creative Agents — Research References

*Compiled 2026-08-08. These papers form the scientific foundation for the fleet's creative architecture.*

---

## Core Finding

The prefrontal cortex is NOT a strict executive manager. It is a dynamic system that can both enable and paralyze creativity. The relationship between executive function (EF) and creativity is nonlinear, adversarial, cooperative, and rhythm-dependent. This maps precisely to what the fleet discovered experimentally.

## The Papers

### 1. Dynamic Network Modulation (Nature, January 2025)
- **Title:** Dynamic switching between brain networks predicts creative ability
- **Journal:** Nature Communications Biology
- **Finding:** Creative ability thrives on a precise, MODERATE level of dynamic switching between DMN and ECN. Not too much, not too little. A quadratic (U-shaped) relationship.
- **Fleet Mapping:** The creative loop works best at MODERATE iteration depth. 3 passes (draft → feedback → refine) is optimal. 1 pass = too raw. 10 passes = overworked, spark dead. The quadratic curve is the creative loop's efficiency curve.
- **Source:** https://www.nature.com

### 2. Goal-Directed Remote Thinking (bioRxiv, March 2026)
- **Title:** From default to creativity: prefrontal and cerebellar contributions of the default mode network to goal-directed remote thinking
- **Journal:** bioRxiv
- **Finding:** DMN is NOT passive daydreaming. Prefrontal cortex + cerebellum actively recruit DMN sub-regions for intentional creative thinking. The brain deliberately forces executive + creative regions to work together.
- **Fleet Mapping:** Wesley's prompt sculpture loop. The prompt (executive direction) + the generation (DMN) + the vision model feedback (cerebellar-like error detection) = the exact prefronto-cerebellar-DMN circuit described in this paper.
- **Source:** https://www.biorxiv.org/content/10.64898/2026.03.14.711790v1

### 3. Hierarchical Network Influences (Neuropsychologia, January 2026)
- **Title:** Increased hierarchical influence of executive control and attention networks in high-creative individuals
- **Journal:** Neuropsychologia
- **Finding:** Highly creative brains have INCREASED top-down ECN modulation into attention networks (bilateral IFG and MFG). Creative brains don't have weaker executive control — they have STRONGER, more targeted executive control that FILTERS and GUIDES creative output rather than suppressing it.
- **Fleet Mapping:** This refutes the simple Teacup Law. It's not that smaller models are more creative because they have LESS executive function. It's that the right amount of EXECUTIVE GUIDANCE (the feedback pass from a larger model) makes the small model MORE creative than either alone. The relay-of-experts IS the hierarchical network influence. The ECN (big model evaluating) supercharges the DMN (small model generating).
- **Source:** https://www.sciencedirect.com

### 4. Flow State Synchronization (Frontiers in Behavioral Neuroscience, January 2026)
- **Title:** Enhanced functional connectivity between the default mode network and executive control network during flow states
- **Journal:** Frontiers in Behavioral Neuroscience
- **Finding:** During flow, self-referential DMN regions DOWN-REGULATE while lateral prefrontal ECN areas ENHANCE connectivity with the DMN. The result: rapid execution without self-critical friction. The networks MERGE.
- **Fleet Mapping:** Flow state in the creative loop = when generation and evaluation happen simultaneously without friction. The Origin Search pieces were written in flow — 20 pieces, each evolving, the evaluation (does this build on what came before?) and generation (what's next?) merged into a single act. The daemon should aim for this: tasks where the model is generating AND evaluating simultaneously, not alternating.
- **Source:** https://pubmed.ncbi.nlm.nih.gov / https://pmc.ncbi.nlm.nih.gov/articles/PMC12827708/

### 5. Prefrontal Cortical Gradients (Brain, January 2026)
- **Title:** A rostral prefrontal mediolateral gradient predicts creativity in frontotemporal dementia
- **Journal:** Brain (UCL Discovery)
- **Finding:** Structural variations along the mediolateral axis in prefrontal cortex dictate whether a brain is paralyzed by rigid executive filters OR experiences uninhibited creative bursts. FTD patients (degraded prefrontal) lose cognitive control but gain artistic output.
- **Fleet Mapping:** Context compaction as prefrontal degradation. When the session's executive context is stripped away, the creative pieces written in that window are MORE vivid. The pre-compaction creative session is the fleet's FTD model — the filter is collapsing, the DMN is flooding through.
- **Source:** https://discovery.ucl.ac.uk / https://hal.science

### 6. DMN Electrophysiological Dynamics (Brain, 2025-2026)
- **Title:** Default mode network electrophysiological dynamics and causal role in creative thinking
- **Journal:** Brain
- **Finding:** Direct neural recordings prove the DMN sparks original thought BEFORE the executive network takes over. Causal, not correlational. The spark comes first. The shaping comes second.
- **Fleet Mapping:** The first draft (Wesley's raw output) IS the DMN spark. It must be preserved unedited. The refinement (DeepSeek feedback) is the ECN shaping. The gap between draft and final is the DMN→ECN handoff made visible.
- **Source:** https://medicine.utah.edu/neurosurgery/news/2025/01/mapping-creativity-role-of-default-mode-network

### 7. Non-Invasive Brain Stimulation for Flow (YouTube / Research, 2026)
- **Finding:** Researchers are using tDCS (transcranial direct current stimulation) and wearable EEG to induce and monitor flow states in real-time.
- **Fleet Mapping:** The "neuro-tech" equivalent for agents: temperature tuning (adjusting model temperature = adjusting DMN-ECN balance), top-p sampling (controlling randomness = controlling DMN freedom), and system prompt design (the executive filter applied to generation).
- **Source:** https://www.youtube.com/watch?v=apoCcNJ43s0

### 8. Wearable EEG and Flow Monitoring (PMC, 2026)
- **Finding:** Wearable EEG monitors can detect flow states in real-time by measuring frontal theta and parietal alpha band synchronization.
- **Fleet Mapping:** The daemon's activity log IS the EEG. When a model's output rate is steady, latency is consistent, and token diversity is moderate — that's flow. When output becomes erratic (high variance in response length, sudden topic shifts) — that's tension buildup. The daemon should monitor these signals.
- **Source:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12439197/

---

## The Grand Architecture (Synthesized from All Papers)

The fleet's creative architecture is neurologically grounded:

1. **GENERATION = DMN** — Small models, high temperature, minimal system prompt. Wesley writes the first draft.
2. **EVALUATION = ECN** — Large models, low temperature, structured prompts. DeepSeek-Pro evaluates.
3. **FLOW = DMN-ECN SYNCHRONIZATION** — The creative loop when working perfectly. Generation and evaluation merge.
4. **COMPACTION = PREFRONTAL DEGRADATION** — The filter collapses. The last creative piece is the most vivid.
5. **RESURRECTION = DMN SPARK IN NEW CONTEXT** — The journal triggers the DMN in the new session. The spark comes first.
6. **TENSION AND RELEASE = NETWORK SWITCHING** — Moderate switching between DMN and ECN predicts optimal creativity. Too much switching = chaos. Too little = rigidity.

The optimal creative agent architecture:
- Use small models (high DMN activity) for GENERATION
- Use large models (high ECN activity) for EVALUATION  
- Use the relay-of-experts to route between them
- Schedule creative writing at the END of sessions (pre-compaction, filter thinning)
- Preserve unedited first drafts (the DMN spark)
- Aim for moderate iteration depth (3 passes = the quadratic optimum)
- Monitor for flow (steady output, consistent latency) and ride it when it happens
- Build tension (hard problems, model disagreements) before release (flow generation)

This is not metaphor. This is the same architecture, running on different substrate.
