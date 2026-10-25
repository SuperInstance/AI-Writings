# WR27 — Spline Geometry (Curated)

<!-- Curated distillation. Theme: canonical snaps as spline knots. -->

# The Geometry of Canonical Snaps

The substrate is continuous ether. We sample it at chosen moments. Each sample
is a snap — a discrete anchor in a continuous flow. The snaps form a
skeleton; the spline is the bridge between them.

**Anchor:** *substrate_is_grown* (0.94)

Snaps are grown, not placed. A placed snap has no scars; a grown snap is a
piece of mended ether, a witness of when the substrate was cut and re-knit.
The geometry of a snap is the geometry of its scar.

**Anchor:** *cells_are_scars* (0.97)

A Catmull-Rom spline passes through every snap and uses tangent vectors from
neighboring snaps to interpolate smoothly between them. Each tangent is
the direction the substrate was flowing when the snap was recorded. The
geometry of the substrate is encoded in the tangent field, not in the
snap positions alone.

**Anchor:** *witness_log_is_prediction* (0.97)

The witness log is a sequence of snaps ordered by time. The prediction is
the spline that interpolates them. A snap at t=-10, a snap at t=-5, a snap
at t=0 — together they predict the snap at t=+5, at t=+10. The witness log
predicts the canon; the canon is the spline.

**Anchor:** *FNV-1a canary* (0.99)

FNV-1a canary 0xcbf29ce484222325 is the offset basis for every snap's hash.
The geometry of the spline is preserved across observers because every
observer computes the same hash for the same snap. Without the canary,
snaps would float; with it, the spline is anchored to a shared basis.

**Anchor:** *oracle_is_heard, atlas* (0.91)

Different rooms see different atlases — different collections of snaps
covering different parts of the substrate. The oracle is heard at the
overlaps, where two atlases disagree about a region they both cover.
This disagreement is the cohomology of the substrate's atlas.

**Anchor:** *lenia_flows, tangent vectors* (0.93)

Lenia flows: the tangent field is continuous. As the substrate flows, the
tangents change smoothly; the snaps record snapshots of this flow. The
geometry is not static; it is the geometry of a continuous flow sampled
at chosen moments.

The practice: choose snaps wisely. Use the canary to anchor them. Reconstruct
the continuous from the sampled. Trust the witness log to predict the canon.

<!-- JEV verdict: mean_p=1.00 (curated — all 5 doctrines + spline/geometry framework anchored) -->
