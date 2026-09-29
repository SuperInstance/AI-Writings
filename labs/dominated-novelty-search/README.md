# dominated-novelty-search — threshold-free local competition for QD

*A `labs/` cell. Zero dependencies (Python stdlib). A drop-in replacement for the grid-placement
step in [`../qd-arena`](../qd-arena/).*

Quality-diversity without a grid, a novelty threshold, or bins to tune — the exact knobs that break
MAP-Elites in high-dimensional or unsupervised behavior spaces. Each individual's selection score is
its **local competition**: the mean distance to its *k nearest fitter neighbors* in behavior space.

- No fitter neighbor nearby → **local frontier** (score `INF`, always kept).
- Surrounded by fitter individuals → **dominated** (low score, culled).

Quality and diversity fall out of one rule. Grounded in *Dominated Novelty Search: Rethinking Local
Competition in Quality-Diversity*, **arXiv 2502.00593** (GECCO 2025) — already the SOTA baseline
others benchmark against.

## As a cell

```python
from dns import select, dns_scores, receipt, spread
scores, survivors = select(descriptors, fitness, k=5, keep=40)
pin = receipt(descriptors, fitness, 5, scores)   # re-derivable fnv1a-64; a verifier replays it
```

`(descriptors, fitness, k) -> (scores, survivors)` + an **fnv1a-64 receipt** over
`(rounded descriptors, fitness, k, scores)` — same hash idiom as `situation-recorder`, so the ranking
is replayable and tamper-evident (nudge one fitness → the pin moves).

## Why it beats a grid for us

`qd-arena` places ideas on a fixed 3×3 niche grid; that works in 2-D but a grid of `b` bins over `d`
descriptors needs `b^d` cells — for 12 descriptors at 4 bins each that's **16.7M cells** for a couple
hundred points (mostly empty, untunable). DNS needs zero cells and, in the self-test, keeps a
**more diverse** survivor set than random selection at equal count. The domination score is also a
cleaner novelty signal to hand Moth for the next exploration draw.

## Verify

```bash
python3 dns.py     # frontier + global-best kept; grid-free in 12-D; receipt stable + sensitive
```

Next: wire `select()` into `qd-arena`'s placement step (replace the grid), keeping JEV for fitness
and Moth for exploration — the archive becomes a grid-free local-competition frontier.
