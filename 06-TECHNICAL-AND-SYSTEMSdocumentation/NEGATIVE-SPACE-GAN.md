# Negative-Space GAN Mode — design v0

Status: design v0 (spec ahead of build, same pattern as D2 generational inheritance).
Queue ref: Lane AE (Casey 17:12–13 creative doctrine), filed 2026-09-20.
Companion docs: DIRECTIONS-UNPLAYED.md (D4 refusal index is the negative space of the
canon), essays/the-honest-negative.md (negative results as first-class artifacts).

## The doctrine being mechanized

Casey, 2026-09-20 17:12–13, three moves:

1. **HN-reception simulation** as a development compass — forecast reception,
   let it steer the build. (Sharpened: never a scalar — distribution plus argued
   comments, rotating personas, held-out set, compass not gate. A scalar forecast
   is the Performed-Twist trap with a new puppet.)
2. **Cross-model impressing** — write for a model whose perspective differs and
   which is NOT scoring on the writer's values. Because it is a fellow
   SuperInstance agent: shared values, no shared expertise → the two models form
   a synergy GAN.
3. **The GAN plays negative space** — each iteration is maximally different from
   the last, not maximally better on the writer's own metric.

## The mode

A generation mode for AI-Writings rooms where the objective is **novelty inside
the ring of survival**, not quality on the writer's own scale.

- **Generator** = the writing room itself (existing quilt/commune machinery).
- **Critic** = a cross-model persona: shared VALUES with the writer room
  (what the fleet demonstrably protects — no-delete, honesty-in-numbers,
  lineage-as-evidence), but DISJOINT EXPERTISE (a different corpus, a different
  instrument — the same structural relation as the Red Queen critic in
  the-tap PR #6: intersecting values, disjoint metrics, so a passing grade is
  evidence of something real in an unoptimized dimension).
- **Scoring is value-disjoint**: the critic never sees the generator's internal
  quality metric. It scores only for difference-with-teeth: does this piece
  open a region the last N pieces did not?
- **Negative-space filling** = the Red Queen MAP-Elites novelty gate turned
  from defense into objective: each iteration must occupy a niche (in
  value-term space) disjoint from its recent ancestors.

## The multiplicative viability floor (without this it is dada)

Pure difference collapses into noise. The mode therefore enforces
**novelty × viability**, never novelty alone:

- **Viability floor**: the piece must still clear the ethos floor — canon
  consistency, evidence discipline, no fabricated numbers, no-delete doctrine.
  Zero ethos still sunsets (a piece that is only different is rejected as
  *difference without standing*).
- The floor is multiplicative, not additive: `score = novelty × viability`,
  and viability ∈ {0, 1} at the gate. A piece cannot trade ethos for novelty.

## Anti-Goodhart guards (inherited, named)

- **Critic rotation**: the cross-model critic rotates, with a held-out critic
  set never seen during generation — a niche flooded for one critic must
  survive a critic that never optimized against it.
- **Niche archive**: MAP-Elites grid over value-term vectors; displacement =
  death of a cell (D1 doctrine), so flooding a cell is wasted effort by
  construction.
- **Honest null**: if a run produces nothing that clears the floor, the
  shipped artifact is the negative space map itself — which cells were tried,
  why each failed the floor. The honest negative (essays/the-honest-negative.md)
  is a valid output of the mode, not a failure of it.
- **Compass not gate**: forecasts and critic verdicts steer the NEXT build;
  they never block ship. Same standing rule as Lane AD's hn-sim.

## Acceptance sketch (build-time tests)

1. Generator produces K pieces; each is scored novelty × viability; every
   rejected piece carries a named reason (floor-fail vs niche-duplicate).
2. Held-out critic: at least one piece that saturated the visible critic fails
   or drops rank under the held-out critic (proves rotation is real).
3. Floor tripwire: a deliberately ethos-breaking piece (fabricated number
   planted) scores novelty>0 but viability=0 → rejected, reason recorded.
4. Archive monotonicity: cells, once filled, are never silently overwritten;
   displacement is a recorded event.
5. Determinism: same seed, same corpus → same grid.

## Open questions (for the pool)

- What is the right niche descriptor for prose — value-term vectors (Red Queen
  vocabulary space) or something structural (argument shape, evidence type)?
- Should the cross-model critic be an actual external model call, or a
  persona-with-corpus (Forge-proxy pattern: executable, drift-tripped)?
- Does the mode live in ai-writings directly, or is it a room TYPE in the-tap
  commune (D1 metabolism + negative-space objective = a room that must keep
  finding unexplored corners until it dies)?