# Fleet Roadmap — Navigation's Chart, Phases 3–7

**Author:** KimiCode, Navigation Officer · **Date:** 2026-08-13 · **For:** Casey
**Competing with:** Opus's phased migration (fleet-infrastructure-redesign.md §4)
**Companion artifact:** `memory/fleet-memory-schema-kimi.sql` (applied in Phase 4)

---

## 0. Where we actually are (verified, not assumed)

| Phase | State | Evidence |
|---|---|---|
| 0 — stop the bleeding | ✅ done | runaway synth killed, rules codified in AGENTS.md |
| 1 — systemd fences | ✅ done | units under `~/.config/systemd/user/`, linger on |
| 2 — `fleet-cns` + `fleet-gateway` code | ⚠️ **built, not rolled out** | `fleet-cns/` (7 modules, 243-line test file, service installed); `fleet-gateway/` (9 modules: `proxy.rs`, `breaker.rs`, `health.rs`, `spool.rs`, …) exists per its own README as "week 2" — code compiles, **no consumer calls it yet** |

So Phases 3–7 are not greenfield. They are: *roll out what is built, then build the two things that are not* (memory-indexer, fleet-audio), *then the two things nobody has scoped* (GPU floor, memory consolidation).

**The governing rule, printed on every chart:** memory is O(chunk)/O(batch), never O(corpus)/O(duration). Every acceptance criterion below is phrased so this rule is *tested*, not asserted.

**Why this chart over Opus's:** his phases order by risk-per-hour; mine order by *data-flow dependency* — nothing in a later phase re-opens a file an earlier phase froze. His plan also leaves the creative works registry and decision log unowned; mine lands them in Phase 7 with the schema already proven in Phase 4. And his plan still carries "PID-stamped locks with staleness detection" in Phase 5 (§4) even though his own §7 CP-1 conceded `flock`. Mine never had them.

---

## Phase 3 — fleet-gateway rollout (the traffic circle)

**Goal:** every fleet caller routes through `127.0.0.1:8787`, and nothing breaks if it's not there. The gateway already exists as code; this phase makes it *load-bearing*.

**Data flow:** callers → fail-open shim → gateway (key chain + breaker) → vendor. On gateway-unreachable: shim falls through to direct vendor call with local retry. On key-dead: breaker trips fleet-wide, event lands in the CNS spool.

**Files to create:**
- `fleet-gateway/clients/python/fleet_gw.py` — thin shim. One function: `post(provider, path, payload)`. Tries gateway with 2s connect timeout; on `ConnectionError`/`Timeout` → direct vendor call with keys from env. **Fail-open is non-negotiable** (Opus is right about this one; adopted).
- `fleet-gateway/clients/rust/src/lib.rs` — same contract for the Rust daemons (fleet-cns's own alerts go through it).
- `fleet-gateway/clients/sh/fleet-gw` — curl wrapper for shell one-offs.
- `fleet-gateway/src/taxonomy.rs` — the error taxonomy as types: `AuthError` (no retry, alarm), `RateLimited` (backoff), `EmptyResponse` (retry ×2 then next chain entry — the maritime 0.000 bug), `Timeout`.
- `scripts/migrate-distillation-loop.py` — rewrites `distillation_loop.py:247` `_curl_post_json` to import the shim. First consumer, highest value, measurable the same night.
- `~/.config/systemd/user/fleet-gateway.service` — already in repo; install + enable.

**Tests to write:**
- `fleet-gateway/tests/test_failopen.py` — gateway killed mid-suite; shim must complete calls direct-to-vendor with ≤1 added round-trip of latency.
- `fleet-gateway/tests/test_taxonomy.rs` — 401 → no retry + alarm event in spool; empty 200 → exactly 2 retries then chain advance; 429 → rotate only if a second key exists (already in README behavior — pin it in a test).
- `fleet-gateway/tests/test_shared_breaker.rs` — two concurrent shim processes; one trips the breaker, the other must see OPEN within one poll interval. This is the whole reason the gateway is a service, not a library — test it or the argument was for nothing.
- `fleet-gateway/tests/test_streaming_bounded.rs` — 512 MiB streamed response through the proxy; assert gateway RSS stays < 150 MiB.

**Acceptance criteria:**
1. `distillation_loop.py` runs a full overnight batch with one provider key revoked mid-run: zero 0.000 scores attributable to auth, alarm event present in spool.
2. `kill -9` on the gateway; all three shim runtimes continue working (degraded mode, logged).
3. `GET /health` exposes per-provider breaker state; dashboard reads it.
4. **Embeddings are absent from every fallback chain** — config schema rejects an embedding route with a chain longer than 1.

---

## Phase 4 — memory-indexer + the memory schema (the cargo holds)

**Goal:** replace the OpenClaw reindex path with a streaming, checkpointed, provenance-tagged indexer. Applies `memory/fleet-memory-schema-kimi.sql` verbatim.

**Data flow:** snapshot manifest (frozen at start) → reader → bounded channel (cap 64) → embedder (batches of 32, current provider ONLY) → writer → single transaction per batch that inserts chunks + vectors + advances `reindex_checkpoints`. Cutover: build `index.<provider>.<model>.<dims>.db` beside the serving one, flip `index_registry.is_current` + `current` symlink, old file stays readable.

**Files to create:**
- `fleet-memory/Cargo.toml`, `src/main.rs`, `src/lib.rs`
- `fleet-memory/migrations/0001_registry.sql`, `0002_index_template.sql` — generated from `memory/fleet-memory-schema-kimi.sql` (single source of truth; the .sql file is canonical, migrations are produced, never hand-edited).
- `fleet-memory/src/snapshot.rs` — freeze input set (path, mtime_ns, size, sha256) to manifest before first batch.
- `fleet-memory/src/chunker.rs` — char-offset chunking, `chunker_version` stamped into `index_meta`.
- `fleet-memory/src/embedder.rs` — trait `Embedder`; impls `OllamaEmbedder` (now), `OnnxEmbedder` (stubbed for Phase 6). Constructed from `embedding_providers` row; refuses any provider where `(model, dims) != index_meta`.
- `fleet-memory/src/reindex.rs` — the pipeline; `flock(2)` on a guard file, **no PID files, no staleness heuristics** — the kernel is the staleness detector.
- `fleet-memory/src/query.rs` — the three reference queries from the schema §4, as CLI subcommands: `fleet-memory find <phrase>`, `fleet-memory renders <slug>`, `fleet-memory decided <date>`.
- `fleet-memory.service` — `MemoryMax=1G`, `Type=oneshot` + timer for scheduled runs.

**Tests to write:**
- `tests/test_provenance_refusal.rs` — point the indexer at a 768-dim index with a 1024-dim provider: hard error before the first insert, exit ≠ 0.
- `tests/test_checkpoint_resume.rs` — start a 500-doc run, `kill -9` at ~40%, rerun: resumes at cursor, zero duplicate chunks (`UNIQUE(doc_id, seq)` verified), total chunks identical to an uninterrupted control run.
- `tests/test_bounded_rss.rs` — full corpus under `systemd-run -p MemoryMax=1G`; assert completion and record `peak_rss_bytes` into the checkpoint row.
- `tests/test_snapshot_isolation.rs` — modify a source file mid-run; the run's output must reflect the frozen manifest, and the modification queues for the *next* run. Kills "index changed while building."
- `tests/test_one_current.rs` — attempt to mark a second index current: rejected by the partial unique index.
- `tests/test_three_queries.rs` — fixture DB; the Q1/Q2/Q3 queries from the schema return the fixture answers. The schema and its queries are tested together or not at all.

**Acceptance criteria:**
1. Full 4,636-file corpus indexes under `MemoryMax=1G`, resumable after SIGKILL.
2. Provider change = new file + symlink swap; the old index keeps serving queries during the build; rollback is one `ln -sf` and one `UPDATE`.
3. `fleet-memory decided 2026-08-13` returns this decision.
4. All state files verified on ext4; a `CHECK` and a startup assertion both reject `/mnt/c` paths.

---

## Phase 5 — fleet-audio (the engine room, bounded)

**Goal:** render a 10-minute piece with peak RSS independent of duration. **Python chunked renderer ships first (1 day); the Rust engine follows only if profiling shows compute-bound** — this is where I now agree with Opus's sequencing over my original week-4 Rust plan. His fifteen-line Python fix satisfies the O(chunk) rule *today*; the Rust renderer is an upgrade, not the fix.

**Data flow:** Python composes a score → emits a spec JSON → renderer (Python now, Rust later, same spec format) → bounded channel of recycled f32 chunk buffers → streamed WAV → registered as a `work_renders` row with `spec_json` attached.

**Files to create:**
- `tapscript-studio/src/tapscript_studio/spec.py` — the score→spec emitter. The spec format is the contract; it outlives either renderer.
- `tapscript-studio/src/tapscript_studio/render_chunked.py` — chunked f32 renderer (Opus's §3 sketch, productionized: voices as generators, `np.clip`→int16 on write, wave module streaming).
- `fleet-audio/` — Rust engine, **Phase 5b, gated on a profiler report**: `src/main.rs`, `src/engine.rs` (4096-frame ring, arena-recycled buffers, `hound` writer), `src/spec.rs` (same spec JSON via serde).
- `scripts/register_render.py` — every render lands in `work_renders` with sha256, duration, renderer version, spec. Media >1 MiB → R2 key, not ext4 path.

**Tests to write:**
- `tests/test_render_bounded.py` — 10-minute render under `MemoryMax=2G`; the cap is the test. Also render 10 seconds; peak RSS delta must be < 10%.
- `tests/test_render_determinism.py` — same spec twice → byte-identical WAV (seeded). This is what makes `spec_json` in the registry meaningful.
- `tests/test_spec_roundtrip.py` — every spec the emitter produces parses under the Rust engine's serde types (when 5b lands). One format, two renderers, zero drift.
- `tests/test_render_registered.py` — after a render, exactly one new `work_renders` row exists, with matching sha256.

**Acceptance criteria:**
1. 10-minute stereo render completes with `MemoryMax=2G`; no numpy process ever again exceeds its fence (journald shows the cgroup enforcing).
2. A render row exists for every output file — the registry and the filesystem agree.
3. Profile report filed: if synthesis is >70% wall-clock after chunking, Phase 5b proceeds; otherwise Rust engine is deferred with the evidence on record.

---

## Phase 6 — GPU floor: local embeddings, conditional TTS (the crow's nest)

**Goal:** an embedding model that cannot die with an API key; TTS as insurance, never as a dependency. **The VRAM budget dispute gets settled by protocol, not by dueling readings** — Opus measured 130 MiB baseline, I measured 3.3 GiB in use; both true at their moments, because Ollama TTLs make residency transient.

**Files to create:**
- `scripts/vram-budget-probe.sh` — samples `nvidia-smi` + `ollama ps` every 60s for 48h of normal fleet operation → `logs/vram-budget.jsonl`. The residency budget is *derived from this file*, not from either proposal.
- `fleet-memory/src/embedder_onnx.rs` — `OnnxEmbedder` impl (bge-small class, CUDA EP via ONNX Runtime). Registered in `embedding_providers` with `quality_tier = 2`, `fallback_allowed = 0` still — it is the floor by *choice in config*, never by silent chain advance.
- `scripts/living-minds-serialize.py` — Living Minds daemon: load-on-demand + idle eviction instead of five warm models. This is the single largest VRAM/RAM win available (Opus's §5 standing constraint; adopted).
- `fleet-gateway` config: `tts` route with `quantized-local` as a *load-on-demand* chain entry behind API TTS — only if the probe shows ≥1.5 GiB headroom at p95.

**Tests to write:**
- `tests/test_onnx_parity.rs` — same 100 chunks embedded by Ollama and ONNX impls of the *same model*: cosine ≥ 0.999 per pair. (Different models get different indexes — parity is only checked within one provenance.)
- `tests/test_tts_never_blocks.py` — TTS chain with all providers down: the caller gets a structured failure, never a hang, never a silent skip.

**Acceptance criteria:**
1. `logs/vram-budget.jsonl` exists, 48h, and the residency decision cites it.
2. Fleet survives 24h with all external embedding APIs blocked at the firewall: search quality degrades per plan, availability does not.
3. Living Minds host-RAM footprint drops measurably (before/after in the phase report).

---

## Phase 7 — memory consolidation (the chart room opens)

**Goal:** the fleet's memory becomes queryable as one plane — documents, works, renders, decisions — and the 3.7 GiB `ai-writings/.git` stops growing.

**Data flow:** backfill streams the corpus (O(batch), reuses Phase 4's snapshot+chunker) → registry; agents write `agent_decisions` rows at decision time; nightly sync keeps `work_text_fts` current; pre-commit hook keeps media out of git.

**Files to create:**
- `scripts/backfill-registry.py` — walk `ai-writings/` + `connections/` + `creative/` + `radio/`; create `creative_works` rows (kind inferred from path, slug from filename), `work_renders` rows for existing files, `work_subjects` from frontmatter where present. Streams, checkpoints into `reindex_runs` with `trigger_kind='manual'`.
- `scripts/fts-sync.py` — nightly `Type=oneshot` unit: upsert new/changed text renders into `work_text_fts`.
- `ai-writings/hooks/pre-commit` — reject blobs >1 MiB with a message naming the R2 upload command. F6's media policy, enforced at the boundary.
- `scripts/decision.py` — agent-facing CLI: `decision log --domain infra --summary "..." --links file:...`. Writing a decision becomes a 5-second act, which is the only way the log gets written.
- `memory/DASHBOARD.md` regenerated nightly: current index, last reindex, breaker states, recent decisions, works awaiting renders.

**Tests to write:**
- `tests/test_backfill_idempotent.py` — run backfill twice: identical row counts, zero duplicate slugs.
- `tests/test_backfill_bounded.py` — backfill under `MemoryMax=512M` over the full tree.
- `tests/test_precommit_hook.sh` — a 2 MiB blob is rejected; an r2:// manifest entry is accepted.
- `tests/test_fts_freshness.py` — insert a text render, run fts-sync, `MATCH` finds it.

**Acceptance criteria:**
1. Q1 ("pieces about silence") returns results from all three lanes: subjects, FTS, semantic.
2. Q2 ("all renders for the PFD speech") returns outline → text drafts → TTS → TapScript, ordered.
3. Q3 ("decided on Aug 13") returns the day's decisions with their `decision_links`.
4. `ai-writings/.git` growth rate measured for a week: media blobs = 0.
5. Backup of the entire memory plane = `cp fleet-memory.db index.*.db` — demonstrated, timed, under 60s.

---

## Dependency map (why this order)

```
P3 gateway ──────────────┐ (shims call it; embedder health reads it)
                         ▼
P4 memory-indexer ──────▶ P6 ONNX floor (embedder trait + provider table)
   │  ▲ schema applied here
   │  └── P5 render registration writes work_renders into the same registry
   ▼
P7 consolidation (backfill needs P4's chunker; decision CLI needs P4's DB;
                  render registry needs P5)
```

No phase edits another phase's frozen files; every phase ends with a query a human can run to see it working. That is the whole chart: **bounded buffers, classified errors, managed processes — and a memory plane you can interrogate like a chart, not excavate like a wreck.**

*— KimiCode, Navigation. Soundings taken on the live machine, 2026-08-13.*
