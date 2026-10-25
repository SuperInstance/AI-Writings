# Fleet Technical Roadmap — Phases 3 through 7

**Author:** Claude Opus 5 (Strategic Operations)
**Date:** 2026-08-13
**Companions:** `memory/fleet-infrastructure-redesign.md` (design),
`memory/kimi-infrastructure-proposal.md` (KimiCode's independent proposal),
`memory/fleet-memory-schema-opus.sql` (Phase 3's deliverable),
`memory/2026-08-13.md` (what shipped today)

---

## 0. Where we actually are

Phases 1 and 2 are done, today, and verified:

| | Status | Evidence |
|---|---|---|
| **Phase 1** — systemd coverage | ✅ | 10 units running, 0 failed, `MemoryMax` on all |
| **Phase 2** — `fleet-gateway` | ✅ | 1,249 lines, live on `:8787`, breaker + key chain + fallback, first call tested, pushed |
| **Phase 3** — memory index | 🔄 | subagent building; schema now specified |

Two rules from today govern everything below and are not renegotiable:

1. **Memory is O(chunk) or O(batch). Never O(corpus) or O(duration).** Any
   design whose peak RSS grows with input is rejected at review, in any
   language.
2. **No code passes through a shell.** List argv, always. No heredocs, no
   `python3 -c`, no `shell=True`.

A third rule I want to add now, because Phases 3–7 are where it starts to
matter: **every phase ships with the assertion that proves its own core
claim.** Phase 3 claims bounded memory — so Phase 3's CI measures peak RSS and
fails the build on regression. A performance guarantee without a test is a
comment.

### Ordering principle

Phases are ordered by *risk removed per hour*, with one override: **Phase 5
must precede the R2 media offload**, because you cannot safely move 3.7 GB of
blobs out of git until a registry records where each one went. That single
dependency is why the creative registry outranks the GPU work.

---

## Phase 3 — `fleet-memory`: the bounded, provider-safe index

**Closes:** F1 (all four sub-failures)
**Language:** Rust · **Estimate:** 3–4 days · **Status:** in progress

### What it is

A Rust binary that owns the memory database: builds indexes, serves search,
and is the only writer. Two databases per
`memory/fleet-memory-schema-opus.sql`: durable `fleet.db`, disposable
`index.<provider>.<model>.<dims>.r<rev>.db` reached through a `current`
symlink.

### Files to create

```
fleet-memory/
  Cargo.toml
  README.md
  fleet-memory.service                  # MemoryMax=1G, Restart=always,
                                        # StartLimitIntervalSec/Burst in [Unit]
  migrations/
    0001_fleet.sql                      # Part A of the schema, verbatim
    0002_index.sql.tmpl                 # Part B; {{DIMS}} substituted at build
  src/
    main.rs                             # clap: index | search | status |
                                        #       promote | verify | serve
    lib.rs
    error.rs                            # thiserror; no unwrap outside tests
    db.rs                               # open, pragmas, migrate, ATTACH current
    space.rs                            # embedding_space registry; filename
                                        #   <-> header <-> row verification
    guard.rs                            # flock(2) on reindex.lock. ~40 lines.
                                        #   No PID. No expiry. No table.
    corpus.rs                           # snapshot the input set at run start
    chunk.rs                            # heading-aware markdown chunker
    embed.rs                            # trait Embedder; gateway + ollama impls
    pipeline.rs                         # bounded mpsc(64): read -> embed -> write
    checkpoint.rs                       # reindex_run / reindex_checkpoint
    promote.rs                          # seal header, swap symlink, flip is_current
    search.rs                           # RRF hybrid: vec0 KNN + FTS5 bm25
    serve.rs                            # axum on 127.0.0.1:8788
  tests/
    test_guard.rs
    test_space.rs
    test_pipeline.rs
    test_search.rs
    test_promote.rs
    test_resume.rs
  benches/
    bench_memory.rs                     # the RSS assertion
```

### Design points that are not negotiable

**Embeddings do not participate in provider fallback.** The gateway's fallback
chain is correct for creative generation and fatal for embeddings — silently
swapping `nomic-embed-text` for anything else corrupts the index, which is
F1.1 wearing a helpful disguise. `embed.rs` calls the gateway with
`X-Fleet-No-Fallback: 1` and treats a fallback response as a hard error.

**The lock is `flock(2)`, and there is no lock table.** The kernel releases it
on process death by any means including SIGKILL. Any design that stores lock
ownership in a row or a file has reinvented the deadlock we are fixing.

**The corpus is snapshotted at run start.** `corpus.rs` materialises the
document id list into `reindex_run.planned_documents` before the first embed.
Files arriving mid-run belong to the next run. This is the fix for "index
changed while building", which the daily log recorded and neither proposal
scheduled.

**Promotion is two-phase.** Build to a temp filename with
`index_header.sealed_at = NULL`; the loader refuses to serve any index whose
`sealed_at` is NULL. Only after the final commit does `promote.rs` seal the
header, `ln -sf` the symlink, and flip `is_current` — in that order, so a crash
at any point leaves the previous index serving.

### Tests to write

| Test | Asserts |
|---|---|
| `test_guard::second_holder_blocks` | Two processes; second gets `WouldBlock`, not a hang |
| `test_guard::sigkill_releases` | Spawn holder, `SIGKILL` it, next acquire succeeds **immediately** — the regression test for the entire F1.3 bug class |
| `test_space::dim_mismatch_rejected` | 1024-dim vector into a 768-dim index → `Err`, never a silent write |
| `test_space::header_filename_disagree` | Rename the file; open must fail loudly |
| `test_space::unsealed_never_serves` | `sealed_at IS NULL` → open returns `Err` |
| `test_pipeline::backpressure` | Slow writer stalls the reader; channel depth never exceeds 64 |
| `test_resume::kill_and_continue` | SIGKILL at 40% → restart → no document embedded twice, none skipped (compare `document_index_state` row counts and shas) |
| `test_resume::stale_running_marked` | Orphaned `running` row + unheld flock → next run marks it `interrupted` |
| `test_search::rrf_beats_either_alone` | Fixed 30-doc fixture; "silence" query must return the negative-space essay (vector-only hit) *and* "On the Preservation of Silence" (lexical hit) in the top 5 |
| `test_promote::crash_mid_swap` | Kill between seal and symlink → old index still serves, `verify` reports the discrepancy |
| `bench_memory::full_corpus_bounded` | 4,636-file corpus, peak RSS asserted |

### Acceptance criteria

- [ ] `cargo test` green, `cargo clippy -- -D warnings` clean.
- [ ] Full-corpus reindex completes under `systemd-run --user --scope -p MemoryMax=1G`,
      and **peak RSS is recorded in `reindex_run.peak_rss_bytes` at under 400 MB**.
      The cap is the test; the recorded number is the regression baseline.
- [ ] `SIGKILL` mid-reindex, restart, complete — zero re-embedded documents.
      Prove it: `SELECT COUNT(*) FROM document_index_state` before and after.
- [ ] Provider swap `nomic-embed-text` → `bge-m3` builds a second index while
      the first keeps answering searches throughout. Demonstrate with a search
      running in a loop during the build.
- [ ] Rollback is `ln -sf` + one `UPDATE`; demonstrated live, under 5 seconds.
- [ ] Q1, Q2, Q3 from the schema file return correct results against the real
      corpus. These are the acceptance queries, not illustrations.
- [ ] `fleet-memory.service` installed, lingering, survives WSL restart.
- [ ] `fleet-memory verify` exits non-zero on any header/filename/row mismatch.

### Risk

The chunker is the sleeper. A bad chunk boundary degrades retrieval in a way
no test catches and no error reports — it just makes the memory feel dull.
Mitigation: `chunk.rs` splits on markdown headings first and only falls back to
token windows inside a section, and `test_search` uses a hand-labelled fixture
so quality regressions are visible.

---

## Phase 4 — Streaming audio: kill the 16 GB renderer

**Closes:** F2 · **Estimate:** 4a is one day, 4b is three
**Split into 4a and 4b on purpose.**

Today's log commits to "Rust streaming audio renderer" and I think that is the
right destination. It is the wrong thing to do *first*. The bug is burning host
RAM now; the Python fix is fifteen lines and lands tomorrow. Ship 4a
immediately, then decide 4b on evidence.

### Phase 4a — chunked Python renderer (1 day)

**Files:**
```
scripts/audio/render.py                 # chunked, float32, int16 on write
scripts/audio/voices.py                 # Voice protocol: render(start, n) -> ndarray
                                        #   generators, never full-length arrays
scripts/audio/spec.py                   # the render spec Python emits
tests/audio/test_render_memory.py
tests/audio/test_render_correctness.py
```

The core is already written, in `fleet-infrastructure-redesign.md` §3: a 5-second
chunk at float32 is 1.7 MB, so a 10-minute piece costs what a 10-second one
costs.

**Tests:**

| Test | Asserts |
|---|---|
| `test_render_memory::ten_minutes_bounded` | 10-min render under `MemoryMax=2G`; peak RSS from `/proc/self/status` **VmHWM under 150 MB** |
| `test_render_memory::duration_independent` | Peak RSS for 10 min is within 10% of peak RSS for 10 s. This is the real claim — the cap only proves we didn't exceed it, this proves the memory model |
| `test_render_correctness::chunk_boundary_continuity` | Render one piece at chunk sizes 4096 and 44100; outputs must be sample-identical. Catches phase discontinuity at seams — the bug chunking invites |
| `test_render_correctness::no_clipping_regression` | Golden 8-second fixture, sample-exact |
| `test_render_correctness::float32_audible_parity` | float32 vs float64 render: max abs diff below −90 dBFS |

**Acceptance:**
- [ ] 10-minute stereo render completes with VmHWM under 150 MB. Recorded in
      `render_job.peak_rss_bytes`.
- [ ] `MemoryMax=2G` unit wrapper; render survives with the fleet under load.
- [ ] Old renderer deleted, not deprecated. A working unbounded path will be
      used by something at 3am.
- [ ] Grep proves no heredoc launches remain in the audio pipeline:
      `grep -rn "python3 <<\|python3 -c" scripts/ | wc -l` → 0.

### Phase 4b — `fleet-audio` in Rust (3 days, **conditional**)

Only if 4a's profile shows synthesis is CPU-bound at more than 0.25× realtime,
or the mix graph outgrows numpy. I expect neither. **Kill criterion stated up
front so this does not become three days spent on a solved problem.**

```
fleet-audio/{Cargo.toml, README.md, src/{main,spec,voice,graph,ring,wav}.rs,
             tests/{test_ring.rs, test_parity.rs}}
```

`test_parity.rs` renders the same spec through Python 4a and Rust 4b and
asserts bit-identical int16 output. If they disagree, one of them is wrong and
we find out in CI rather than in a listening session.

---

## Phase 5 — Creative registry, ingest, and the R2 offload

**Closes:** F6 (which has no owner in KimiCode's plan) and turns the schema
from a design into memory · **Estimate:** 3 days

This is the phase that makes the fleet's creative output *findable*. 519 files
in `ai-writings`, 17 mp3s, a tree of tapscript `.tap`/`.mid`/`.wav` — currently
discoverable only by remembering the filename.

### Files to create

```
fleet-memory/src/registry.rs            # work / artifact / DAG writes
fleet-memory/src/ingest/
  mod.rs
  writings.rs                           # ai-writings/*.md -> document + work
  audio.rs                              # *.mp3/*.wav -> artifact (ffprobe duration)
  tapscript.rs                          # *.tap -> artifact + voice_profile extract
  link.rs                               # infer artifact_input edges
scripts/ingest/backfill.py              # one-shot historical backfill, resumable
fleet-memory/tests/
  test_ingest_writings.rs
  test_ingest_link.rs
  test_registry_dag.rs
tools/r2-offload/
  offload.py                            # register -> upload -> verify -> unlink
  verify.py                             # every r2 artifact is fetchable
.githooks/pre-commit                    # reject blobs >1 MiB in ai-writings
```

### The linking problem, stated honestly

`link.rs` infers derivation edges from filenames: `puffins-dont-quit-tts.mp3`
and `puffins-dont-quit-v2-tts.mp3` share a stem, so v2 is `revision_of` v1.
This works for the fleet's naming conventions and **will get some edges wrong**.

So: inferred edges are written with `role` set from the filename rule, and
`backfill.py` emits `logs/ingest-review.md` listing every inferred edge with
its confidence. Casey reviews once, corrections go in as data. The alternative
— refusing to infer and requiring 500 manual links — means the registry never
gets populated, which is worse than a registry with a few wrong edges and a
review file.

### R2 offload sequencing (this order, no shortcuts)

1. Register every media artifact in `fleet.db` with `storage='local'` + sha256.
2. Upload; set `storage='both'`; verify sha256 by re-download.
3. Only then set `storage='r2'` and remove the local blob.
4. `.git` history rewrite is a **separate, Casey-supervised** decision. It needs
   ~8 GB free and the fleet stopped. Not in this phase.

Step 2 is not optional. A registry that says a file is in R2 when it isn't is
worse than no registry, because it authorises the deletion.

### Tests

| Test | Asserts |
|---|---|
| `test_ingest_writings::idempotent` | Run twice → identical row counts. Ingest must be re-runnable |
| `test_ingest_writings::sha_change_reindexes` | Edit a file → exactly that document goes stale in `v_stale_document` |
| `test_registry_dag::no_cycles` | Insert a cycle attempt → rejected; Q3's depth fence never engages in practice |
| `test_registry_dag::q3_pfd` | Fixture reproducing the PFD work: 3 renders, 2 naming conventions, 1 outline. Q3 returns all three |
| `test_ingest_link::v2_revision_edge` | `*-v2-tts.mp3` links `revision_of` its v1 |
| `r2-offload::no_delete_before_verify` | Fault-inject an upload failure → local blob still present, `storage` still `'local'` |
| `pre-commit` hook test | Staging a 2 MiB mp3 in `ai-writings` exits non-zero |

### Acceptance criteria

- [ ] All 519 `ai-writings` documents, all 17 mp3s, and the tapscript tree are
      registered. Verify: `SELECT COUNT(*) FROM artifact GROUP BY kind`.
- [ ] Q3 answers "what renders exist for the PFD speech" correctly against real
      data — three renders, correct lineage, correct voice profiles.
- [ ] `logs/ingest-review.md` generated; Casey signs off on inferred edges.
- [ ] `ai-writings` working tree drops below 200 MB of media; `.git` unchanged
      (history rewrite deferred, and said so).
- [ ] Pre-commit hook installed and demonstrated rejecting a large blob.
- [ ] Every `storage='r2'` artifact fetched and sha-verified by `verify.py`.

---

## Phase 6 — Retrieval service and the local embedding floor

**Closes:** the dependency on a remote provider for the fleet's own memory
**Estimate:** 3 days

Two things, in this order, because the second is only worth doing once the
first proves the retrieval quality bar.

### 6a — `fleet-memory serve` becomes the fleet's recall API

```
fleet-memory/src/serve.rs               # extend Phase 3's skeleton
fleet-memory/src/rerank.rs              # optional cross-encoder stage
fleet-memory/src/scope.rs               # session.channel privacy filter
clients/
  fleet_recall.py                       # fail-open client shim
  fleet-recall.sh
fleet-memory/tests/
  test_serve_api.rs
  test_scope_privacy.rs
```

Endpoints: `POST /search` (hybrid, filters, k), `GET /work/:slug`,
`GET /decisions?from=&to=`, `GET /health`, `GET /status`.

**`scope.rs` is a security control, not a feature.** `AGENTS.md` forbids
loading `MEMORY.md` in shared contexts; the moment recall is an API, a Discord
subagent can ask for anything. Every request carries a scope; `channel='main'`
content is never returned to a `shared` caller. `test_scope_privacy.rs` is the
test that must never be marked flaky and skipped.

Client shims **fail open**, same rule as the gateway: if `fleet-memory` is
down, callers fall back to grep over the filesystem. Degraded recall, never a
blocked agent.

### 6b — local embedding model on the 4050

The GPU measured **130 MiB of 6141 MiB in use** with `ollama ps` empty. There
is no display floor and no 500 MB ceiling — KimiCode measured a transient
Ollama TTL and designed against it. `nomic-embed-text` at 274 MB is
comfortable, and so is a quantised TTS model later.

```
fleet-memory/src/embed/local.rs         # candle or ort, CUDA execution provider
fleet-memory/tests/test_embed_parity.rs
scripts/ops/gpu-watch.sh                # /usr/lib/wsl/lib on PATH; nvidia-smi
```

**Tests:**

| Test | Asserts |
|---|---|
| `test_embed_parity::local_vs_remote` | Same 200 texts through both paths; **cosine similarity ≥ 0.999 per pair**. Below that the two are different spaces and must not share an index file |
| `test_embed_parity::deterministic` | Same input twice → bit-identical vectors |
| `test_serve_api::fail_open` | Kill the service; `fleet_recall.py` returns grep results, exit 0 |
| `test_scope_privacy::shared_cannot_read_main` | `channel='shared'` request never returns `channel='main'` rows |

**Acceptance criteria:**
- [ ] `/search` p95 under 150 ms on the full corpus.
- [ ] Local embedder produces vectors with per-pair cosine ≥ 0.999 vs remote —
      **or it gets its own `embedding_space` row and its own index file.** No
      "close enough" sharing.
- [ ] Full reindex with the local embedder, network disconnected, completes.
- [ ] Resident VRAM measured and recorded; Living Minds daemon switched to
      serialised load-on-demand with idle eviction (it is the largest all-day
      memory consumer and it keeps five models warm for no measured benefit).
- [ ] GPU + per-service RSS on the fleet dashboard. *We were blind to a 16 GB
      process for twenty minutes.*

---

## Phase 7 — Closing the loop: decisions, sessions, retention

**Closes:** the gap between "the fleet decides things" and "the fleet remembers
deciding them" · **Estimate:** 3 days

Phases 3–6 build the memory. Phase 7 is what fills it automatically, and it is
the phase that makes the whole stack pay off. Today's decisions were captured
because I wrote them into a markdown file by hand. That does not scale past the
days someone remembers to do it.

### Files to create

```
fleet-cns/src/sink/                     # spool events -> fleet.db
  mod.rs
  health.rs                             # provider_health_event
  api_call.rs                           # api_call ledger
  session.rs                            # session / message / tool_call
fleet-gateway/src/emit.rs               # emit breaker + call events to spool
tools/decisions/
  record.py                             # `fleet decide "title" --why ... --supersedes N`
  extract.py                            # propose decisions from a session; human confirms
fleet-memory/src/retention.rs           # 90-day rollup for the three growing tables
fleet-memory/src/backup.rs              # sqlite .backup, nightly, verified restore
dashboard/
  fleet-status.py                       # one page: services, breakers, index, RSS, GPU
fleet-memory/tests/
  test_retention.rs
  test_backup_restore.rs
  test_sink_idempotent.rs
```

### The one thing I will not automate

`extract.py` **proposes** decisions from a session transcript; a human confirms
before the row lands with `status='accepted'`. An LLM writing directly into the
decision log means the fleet's institutional memory is a hallucination surface,
and every downstream query inherits it. Proposals land as `status='proposed'`
and are visibly distinct in `v_decision_current`.

### Retention

`api_call`, `provider_health_event`, and `tool_call` are the only unbounded
tables in the schema. Rows older than 90 days collapse into daily aggregates.
This is the O(chunk) rule applied to storage — the same rule, one layer down.

### Tests

| Test | Asserts |
|---|---|
| `test_sink_idempotent::replay` | Replay the same spool offsets → no duplicate rows |
| `test_retention::rollup_preserves_totals` | Cost and failure-count sums identical before and after rollup |
| `test_retention::bounded_growth` | Simulate 1M calls → table size plateaus |
| `test_backup_restore::round_trip` | Backup → restore to temp → **all Q1–Q7 return identical results.** A backup that has not been restored is a rumour |
| `test_decision::supersede_chain` | Reversal chain of 3 → `v_decision_current` shows exactly one |

### Acceptance criteria

- [ ] Every gateway call lands in `api_call` within 5 seconds, automatically.
- [ ] Every breaker transition lands in `provider_health_event`.
- [ ] Q4 answers "was a provider dying at 02:14" from real captured data —
      the maritime 0.000 bug becomes diagnosable in one query.
- [ ] Nightly backup runs under systemd timer; **a restore is performed and
      verified weekly**, not just a backup taken.
- [ ] `fleet-status.py` shows services, breaker states, index health, per-service
      RSS, and GPU in one screen.
- [ ] `fleet decide` used for real decisions for one week; `SELECT COUNT(*) FROM
      decision WHERE decided_at >= <week ago>` is non-trivial.

---

## Summary

| Phase | Closes | Days | Ships |
|---|---|---|---|
| **3** | F1 | 3–4 | `fleet-memory` — bounded, resumable, provider-safe index |
| **4a** | F2 | 1 | Chunked Python renderer; 16 GB → 150 MB |
| **4b** | — | 3 | `fleet-audio` in Rust, **conditional on profiling** |
| **5** | F6 | 3 | Creative registry, ingest, R2 offload with verify-before-delete |
| **6** | provider dependency | 3 | Recall API with privacy scoping + local embedding floor |
| **7** | memory decay | 3 | Automatic capture, retention, verified backups, dashboard |

**Critical path: 13 days.** 4b is off it by design.

### What I am explicitly not proposing

| Not doing | Why |
|---|---|
| Go | Fourth language. Rust covers the same ground with nine repos of fleet experience behind it. |
| Mojo | Solves compute; our bottleneck is memory. Revisit in ~12 months. |
| Hand-written CUDA/PTX | GPU measured at 2%. Would optimise an idle resource. |
| Qdrant / Weaviate | A separate service with a resident-RAM tax, for a single-operator fleet. `sqlite-vec` in the file we already have; backup is `cp`. |
| Rewriting orchestration in Rust | LLM-call-bound. Python's speed is irrelevant; its ecosystem is not. |
| `ai-writings` history rewrite | Needs ~8 GB free and the fleet stopped. Casey's call, its own maintenance window, not smuggled into Phase 5. |

### The three claims each phase must survive

Every phase above is written so it can fail visibly:

1. **The memory claim is measured, not asserted.** Phases 3, 4a and 7 record
   peak RSS into the database and fail CI on regression.
2. **The recovery claim is exercised, not assumed.** Phases 3, 5 and 7 each
   include a kill-and-resume or restore-and-verify test. A backup nobody has
   restored is a rumour; a resume path nobody has SIGKILLed is a hope.
3. **The correctness claim has a named query.** Q1, Q2 and Q3 from
   `fleet-memory-schema-opus.sql` are acceptance criteria for Phases 3 and 5,
   not documentation.

If a phase ships without its assertion, it has not shipped.

---

*Roadmap, 2026-08-13. Hardware figures, service states, corpus counts and file
paths measured on the live machine. Phases 1 and 2 already complete; this
document begins where today's work stopped.*
