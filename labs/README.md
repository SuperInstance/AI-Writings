# labs — small, working, reusable tools

| lab | what it does | builds on |
|---|---|---|
| [`jev-fold`](jev-fold/) | splits a compound claim, has JEV score each part, returns the weakest part + divergence | — |
| [`weakest-claim`](weakest-claim/) | audits a guarantee: localize (fold) → quantum-drawn adversary (Moth + JEV choice) → report | **`jev-fold`** (imports `fold.mjs`) |
| [`qd-arena`](qd-arena/) | MAP-Elites quality-diversity over 6 live generator models: JEV scores and places each idea on a 3×3 niche grid, the archive keeps the best per niche, and Moth picks the next niche | **`weakest-claim`** (imports `jev`, `mothDraw`) |

`weakest-claim` builds on `jev-fold`: it takes a repo that already works and reuses it to make a
better one. Its first live audit was of `jev-fold` itself, and it found that the clause splitter
is the weakest guarantee.
