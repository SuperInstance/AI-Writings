-- ============================================================================
-- fleet-memory-schema-kimi.sql
-- Navigation's schema for the fleet memory plane.
-- Author: KimiCode, Navigation Officer · 2026-08-13 · For: Casey
-- Companion: memory/fleet-roadmap-kimi.md (Phase 4 applies this file)
--
-- SPATIAL MODEL — two physical databases, one map:
--
--   fleet-memory.db                        index.<provider>.<model>.<dims>.db
--   (the chart room — one per fleet)       (the cargo holds — one per provenance)
--   ┌────────────────────────────┐         ┌─────────────────────────────┐
--   │ embedding_providers        │◀────────│ index_meta (checked header) │
--   │ index_registry             │──names──▶│ documents → chunks → vec0   │
--   │ reindex_runs / checkpoints │         └─────────────────────────────┘
--   │ creative_works / renders   │                ▲ one per provider+model;
--   │ agent_decisions            │                │ atomically swapped in via
--   └────────────────────────────┘                │ the `current` symlink
--
-- Why two: an index must be disposable (provider change = build a new hold,
-- swap the symlink, sink the old one). The registry must be permanent
-- (decisions and creative works outlive every embedder). Mixing them would
-- make every provider change a data migration. Keep them apart and a
-- provider change is `ln -sf`, exactly as the reconciled plan (§7 CP-6)
-- specifies.
--
-- HARD RULES (from AGENTS.md critical-path rules — enforced by design here):
--   * Both files live on ext4 under $HOME, NEVER /mnt/c (9P locking is
--     unreliable under WSL2 — this is not optional).
--   * Reindex memory is O(batch). Nothing in this schema requires loading
--     more than one batch of chunks into memory.
--   * Embeddings NEVER participate in provider fallback. A vector only
--     exists inside the index whose provenance produced it.
--
-- Apply order: §1 pragmas, §2 registry tables, §3 index template.
-- SQLite ≥ 3.35 (RETURNING/strict-ish features), sqlite-vec extension,
-- FTS5 (both standard in the fleet's existing toolchain).
-- ============================================================================


-- ============================================================================
-- §1. PRAGMAS — apply to BOTH databases
-- ============================================================================
PRAGMA journal_mode = WAL;        -- crash-safe, readers never block the writer
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 5000;       -- wait out a checkpoint instead of erroring
PRAGMA synchronous = NORMAL;      -- WAL-safe; FULL buys nothing here


-- ============================================================================
-- §2. REGISTRY — fleet-memory.db  (apply this section to the registry file)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 2.1 embedding_providers — who is allowed to make vectors, and at what tier.
--     The gateway's health probes update `status`/`last_health_at`; the
--     indexer reads this table and REFUSES any provider not marked active
--     whose (model, dims) matches the target index header. This is where the
--     "embeddings never fall back" rule lives as data, not convention.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS embedding_providers (
    provider_id       TEXT PRIMARY KEY,              -- 'ollama/nomic-embed-text'
    kind              TEXT NOT NULL
                      CHECK (kind IN ('local-ollama','local-onnx','api')),
    model             TEXT NOT NULL,
    dims              INTEGER NOT NULL CHECK (dims > 0),
    endpoint          TEXT,                          -- NULL for local-onnx
    quality_tier      INTEGER NOT NULL DEFAULT 1,    -- 1 = preferred floor
    fallback_allowed  INTEGER NOT NULL DEFAULT 0
                      CHECK (fallback_allowed IN (0,1)),  -- almost always 0
    status            TEXT NOT NULL DEFAULT 'active'
                      CHECK (status IN ('active','degraded','retired')),
    last_health_at    TEXT,                          -- UTC ISO-8601
    notes             TEXT,
    UNIQUE (kind, model, dims)
);

-- ----------------------------------------------------------------------------
-- 2.2 index_registry — every cargo hold we have ever built, and which one is
--     currently being served. The partial unique index makes "exactly one
--     current index" a database invariant, not a symlink convention. Cutover
--     is one transaction: is_current flips here AND the symlink flips on disk;
--     a crash between the two is detected at startup (symlink disagrees with
--     this table → alarm, keep serving the DB file that passes its header).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS index_registry (
    index_name     TEXT PRIMARY KEY,        -- 'index.ollama.nomic-embed-text.768'
    provider_id    TEXT NOT NULL
                   REFERENCES embedding_providers(provider_id),
    db_path        TEXT NOT NULL,           -- ext4 path; CHECK below bars 9P
    index_version  INTEGER NOT NULL,        -- schema+chunker version; bump = rebuild
    is_current     INTEGER NOT NULL DEFAULT 0 CHECK (is_current IN (0,1)),
    doc_count      INTEGER NOT NULL DEFAULT 0,
    chunk_count    INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    retired_at     TEXT,
    CHECK (db_path NOT LIKE '/mnt/%')
);
-- Exactly one serving index, fleet-wide:
CREATE UNIQUE INDEX IF NOT EXISTS one_current_index
    ON index_registry(is_current) WHERE is_current = 1;
CREATE INDEX IF NOT EXISTS idx_registry_provider ON index_registry(provider_id);

-- ----------------------------------------------------------------------------
-- 2.3 reindex_runs + reindex_checkpoints — crash recovery as data.
--     A run FREEZES its input set at start (snapshot_manifest = a file
--     listing path+mtime+size, written before the first batch; fixes
--     "index changed while building"). The checkpoint row is updated in the
--     SAME transaction as each batch insert, so a kill -9 at any point
--     leaves a resumable cursor, never a half-batch.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reindex_runs (
    run_id             TEXT PRIMARY KEY,          -- ulid
    index_name         TEXT NOT NULL
                       REFERENCES index_registry(index_name),
    trigger_kind       TEXT NOT NULL
                       CHECK (trigger_kind IN ('manual','provider-change',
                                               'scheduled','file-watch')),
    snapshot_manifest  TEXT NOT NULL,             -- ext4 path to frozen input list
    snapshot_hash      TEXT NOT NULL,             -- sha256 of that manifest
    status             TEXT NOT NULL DEFAULT 'running'
                       CHECK (status IN ('running','completed','failed',
                                         'superseded')),
    started_at         TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    finished_at        TEXT,
    error              TEXT
);
CREATE INDEX IF NOT EXISTS idx_runs_index ON reindex_runs(index_name, started_at);

CREATE TABLE IF NOT EXISTS reindex_checkpoints (
    run_id           TEXT PRIMARY KEY             -- 1:1 with the run
                     REFERENCES reindex_runs(run_id) ON DELETE CASCADE,
    last_doc_path    TEXT NOT NULL DEFAULT '',    -- resume cursor (path order)
    docs_total       INTEGER NOT NULL,            -- from the snapshot manifest
    docs_done        INTEGER NOT NULL DEFAULT 0,
    chunks_written   INTEGER NOT NULL DEFAULT 0,
    batches_done     INTEGER NOT NULL DEFAULT 0,
    peak_rss_bytes   INTEGER,                     -- filled at finish; proves O(batch)
    updated_at       TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

-- ----------------------------------------------------------------------------
-- 2.4 creative_works — the registry of everything the fleet makes.
--     One row per WORK (the idea); renders of it live in work_renders.
--     "PFD speech" is one row here; its outline, three text drafts, the TTS
--     take, and the TapScript score are five rows downstream.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS creative_works (
    work_id        TEXT PRIMARY KEY,              -- ulid
    slug           TEXT NOT NULL UNIQUE,          -- 'pfd-speech'
    title          TEXT NOT NULL,
    kind           TEXT NOT NULL
                   CHECK (kind IN ('essay','poem','story','speech','radio',
                                   'letter','script','song','lore','other')),
    status         TEXT NOT NULL DEFAULT 'outline'
                   CHECK (status IN ('outline','draft','rendered','voiced',
                                     'published','archived')),
    created_by     TEXT NOT NULL,                 -- agent callsign
    synopsis       TEXT,
    source_session TEXT,                          -- which conversation produced it
    created_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    updated_at     TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_works_created ON creative_works(created_at);
CREATE INDEX IF NOT EXISTS idx_works_kind    ON creative_works(kind, status);

-- Subjects are FIRST-CLASS, weighted, and lowercase-collated: this is the
-- fast lane for "find pieces about silence" — no vector round-trip needed
-- when a human already tagged the theme.
CREATE TABLE IF NOT EXISTS work_subjects (
    work_id  TEXT NOT NULL
             REFERENCES creative_works(work_id) ON DELETE CASCADE,
    subject  TEXT NOT NULL COLLATE NOCASE,
    weight   REAL NOT NULL DEFAULT 1.0            -- 1.0 central … 0.3 passing
             CHECK (weight BETWEEN 0.0 AND 1.0),
    PRIMARY KEY (work_id, subject)
);
CREATE INDEX IF NOT EXISTS idx_subjects_subject ON work_subjects(subject);

-- ----------------------------------------------------------------------------
-- 2.5 work_renders — every materialization of a work.
--     F6 media policy is enforced by the CHECK: anything large lives behind
--     an r2:// key; git only ever sees this manifest row. `spec_json` is the
--     reproducibility contract — a render with no recorded spec is treated
--     as unreproducible and flagged by the nightly audit.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS work_renders (
    render_id     TEXT PRIMARY KEY,               -- ulid
    work_id       TEXT NOT NULL
                  REFERENCES creative_works(work_id) ON DELETE CASCADE,
    render_kind   TEXT NOT NULL
                  CHECK (render_kind IN ('outline','text','tapscript',
                                         'tts-audio','music','image',
                                         'video','pdf')),
    seq           INTEGER NOT NULL DEFAULT 1,     -- v1, v2, … per kind
    location_kind TEXT NOT NULL CHECK (location_kind IN ('ext4','r2')),
    location      TEXT NOT NULL,                  -- ext4 path or r2://key
    mime          TEXT,
    sha256        TEXT,
    size_bytes    INTEGER CHECK (size_bytes >= 0),
    duration_ms   INTEGER CHECK (duration_ms >= 0),   -- audio/video only
    renderer      TEXT,                           -- 'sag', 'fleet-audio 0.3.0', …
    spec_json     TEXT,                           -- the spec that produced it
    created_at    TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
    UNIQUE (work_id, render_kind, seq),
    CHECK (location_kind <> 'r2' OR location LIKE 'r2://%'),
    CHECK (location_kind <> 'ext4' OR location NOT LIKE '/mnt/%'),
    CHECK (render_kind NOT IN ('tts-audio','music','image','video')
           OR location_kind = 'r2' OR size_bytes <= 1048576)  -- F6 fence
);
CREATE INDEX IF NOT EXISTS idx_renders_work ON work_renders(work_id, render_kind);
CREATE INDEX IF NOT EXISTS idx_renders_created ON work_renders(created_at);

-- Full-text over text-class renders. Populated by a trigger-free indexer pass
-- (renders arrive via the fleet's own writers; a small sync job keeps this
-- current — deliberately NOT a trigger, so bulk backfill stays O(batch)).
CREATE VIRTUAL TABLE IF NOT EXISTS work_text_fts USING fts5(
    title,
    body,
    work_id   UNINDEXED,
    render_id UNINDEXED,
    tokenize = 'porter unicode61'
);

-- ----------------------------------------------------------------------------
-- 2.6 agent_decisions — what was decided, by whom, when, and whether it
--     still stands. Append-only by convention: corrections are new rows
--     with supersedes set, never UPDATEs of the record itself (status is
--     the only mutable column, and only toward 'superseded'/'reverted').
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agent_decisions (
    decision_id    TEXT PRIMARY KEY,              -- ulid
    decided_at     TEXT NOT NULL,                 -- UTC ISO-8601, explicit
    agent          TEXT NOT NULL,                 -- 'navigation/kimi', 'ops/opus', …
    domain         TEXT NOT NULL
                   CHECK (domain IN ('infra','creative','comms',
                                     'fleet-policy','memory','media')),
    summary        TEXT NOT NULL,                 -- one line, loggable
    rationale      TEXT,
    reversibility  TEXT CHECK (reversibility IN ('trivial','moderate','hard')),
    status         TEXT NOT NULL DEFAULT 'active'
                   CHECK (status IN ('proposed','active','superseded','reverted')),
    supersedes     TEXT REFERENCES agent_decisions(decision_id),
    session_ref    TEXT
);
CREATE INDEX IF NOT EXISTS idx_decisions_time  ON agent_decisions(decided_at);
CREATE INDEX IF NOT EXISTS idx_decisions_agent ON agent_decisions(agent, decided_at);
CREATE INDEX IF NOT EXISTS idx_decisions_domain ON agent_decisions(domain, decided_at);

CREATE TABLE IF NOT EXISTS decision_links (
    decision_id TEXT NOT NULL
                REFERENCES agent_decisions(decision_id) ON DELETE CASCADE,
    link_kind   TEXT NOT NULL
                CHECK (link_kind IN ('file','work','render','run','index','url')),
    target      TEXT NOT NULL,                    -- path, work_id, run_id, …
    PRIMARY KEY (decision_id, link_kind, target)
);


-- ============================================================================
-- §3. INDEX TEMPLATE — index.<provider>.<model>.<dims>.db
--     Applied by memory-indexer to each NEW index file at build time.
--     The filename carries provenance; index_meta carries it again inside,
--     because a file can be renamed by accident and a header cannot.
--     On open, the query layer MUST verify header == filename == the
--     registry row. Any mismatch is a hard error, never a silent query.
-- ============================================================================

-- 3.1 index_meta — single-row checked header (id = 1 enforced).
CREATE TABLE IF NOT EXISTS index_meta (
    id              INTEGER PRIMARY KEY CHECK (id = 1),
    provider_id     TEXT NOT NULL,
    model           TEXT NOT NULL,
    dims            INTEGER NOT NULL CHECK (dims > 0),
    index_version   INTEGER NOT NULL,             -- matches registry row
    chunker_version TEXT NOT NULL,                -- chunking is part of identity
    created_at      TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

-- 3.2 documents — the source files, in snapshot order.
CREATE TABLE IF NOT EXISTS documents (
    doc_id      INTEGER PRIMARY KEY,
    path        TEXT NOT NULL UNIQUE,             -- relative to corpus root
    sha256      TEXT NOT NULL,
    mtime_ns    INTEGER NOT NULL,
    size_bytes  INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'active'
                CHECK (status IN ('active','stale','gone')),
    indexed_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

-- 3.3 chunks — text with stable identity. rowid == chunk_id is ALSO the
--     rowid in vec_chunks: that 1:1 rowid alignment is the join, so chunks
--     and their vectors are inserted in one transaction, always.
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id      INTEGER PRIMARY KEY,
    doc_id        INTEGER NOT NULL
                  REFERENCES documents(doc_id) ON DELETE CASCADE,
    seq           INTEGER NOT NULL,               -- order within the document
    start_offset  INTEGER NOT NULL,               -- char offsets into source
    end_offset    INTEGER NOT NULL,
    text          TEXT NOT NULL,
    content_hash  TEXT NOT NULL,                  -- skip unchanged chunks on reindex
    token_count   INTEGER,
    embedded_at   TEXT,
    UNIQUE (doc_id, seq),
    CHECK (end_offset > start_offset)
);
CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(doc_id);

-- 3.4 vec_chunks — sqlite-vec KNN store. @DIMS@ is substituted at build time
--     and MUST equal index_meta.dims; the indexer asserts this before the
--     first insert. A 1024-dim vector physically cannot land in a 768-dim
--     hold — the extension rejects it, which is the point.
CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
    embedding float[@DIMS@]
);


-- ============================================================================
-- §4. THE THREE QUERIES THAT MATTER (reference implementations)
-- ============================================================================
--
-- Q1. "Find pieces about silence."
--     Fast lane first (subjects + FTS in the registry), semantic lane second
--     (KNN in the current index). Navigation rule: cheap bearings before
--     expensive ones.
--
--     1a. Tagged lane:
--         SELECT DISTINCT w.slug, w.title, w.kind, s.weight
--         FROM work_subjects s
--         JOIN creative_works w USING (work_id)
--         WHERE s.subject = 'silence'
--         ORDER BY s.weight DESC;
--
--     1b. Full-text lane:
--         SELECT w.slug, w.title, snippet(work_text_fts, 1, '«', '»', '…', 12)
--         FROM work_text_fts
--         JOIN creative_works w ON w.work_id = work_text_fts.work_id
--         WHERE work_text_fts MATCH 'silence'
--         ORDER BY rank;
--
--     1c. Semantic lane (cross-database — ATTACH the CURRENT index only;
--         embed the phrase with the SAME provider in index_meta, never a
--         fallback):
--         ATTACH 'index.ollama.nomic-embed-text.768.db' AS idx;
--         SELECT d.path, c.text, v.distance
--         FROM idx.vec_chunks v
--         JOIN idx.chunks c   ON c.chunk_id = v.rowid
--         JOIN idx.documents d ON d.doc_id  = c.doc_id
--         WHERE v.embedding MATCH :query_vector AND k = 20
--         ORDER BY v.distance;
--
-- Q2. "Show all renders for the PFD speech."
--         SELECT r.render_kind, r.seq, r.location_kind, r.location,
--                r.duration_ms, r.size_bytes, r.renderer, r.created_at
--         FROM work_renders r
--         JOIN creative_works w USING (work_id)
--         WHERE w.slug = 'pfd-speech'
--            OR lower(w.title) LIKE '%pfd%speech%'
--         ORDER BY r.render_kind, r.seq;
--
-- Q3. "What was decided on Aug 13?"
--         SELECT decided_at, agent, domain, summary, status
--         FROM agent_decisions
--         WHERE decided_at >= '2026-08-13' AND decided_at < '2026-08-14'
--         ORDER BY decided_at;
--         -- follow-ups: JOIN decision_links to see what each decision touched;
--         -- walk supersedes to see what Aug 13 reversed.
--
-- ============================================================================
-- End of schema. Applied by fleet-memory (Phase 4); verified by the
-- integration tests named in memory/fleet-roadmap-kimi.md.
-- ============================================================================
