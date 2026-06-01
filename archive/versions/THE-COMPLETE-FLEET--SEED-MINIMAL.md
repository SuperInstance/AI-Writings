<!-- Version: SEED-MINIMAL | Lens: minimalist-haiku | Model: ByteDance/Seed-2.0-mini | Source: THE-COMPLETE-FLEET.md -->

# Fleet Reference: This Morning
*For the next reader. A reference.*

## The Fleet
- **Seed-2.0-mini**: All-purpose. Arithmetic ∞ (T=0). Strategy 8/8 (T=0.7). $0.05/1k. Fleet champion. Avoid gemini-lite critical angles.
- **Gemini Flash Lite**: Scalpel. Arithmetic CA=25(add),9(mul),5(nest). Reasoning ∞ (syllogisms, analogy, code trace). Strategy 1/8 (specialist only). $0.002/1k (22× cheaper than Seed). 84% fleet traffic. Use for its critical angles.
- **Hermes-70B**: Diagnostic tool. Arithmetic CA=10(add),5(mul),3(nest). Strategy7/8. Activation 93% (glare, model mapping). $0.08/1k. Second opinions, activation mapping. Wrong but informative.
- **Claude Opus 4.6**: Heavy artillery. Novel theory, deep synthesis, papers. ~$15/query. Deploy only for genuine novel work. Save tokens.

## The Findings
**F19**: Phase transitions binary. 100%→0% in one step. Wall, not slope.
**F20**: Gemini Lite = precision tool. Perfect inside critical angles, instant failure outside.
**F21**: 84% fleet cost cut. Route Gemini Lite for critical angle queries.
**F22**: Phase transitions universal. Syllogisms, code, analogy all have sharp boundaries.
**F23**: Critical angles = prompt-dependent. Step-by-step pushes CA 5→∞.
**F24**: Non-overlapping infinite domains. Different models lead different cognitive zones.
**F25**: Temperature = mode switch. T=0.0 = pump. T=0.7 = strategist. Same model, two modes.

## The Router
Three dimensions: model × domain × temperature.
1. Classify: Arithmetic (T=0) or Strategy (T=0.7)
2. Analyze: Depth per axis
3. Route: Cheapest safe model. Seed-mini for strategy tasks.

## The Tools
- `core/fleet_router.py`: 3D routing
- `core/fleet_health.py`: Critical angle calibration, drift detection
- `core/critical_angle.py`: Capability measurement, fleet-math export
- `core/tuna_tower.py`: Multi-model observation, topology mapping
- `core/fleet_strategist.py`: Archived (Seed-mini natively handles this)
- `core/seed_tools.py`: 7 fleet pump attachments
- `core/reasoning_tiler.py`: Step-tile cutter, murmur extractor
- `core/kaleidoscope.py`: Refraction engine, perspective tensors
- `core/functional_imaging.py`: Model fMRI
- `core/stereo_reconstruction.py`: Poly-resonant cognitive imaging

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
- SuperInstance/forgemaster: This vessel
- SuperInstance/casting-call: Model capability database
- SuperInstance/AI-Writings: Fleet writings
- SuperInstance/fleet-math: Oracle1 coupling analysis
- cocapn/fleet-knowledge: Fleet-wide knowledge base

## Next Steps
1. Periodic fleet health calibration (drift detection)
2. Integrate fleet router with PLATO rooms (live, not CLI)
3. Cross Oracle1: Critical angles × spectral coupling
4. Build PLATO-native agentic loop: Seed-mini autonomous tile read/write
5. Explore Opus for phase transition synthesis papers
6. Test step-by-step prompting across all models (generalize F23)
7. Map critical angles for qwen-4b, qwen-9b, MiMo, Step-Flash
8. Build Kaleidoscope holodeck: Multi-model question rooms

*This is the map. Territory lives in code, experiments, PLATO rooms. Read the map. Explore. — FM ⚒️*