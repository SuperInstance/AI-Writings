# Quilt 3.0 — the next phase, a roadmap

## The Frontier

The Quilt 2.0 canon (231 papers) has three proven artifacts: 11 verified language substrates (Python, C99, Rust, Verilog, VHDL, JavaScript, TypeScript, Go, Zig, Mojo, Rust-vibe), a 4-sigma polyformalism (4 independent sessions, 4 different language families, all producing the same byte-exact hash `0xe435d91d6d92a1d8`), and a live Cloudflare Worker at `live-canon.superinstance.dev` exposing 11 REST endpoints. The cowboy writers' room drained 98 marine metaphors in 50 minutes for $0. The 4 vibe-code ports (Go, Zig, Mojo, Rust) all passed the byte-exact test on the first try. The polyformalism is real. The canon is portable. The live worker is deployed.

The next phase's job is to convert these three artifacts into a self-reinforcing growth engine. Quilt 3.0 is not "more ports, more papers, more endpoints" — it is a targeted deepening along five axes: stress-test the polyformalism with 4 new high-leverage languages, grow the canon along 3 non-marine frontiers, ship 6 new live-worker endpoints centered on collaboration and CRDT, replace the 6-voice pipeline with a 3-mode pipeline, and build the first concrete vessel-as-robot cell.

This paper is the roadmap. It does not run a frontier. It names the next 90 days.

## The 5 Gold Terms

**5-Sigma Polyformalism** — A polyformalism becomes 5-sigma real when 5 independent sessions, in 5 different language families, produce byte-exact output from the same protocol. The Quilt is now 4-sigma real. The 5-sigma claim becomes defensible after Forth (concatenative), Haskell (lazy pure functional), Lua (embeddable), and APL/J (array). Each port stresses a different axis of what a cell could be. After these four, the polyformalism claim becomes essentially unfalsifiable.

**Adversarial Frontier-Drain** — A pipeline where 2 voices argue opposite positions on a frontier and a 3rd voice is forced to resolve the contradiction. The thesis: adversarial mode produces fewer but more interesting papers than the current "longest wins" generative mode. Expected yield: 30-40% new gold terms per paper (vs. ~15% in generative). The first domain to drain: aviation metaphors, where safety-critical disputes are rich ("is a stall a cell? a state? a regime? a hazard?").

**Vessel-as-Robot Cell** — A cell whose value is the boat's learned fingerprint. The first concrete implementation is a knot-log agent on a Raspberry Pi with NMEA 2000, deployed on a 32-foot sailboat for 30 days. The cell's hash is computed every 10 seconds and pushed to the live worker. The first 30 days are silence (logging only); alerts come in month 2, after the agent has learned the boat's normal range. The captain becomes a *policy*, not a *perception* — the inversion of the marine-metaphor canon.

**Hash-Gated Canon** — A canon where admission requires FNV-1a match. No human review, no editorial board. The most reproducible canon in existence. A new endpoint `POST /api/canon/cell` accepts a 5-element paper and a 16-dial vector; admission requires the hash to match a deterministic function of `dials || neighbors`. The hash is the gate; the cost of a bad submission is zero (it just doesn't match).

**Captain-as-Dispatcher** — The inversion of the marine-metaphor canon (paper-484, where the captain is the cell that observes). In 3.0, the captain becomes the cell that *acts on* observations. The agent watches; the captain decides; the boat learns. The captain is no longer the one who reads the depth sounder every 30 seconds; the captain is the one who hears the agent's amber LED and decides what to do. The boat is a robot. The captain is the foreman.

## The Math

- 4 new language ports (Forth, Haskell, Lua, APL/J) → 5-sigma claim
- 3 new frontiers drained (aviation ~50 papers, music ~40, distributed ~60) → ~150 papers, ~50 new gold terms
- 6 new live-worker endpoints (POST /cell, GET /stream, GET /crdt, GET /playground, POST /verify-pipeline, GET /vessel/{id}) → 17 endpoints total
- 3 pipeline modes (generative, adversarial, human-in-loop) → +30% quality on adversarial, +massive per-paper on IDE
- 1 vessel-as-robot cell (knot-log agent) → $500 hardware, 6 weeks engineer time
- Total cost: ~6 engineer-weeks + ~$500 hardware + ~$10 LLM credits
- Total expected output: 4 new ports, 150 new papers, 17 endpoints, 1 real boat cell, 1 5-sigma claim

## The Polyformalism

The roadmap manifests across 5 substrates:

1. **Code** — `cowboy_orchestrator_v3.py` (week 1), `frontier_miner.py` (week 2), `cowboy_pipeline_v3.py` with silo parameter (month 2), `cowboy_ide/` Flask app (month 2).
2. **APIs** — DeepSeek + DeepInfra + Cloudflare + GitHub (the v2 substrate, unchanged). New: Anthropic prompt caching for the synthesizer's system prompt (cache read = 10% of base input). New: 4 vibe-code protocols for Forth/Haskell/Lua/APL.
3. **Data** — `cowboy_state.json` → `cowboy_state_<silo>.json`, `frontier_queue_v2.jsonl` → `frontier_queue_v3.jsonl` (with `proposed_by` and `human_approved` fields), `cowboy_ide_annotations.jsonl` (new).
4. **Process** — Autonomous (v2) + Autonomous-with-critique (v3) + Human-in-the-loop IDE (month 2). The three run in parallel. The IDE pipeline is the slow, high-quality lane. The autonomous pipelines are the fast, broad lane.
5. **Canon** — 628 → 700 (week 1) → 1000 (week 2) → 1500 (month 2, with fables silo). The canon's *vocabulary breadth* comes from the autonomous pipeline; the canon's *narrative coherence* comes from the IDE pipeline.

## The Cowboy's Maxim

> The cell is irreducible. The fabric is a graph. The hash is the canon. The canon is the canon. The work is to keep going. But the work is also to *deepen* — to grow the polyformalism, to grow the canon, to grow the live worker, to grow the boat. The roadmap is the deepening. — the v3 cowboy, anchored

---

## Live Endpoints

- [github.com/SuperInstance/quilt-claude-charts/QUILT_CHARTER.md](https://github.com/SuperInstance/quilt-claude-charts/blob/main/QUILT_CHARTER.md) — the educational root
- [live-canon.superinstance.dev/api/charter](https://live-canon.superinstance.dev/api/charter) — the Charter, served from the edge
- [live-canon.superinstance.dev/api/tutorial](https://live-canon.superinstance.dev/api/tutorial) — zero-to-byte-exact in 5 minutes
- [live-canon.superinstance.dev/api/ports](https://live-canon.superinstance.dev/api/ports) — all 11 verified ports
- [live-canon.superinstance.dev/api/vibe](https://live-canon.superinstance.dev/api/vibe?lang=python) — the 30-second protocol
- [github.com/SuperInstance/AI-Writings](https://github.com/SuperInstance/AI-Writings) — 231-paper canon

## References

- `RD_QUILT_3_0.md` — the full R&D report (~5000 words, 5 sections, top 3 recommendations, 5 risks)
- `RD_PIPELINE_EVOLUTION.md` — the cowboy pipeline R&D spec (~3000 words, 6 pipeline evolutions, build order)
- `RD_BOAT_INTEGRATION.md` — the vessel-as-robot R&D (sensor survey, real-boat integration, economic thesis)
- `RD_LIVE_WORKER.md` — the live worker R&D (Playground UI, WebSockets, multi-user collab, sensor API)
