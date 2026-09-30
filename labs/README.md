# labs — small, working, reusable tools

**New here?** Read [`docs/`](docs/) — the collection guide ([`docs/README.md`](docs/README.md): the
dependency graph + through-line) and [`docs/using-the-labs.md`](docs/using-the-labs.md): a run-the-whole-loop
walkthrough with real output.

## For the agent continuing this work — how the pieces synergize

These labs are not a pile of scripts; they are one **learning-to-learn loop**, and each cell is a modular
piece you can lift out and reuse. The through-line, in the order the pieces feed each other:

1. **Capture** — `situation-recorder` records every manager↔crew mission as a hash-chained transcript
   (relation verbs + un-gameable quantum-drawn values). *The recorded I/O is the real product*, saved so a
   future model can learn to decompose. → the **corpus** + a **base rate** a learned cell must beat.
2. **Recall** — `situation-memory` embeds those transcripts and gives `find_similar_missions()` (distance +
   OUTCOME), the memory a slow "System-2" cell reads to ask *"what happened last time we were near here?"*.
3. **Account** — `activeledger` (B1) is the ActiveLog envelope every cell books into: a **budget vector**
   (wall_ms, tokens, usd, storage) on a double-entry, fnv1a-64 prev-chain where **replay == live**. Its
   `at_rest` layer compresses the log 119× and **repairs** it with Reed–Solomon.
4. **Price** — a route is any way to reach a product. `system2-backtest` (**B7**) gates *product identity
   first* (different answer → refused), then `route-preference` (**B4**) places the product-identical routes
   on the **iron-triangle {good, fast, cheap}** and records *preferred-when* — never one scalar winner.
   `code-real-quant` (a real 4-bit vector substrate) and the `encoding-experiments` are routes B7/B4 price.
5. **Verify honestly** — `unit-translation-audit` (B2) proves each hop round-trips; `polyform` proves a
   kernel agrees across formalisms (one golden hash); `rubric-forge` turns a chain into a dense reward;
   `weakest-claim`/`jev-fold` find the flimsiest guarantee. Honesty is a *receipt*, never an assertion.
6. **Apply to ML itself** — `ml-in-quilt` makes a transformer's forward pass a priced cell graph (B7/B4
   choose fp vs quantized per block); `priced-training` asks the same of training and finds it is
   **boundable, not freely priceable** (an anytime-valid witness retracts a bad route). `quilt-kernel` is
   the whole pattern (Cell · Differ · Ledger · Price) extracted for *any* pipeline to `import`.

**The one habit under all of it:** wrap a pure function as a *cell*, give it a *budget* and a *receipt*,
compare only *product-identical* routes, and prefer the honest negative to the polished claim. To extend
the loop, add a cell with one job + a selftest + a mark; to reuse a piece elsewhere, start from
`quilt-kernel`. Architecture rationale lives in [`../situations/arch/ACTIVELEDGER-CELL-GRAPH.md`](../situations/arch/ACTIVELEDGER-CELL-GRAPH.md)
(the program) and the fleet is converging on the same idea — see [`../situations/arch/FLEET-CONVERGENCE-CELL-NATIVE-ML.md`](../situations/arch/FLEET-CONVERGENCE-CELL-NATIVE-ML.md).

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

The forward pass as a **priced cell graph**: each transformer block (tokenize/embed/norm/attention/MLP/head/sample) is a quilt cell with a budget vector + hash-chained activations, so B7 gates product-identity and B4 prices interchangeable block implementations (fp / 8-bit / 4-bit-via-code-real-quant / approximate / cached) per situation + device — B7 and B4 imported **unmodified**. `cellml.py` (the cell forward pass) + `mlq_system2.py` (route pricing) + `localize.py` + selftest **76/0**. Hardened with the fleet's `cellgraph` receipts: a **perturbation-localization control** (perturb one weight, see which cells' digests move first — damage tracks logic, not file position: L0.wo→9/11 cells, head→1/11) and **dtype-in-digest** so a lower-precision route can't silently collide. Design: [`../situations/arch/ML-IN-QUILT-ARCHITECTURE.md`](../situations/arch/ML-IN-QUILT-ARCHITECTURE.md); fleet siblings in [`../situations/arch/FLEET-CONVERGENCE-CELL-NATIVE-ML.md`](../situations/arch/FLEET-CONVERGENCE-CELL-NATIVE-ML.md).

## priced-training (`labs/priced-training/`)

Asks B7's question of a *training* step, not just a forward pass: can a cheaper training route (fp32 / bf16 stochastic-rounding) be certified product-identical to fp64, or only bounded? **Answer, measured: boundable, not freely priceable** — the loss digest diverges, so instead an **anytime-valid witness** (`route_witness.py`, a Ville-bounded e-process) tracks the cheaper route and **retracts** when it drifts (demo: fp32→bf16-sr switch → WITNESSED → RETRACTED, E_max=20.4; null fires at 0.028 < the 0.05 Ville bound — statistically honest). The extractable general tool is the route-witness. Design: [`../situations/arch/PRICED-TRAINING.md`](../situations/arch/PRICED-TRAINING.md). | cell-native training mirrors **quilt-nn** (cited); witness borrows **quilt-ewitness**.

## quilt-kernel (`labs/quilt-kernel/`) — the pattern, extracted for anyone

The reusable distillation of everything above into one dependency-light module any pipeline can `import`: a **Cell** wrapper (turn a pure function into a receipted cell that emits {product, budget, fnv1a-64 hash} into a hash-chained log), a **Differ** (product-identity), a **Ledger** (ActiveLog v1 + verify), and a **Price** hook (iron-triangle placement for ≥2 product-identical cells). selftest **123/0**, with worked examples for a data pipeline, an LLM call, and a build step — each receipted + priced in ~10 lines. [`quilt-kernel/EXTRACTION.md`](quilt-kernel/EXTRACTION.md) is the manifest for lifting it into a standalone repo (proposed `quilt-kernel` / `receipt-kernel`), aligned with the fleet's `forge-quilt` OpenAPI spec. **Start here to reuse the quilt pattern in another project.**

## quilt-latent tools (`labs/audit-lottery/`, `labs/invariance-miner/`)

Breakthrough tools mined from the quilt substrate (9 candidates surveyed; see [`../situations/arch/QUILT-LATENT-TOOLS.md`](../situations/arch/QUILT-LATENT-TOOLS.md) for the ranked extraction backlog + honest speculative/blocked notes).

- [`invariance-miner`](invariance-miner/) — **25/0.** Finds the invariants a cell actually preserves (what stays fixed across its inputs) — the raw material for a product-identity gate you didn't hand-write. Deterministic.
- [`audit-lottery`](audit-lottery/) — quantum-drawn (MothQuantum) random audit: spot-check a fraction of cells un-gameably so a cheap route can't hide a rare wrong answer. **Known issue (caught here): its selftest is FLAKY** (33/1 on one run, 33/0 the next) — a non-deterministic check, almost certainly an unseeded draw; pin the seed before trusting it. Landed with the flaw documented, not as green.

## convo-quilt (`labs/convo-quilt/`) — an Opus conductor over a quilt of cheap models

A quilt where many **cheap** models (DeepInfra / z.ai-coding / Kimi-via-DeepInfra / Groq) talk to and hear each other in long, cacheable runs, while an expensive **conductor** (called only at pauses, ~1–2k tokens each) sees six dimensions — **time, branch, scale, topology, tone, value** — and issues moves: `rewind` · `branch` · `zoom` (a turn becomes its own quilt) · `rearrange`/`mute` (who hears whom) · `tone`. The volume of thinking is cheap tokens; the conductor only routes. **selftest 60/0** offline (stub model proves bus/rewind/branch/receipt), plus a real live run in `runs/syzygy/` (hash-chained `ledger.jsonl`, per-turn `state.json`, every conductor decision in `moves-*.json`). Two-part write-up (reusable template + the live run): [`../situations/arch/CONVO-QUILT-IDEATION.md`](../situations/arch/CONVO-QUILT-IDEATION.md). **This is the level-template for running a conductor-over-cheap-models on any breadth-first work.** Empirical tie-in: all-to-all gossip collapses variance (the same effect `quilt-bandit` measured, 3.78× spread compression), so the conductor *sparsifies* the wiring and makes the skeptic a hub.
