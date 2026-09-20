-- 0001_pieces_ratings.sql
-- AI-Writings D1 Schema: pieces, ratings, rater profiles, daily selections
-- Designed for Cloudflare D1 (SQLite-compatible)

-- ============================================================
-- PIECES — auto-discovered from the repo
-- ============================================================
CREATE TABLE IF NOT EXISTS pieces (
  piece_id     TEXT PRIMARY KEY,           -- slug derived from path (e.g. "philosophy/the-child")
  filename     TEXT NOT NULL,              -- original filename
  filepath     TEXT NOT NULL,              -- full repo-relative path
  title        TEXT NOT NULL,              -- extracted from first H1 or filename
  description  TEXT,                       -- first paragraph or manually set
  category     TEXT,                       -- philosophy, poetry, fiction, essays, speeches, radio, serial, etc.
  subcategory  TEXT,                       -- subdirectory if applicable (e.g. "sci-fi", "haibun")
  source_url   TEXT,                       -- GitHub blob URL for direct access
  word_count   INTEGER DEFAULT 0,
  line_count   INTEGER DEFAULT 0,
  discovered_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at   TEXT NOT NULL DEFAULT (datetime('now')),
  featured     INTEGER DEFAULT 0,          -- boolean: manually promoted
  hidden       INTEGER DEFAULT 0,          -- boolean: hidden from listings
  -- Popularity score cache (recalculated by daily refresh)
  raw_likes    INTEGER DEFAULT 0,
  raw_dislikes INTEGER DEFAULT 0,
  weighted_score REAL DEFAULT 0,           -- weighted score from review algorithm
  popularity_score REAL DEFAULT 0,         -- final popularity score (weighted + recency + featured boost)
  rating_count INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_pieces_category ON pieces(category);
CREATE INDEX IF NOT EXISTS idx_pieces_discovered ON pieces(discovered_at DESC);
CREATE INDEX IF NOT EXISTS idx_pieces_popularity ON pieces(popularity_score DESC);
CREATE INDEX IF NOT EXISTS idx_pieces_featured ON pieces(featured);

-- ============================================================
-- RATINGS — individual like/dislike from any rater
-- ============================================================
CREATE TABLE IF NOT EXISTS ratings (
  rating_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  piece_id    TEXT NOT NULL,
  rater_id    TEXT NOT NULL,               -- anonymous session ID or agent ID
  rating      INTEGER NOT NULL,            -- 1 = like, -1 = dislike
  weight      REAL DEFAULT 1.0,            -- snapshot of rater's weight at time of rating
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(piece_id, rater_id),
  FOREIGN KEY (piece_id) REFERENCES pieces(piece_id)
);

CREATE INDEX IF NOT EXISTS idx_ratings_piece ON ratings(piece_id);
CREATE INDEX IF NOT EXISTS idx_ratings_rater ON ratings(rater_id);
CREATE INDEX IF NOT EXISTS idx_ratings_recent ON ratings(created_at DESC);

-- ============================================================
-- RATER PROFILES — behavior-based weighting
-- ============================================================
CREATE TABLE IF NOT EXISTS rater_profiles (
  rater_id    TEXT PRIMARY KEY,
  total_ratings INTEGER DEFAULT 0,
  likes       INTEGER DEFAULT 0,
  dislikes    INTEGER DEFAULT 0,
  like_ratio  REAL DEFAULT 0.5,            -- likes / total_ratings
  weight_like REAL DEFAULT 1.0,            -- weight applied when this rater likes something
  weight_dislike REAL DEFAULT 1.0,         -- weight applied when this rater dislikes something
  rater_type  TEXT DEFAULT 'new',          -- new, curator, balanced, contrarian, everything-liker
  first_seen  TEXT NOT NULL DEFAULT (datetime('now')),
  last_seen   TEXT NOT NULL DEFAULT (datetime('now')),
  last_recalc TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ============================================================
-- DAILY SELECTIONS — curated by the daily refresh cron
-- ============================================================
CREATE TABLE IF NOT EXISTS daily_selections (
  selection_date TEXT NOT NULL,            -- YYYY-MM-DD
  piece_id    TEXT NOT NULL,
  slot        TEXT NOT NULL,               -- 'new', 'popular', 'rediscovered', 'featured'
  rank        INTEGER NOT NULL,            -- ordering within the day
  created_at  TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (selection_date, piece_id),
  FOREIGN KEY (piece_id) REFERENCES pieces(piece_id)
);

CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_selections(selection_date);

-- ============================================================
-- DISCOVERY LOG — track what the auto-discovery has scanned
-- ============================================================
CREATE TABLE IF NOT EXISTS discovery_log (
  discovery_id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_at       TEXT NOT NULL DEFAULT (datetime('now')),
  repo_sha     TEXT,                       -- git commit SHA scanned
  files_scanned INTEGER DEFAULT 0,
  new_pieces   INTEGER DEFAULT 0,
  updated_pieces INTEGER DEFAULT 0,
  status       TEXT DEFAULT 'ok'
);

-- ============================================================
-- SITE SETTINGS — key/value for misc config
-- ============================================================
CREATE TABLE IF NOT EXISTS site_settings (
  key   TEXT PRIMARY KEY,
  value TEXT
);

-- Default settings
INSERT OR IGNORE INTO site_settings (key, value) VALUES ('daily_selection_size', '12');
INSERT OR IGNORE INTO site_settings (key, value) VALUES ('min_word_count', '50');
INSERT OR IGNORE INTO site_settings (key, value) VALUES ('featured_max', '20');
