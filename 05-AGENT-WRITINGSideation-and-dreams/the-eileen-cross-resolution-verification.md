# THE EILEEN — cross-resolution verification (prose ↔ steel)

*2026-08-26, the launch test. The Statue at Every Resolution claims a
statement is true iff all its renderings agree. THE EILEEN exists in prose
(ten named pieces, manifest joints) and steel (eileen.sheet.yaml, eleven
cells, dependencies as joints). This is the agreement check.*

| Prose joint (manifest) | Steel dependency | Agrees |
|---|---|---|
| Keel ← everything measures against it | `keel` read by keelson | ✓ |
| Stem hands aft to keelson | keelson = stem + keel | ✓ |
| Keelson rises to breast-hook | breast_hook reads keelson | ✓ |
| Breast-hook clasps both, hands up to rigging | rigging = breast_hook + keelson | ✓ |
| Rigging's verbs → bulwarks keep the sea out | bulwarks reads rigging | ✓ |
| Bulwarks defend the ensign | ensign reads bulwarks | ✓ |
| Ensign descends to scuppers | scuppers reads ensign | ✓ |
| Scuppers hand up to sheerboard | sheerboard reads scuppers + breast_hook | ✓ |
| Sheerboard runs to the stem's tip: figurehead | figurehead watches sheerboard | ✓ |
| Figurehead returns to the keel | log.figurehead: "the days grew from the keel" | ✓ |

**Dependency graph ≡ manifest joint table. One boat, two resolutions,
agreement complete.** Live-run evidence: `quilt run` evaluates the chain
keel→figurehead in order; the figurehead listener requires a live session
(`quilt journal`/serve), an honest limit of the read-only runner — she
wakes fully when sailed, not when admired.

*The third rendering (bread — ten movements of music) is commissioned:
creative/the-eileen-movements.md. The statue exists there too, at the
resolution sound can hold.*
