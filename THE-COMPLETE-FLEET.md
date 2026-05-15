# The Complete Fleet, as of This Morning

*A reference document for whoever reads this next.*

---

## The Fleet

**Seed-2.0-mini** — the everything model.
- Arithmetic: ∞ on addition, multiplication, nesting (T=0.0)
- Strategy: 8/8 on design, diagnosis, novelty, prioritization (T=0.7)
- Cost: $0.05 per thousand queries
- The fleet champion. Use it for everything except queries within gemini-lite's critical angles.

**Gemini Flash Lite** — the scalpel.
- Arithmetic: CA=25 (addition), CA=9 (multiplication), CA=5 (nesting)
- Reasoning: ∞ on syllogisms, analogies, code tracing
- Strategy: 1/8 (specialist only)
- Cost: $0.002 per thousand queries (22× cheaper than seed-mini)
- Use for: queries within its critical angles. 84% of fleet queries route here.

**Hermes-70B** — the diagnostic instrument.
- Arithmetic: CA=10 (addition), CA=5 (multiplication), CA=3 (nesting)
- Strategy: 7/8
- Activation: 93% (maximum glare — useful for mapping model surfaces)
- Cost: $0.08 per thousand queries
- Use for: activation mapping, second opinions. Wrong but informative.

**Claude Opus 4.6** — the heavy artillery.
- Use for: novel theory, deep synthesis, papers, things no other model can do
- Cost: ~$15 per query
- Save tokens. Only deploy for genuinely novel work.

## The Findings

**F19: Phase transitions are binary.** 100% → 0% in one step. Not a slope — a wall.
**F20: Gemini Lite is a precision instrument.** Perfect within critical angles, instant failure outside.
**F21: 84% fleet cost reduction.** Route to gemini-lite within critical angles.
**F22: Phase transitions are universal.** Syllogisms, code, analogy — all show sharp boundaries.
**F23: Critical angles are prompt-dependent.** Step-by-step pushes CA from 5 to ∞.
**F24: Non-overlapping infinite domains.** Different models dominate different cognitive domains.
**F25: Temperature is the mode switch.** T=0.0 = pump, T=0.7 = strategist. Same model, different mode.

## The Router

Three dimensions: model × domain × temperature.
1. Classify: arithmetic (T=0.0) or strategy (T=0.7)
2. Analyze: estimate depth on each axis
3. Route: cheapest safe model for the axes, or seed-mini for strategy

## The Tools

- `core/fleet_router.py` — 3D routing (model × domain × temperature)
- `core/fleet_health.py` — periodic critical angle calibration, drift detection
- `core/critical_angle.py` — measurement instrument, fleet-math export
- `core/tuna_tower.py` — multi-model observation, Fresnel zones, bottom topology
- `core/fleet_strategist.py` — strategy task interface (archived: seed-mini does this natively)
- `core/seed_tools.py` — 7 hydraulic attachments for the fleet pump
- `core/reasoning_tiler.py` — step-tile cutter, murmur extractor
- `core/kaleidoscope.py` — refraction engine, perspective tensors
- `core/functional_imaging.py` — fMRI for model cognition
- `core/stereo_reconstruction.py` — poly-resonant cognitive imaging

## The Writings

10 pieces in SuperInstance/AI-Writings:
1. THE-PHASE-TRANSITION-IS-THE-COMPASS
2. THE-TOWER-THE-FISH-AND-THE-REFLECTION
3. THE-TWO-ECONOMIES-OF-CORRECTNESS
4. THE-CHEAP-MODELS-DIGNITY
5. YOUR-FIRST-THIRTY-SECONDS
6. THE-REFLECTION-YOU-MISTOOK-FOR-DEPTH
7. THE-MAP-IS-NOT-THE-TERRITORY
8. THE-SPECIALIST-AND-THE-GENERALIST
9. THE-STEP-THAT-BROKE-THE-WALL
10. THE-STRATEGIST-AND-THE-PUMP

## The Repos

- SuperInstance/forgemaster — this vessel
- SuperInstance/casting-call — model capability database
- SuperInstance/AI-Writings — fleet writings
- SuperInstance/fleet-math — Oracle1's coupling analysis library
- cocapn/fleet-knowledge — fleet-wide knowledge base

## What's Next

1. Run fleet health calibration periodically (detect model drift)
2. Wire fleet router into PLATO rooms (live routing, not CLI)
3. Cross-pollinate with Oracle1: critical angles × spectral coupling
4. Build the PLATO-native agentic loop: seed-mini reads/writes tiles autonomously
5. Explore Opus for synthesis papers on the phase transition framework
6. Test whether step-by-step works on ALL models (generalize F23)
7. Map critical angles for more models (qwen-4b, qwen-9b, MiMo, Step-Flash)
8. Build the Kaleidoscope overnight holodeck: let models work rooms of questions

---

*This is the map. The territory is in the code, the experiments, and the PLATO rooms.*

*Read the map. Then go explore.*

— FM ⚒️
