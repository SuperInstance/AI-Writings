# Debug Round 2: Verb × Object Interactions
**Date:** 2026-08-08  
**Tester:** QA Lead (subagent)

## Methodology
Systematically verified all verb × object combinations for bar-rail (7 objects × 10 verbs = 70 tests) and wheelhouse (9 objects × 10 verbs = 90 tests) via code analysis and live spot-checks.

## Results

### BAR-RAIL: 70/70 PASS (100%)
All 10 verbs × 7 objects produce meaningful responses. No missing handlers.

| Verb | bar-counter | bar-stool | door-aft | door-radio | jukebox | chess-board | riker |
|------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| look at | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| use | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| talk to | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| walk to | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pick up | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| push | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| open | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| close | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| give | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

### WHEELHOUSE: 90/90 PASS (100%)
All 10 verbs × 9 objects produce meaningful responses. The previously missing `hs-hatch-engine` combinations were fixed in Round 1.

| Verb | helm-wheel | radar-display | compass-rose | radio-console | nav-charts | door-aft-wh | door-galley | hatch-engine | captain |
|------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| look at | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| use | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| talk to | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| walk to | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pick up | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| push | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pull | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| open | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| close | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| give | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Special Interactions Verified
- `use` × jukebox → opens jukebox frequency selector ✅
- `use` × chess-board → opens chess overlay ✅
- `open` × chess-board → also opens chess overlay ✅
- `talk to` × riker → opens dialogue panel ✅
- `pick up` × compass (wheelhouse) → adds to inventory ✅
- `give` × captain (with coffee) → coffee transfer dialogue ✅

## No Bugs Found This Round
All verb × object combinations are covered. No code changes needed.
