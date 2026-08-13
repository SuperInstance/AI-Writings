-- ============================================================================
-- FLEET MEMORY DATABASE — SCHEMA
-- ============================================================================
--
--   Author:  Claude Opus 5 (Strategic Operations)
--   Date:    2026-08-13
--   Target:  SQLite >= 3.45 (STRICT tables, FTS5) + sqlite-vec >= 0.1.6
--   Companion designs: memory/fleet-infrastructure-redesign.md  (§3, F1)
--                      memory/kimi-infrastructure-proposal.md   (§2.1)
--   Roadmap: memory/fleet-roadmap-opus.md  (Phase 3 ships Part A + Part B)
--
-- ----------------------------------------------------------------------------
-- WHY THIS IS TWO DATABASES, NOT ONE
-- ----------------------------------------------------------------------------
--
-- Both designs agreed the vector index carries its provenance in its filename
-- (`index.<provider>.<model>.<dims>.db`) and that a provider change builds a
-- NEW index while the old one keeps serving, with `current ->` swapped
-- atomically. That is correct, and it has a consequence neither proposal
-- stated:
--
--     *** A symlink swap discards everything stored beside the vectors. ***
--
-- Session transcripts, decision logs and the creative works registry are the
-- fleet's actual memory. They must outlive every reindex, every provider
-- change, and every rollback. Embeddings are derived data and are disposable
-- by design. Putting them in one file means either (a) you cannot swap, or
-- (b) you lose the transcripts. So:
--
--   PART A   fleet.db                             DURABLE.  Never rebuilt.
--            Documents, sessions, decisions, works, artifacts, providers,
--            reindex bookkeeping. Backed up. Survives everything.
--
--   PART B   index.<provider>.<model>.<dims>.db   DISPOSABLE. Rebuilt freely.
--            Chunks, vectors, full-text. Reachable as `current`. Delete it
--            and the fleet loses speed, never memory.
--
--   PART C   ATTACH, views, and the queries that cross the boundary.
--
-- The join key across the boundary is `document.content_sha256` — a value that
-- is stable, content-addressed, and independent of any embedding model. Chunk
-- ids are NOT stable across reindexes and are never referenced from Part A.
--
-- ----------------------------------------------------------------------------
-- WHAT IS DELIBERATELY ABSENT
-- ----------------------------------------------------------------------------
--
--   * There is NO lock table, NO `locked_by` column, NO `lock_expires_at`.
--     Single-writer exclusion is `flock(2)` on `<state_dir>/reindex.lock`,
--     released by the kernel when the holder dies by any means including
--     SIGKILL. A lock row in a database is a PID file wearing a nicer hat and
--     reintroduces the exact deadlock this schema exists to kill (F1.3).
--
--   * There is NO `embedding BLOB` column on a normal table. Vectors live only
--     in `vec0`, whose dimension is a DDL constant. A 1024-dim vector cannot be
--     inserted into a 768-dim index — not "is rejected by a CHECK", cannot.
--
--   * There is NO cross-database foreign key. SQLite does not enforce them.
--     Where Part B references Part A, the reference is a content hash and the
--     invariant is asserted by `index_header` + a startup check, not pretended.
--
-- ----------------------------------------------------------------------------
-- CONVENTIONS
-- ----------------------------------------------------------------------------
--
--   * Timestamps are TEXT, ISO-8601, UTC, 'YYYY-MM-DDTHH:MM:SSZ'. For UTC
--     ISO-8601 lexicographic order IS chronological order, so BETWEEN and
--     range scans work on a plain index, and a human grepping the file can
--     read them. "Decisions from Aug 13" is a prefix comparison. See Q2.
--   * All non-virtual tables are STRICT. Typed storage is the same discipline
--     as serde typed packets in fleet-cns: no silent coercion.
--   * Enumerations are CHECK constraints, not lookup tables. They change at
--     the speed of migrations, not of data.
--   * `id` columns are INTEGER PRIMARY KEY (rowid aliases). Natural keys get
--     a UNIQUE index alongside.
--
-- ============================================================================


-- ############################################################################
-- ############################################################################
--   PART A — fleet.db   (DURABLE)
-- ############################################################################
-- ############################################################################

PRAGMA journal_mode = WAL;          -- crash-safe; concurrent readers
PRAGMA foreign_keys = ON;           -- must be set per-connection, every time
PRAGMA synchronous = NORMAL;        -- WAL + NORMAL is durable across process
                                    -- crash; only a host power loss can lose
                                    -- the last commits. Correct for ext4.
PRAGMA busy_timeout = 5000;
PRAGMA temp_store = MEMORY;
PRAGMA mmap_size = 268435456;       -- 256 MiB. Bounded: never O(corpus).

-- ============================================================================
-- A0. SCHEMA VERSIONING
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_migration (
    version      INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    applied_at   TEXT    NOT NULL,
    checksum     TEXT    NOT NULL          -- sha256 of the migration text
) STRICT;

INSERT OR IGNORE INTO schema_migration (version, name, applied_at, checksum)
VALUES (1, 'initial-fleet-memory', '2026-08-13T12:00:00Z', 'pending');


-- ============================================================================
-- A1. PROVIDER METADATA
-- ============================================================================
--
-- Mirrors fleet-gateway's `[[provider]]` config (gateway.example.toml) so the
-- database can answer "was DeepInfra down when this render failed?" without
-- parsing journald. The gateway remains the authority on live breaker state;
-- this is the durable ledger it writes into.
--
-- Note `keys` are NEVER stored here — not even names of env vars are needed.
-- The gateway owns credentials. This table owns history.

CREATE TABLE IF NOT EXISTS provider (
    id              INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,      -- 'deepinfra','zai','ollama',...
    base_url        TEXT,
    kind            TEXT NOT NULL
                    CHECK (kind IN ('remote','local')),
    -- Local providers (ollama) cannot 401 and do not participate in key
    -- rotation; the distinction drives fallback policy.
    is_active       INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    first_seen_at   TEXT NOT NULL,
    notes           TEXT
) STRICT;

CREATE TABLE IF NOT EXISTS provider_model (
    id              INTEGER PRIMARY KEY,
    provider_id     INTEGER NOT NULL REFERENCES provider(id) ON DELETE CASCADE,
    model_id        TEXT NOT NULL,             -- 'nomic-embed-text','deepseek-v3'
    modality        TEXT NOT NULL
                    CHECK (modality IN ('embedding','text','tts','image',
                                        'video','music','rerank','asr')),

    -- Embedding-only. NULL for every other modality. The CHECK below makes
    -- "an embedding model with no declared dimension" unrepresentable, which
    -- is root cause F1.1 closed at the schema level.
    dims            INTEGER
                    CHECK (dims IS NULL OR dims > 0),
    max_input_tokens INTEGER,

    -- Cost ledger inputs, USD per million tokens / per unit. NULL = unknown,
    -- which is honest; 0 would lie in the cost report.
    cost_in_per_mtok  REAL,
    cost_out_per_mtok REAL,

    deprecated_at   TEXT,
    UNIQUE (provider_id, model_id),
    CHECK (modality <> 'embedding' OR dims IS NOT NULL)
) STRICT;

CREATE INDEX IF NOT EXISTS ix_provider_model_modality
    ON provider_model (modality, deprecated_at);

-- ---------------------------------------------------------------------------
-- A1.1 EMBEDDING SPACE — the identity of an index file
-- ---------------------------------------------------------------------------
--
-- One row per (provider, model, dims, revision). `file_name` is the exact
-- basename Part B is built into. This is the registry the symlink swap reads:
-- rollback is `UPDATE ... SET is_current=1` plus one `ln -sf`, and the pair is
-- verifiable after the fact.
--
-- `revision` exists because a chunker change invalidates an index just as
-- thoroughly as a model change, and the model id alone would not notice.

CREATE TABLE IF NOT EXISTS embedding_space (
    id                INTEGER PRIMARY KEY,
    provider_id       INTEGER NOT NULL REFERENCES provider(id),
    provider_model_id INTEGER NOT NULL REFERENCES provider_model(id),
    dims              INTEGER NOT NULL CHECK (dims > 0),
    revision          INTEGER NOT NULL DEFAULT 1 CHECK (revision > 0),

    -- Chunking parameters are part of the index identity, not a runtime knob.
    chunk_target_tokens  INTEGER NOT NULL CHECK (chunk_target_tokens > 0),
    chunk_overlap_tokens INTEGER NOT NULL DEFAULT 0
                         CHECK (chunk_overlap_tokens >= 0
                                AND chunk_overlap_tokens < chunk_target_tokens),
    normalize         INTEGER NOT NULL DEFAULT 1 CHECK (normalize IN (0,1)),
    distance_metric   TEXT NOT NULL DEFAULT 'cosine'
                      CHECK (distance_metric IN ('cosine','l2')),

    file_name         TEXT NOT NULL UNIQUE,    -- index.ollama.nomic-embed-text.768.r1.db
    built_at          TEXT,                    -- NULL until first build completes
    is_current        INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),
    retired_at        TEXT,

    UNIQUE (provider_model_id, dims, revision)
) STRICT;

-- At most one current space. A partial unique index enforces it; there is no
-- application code path that can produce two `current` symlink targets.
CREATE UNIQUE INDEX IF NOT EXISTS ux_embedding_space_current
    ON embedding_space (is_current) WHERE is_current = 1;

-- ---------------------------------------------------------------------------
-- A1.2 PROVIDER HEALTH — breaker transitions from the gateway spool
-- ---------------------------------------------------------------------------
--
-- fleet-gateway emits breaker events to cns-spool/gateway.jsonl; fleet-cns
-- tails it and lands them here. Answers "the maritime run scored 0.000 at
-- 02:14 — was the key dead?" in one query instead of a log archaeology dig.

CREATE TABLE IF NOT EXISTS provider_health_event (
    id            INTEGER PRIMARY KEY,
    provider_id   INTEGER NOT NULL REFERENCES provider(id) ON DELETE CASCADE,
    occurred_at   TEXT NOT NULL,
    state         TEXT NOT NULL
                  CHECK (state IN ('closed','open','half_open')),
    prev_state    TEXT
                  CHECK (prev_state IS NULL OR
                         prev_state IN ('closed','open','half_open')),

    -- The error taxonomy from fleet-infrastructure-redesign.md §3. These are
    -- distinct because their correct handling is distinct: auth_error pages a
    -- human and never retries; empty_response retries then falls back — that
    -- specific conflation is the Wesley 0.000 bug.
    reason        TEXT
                  CHECK (reason IS NULL OR reason IN
                         ('auth_error','rate_limited','empty_response',
                          'timeout','upstream_5xx','network','probe_ok',
                          'manual')),
    consecutive_failures INTEGER NOT NULL DEFAULT 0,
    cooldown_secs INTEGER,
    detail        TEXT
) STRICT;

CREATE INDEX IF NOT EXISTS ix_health_provider_time
    ON provider_health_event (provider_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS ix_health_time
    ON provider_health_event (occurred_at DESC);

-- ---------------------------------------------------------------------------
-- A1.3 API CALL LEDGER
-- ---------------------------------------------------------------------------
--
-- One row per gateway-proxied call. This is the cost report's source of truth
-- and the evidence trail for every render in A4. Bounded by retention (see
-- A6 note), not by hope.

CREATE TABLE IF NOT EXISTS api_call (
    id                INTEGER PRIMARY KEY,
    provider_id       INTEGER NOT NULL REFERENCES provider(id),
    provider_model_id INTEGER REFERENCES provider_model(id),
    started_at        TEXT NOT NULL,
    latency_ms        INTEGER CHECK (latency_ms IS NULL OR latency_ms >= 0),
    http_status       INTEGER,
    outcome           TEXT NOT NULL
                      CHECK (outcome IN ('ok','auth_error','rate_limited',
                                         'empty_response','timeout',
                                         'upstream_5xx','network','fell_back')),
    tokens_in         INTEGER,
    tokens_out        INTEGER,
    cost_usd          REAL,
    fell_back_to_provider_id INTEGER REFERENCES provider(id),

    session_id        INTEGER REFERENCES session(id) ON DELETE SET NULL,
    request_id        TEXT                          -- gateway correlation id
) STRICT;

CREATE INDEX IF NOT EXISTS ix_api_call_time     ON api_call (started_at DESC);
CREATE INDEX IF NOT EXISTS ix_api_call_outcome  ON api_call (outcome, started_at DESC);
CREATE INDEX IF NOT EXISTS ix_api_call_request  ON api_call (request_id);


-- ============================================================================
-- A2. DOCUMENTS — the universal indexable unit
-- ============================================================================
--
-- A document is anything the fleet might want to retrieve semantically: a file
-- in ai-writings, one message in a session, an artifact's text body, a
-- decision's rationale. `source_uri` carries the scheme; the nullable typed
-- FKs give real referential integrity where the source lives in this database.
--
-- `content_sha256` is the cross-database join key and the staleness signal.
-- Reindex compares it against document_index_state.indexed_sha256 — a file
-- whose mtime changed but whose bytes did not is never re-embedded.

CREATE TABLE IF NOT EXISTS document (
    id              INTEGER PRIMARY KEY,
    source_uri      TEXT NOT NULL UNIQUE,
    -- 'file:///home/eileen/.openclaw/workspace/ai-writings/S156-compile.md'
    -- 'session://41f2/0007'
    -- 'artifact://118'
    -- 'decision://23'
    source_kind     TEXT NOT NULL
                    CHECK (source_kind IN ('file','message','artifact',
                                           'decision','external')),

    -- Typed backrefs. Exactly the one matching source_kind is non-NULL.
    message_id      INTEGER REFERENCES message(id)  ON DELETE CASCADE,
    artifact_id     INTEGER REFERENCES artifact(id) ON DELETE CASCADE,
    decision_id     INTEGER REFERENCES decision(id) ON DELETE CASCADE,

    repo            TEXT,                     -- 'ai-writings', 'fleet-cns'
    rel_path        TEXT,                     -- repo-relative, NULL for non-file
    title           TEXT,
    lang            TEXT,                     -- 'en', 'tapscript', 'rust', ...
    byte_len        INTEGER NOT NULL CHECK (byte_len >= 0),
    content_sha256  TEXT NOT NULL CHECK (length(content_sha256) = 64),
    mtime           TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    deleted_at      TEXT,                     -- tombstone; index prunes on it

    CHECK ( (source_kind = 'message'  AND message_id  IS NOT NULL)
         OR (source_kind = 'artifact' AND artifact_id IS NOT NULL)
         OR (source_kind = 'decision' AND decision_id IS NOT NULL)
         OR (source_kind IN ('file','external')) )
) STRICT;

CREATE INDEX IF NOT EXISTS ix_document_sha    ON document (content_sha256);
CREATE INDEX IF NOT EXISTS ix_document_repo   ON document (repo, rel_path);
CREATE INDEX IF NOT EXISTS ix_document_live   ON document (deleted_at) WHERE deleted_at IS NULL;

-- ---------------------------------------------------------------------------
-- A2.1 PER-SPACE INDEX STATE — what is embedded, in which space, at which sha
-- ---------------------------------------------------------------------------
--
-- This is the resumability primitive. It lives in the DURABLE database on
-- purpose: after a crash mid-reindex, the truth about what was completed must
-- not be inside the half-written file we are deciding whether to trust.

CREATE TABLE IF NOT EXISTS document_index_state (
    document_id     INTEGER NOT NULL REFERENCES document(id) ON DELETE CASCADE,
    space_id        INTEGER NOT NULL REFERENCES embedding_space(id) ON DELETE CASCADE,
    indexed_sha256  TEXT NOT NULL CHECK (length(indexed_sha256) = 64),
    chunk_count     INTEGER NOT NULL CHECK (chunk_count >= 0),
    indexed_at      TEXT NOT NULL,
    embed_ms        INTEGER,
    PRIMARY KEY (document_id, space_id)
) STRICT, WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS ix_dis_space ON document_index_state (space_id, indexed_at);


-- ============================================================================
-- A3. REINDEX RUNS AND CHECKPOINTS
-- ============================================================================
--
-- Shape borrowed from fleet-cns's Checkpointer (offsets.json), promoted into
-- SQL so it is queryable and transactional with the inserts it describes. The
-- cursor is (document_id) ordered — a monotonic, resumable scan over a
-- SNAPSHOT of the corpus taken at run start.
--
-- The snapshot is why `planned_documents` is written at start and never
-- updated: it fixes "index changed while building" (F1, fourth failure). Files
-- that arrive mid-run are the next run's problem, by design.

CREATE TABLE IF NOT EXISTS reindex_run (
    id                 INTEGER PRIMARY KEY,
    space_id           INTEGER NOT NULL REFERENCES embedding_space(id),
    started_at         TEXT NOT NULL,
    finished_at        TEXT,
    status             TEXT NOT NULL DEFAULT 'running'
                       CHECK (status IN ('running','completed','failed',
                                         'interrupted','superseded')),
    -- 'interrupted' is written by the NEXT run when it finds a stale 'running'
    -- row whose flock is unheld. The lock stays a kernel fact; this column is
    -- only its shadow, for reporting.
    trigger            TEXT NOT NULL
                       CHECK (trigger IN ('manual','provider_change','schedule',
                                          'drift','bootstrap')),
    planned_documents  INTEGER NOT NULL CHECK (planned_documents >= 0),
    done_documents     INTEGER NOT NULL DEFAULT 0,
    done_chunks        INTEGER NOT NULL DEFAULT 0,
    failed_documents   INTEGER NOT NULL DEFAULT 0,
    peak_rss_bytes     INTEGER,        -- asserted in CI; see roadmap Phase 3
    host               TEXT,
    pid                INTEGER,        -- diagnostics ONLY. Never an exclusion
                                       -- mechanism. See header note on flock.
    error              TEXT
) STRICT;

CREATE INDEX IF NOT EXISTS ix_reindex_run_space
    ON reindex_run (space_id, started_at DESC);
CREATE INDEX IF NOT EXISTS ix_reindex_run_active
    ON reindex_run (status) WHERE status = 'running';

CREATE TABLE IF NOT EXISTS reindex_checkpoint (
    run_id             INTEGER PRIMARY KEY REFERENCES reindex_run(id) ON DELETE CASCADE,
    cursor_document_id INTEGER NOT NULL DEFAULT 0,   -- resume WHERE id > this
    batch_size         INTEGER NOT NULL CHECK (batch_size > 0),
    updated_at         TEXT NOT NULL
) STRICT;

-- Spool-tailing checkpoints (fleet-cns parity): byte offsets per JSONL file.
-- Same table shape, different corpus. Kept here so one `.backup` captures the
-- whole recovery state of the fleet.
CREATE TABLE IF NOT EXISTS spool_checkpoint (
    spool_file      TEXT PRIMARY KEY,          -- basename within cns-spool/
    byte_offset     INTEGER NOT NULL CHECK (byte_offset >= 0),
    inode           INTEGER,                   -- rotation detection
    processed_lines INTEGER NOT NULL DEFAULT 0,
    dead_lettered   INTEGER NOT NULL DEFAULT 0,
    updated_at      TEXT NOT NULL
) STRICT, WITHOUT ROWID;


-- ============================================================================
-- A4. SESSIONS, MESSAGES, AGENTS
-- ============================================================================

CREATE TABLE IF NOT EXISTS agent (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,     -- 'Claude Opus 5','KimiCode','Hermes'
    role         TEXT,                     -- 'Strategic Operations','Navigation'
    provider_id  INTEGER REFERENCES provider(id),
    model_id     TEXT,
    first_seen_at TEXT NOT NULL,
    is_active    INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1))
) STRICT;

CREATE TABLE IF NOT EXISTS session (
    id             INTEGER PRIMARY KEY,
    external_id    TEXT UNIQUE,            -- harness session uuid
    agent_id       INTEGER REFERENCES agent(id),
    started_at     TEXT NOT NULL,
    ended_at       TEXT,
    workspace      TEXT,
    channel        TEXT NOT NULL DEFAULT 'main'
                   CHECK (channel IN ('main','subagent','cron','discord',
                                      'overnight','shared')),
    -- `channel` is load-bearing for privacy, not just reporting: AGENTS.md
    -- forbids loading MEMORY.md in shared contexts. Retrieval filters on it.
    parent_session_id INTEGER REFERENCES session(id) ON DELETE SET NULL,
    title          TEXT,
    summary        TEXT,
    total_cost_usd REAL
) STRICT;

CREATE INDEX IF NOT EXISTS ix_session_time    ON session (started_at DESC);
CREATE INDEX IF NOT EXISTS ix_session_channel ON session (channel, started_at DESC);

CREATE TABLE IF NOT EXISTS message (
    id            INTEGER PRIMARY KEY,
    session_id    INTEGER NOT NULL REFERENCES session(id) ON DELETE CASCADE,
    seq           INTEGER NOT NULL CHECK (seq >= 0),
    role          TEXT NOT NULL
                  CHECK (role IN ('user','assistant','system','tool')),
    created_at    TEXT NOT NULL,
    content       TEXT,                    -- NULL for pure tool-call turns
    content_sha256 TEXT CHECK (content_sha256 IS NULL OR length(content_sha256) = 64),
    tokens_in     INTEGER,
    tokens_out    INTEGER,
    UNIQUE (session_id, seq)
) STRICT;

CREATE INDEX IF NOT EXISTS ix_message_time ON message (created_at DESC);

CREATE TABLE IF NOT EXISTS tool_call (
    id           INTEGER PRIMARY KEY,
    message_id   INTEGER NOT NULL REFERENCES message(id) ON DELETE CASCADE,
    tool_name    TEXT NOT NULL,
    started_at   TEXT NOT NULL,
    duration_ms  INTEGER,
    ok           INTEGER NOT NULL DEFAULT 1 CHECK (ok IN (0,1)),
    args_json    TEXT,
    error        TEXT
) STRICT;

CREATE INDEX IF NOT EXISTS ix_tool_call_name ON tool_call (tool_name, started_at DESC);


-- ============================================================================
-- A5. AGENT DECISION LOG
-- ============================================================================
--
-- Models exactly what memory/2026-08-13.md records by hand under "Key
-- Decisions Made Today" — but queryable, attributable, and supersedable.
--
-- The `superseded_by_id` self-reference is the important column. Today's log
-- contains a decision ("PID-stamped lock files with staleness detection") that
-- was reversed within hours after KimiCode's review. A flat list cannot express
-- that; it just goes stale and starts lying. Decisions are never deleted —
-- being able to read a reversed decision AND its replacement is the whole point
-- of an institutional memory.

CREATE TABLE IF NOT EXISTS decision (
    id            INTEGER PRIMARY KEY,
    decided_at    TEXT NOT NULL,
    agent_id      INTEGER REFERENCES agent(id),
    session_id    INTEGER REFERENCES session(id) ON DELETE SET NULL,

    title         TEXT NOT NULL,
    -- e.g. 'flock(2) guard file, not PID lockfiles'
    rationale     TEXT NOT NULL,
    alternatives  TEXT,          -- what was rejected and why
    confidence    TEXT CHECK (confidence IS NULL OR
                              confidence IN ('low','medium','high')),

    scope         TEXT NOT NULL
                  CHECK (scope IN ('architecture','infra','creative',
                                   'process','security','ops')),
    phase         TEXT,          -- roadmap phase, e.g. 'P3'
    component     TEXT,          -- 'memory-indexer','fleet-gateway','audio'

    status        TEXT NOT NULL DEFAULT 'accepted'
                  CHECK (status IN ('proposed','accepted','superseded',
                                    'reverted','rejected')),
    superseded_by_id INTEGER REFERENCES decision(id) ON DELETE SET NULL,
    reversal_reason  TEXT,

    CHECK (status <> 'superseded' OR superseded_by_id IS NOT NULL)
) STRICT;

CREATE INDEX IF NOT EXISTS ix_decision_time      ON decision (decided_at DESC);
CREATE INDEX IF NOT EXISTS ix_decision_component ON decision (component, decided_at DESC);
CREATE INDEX IF NOT EXISTS ix_decision_live      ON decision (status)
    WHERE status IN ('accepted','proposed');

-- Evidence: what the decision was based on. Makes "show me why we rejected Go"
-- return the measurements, not just the verdict.
CREATE TABLE IF NOT EXISTS decision_evidence (
    decision_id  INTEGER NOT NULL REFERENCES decision(id) ON DELETE CASCADE,
    document_id  INTEGER REFERENCES document(id) ON DELETE CASCADE,
    artifact_id  INTEGER REFERENCES artifact(id) ON DELETE CASCADE,
    note         TEXT,
    PRIMARY KEY (decision_id, document_id, artifact_id),
    CHECK (document_id IS NOT NULL OR artifact_id IS NOT NULL)
) STRICT;


-- ============================================================================
-- A6. CREATIVE WORKS REGISTRY
-- ============================================================================
--
-- The observed pipeline (memory/2026-08-13.md, mid-morning):
--
--     outline (S-numbered .md)
--        -> text render (DeepSeek)
--        -> TTS audio (Qwen3-TTS-VoiceDesign)   [+ voice profile]
--        -> v2 re-render after Casey's feedback
--     and separately: TapScript notation -> MIDI -> WAV
--
-- The naive model is a table with four columns. That model is already wrong on
-- disk: `wear-your-life-jacket-vhf-tts.mp3` and
-- `wear-your-life-jacket-vhf-gateway.mp3` are two renders of one work through
-- two different paths, and `puffins-dont-quit-v2-tts.mp3` is a re-render whose
-- parent is a REWRITTEN text, not the original.
--
-- So the registry is a DAG: `work` is the conceptual piece; `artifact` is every
-- concrete file; `artifact_input` records which artifacts fed which. Adding a
-- stage (a video render, a print layout) is a new `kind`, not a migration.

CREATE TABLE IF NOT EXISTS work (
    id            INTEGER PRIMARY KEY,
    slug          TEXT NOT NULL UNIQUE,     -- 'wear-your-pfd'
    title         TEXT NOT NULL,            -- 'Wear Your PFD'
    form          TEXT NOT NULL
                  CHECK (form IN ('speech','poem','essay','story','song',
                                  'lesson','report','notation','mixed')),
    series        TEXT,                     -- 'S' (the S-numbered sequence)
    series_no     INTEGER,                  -- 156 for S156
    created_at    TEXT NOT NULL,
    updated_at    TEXT NOT NULL,
    status        TEXT NOT NULL DEFAULT 'draft'
                  CHECK (status IN ('draft','rendered','approved','published',
                                    'shelved')),
    summary       TEXT,
    UNIQUE (series, series_no)
) STRICT;

-- Aliases matter more than they look. Casey asks for "the PFD speech"; the
-- files on disk are named `wear-your-life-jacket-vhf-*` and
-- `wear-your-pfd-qwen-tts.mp3`. Without aliases, Q3 finds nothing and the
-- registry is a filing cabinet nobody can open.
CREATE TABLE IF NOT EXISTS work_alias (
    work_id  INTEGER NOT NULL REFERENCES work(id) ON DELETE CASCADE,
    alias    TEXT NOT NULL,
    PRIMARY KEY (alias, work_id)
) STRICT, WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS tag (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE               -- 'silence','maritime','hermit-crab'
) STRICT;

CREATE TABLE IF NOT EXISTS work_tag (
    work_id INTEGER NOT NULL REFERENCES work(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
    -- Curated tags complement semantic search; they do not replace it. A tag
    -- says "we decided this is about silence"; the vector index says "this
    -- reads like silence". Q1 uses both.
    PRIMARY KEY (work_id, tag_id)
) STRICT, WITHOUT ROWID;

-- ---------------------------------------------------------------------------
-- A6.1 VOICE PROFILES — the sound-quality encoding system
-- ---------------------------------------------------------------------------
--
-- From 2026-08-13 decision #9: warmth / brightness / breathiness / pace /
-- reverb / proximity. Stored as a first-class row rather than buried in a
-- params blob so Casey's feedback ("Puffins too high-pitched") becomes an
-- adjustable, reusable, diffable object — and so "render the new one with the
-- Compile Silence voice" is a foreign key, not a re-derivation from memory.

CREATE TABLE IF NOT EXISTS voice_profile (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL UNIQUE,      -- 'oral-tradition-elder'
    warmth       REAL CHECK (warmth       IS NULL OR warmth       BETWEEN 0 AND 1),
    brightness   REAL CHECK (brightness   IS NULL OR brightness   BETWEEN 0 AND 1),
    breathiness  REAL CHECK (breathiness  IS NULL OR breathiness  BETWEEN 0 AND 1),
    pace         REAL CHECK (pace         IS NULL OR pace         BETWEEN 0 AND 1),
    reverb       REAL CHECK (reverb       IS NULL OR reverb       BETWEEN 0 AND 1),
    proximity    REAL CHECK (proximity    IS NULL OR proximity    BETWEEN 0 AND 1),
    pitch_shift_semitones REAL,
    prompt_text  TEXT,                       -- the VoiceDesign prompt itself
    derived_from_id INTEGER REFERENCES voice_profile(id) ON DELETE SET NULL,
    created_at   TEXT NOT NULL,
    notes        TEXT
) STRICT;

-- ---------------------------------------------------------------------------
-- A6.2 ARTIFACTS — every concrete file, and how it was made
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS artifact (
    id            INTEGER PRIMARY KEY,
    work_id       INTEGER REFERENCES work(id) ON DELETE CASCADE,
    -- NULL work_id is legal: not every artifact belongs to a creative work
    -- (a fleet diagram, a one-off image). It still gets provenance.

    kind          TEXT NOT NULL
                  CHECK (kind IN ('outline','text','tapscript','midi',
                                  'audio_tts','audio_synth','image','video',
                                  'score','transcript','other')),
    variant       TEXT,          -- 'v2', 'gateway', 'qwen' — the disk suffix
    revision      INTEGER NOT NULL DEFAULT 1 CHECK (revision > 0),

    -- Storage. `uri` is authoritative and may be local or remote; the two are
    -- not alternatives but a lifecycle. Media migrates local -> R2 (F6: the
    -- ai-writings .git is 3.7 GB of committed blobs) and `storage` records
    -- where it currently is. You cannot safely offload what you have not
    -- registered — which is why this table precedes the R2 move in the roadmap.
    storage       TEXT NOT NULL DEFAULT 'local'
                  CHECK (storage IN ('local','r2','both','missing')),
    uri           TEXT NOT NULL UNIQUE,      -- file:///... or r2://bucket/key
    byte_len      INTEGER CHECK (byte_len IS NULL OR byte_len >= 0),
    content_sha256 TEXT CHECK (content_sha256 IS NULL OR length(content_sha256) = 64),
    mime          TEXT,
    duration_ms   INTEGER,                   -- audio/video only
    sample_rate   INTEGER,

    created_at    TEXT NOT NULL,
    render_job_id INTEGER REFERENCES render_job(id) ON DELETE SET NULL,
    superseded_by_id INTEGER REFERENCES artifact(id) ON DELETE SET NULL,
    -- v1 is superseded by v2 but NEVER deleted. Casey compared them.

    is_approved   INTEGER NOT NULL DEFAULT 0 CHECK (is_approved IN (0,1))
) STRICT;

CREATE INDEX IF NOT EXISTS ix_artifact_work    ON artifact (work_id, kind, revision);
CREATE INDEX IF NOT EXISTS ix_artifact_kind    ON artifact (kind, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_artifact_sha     ON artifact (content_sha256);
CREATE INDEX IF NOT EXISTS ix_artifact_storage ON artifact (storage) WHERE storage <> 'r2';

-- The DAG edge. A TTS render has TWO inputs: the text it speaks and the voice
-- profile it speaks in. A self-FK on artifact could not express that.
CREATE TABLE IF NOT EXISTS artifact_input (
    artifact_id       INTEGER NOT NULL REFERENCES artifact(id) ON DELETE CASCADE,
    input_artifact_id INTEGER NOT NULL REFERENCES artifact(id) ON DELETE CASCADE,
    role              TEXT NOT NULL
                      CHECK (role IN ('source','revision_of','reference',
                                      'accompaniment','master')),
    PRIMARY KEY (artifact_id, input_artifact_id, role),
    CHECK (artifact_id <> input_artifact_id)     -- no self-loops
) STRICT, WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS ix_artifact_input_rev
    ON artifact_input (input_artifact_id, artifact_id);

-- ---------------------------------------------------------------------------
-- A6.3 RENDER JOBS — reproducibility
-- ---------------------------------------------------------------------------
--
-- "How did we get that voice?" must be answerable six months later. Params are
-- JSON because they are provider-shaped and change without warning; everything
-- we query on is promoted to a real column.

CREATE TABLE IF NOT EXISTS render_job (
    id                INTEGER PRIMARY KEY,
    started_at        TEXT NOT NULL,
    finished_at       TEXT,
    status            TEXT NOT NULL DEFAULT 'running'
                      CHECK (status IN ('running','ok','failed','cancelled')),
    provider_id       INTEGER REFERENCES provider(id),
    provider_model_id INTEGER REFERENCES provider_model(id),
    voice_profile_id  INTEGER REFERENCES voice_profile(id),
    session_id        INTEGER REFERENCES session(id) ON DELETE SET NULL,
    api_call_id       INTEGER REFERENCES api_call(id) ON DELETE SET NULL,
    seed              INTEGER,
    params_json       TEXT,
    peak_rss_bytes    INTEGER,      -- audio renders assert this; see Phase 4
    error             TEXT
) STRICT;

CREATE INDEX IF NOT EXISTS ix_render_job_time ON render_job (started_at DESC);

-- ---------------------------------------------------------------------------
-- A6.4 FEEDBACK — why v2 exists
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS feedback (
    id           INTEGER PRIMARY KEY,
    artifact_id  INTEGER NOT NULL REFERENCES artifact(id) ON DELETE CASCADE,
    given_at     TEXT NOT NULL,
    author       TEXT NOT NULL DEFAULT 'casey',
    verdict      TEXT NOT NULL
                 CHECK (verdict IN ('approve','revise','reject','note')),
    dimension    TEXT
                 CHECK (dimension IS NULL OR
                        dimension IN ('voice','pacing','content','structure',
                                      'length','tone','mix','other')),
    body         TEXT NOT NULL,     -- 'too high-pitched'
    resulted_in_artifact_id INTEGER REFERENCES artifact(id) ON DELETE SET NULL
) STRICT;

CREATE INDEX IF NOT EXISTS ix_feedback_artifact ON feedback (artifact_id, given_at DESC);

-- RETENTION NOTE (the O(chunk) rule applied to storage): `api_call`,
-- `provider_health_event` and `tool_call` grow with fleet activity and nothing
-- else. They are the only unbounded tables here. Roadmap Phase 7 ships a
-- rollup job: rows older than 90 days collapse into daily aggregates. Every
-- other table grows with the corpus, which grows with Casey.


-- ############################################################################
-- ############################################################################
--   PART B — index.<provider>.<model>.<dims>.r<rev>.db   (DISPOSABLE)
-- ############################################################################
-- ############################################################################
--
--   *** THIS SECTION IS A TEMPLATE. `{{DIMS}}` is substituted at build time. ***
--
-- The dimension is a DDL constant in vec0. That is not a limitation to work
-- around — it is the fix for F1.1. A 1024-dim vector from bge-m3 cannot be
-- inserted into a file whose vec0 was declared FLOAT[768]; sqlite-vec rejects
-- it at the storage layer, before any cosine comparison can be silently
-- meaningless. The schema cannot be shared across spaces because the failure
-- it prevents is exactly "these spaces got shared".
--
-- Current fleet default: ollama / nomic-embed-text / 768 / r1
--   -> index.ollama.nomic-embed-text.768.r1.db, reachable as `current`.
--
-- Build target is a temp name; `current` is repointed only after the run
-- commits and `index_header` verifies. Rollback is `ln -sf` plus one UPDATE.

PRAGMA journal_mode = WAL;
PRAGMA synchronous  = NORMAL;
PRAGMA busy_timeout = 5000;

-- ============================================================================
-- B0. HEADER — self-describing, verified on every open
-- ============================================================================
--
-- KimiCode put provenance in the filename; I kept it in a table; both belong.
-- A filename can be renamed by an operator at 2am. A header cannot be renamed
-- by accident. The loader asserts filename == header == embedding_space row,
-- and refuses to serve on any mismatch rather than returning wrong neighbours.

CREATE TABLE IF NOT EXISTS index_header (
    singleton        INTEGER PRIMARY KEY CHECK (singleton = 1),
    space_id         INTEGER NOT NULL,      -- fleet.db embedding_space.id
    provider_name    TEXT    NOT NULL,
    model_id         TEXT    NOT NULL,
    dims             INTEGER NOT NULL CHECK (dims > 0),
    revision         INTEGER NOT NULL,
    distance_metric  TEXT    NOT NULL CHECK (distance_metric IN ('cosine','l2')),
    normalize        INTEGER NOT NULL CHECK (normalize IN (0,1)),
    chunk_target_tokens  INTEGER NOT NULL,
    chunk_overlap_tokens INTEGER NOT NULL,
    schema_version   INTEGER NOT NULL,
    built_by         TEXT    NOT NULL,      -- 'fleet-memory 0.1.0'
    built_at         TEXT    NOT NULL,
    fleet_db_path    TEXT    NOT NULL,
    sealed_at        TEXT                   -- set when the run completes;
                                            -- NULL means "still building,
                                            -- do not promote to current"
) STRICT;

-- ============================================================================
-- B1. CHUNKS
-- ============================================================================
--
-- `document_sha256` — not `document_id` — is the cross-database key. It is
-- content-addressed, so it stays correct if fleet.db is restored from a backup
-- with different rowids, and it makes staleness detection a string compare.
-- `document_id` is carried alongside purely as a join accelerator and is
-- treated as a hint, never as truth.

CREATE TABLE IF NOT EXISTS chunk (
    chunk_id        INTEGER PRIMARY KEY,
    document_sha256 TEXT NOT NULL CHECK (length(document_sha256) = 64),
    document_id     INTEGER NOT NULL,        -- hint; no cross-db FK exists
    ord             INTEGER NOT NULL CHECK (ord >= 0),
    byte_start      INTEGER NOT NULL CHECK (byte_start >= 0),
    byte_end        INTEGER NOT NULL,
    token_count     INTEGER NOT NULL CHECK (token_count > 0),
    heading_path    TEXT,                    -- '## Late Morning > Infrastructure'
    text            TEXT NOT NULL,
    UNIQUE (document_sha256, ord),
    CHECK (byte_end > byte_start)
) STRICT;

CREATE INDEX IF NOT EXISTS ix_chunk_doc ON chunk (document_id, ord);

-- ============================================================================
-- B2. VECTORS
-- ============================================================================

CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunk USING vec0(
    chunk_id  INTEGER PRIMARY KEY,
    embedding FLOAT[{{DIMS}}]
);

-- ============================================================================
-- B3. FULL TEXT
-- ============================================================================
--
-- Vectors alone are the wrong tool for half of Casey's real queries. "Find
-- pieces about silence" wants both: BM25 finds the pieces that say the word,
-- the vector index finds the ones that are about the idea without naming it
-- ("On the Acoustics of an Empty Engine Room" contains neither the word nor
-- the theme spelled out). Shipping only one of the two makes the memory feel
-- either literal-minded or vague. Q1 fuses them.
--
-- External-content FTS5: the text lives once, in `chunk`.

CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts USING fts5(
    text,
    heading_path,
    content='chunk',
    content_rowid='chunk_id',
    tokenize='porter unicode61 remove_diacritics 2'
);

CREATE TRIGGER IF NOT EXISTS trg_chunk_ai AFTER INSERT ON chunk BEGIN
    INSERT INTO chunk_fts (rowid, text, heading_path)
    VALUES (new.chunk_id, new.text, new.heading_path);
END;

CREATE TRIGGER IF NOT EXISTS trg_chunk_ad AFTER DELETE ON chunk BEGIN
    INSERT INTO chunk_fts (chunk_fts, rowid, text, heading_path)
    VALUES ('delete', old.chunk_id, old.text, old.heading_path);
END;

CREATE TRIGGER IF NOT EXISTS trg_chunk_au AFTER UPDATE ON chunk BEGIN
    INSERT INTO chunk_fts (chunk_fts, rowid, text, heading_path)
    VALUES ('delete', old.chunk_id, old.text, old.heading_path);
    INSERT INTO chunk_fts (rowid, text, heading_path)
    VALUES (new.chunk_id, new.text, new.heading_path);
END;

-- Note: no trigger maintains vec_chunk. Vectors are written explicitly by the
-- indexer in the same transaction as the chunk insert, because a trigger
-- cannot embed. The batch transaction is the consistency boundary.


-- ############################################################################
-- ############################################################################
--   PART C — CROSS-DATABASE VIEWS AND THE QUERIES THAT MATTER
-- ############################################################################
-- ############################################################################
--
-- Open fleet.db, then:
--     ATTACH DATABASE '/home/eileen/.openclaw/state/memory/current' AS idx;
--
-- `current` is the symlink. SQLite follows it, so a swap is invisible to
-- callers that reconnect, and in-flight readers keep their open file handle on
-- the old inode until they finish — which is precisely the "old index keeps
-- serving" property the design promised.
--
-- MANDATORY on open (this is the F1 guard, in three lines):
--
--     SELECT CASE WHEN (SELECT dims FROM idx.index_header)
--                    = (SELECT dims FROM main.embedding_space WHERE is_current=1)
--                 AND (SELECT sealed_at FROM idx.index_header) IS NOT NULL
--            THEN 1 ELSE raise_abort() END;
--
-- In practice the indexer does this in Rust and returns Err. Do not query a
-- space you have not verified; a mismatched cosine returns confident nonsense,
-- which is worse than an error by exactly the amount of trust placed in it.

-- ============================================================================
-- C1. VIEWS
-- ============================================================================

-- Current architectural decisions, reversals folded in.
CREATE VIEW IF NOT EXISTS v_decision_current AS
SELECT d.id, d.decided_at, a.name AS agent, d.scope, d.phase, d.component,
       d.title, d.rationale, d.status,
       s.title AS superseded_by
FROM decision d
LEFT JOIN agent a    ON a.id = d.agent_id
LEFT JOIN decision s ON s.id = d.superseded_by_id
WHERE d.status IN ('accepted','proposed');

-- Every artifact of every work, with its immediate parent and its maker.
CREATE VIEW IF NOT EXISTS v_work_artifact AS
SELECT w.id            AS work_id,
       w.slug,
       w.title,
       ar.id           AS artifact_id,
       ar.kind,
       ar.variant,
       ar.revision,
       ar.uri,
       ar.storage,
       ar.duration_ms,
       ar.is_approved,
       ar.created_at,
       p.name          AS provider,
       pm.model_id     AS model,
       vp.name         AS voice_profile,
       parent.id       AS derived_from_artifact_id,
       parent.kind     AS derived_from_kind
FROM work w
JOIN artifact ar         ON ar.work_id = w.id
LEFT JOIN render_job rj  ON rj.id = ar.render_job_id
LEFT JOIN provider p     ON p.id = rj.provider_id
LEFT JOIN provider_model pm ON pm.id = rj.provider_model_id
LEFT JOIN voice_profile vp  ON vp.id = rj.voice_profile_id
LEFT JOIN artifact_input ai ON ai.artifact_id = ar.id AND ai.role = 'source'
LEFT JOIN artifact parent   ON parent.id = ai.input_artifact_id;

-- Documents whose bytes changed since they were last embedded in the current
-- space, plus documents never embedded at all. This IS the reindex work queue.
CREATE VIEW IF NOT EXISTS v_stale_document AS
SELECT d.id, d.source_uri, d.repo, d.rel_path, d.content_sha256,
       dis.indexed_sha256, es.id AS space_id,
       CASE WHEN dis.document_id IS NULL THEN 'never' ELSE 'changed' END AS reason
FROM document d
CROSS JOIN embedding_space es
LEFT JOIN document_index_state dis
       ON dis.document_id = d.id AND dis.space_id = es.id
WHERE es.is_current = 1
  AND d.deleted_at IS NULL
  AND (dis.document_id IS NULL OR dis.indexed_sha256 <> d.content_sha256);

-- Provider health at a glance: latest state per provider + 24h failure counts.
CREATE VIEW IF NOT EXISTS v_provider_health AS
SELECT p.name,
       (SELECT state FROM provider_health_event e
         WHERE e.provider_id = p.id ORDER BY e.occurred_at DESC LIMIT 1) AS state,
       (SELECT occurred_at FROM provider_health_event e
         WHERE e.provider_id = p.id ORDER BY e.occurred_at DESC LIMIT 1) AS since,
       (SELECT COUNT(*) FROM api_call c
         WHERE c.provider_id = p.id
           AND c.outcome <> 'ok'
           AND c.started_at >= strftime('%Y-%m-%dT%H:%M:%SZ','now','-1 day')) AS failures_24h
FROM provider p
WHERE p.is_active = 1;


-- ============================================================================
-- C2. THE QUERIES CASEY NAMED
-- ============================================================================

-- ---------------------------------------------------------------------------
-- Q1. "Find pieces about silence."
-- ---------------------------------------------------------------------------
--
-- Hybrid retrieval with Reciprocal Rank Fusion. RRF is used instead of a
-- weighted score blend because BM25 scores and cosine distances are not on a
-- common scale and never will be; fusing RANKS sidesteps the normalisation
-- problem entirely, and the constant k=60 is the standard damping term.
--
-- Bind :qvec as the query embedding (a JSON array or the raw f32 blob),
-- produced by the SAME model as index_header.model_id. Bind :qtext as the
-- FTS5 query string.
--
-- Results roll up to works, because Casey asked for pieces, not chunks.

WITH vec_hits AS (
    SELECT chunk_id,
           ROW_NUMBER() OVER (ORDER BY distance) AS rnk
    FROM idx.vec_chunk
    WHERE embedding MATCH :qvec
      AND k = 60
),
fts_hits AS (
    SELECT rowid AS chunk_id,
           ROW_NUMBER() OVER (ORDER BY bm25(chunk_fts, 1.0, 0.4)) AS rnk
    FROM idx.chunk_fts
    WHERE chunk_fts MATCH :qtext          -- e.g. 'silence OR quiet OR hush'
    LIMIT 60
),
fused AS (
    SELECT COALESCE(v.chunk_id, f.chunk_id) AS chunk_id,
           COALESCE(1.0 / (60 + v.rnk), 0.0)
         + COALESCE(1.0 / (60 + f.rnk), 0.0) AS score
    FROM vec_hits v
    FULL OUTER JOIN fts_hits f ON f.chunk_id = v.chunk_id
),
ranked AS (
    -- Best-chunk wins rather than sum: a long essay should not outrank a
    -- four-line poem purely by having more chances to match. The window
    -- function picks the winning passage and its score in one pass.
    SELECT c.document_sha256,
           c.text AS best_passage,
           fused.score,
           ROW_NUMBER() OVER (PARTITION BY c.document_sha256
                              ORDER BY fused.score DESC) AS rn
    FROM fused
    JOIN idx.chunk c ON c.chunk_id = fused.chunk_id
),
scored AS (
    SELECT document_sha256, score AS chunk_score, best_passage
    FROM ranked WHERE rn = 1
)
SELECT w.slug,
       w.title,
       w.form,
       d.rel_path,
       ROUND(s.chunk_score, 5) AS score,
       CASE WHEN EXISTS (SELECT 1 FROM work_tag wt JOIN tag t ON t.id = wt.tag_id
                          WHERE wt.work_id = w.id AND t.name = 'silence')
            THEN 'tagged' ELSE '' END AS curated,
       substr(s.best_passage, 1, 240) AS excerpt
FROM scored s
JOIN document d ON d.content_sha256 = s.document_sha256 AND d.deleted_at IS NULL
LEFT JOIN artifact ar ON ar.uri = d.source_uri
LEFT JOIN work w      ON w.id = ar.work_id
ORDER BY score DESC
LIMIT 20;

-- On the real corpus this is what surfaces "On the Preservation of Silence"
-- (lexical), "On the Acoustics of an Empty Engine Room" and "The Compile
-- Silence" (semantic + lexical), and the negative-space essay (semantic only)
-- — the last of which a pure-FTS memory would never return and a pure-vector
-- memory would rank below three literal near-misses.


-- ---------------------------------------------------------------------------
-- Q2. "Show decisions from Aug 13."
-- ---------------------------------------------------------------------------
--
-- ISO-8601 UTC makes this a prefix range on a plain B-tree index. No date
-- functions on the indexed column, so the index is actually used.

SELECT d.decided_at,
       COALESCE(a.name, 'unattributed')      AS agent,
       d.scope,
       COALESCE(d.component, '—')            AS component,
       d.title,
       d.status,
       COALESCE(sup.title, '')               AS superseded_by,
       COALESCE(d.reversal_reason, '')       AS reversal_reason,
       (SELECT COUNT(*) FROM decision_evidence de WHERE de.decision_id = d.id)
                                             AS evidence_count
FROM decision d
LEFT JOIN agent    a   ON a.id = d.agent_id
LEFT JOIN decision sup ON sup.id = d.superseded_by_id
WHERE d.decided_at >= '2026-08-13T00:00:00Z'
  AND d.decided_at <  '2026-08-14T00:00:00Z'
ORDER BY d.decided_at ASC;

-- Reversals within the window are the interesting rows and this returns them
-- adjacent to their replacements: the PID-lockfile decision and the flock
-- decision are four hours and two rows apart, with `reversal_reason` carrying
-- "kernel releases flock on SIGKILL; PID files carry a reuse race".

-- Variant: decisions still standing that were made on Aug 13 —
--   ... AND d.status = 'accepted' AND d.superseded_by_id IS NULL


-- ---------------------------------------------------------------------------
-- Q3. "What renders exist for the PFD speech?"
-- ---------------------------------------------------------------------------
--
-- Recursive walk of the derivation DAG from the work's outline outward, so a
-- render three hops down (outline -> text -> v2 text -> TTS) is still found,
-- and so stages added later need no query change.
--
-- `:q` matches slug, title, or alias — 'pfd', 'PFD speech' and
-- 'wear your life jacket' all resolve to the same work.

WITH RECURSIVE
target AS (
    SELECT w.id, w.slug, w.title
    FROM work w
    WHERE w.slug = lower(replace(:q,' ','-'))
       OR lower(w.title) LIKE '%' || lower(:q) || '%'
       OR EXISTS (SELECT 1 FROM work_alias wa
                   WHERE wa.work_id = w.id
                     AND lower(wa.alias) LIKE '%' || lower(:q) || '%')
),
roots AS (
    SELECT ar.id AS artifact_id, 0 AS depth
    FROM artifact ar
    JOIN target t ON t.id = ar.work_id
    WHERE ar.kind = 'outline'
       OR NOT EXISTS (SELECT 1 FROM artifact_input ai WHERE ai.artifact_id = ar.id)
),
lineage AS (
    SELECT artifact_id, depth FROM roots
    UNION
    SELECT ai.artifact_id, l.depth + 1
    FROM artifact_input ai
    JOIN lineage l ON l.artifact_id = ai.input_artifact_id
    WHERE l.depth < 12          -- cycle fence; the DAG should never be deep
)
SELECT l.depth,
       ar.kind,
       COALESCE(ar.variant, '')              AS variant,
       ar.revision,
       ar.uri,
       ar.storage,
       CASE WHEN ar.duration_ms IS NULL THEN ''
            ELSE printf('%d:%02d', ar.duration_ms/60000,
                                   (ar.duration_ms%60000)/1000) END AS duration,
       COALESCE(p.name || '/' || pm.model_id, '')  AS rendered_by,
       COALESCE(vp.name, '')                       AS voice,
       CASE ar.is_approved WHEN 1 THEN 'approved' ELSE '' END AS approved,
       COALESCE(sup.uri, '')                       AS superseded_by,
       COALESCE((SELECT fb.body FROM feedback fb
                  WHERE fb.artifact_id = ar.id
                  ORDER BY fb.given_at DESC LIMIT 1), '') AS latest_feedback
FROM lineage l
JOIN artifact ar          ON ar.id = l.artifact_id
LEFT JOIN render_job rj   ON rj.id = ar.render_job_id
LEFT JOIN provider p      ON p.id  = rj.provider_id
LEFT JOIN provider_model pm ON pm.id = rj.provider_model_id
LEFT JOIN voice_profile vp  ON vp.id = rj.voice_profile_id
LEFT JOIN artifact sup    ON sup.id = ar.superseded_by_id
ORDER BY l.depth, ar.kind, ar.revision;

-- Expected shape against today's disk:
--   0  outline    ...  speeches/wear-your-pfd-outline.md
--   1  text       ...  deepseek render
--   1  tapscript  ...  sound-quality notation
--   2  audio_tts  qwen      wear-your-pfd-qwen-tts.mp3
--   2  audio_tts  vhf       wear-your-life-jacket-vhf-tts.mp3
--   2  audio_tts  gateway   wear-your-life-jacket-vhf-gateway.mp3
-- Three renders, one work, two naming conventions — which is exactly the case
-- a flat outline/text/audio/tap table gets wrong, and the reason for the DAG.


-- ============================================================================
-- C3. FURTHER QUERIES THE SCHEMA IS BUILT TO ANSWER
-- ============================================================================

-- Q4. "What did the 02:14 maritime run cost us, and was a provider dying?"
SELECT c.started_at, p.name, c.outcome, c.latency_ms, c.cost_usd,
       fb.name AS fell_back_to
FROM api_call c
JOIN provider p       ON p.id = c.provider_id
LEFT JOIN provider fb ON fb.id = c.fell_back_to_provider_id
WHERE c.started_at BETWEEN '2026-08-13T02:00:00Z' AND '2026-08-13T03:00:00Z'
  AND c.outcome <> 'ok'
ORDER BY c.started_at;

-- Q5. "Which artifacts are still only on local disk?" (the R2 offload queue,
--      ordered by what is costing us the most git history)
SELECT kind, COUNT(*) AS n, SUM(byte_len)/1048576 AS mib
FROM artifact
WHERE storage = 'local'
  AND kind IN ('audio_tts','audio_synth','image','video','midi')
GROUP BY kind
ORDER BY mib DESC;

-- Q6. "Show me everything Casey asked to revise, and whether we did."
SELECT f.given_at, w.title, a1.kind, a1.variant, f.dimension, f.body,
       CASE WHEN f.resulted_in_artifact_id IS NULL THEN 'OPEN' ELSE 'addressed' END
FROM feedback f
JOIN artifact a1 ON a1.id = f.artifact_id
LEFT JOIN work w ON w.id = a1.work_id
WHERE f.verdict = 'revise'
ORDER BY f.given_at DESC;

-- Q7. "Is the current index healthy?" (dashboard one-liner)
SELECT es.file_name,
       es.dims,
       (SELECT COUNT(*) FROM idx.chunk)                       AS chunks,
       (SELECT COUNT(*) FROM document_index_state WHERE space_id = es.id) AS docs,
       (SELECT COUNT(*) FROM v_stale_document)                AS stale,
       (SELECT status FROM reindex_run WHERE space_id = es.id
         ORDER BY started_at DESC LIMIT 1)                    AS last_run,
       (SELECT peak_rss_bytes/1048576 FROM reindex_run WHERE space_id = es.id
         ORDER BY started_at DESC LIMIT 1)                    AS last_peak_mib
FROM embedding_space es WHERE es.is_current = 1;

-- ============================================================================
-- END. Part A is created once. Part B is created per embedding space and may
-- be deleted at any time without loss of memory — which is the property the
-- whole two-file split exists to guarantee.
-- ============================================================================
