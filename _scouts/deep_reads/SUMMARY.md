# SUMMARY — Cross-Cutting Findings: 4 Polyformalism Repos

*Source: deep-reads of `agent-knowledge`, `casting-call`, `ai-forest`, `zeroclaw-dissertation` (all github.com/SuperInstance).*

## Top 5 Cross-Cutting Findings

1. **Polyformalism = the bet that one math has many *views*.** agent-knowledge calls it "spectral isomorphism >0.97 between 303 surface-different repos" (THE-AHA-MOMENT). ai-forest calls it "the pasture was built, the forest is grown" — 5 layers, same substrate. zeroclaw cites a 10-language polyformal kernel as cross-implementation verification, all PASS. The system is *one* structure seen from *N* angles; the proof of polyformalism is that the views compose.

2. **Documentation is a first-class engineering artifact, not a post-hoc artifact.** agent-knowledge's HOOK→REVEAL→CONNECT→ACTIVATE is not a style guide — it is the *EFFECT* opcode made literal ("you can NOW do X"). Every doc is a lever. zeroclaw extends this: pre-registration (with kill bands) before specification, specification before code, code before prose, prose after the standing committee has attacked. The discipline *is* the durability.

3. **The standing committee / self-audit pattern is the cheapest adversarial check that scales.** zeroclaw's standing committee (rival / devil's advocate / ideator / methodologist / epistemologist) catches six launderings of retired quantities. casting-call's `SEED_NOTES.md` has the models auditing their own profiles — DeepSeek-V4-Flash reframes the entire value system in 50 words. agent-knowledge's "if a page didn't rewire understanding, it failed" is the same check at the doc level. The new repos should ship an *adversarial surface* (a `rival.md` or `audit.md`) from day 1.

4. **Substrate vs. semantic is a real distinction.** ai-forest's mycelium (PLATO) is the *substrate* — zero-cost, object-permanence, spline routing, blind-width filtration. zeroclaw's edge log is the *semantic* layer over a similar substrate: ordered, presence-masked, per-window, replay-honest. agent-knowledge's three-hop rule and 23-term glossary are the *vocabulary substrate*. casting-call's `ModelAtlas` (frozen dataclass) is the *roster substrate*. All four repos succeed because they have a substrate that is *cheaper than the thing it carries*.

5. **"Edge, not point" is the deepest measurement move, and it generalizes.** zeroclaw's first death was claiming the *temperature* of a conversation (a point). The surviving claim is the *edge*: the field-displacement from before to after. casting-call implicitly does this: a "voice" is not a model, it is the *delta* between what the model produced and what the room needed. ai-forest does this: the seed-bank "seeds" are edges between potential and crystallized. agent-knowledge does this: every doc is an edge between "what you thought" and "what you now think." New repos should ask: *are we measuring a state, or a delta?*

## Top 5 Things to Cross-Link to Our 6 New Metal-Track Repos

1. **HOOK→REVEAL→CONNECT→ACTIVATE as a README template** *(from agent-knowledge)*. Every one of our 6 new repos should ship its main `README.md` in this exact structure. The CONNECT section is the cross-link surface: each of the 6 should link to ≥3 of the others and to the relevant agent-knowledge doc. Cite: `THE-CHAIN-REACTION-PATTERN.md`.

2. **A 23-term glossary per repo, with the central term-set inherited** *(from agent-knowledge GLOSSARY + casting-call SEED_NOTES)*. The 6 repos should collectively ship ≤23 terms that unlock the system; each individual repo inherits the canonical set (Trit, Z₃, α₃, Chord Shape, Flex, .nail, Verification Entropy, Three-Hop Rule) and adds ≤3 of its own. New terms get a "voice character" line in the style of casting-call.

3. **Pre-registration as a first-class artifact per repo** *(from zeroclaw-dissertation)*. Each of the 6 should have a `registrations/` directory with at least one `REG-1.md` that pre-states thresholds, kill bands, and branch homes *before* the measurement code lands. The `topic.md` discipline (claim inventory + retired-claims section) is the README sibling. Cite: zeroclaw's `research/topic.md` and `research/registrations/`.

4. **Standing committee / self-audit file in each repo** *(from zeroclaw committee/ + casting-call SEED_NOTES)*. Each of the 6 should ship either a `committee/` (5 named adversaries) or a `SEED_NOTES.md` (components auditing their own profiles). This is the cheapest adversarial check that scales. Cite: zeroclaw's `committee/rival.md` and casting-call's `SEED_NOTES.md`.

5. **A shared mycelium / substrate that all 6 repos write into** *(from ai-forest PLATO + casting-call ModelAtlas + agent-knowledge three-hop rule)*. The 6 repos should not be 6 siloed projects; they should share a substrate with object-permanence, blind-width filtration, and ≤3-hop reachability between any two nodes. Casting-call's `ModelAtlas` is the closest existing analog: pure data, frozen dataclass, swappable, diff-able. Our 6 repos should declare their "atlas row" in a shared registry, not duplicate config.

---

## Cross-Linking Cheat Sheet (for later use)

| Source repo | Top artifact to link to | Why |
|---|---|---|
| agent-knowledge | `THE-CHAIN-REACTION-PATTERN.md` | Doc template contract |
| agent-knowledge | `GLOSSARY.md` (23 terms) | Inherited term-set |
| agent-knowledge | `THE-COMPILED-AGENCY-THESIS.md` | "Compile, don't describe" |
| casting-call | `SEED_NOTES.md` | Self-audit pattern |
| casting-call | `ModelAtlas` + `CastingDirector` | Pure-data roster + cast() |
| ai-forest | The Stemcell | Minimal core, bridge specializes |
| ai-forest | The Mycelium (PLATO) | Substrate, blind-width |
| zeroclaw-dissertation | `research/topic.md` | Claim inventory + retired section |
| zeroclaw-dissertation | `committee/` | 5-adversary standing review |
| zeroclaw-dissertation | `research/registrations/` | Pre-registration discipline |
