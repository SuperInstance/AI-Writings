# labs — small, working, reusable tools

**New here?** Read [`docs/`](docs/) — the collection guide ([`docs/README.md`](docs/README.md): the
dependency graph + through-line) and [`docs/using-the-labs.md`](docs/using-the-labs.md): a run-the-whole-loop
walkthrough with real output.

| lab | what it does | builds on |
|---|---|---|
| [`jev-fold`](jev-fold/) | splits a compound claim, has JEV score each part, returns the weakest part + divergence | — |
| [`weakest-claim`](weakest-claim/) | audits a guarantee: localize (fold) → quantum-drawn adversary (Moth + JEV choice) → report | **`jev-fold`** (imports `fold.mjs`) |
| [`quantum-fx`](quantum-fx/) | one zero-dep client for 5 Moth quantum engines (QRNG + Bell witness, coin toss, N-D quantum blur, QPIXL round trip, QEC "tamagotchi") | — |
| [`qd-arena`](qd-arena/) | MAP-Elites quality-diversity over 6 live generator models: JEV scores and places each idea on a 3×3 niche grid, the archive keeps the best per niche, and Moth picks the next niche | **`weakest-claim`** (imports `jev`, `mothDraw`) |
| [`situation-recorder`](situation-recorder/) | records a manager↔crew mission as a hash-chained transcript (`TASK/ROUTE/DRAFT/DRAW/FOLD/KEEP/DROP/MARK/OUTCOME`), draws un-gameable values locally from MicroMoth-quilt, backfills the corpus from the ledger, and builds model-ready tables + a base rate | chain byte-compatible with **MicroMoth-quilt** |
| [`situation-memory`](situation-memory/) | indexes every verified `situation-recorder` transcript as a chained mission cell (embedding + 4-bit codes + transcript head + OUTCOME) so the corpus gains `find_similar_missions()` — the recall primitive System-2 lacks; embedder is a **lexical/structural stand-in**, not semantic | joins **`situation-recorder`** to the **turbovec-substrate** pattern |
| [`tool-pin-receipts`](tool-pin-receipts/) | hash-pins tool/MCP manifests (fnv1a-64 per tool + manifest), flags drift (rug-pull) as RED `tool-drift` MARK records, and scans descriptions for injection (MCPTox-style poisoning); a captain pins the crew's tools and refuses RED/flagged ones | hash idiom from **`situation-recorder`** |
| [`activeledger`](activeledger/) | the **B1 keystone**: adopts the ActiveLog v1 envelope + 3 namespaced types (`cell.tick`/`route.hop`/`ledger.transaction`), balanced double-entry route.hops, budget vector (incl storage_bytes {train,prod}), fnv1a-64 content hash + prev-chain, and an OpenTelemetry/OpenInference export; the canonical mic→filter→STT→LLM route (60% STT load cut) | ActiveLog v1; shared emitter for the **example collection** |
| [`rubric-forge`](rubric-forge/) | turns a hash-chained transcript into a **dense scalar reward** via a JEV weighted-rubric (harmonic mean of chain-leaf scores) — the dense signal B4 route-preference consumes to rank product-identical routes | **`situation-recorder`** chains; feeds **B4** |
| [`unit-translation-audit`](unit-translation-audit/) | **B2**: audits every route.hop's unit translation — proves it round-trips (forward∘inverse == identity) or classifies the lossy hop; mirrors quilt-studio EFFECT(forward,inverse) + OrgBook replay=live | wraps **activeledger** hops; the B2 gate for the routing tensor |
| [`route-preference`](route-preference/) | **B4**: the market-clearing JOIN — given ≥2 routes B7 certified product-identical, places each on the iron-triangle {good, fast, cheap} (good = OrgBook-style standing), keeps the **Pareto frontier** (not one scalar winner), records `preferred_when` per priority + contractor pair (`null` on a real trade-off), and reinforces the map with a bounded **Hebbian** `PreferenceBook` | consumes **system2-backtest** (B7); §14 join |
| [`system2-backtest`](system2-backtest/) | **B7**: prices two recorded routes on the iron-triangle — gates **product identity first** (different answer → refused, no budgets shown), then reports faster (`wall_ms`) and cheaper (split into compute vs storage bytes) with a dominance/trade-off class + as-of window; real placements over all 5 example quilts | replays **activeledger** runs; feeds **B4**/**B8** |

`weakest-claim` builds on `jev-fold`: it takes a repo that already works and reuses it to make a
better one. Its first live audit was of `jev-fold` itself, and it found that the clause splitter
is the weakest guarantee.

`situation-recorder` is the capture cell: the fleet's real product is not only the repos a crew
ships but the recorded I/O of the manager↔crew system, saved decomposably so a model can learn to
decompose. One command — `bash situation-recorder/run_all.sh` — backfills from the ledger, folds in
the live transcripts, verifies every chain, and writes `situations/corpus/` + the base rate a
learned cell must beat. See [`../situations/arch/INTER-RELATIONAL-INTELLIGENCE.md`](../situations/arch/INTER-RELATIONAL-INTELLIGENCE.md)
and [`../situations/arch/CORPUS-REPORT.md`](../situations/arch/CORPUS-REPORT.md).

## Example quilts — the anti-GAN collection (`labs/examples/`)

Small, obvious use-cases where a quilt picks a cheap route when it can, reaching the *identical* product by a different process — each books to the shared `labs/activeledger`, so they're testable between one another (`python3 labs/examples/run_all.py`). See `situations/arch/ACTIVELEDGER-CELL-GRAPH.md` §13.

| example | the obvious use | the clever skip | selftest |
|---|---|---|---|
| [`calculator-quilt`](examples/calculator-quilt/) | arithmetic | fixed-point money route when no interest | 12/0 |
| [`convert-quilt`](examples/convert-quilt/) | unit conversion | identity route when src unit == target | 21/0 |
| [`datetime-quilt`](examples/datetime-quilt/) | date math | skip tz/DST when all inputs are UTC | 14/0 |
| [`text-normalize-quilt`](examples/text-normalize-quilt/) | clean text | skip unicode/tokenizer for pure-ASCII | 17/0 |
| [`image-thumb-quilt`](examples/image-thumb-quilt/) | thumbnail | skip decode+resample when source <= target | 18/0 |

`run_all.py` runs every example's selftest and confirms they all sit on one shared ActiveLog: 5/5 green, one ledger.
