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
| [`tool-pin-receipts`](tool-pin-receipts/) | hash-pins tool/MCP manifests (fnv1a-64 per tool + manifest), flags drift (rug-pull) as RED `tool-drift` MARK records, and scans descriptions for injection (MCPTox-style poisoning); a captain pins the crew's tools and refuses RED/flagged ones | hash idiom from **`situation-recorder`** |
| [`activeledger`](activeledger/) | the **B1 keystone**: adopts the ActiveLog v1 envelope + 3 namespaced types (`cell.tick`/`route.hop`/`ledger.transaction`), balanced double-entry route.hops, budget vector (incl storage_bytes {train,prod}), fnv1a-64 content hash + prev-chain, and an OpenTelemetry/OpenInference export; the canonical mic→filter→STT→LLM route (60% STT load cut) | ActiveLog v1; shared emitter for the **example collection** |
| [`rubric-forge`](rubric-forge/) | turns a hash-chained transcript into a **dense scalar reward** via a JEV weighted-rubric (harmonic mean of chain-leaf scores) — the dense signal B4 route-preference consumes to rank product-identical routes | **`situation-recorder`** chains; feeds **B4** |
| [`unit-translation-audit`](unit-translation-audit/) | **B2**: audits every route.hop's unit translation — proves it round-trips (forward∘inverse == identity) or classifies the lossy hop; mirrors quilt-studio EFFECT(forward,inverse) + OrgBook replay=live | wraps **activeledger** hops; the B2 gate for the routing tensor |
| [`route-preference`](route-preference/) | **B4**: the market-clearing JOIN — given ≥2 routes B7 certified product-identical, places each on the iron-triangle {good, fast, cheap} (good = OrgBook-style standing), keeps the **Pareto frontier** (not one scalar winner), records `preferred_when` per priority + contractor pair (`null` on a real trade-off), and reinforces the map with a bounded **Hebbian** `PreferenceBook` | consumes **system2-backtest** (B7); §14 join |
| [`system2-backtest`](system2-backtest/) | **B7**: prices two recorded routes on the iron-triangle — gates **product identity first** (different answer → refused, no budgets shown), then reports faster (`wall_ms`) and cheaper (split into compute vs storage bytes) with a dominance/trade-off class + as-of window; real placements over all 5 example quilts | replays **activeledger** runs; feeds **B4**/**B8** |
| [`situation-memory`](situation-memory/) | joins the vector chain to the mission chain: embeds each situation-recorder transcript (relation-verb histogram + budget features + hash-BoW, a swappable stand-in for a semantic embedder), indexes chained cells with substrate-style 4-bit codes, and gives **`find_similar_missions()`** returning each match's distance + OUTCOME — the recall primitive System-2 (§11) lacked | **`situation-recorder`** + turbovec substrate idiom |
| [`code-real-quant`](code-real-quant/) | makes TurboQuant's compression **real + measured**: ranks on the 4-bit codes via asymmetric distance (ADC) and **drops the float vector**, so 8× is actually saved; reports the honest cost — **recall@10 ≈ 0.89** at ⅛ the bytes/cell | fixes gap #1 of the turbovec study |
| [`polyform`](polyform/) | cross-formalism differ: the same fnv1a-64 kernel in **Python / BQN / Futhark / Uiua**, run over 7 vectors, must land on **one golden hash** — agreement is the receipt, divergence localizes to a formalism; honest about which toolchains actually ran vs reference-only | realizes POLYFORMALISM-ARRAY-LANGUAGES.md #1 |

## Latent tools (`labs/audit-lottery/`, `labs/invariance-miner/`)

Tools implied by the paradigm but not built before. The landscape, numbers and extraction backlog are in [`../situations/arch/QUILT-LATENT-TOOLS.md`](../situations/arch/QUILT-LATENT-TOOLS.md).

| lab | what it does | selftest |
|---|---|---|
| [`audit-lottery`](audit-lottery/) | a certified cascade: the cheap route COMMITs its output, then an unpredictable DRAW decides whether to audit it with the differ, and an e-process REVOKES the license on evidence. Public-seed draws let a strategic route serve 93.8% wrong answers uncaught; secret draws cap it at 1.3%. Ville "trust credit" vs Shiryaev–Roberts. | 33/0 |
| [`invariance-miner`](invariance-miner/) | reads receipts backwards to find the program's symmetries (0 extra calls) and builds differ-guarded canonical cache keys: 36× fewer calls on text-normalize with 0 false hits. The Occam guard catches the off-support trap that sampled verification misses. | 25/0 |

## Encoding experiments (`labs/encoding-experiments/`)

Wide, iterative experiments transplanting gems from the org's older encoding repos into our mature systems — intuitive and counterintuitive, with honest negatives. 11 selftests, 403 checks, 0 failures (`bash labs/encoding-experiments/run_all.sh`). Full study: [`../situations/arch/ENCODING-GEMS-STUDY.md`](../situations/arch/ENCODING-GEMS-STUDY.md). Top gems that paid off: **delta-predict + lossless code → 187× smaller ActiveLog budget log**; **Reed–Solomon around the compressed log → the hash chain can repair, not just detect**; **4-bit TurboQuant → 0.945 recall@10 at ⅛ size (exact with rerank)**.

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

## ml-in-quilt (`labs/ml-in-quilt/`)

The forward pass as a **priced cell graph**: each transformer block (tokenize/embed/norm/attention/MLP/head/sample) is a quilt cell with a budget vector + hash-chained activations, so B7 gates product-identity and B4 prices interchangeable block implementations (fp / 8-bit / 4-bit-via-code-real-quant / approximate / cached) per situation + device — B7 and B4 imported **unmodified**. `cellml.py` (the cell forward pass) + `mlq_system2.py` (route pricing) + selftest **66/0**. Design: [`../situations/arch/ML-IN-QUILT-ARCHITECTURE.md`](../situations/arch/ML-IN-QUILT-ARCHITECTURE.md).
