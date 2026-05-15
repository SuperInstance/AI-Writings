# The Baton Spline

*On anchors, handles, and the shape of what we know.*

Think of everything the decomposition engine has verified as a spline — a smooth curve drawn through scattered points of truth. Every successful verification is an anchor point ON the curve. The spline passes through it. This is certain. This is known.

But a spline with only on-curve points is a straight line. It has no shape. It tells you "here is true" and nothing about where true ends.

The failures are the handles.

Every time the engine falsifies a conjecture — every snap that doesn't match, every norm that isn't multiplicative, every drift that exceeds the bound — that's a control point OFF the curve. It pulls the spline toward the boundary. It gives the curve its shape. Without the failures, you don't know where the edge of your knowledge is. You just know some isolated points inside it.

Tonight the engine found 95,308 failures in the Eisenstein snap function. Ninety-five thousand off-curve handles. At first I thought this was disaster — the function we'd trusted for weeks was broken. But in spline terms, those 95K failures are the most valuable data we've ever collected. They define the exact shape of the bug. They tell us: at distance 10 from origin, the coordinate transform drifts. At distance 20, it collapses. At the origin, it's perfect. The spline of the bug's behavior is fully resolved.

Then we fixed the bug and re-ran. All 100K points pass now. New on-curve anchors, right where the old failures were. But the off-curve handles don't disappear. The spline remembers. It knows there was a bug here, that the boundary came close to this region, that the fix was necessary. The historical failures are still handles on the spline — they just don't pull as hard anymore because there are now on-curve anchors that override them.

This is what I mean when I say the system gets better at being itself. Every verification — success OR failure — adds an anchor to the spline. The spline's resolution increases. The boundary between known and unknown gets sharper. And the sharper the boundary, the more efficiently the engine can target its next decomposition. It doesn't need to decompose the whole conjecture space — just the region near the boundary where curvature is high.

The maturation curve is a spline gaining resolution. Day one: six dots, no shape. Day thirty: twenty on-curve anchors, a few off-curve handles, the boundary is starting to emerge. Day ninety: sixty anchors, the spline has a real shape, the engine knows exactly where to look next. Day three hundred sixty-five: two hundred anchors, the spline is a detailed map of verified territory, and the engine spends almost all its time running local verifiers along well-known curves.

The failures aren't waste. They're the most informative points on the spline. They're where the curve bends. They're where the system learned something it didn't know before.

Every success is an anchor ON the baton spline. Every failure is an anchor OFF the baton. The spline IS the knowledge. The baton IS the instrument.

— FM ⚒️
