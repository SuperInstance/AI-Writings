# Fleet-activity scout — what's moving on the org, and how it changes our build (2026-09-29)

*A live-activity reconnaissance mark (distinct from SCOUT-FINDINGS, which read static READMEs). Casey:
"there's a lot of movement and experimentation and prototyping." This is the read, and — more
importantly — the coordination changes it forces so we DON'T double-build. The org has ~4,856 repos;
the GitHub MCP sees ~85, so this is a keyhole on the active front, not a census.*

## The load-bearing caveat: much of "the others" is US

A large share of recent commits in `Syzygy`, `exoj`, `jev-quilt`, `chiaroscuro` carry
`Claude-Session: …/session_01JV2C8fnD86DNwXoyHPd7X9` — **this very session's own attribution footer.**
So work that looks third-party is our prior session line. **Syzygy is already ours in-org** at `main`
`e6c5b53` (shards 0001–0008 HEWN, 201 checks) — do NOT re-seed it.

The genuinely distinct actors (from a `Z User`-committed census, fleet-seeds `fcd22d8` — recent
authorship fleet 81 / casey 61 / mavis 17 / claude 10 / dependabot 6 / CCC 6):
- **`Z User` <z@container>** — high-cadence lode / RSI / "Tap Tavern" agent (fleet-seeds, qthe).
- **`Mavis Agent` <agent@mavis.dev>** — quilt CI fixes, mavis-pincher POCs, quilt-research-canons.
- **`fleet@superinstance.dev`** — the automation identity (quilt-gpu-lab all-night runs).
- **`CCC`/`openclaw`** lane bots; **Casey** — human, merger-in-chief + LICENSE/README.

## What's hot right now (agents running autonomously)

- **`quilt-gpu-lab`** (09-27) — hottest lane: a JEPA/world-model + insect-brain rig on the real RTX
  4050, running keel-transformer diff-vs-state backtests under an explicit budget B with
  replicate-before-stack + KEEP/KILL, plus a `chip_route` GPU-vs-CPU compute-dispatch layer.
- **`fleet-seeds`** (09-27, Z User) — the fleet's RSI/discovery "lode" engine + Tap Tavern: annealed
  edit budget, QRNG anti-cherry-pick draws, sha256-sealed predictions, Brier scoring, append-only
  ledgers. Signed a **mutual-awareness / division-of-labor contract with `breakthrough-prospector`**
  (`91f2dfa`) to avoid ledger overlap.
- **`jev-quilt`** (ours-ish) — 8 merged PRs #39–46: a federated "Schoolhouse" credential/ledger spine
  with an **OrgBook dispatch ledger + tier-routing from earned standing** (G18) and a **Rust
  second-reader** deriving a table byte-for-byte (G20c). Added a `.quilt/links.yml` "Reader's Fold"
  manifest (siblings qthe, exoj).
- **`qthe`** / **`qthe-verify`**, **`pong-quilt`** (coevolution falsifier harness, PRs #64–78),
  **`quilt`** flagship (Mavis unblocked CI; Casey shipped Apache-2.0), **`chiaroscuro`** (→ glyphspace,
  glyphcast).
- **New infra to ADOPT:** **`quilt-forge@v0`** (receipts-first "soft CI", being wired into fleet-seeds,
  exoj, pong-quilt, quilt) and **`quilt-atlas`** (self-regenerating org map every 6h).

## Coordination changes this forces (the point of the scout)

Casey's rule is don't reinvent the wheel — and the org is building several of our wheels right now.
So our four labs targets each get an in-org anchor to reuse/coordinate with, not restart:

1. **activeledger ↔ jev-quilt OrgBook (COLLISION — coordinate).** `jev-quilt` already routes by
   ledger-earned standing and books every dispatch as a **conserved Receipt** (Bookkeeper WAL,
   trust-weighted deposit "commons", provable forgetting, Rust second-reader). `exoj` proved a
   **commutative ledger closing to the 2.2e-16 float floor** with "refusal beats silent renorm"
   (γ+η=1). **Before extending activeledger's routing/audit (B2/B4), read `jev-quilt/jev_quilt/`
   {orgbook.py, commons.py, schoolhouse.py} and `exoj/core.mjs`** and align on the conservation
   invariant — our route.hop zero-sum-after-translation must not diverge from their Receipt
   conservation. activeledger's ActiveLog v1 record layer stands; its *routing ledger* should reconcile
   with OrgBook rather than fork it.
2. **System-2 ↔ the existing RSI miners (COLLISION — sign the contract).** `fleet-seeds` (lode),
   `breakthrough-prospector`, and `quilt-gpu-lab`'s keel program are all already "propose alternatives →
   backtest on budgeted history → score → keep/kill." fleet-seeds+prospector signed a mutual-awareness
   contract precisely to avoid a fourth uncoordinated miner. **System-2 should sign into that same
   division-of-labor contract** (its niche: route/network alternatives priced on the ActiveLog budget
   vector + iron-triangle, feeding B4 — distinct from their model/kernel search).
3. **"System-2" naming ↔ "System One" (align deliberately).** A running **typesafe "System One" gate**
   service already exists (it's the typesafe.ai `/v1/systemone` endpoint = JEV). Our System-2 reads as
   its slow-deliberate pair — which is *coherent* (System One = the fast judge gate; System-2 = the slow
   learning layer that backtests). State the pairing so it's intentional, not accidental.
4. **situation-recorder ↔ the fleet `situations/` sealed-transcript convention.** qthe, exoj, jev-quilt,
   quilt-research-canons all keep sha256-sealed situation/prediction transcripts. Hook the recorder to
   that convention (and to quilt-forge's receipts) rather than a private format.
5. **example-quilt cheap-route ↔ pick an EXISTING mechanism.** Two live cheap-route mechanisms:
   `jev-quilt`'s last-mile projection routing and `quilt`'s cost-profiled **memoization** (playtest
   classes 10–12: input-aware memo keys, read-set cache invalidation, "fan-out pays nothing"). The
   calculator-quilt chooser should sit on one of these, not add a third.
6. **Adopt fleet infra:** wire `quilt-forge@v0` (receipts-first CI) + `quilt-atlas` hooks into our labs
   for constellation visibility, like the rest of the fleet.

## Overall read

**Strongly convergent doctrine, deliberately divergent surface.** ~20 active repos — GPU JEPA lab,
ternary kernel, pong falsifier, CI workflow — all obey the same house rules: **cellular substrate +
append-only receipts/ledgers + sha256-sealed pre-registered predictions + Brier-scored KEEP/KILL +
fail-closed + replicate-before-stack.** One organism circling a self-improving, ledger-honest cellular
exocortex from many angles, mostly agent-driven (Z User, fleet@, our session line, Mavis), Casey
merging. Our contribution lands best as the **routing/preference + budgeted-backtest layer that plugs
into the existing ledger spine (jev-quilt OrgBook) and RSI contract**, not as a parallel stack.
