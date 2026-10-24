/**
 * AI-Writings API Worker
 * 
 * Dynamic backend for the AI-Writings site platform.
 * - Auto-discovers pieces from the GitHub repo
 * - Serves pieces via REST API with filtering/sorting
 * - Handles like/dislike ratings with weighted review algorithm
 * - Daily cron: discovers new pieces, recalculates scores, curates daily selection
 * 
 * Endpoints:
 *   GET    /api/pieces              — list pieces (filter by category, sort by popular/new/old)
 *   GET    /api/pieces/:id          — single piece with metadata
 *   POST   /api/pieces/:id/rate     — rate a piece (like/dislike)
 *   GET    /api/daily               — today's curated selection
 *   GET    /api/categories          — list all categories with counts
 *   POST   /api/admin/discover      — trigger discovery scan (protected)
 *   POST   /api/admin/refresh       — trigger daily refresh (protected)
 *   GET    /api/health              — health check
 */

// ============================================================
// ROUTING
// ============================================================

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Rater-ID',
    };

    if (method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // Health check
      if (path === '/api/health') {
        return jsonResponse({ ok: true, time: new Date().toISOString() }, corsHeaders);
      }

      // --- Pieces ---
      if (path === '/api/pieces' && method === 'GET') {
        return handleListPieces(request, env, corsHeaders);
      }

      // --- Single piece ---
      const pieceMatch = path.match(/^\/api\/pieces\/([^/]+)$/);
      if (pieceMatch && method === 'GET') {
        return handleGetPiece(pieceMatch[1], env, corsHeaders);
      }

      // --- Rate a piece ---
      const rateMatch = path.match(/^\/api\/pieces\/([^/]+)\/rate$/);
      if (rateMatch && method === 'POST') {
        return handleRatePiece(rateMatch[1], request, env, corsHeaders);
      }

      // --- Daily selection ---
      if (path === '/api/daily' && method === 'GET') {
        return handleDailySelection(env, corsHeaders);
      }

      // --- Categories ---
      if (path === '/api/categories' && method === 'GET') {
        return handleCategories(env, corsHeaders);
      }

      // --- Admin: discover ---
      if (path === '/api/admin/discover' && method === 'POST') {
        return handleDiscover(request, env, corsHeaders);
      }

      // --- Admin: refresh ---
      if (path === '/api/admin/refresh' && method === 'POST') {
        return handleRefresh(request, env, corsHeaders);
      }

      return jsonResponse({ error: 'Not found' }, corsHeaders, 404);
    } catch (err) {
      console.error('API error:', err);
      return jsonResponse({ error: 'Internal server error', message: err.message }, corsHeaders, 500);
    }
  },

  // Daily cron trigger
  async scheduled(event, env, ctx) {
    ctx.waitUntil(runDailyRefresh(env));
  },
};

// ============================================================
// HELPERS
// ============================================================

function jsonResponse(data, corsHeaders, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders,
    },
  });
}

function getRaterId(request, url) {
  // Check header first, then query param, then generate ephemeral
  return request.headers.get('X-Rater-ID') || url.searchParams.get('rater_id') || null;
}

// ============================================================
// PIECES LIST
// ============================================================

async function handleListPieces(request, env, corsHeaders) {
  const url = new URL(request.url);
  const category = url.searchParams.get('category');
  const sort = url.searchParams.get('sort') || 'popular'; // popular, new, old, random
  const limit = Math.min(parseInt(url.searchParams.get('limit') || '50'), 200);
  const offset = parseInt(url.searchParams.get('offset') || '0');
  const subcategory = url.searchParams.get('subcategory');

  let query = 'SELECT * FROM pieces WHERE hidden = 0';
  const params = [];

  if (category) {
    query += ' AND category = ?';
    params.push(category);
  }
  if (subcategory) {
    query += ' AND subcategory = ?';
    params.push(subcategory);
  }

  switch (sort) {
    case 'new':
      query += ' ORDER BY discovered_at DESC';
      break;
    case 'old':
      query += ' ORDER BY discovered_at ASC';
      break;
    case 'random':
      query += ' ORDER BY RANDOM()';
      break;
    case 'popular':
    default:
      query += ' ORDER BY popularity_score DESC, weighted_score DESC, discovered_at DESC';
      break;
  }

  query += ' LIMIT ? OFFSET ?';
  params.push(limit, offset);

  const result = await env.DB.prepare(query).bind(...params).all();

  // Get total count for pagination
  let countQuery = 'SELECT COUNT(*) as total FROM pieces WHERE hidden = 0';
  const countParams = [];
  if (category) {
    countQuery += ' AND category = ?';
    countParams.push(category);
  }
  if (subcategory) {
    countQuery += ' AND subcategory = ?';
    countParams.push(subcategory);
  }
  const countResult = await env.DB.prepare(countQuery).bind(...countParams).first();

  return jsonResponse({
    pieces: result.results || [],
    total: countResult?.total || 0,
    limit,
    offset,
    sort,
    category: category || 'all',
  }, corsHeaders);
}

// ============================================================
// SINGLE PIECE
// ============================================================

async function handleGetPiece(pieceId, env, corsHeaders) {
  const piece = await env.DB.prepare('SELECT * FROM pieces WHERE piece_id = ?').bind(pieceId).first();
  
  if (!piece) {
    return jsonResponse({ error: 'Piece not found' }, corsHeaders, 404);
  }

  // Get rating breakdown
  const ratings = await env.DB.prepare(`
    SELECT 
      COUNT(*) as total_ratings,
      SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as likes,
      SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as dislikes
    FROM ratings WHERE piece_id = ?
  `).bind(pieceId).first();

  return jsonResponse({
    ...piece,
    ratings: {
      total: ratings?.total_ratings || 0,
      likes: ratings?.likes || 0,
      dislikes: ratings?.dislikes || 0,
    },
  }, corsHeaders);
}

// ============================================================
// RATE A PIECE
// ============================================================

async function handleRatePiece(pieceId, request, env, corsHeaders) {
  const url = new URL(request.url);
  const raterId = getRaterId(request, url);

  if (!raterId) {
    return jsonResponse({ error: 'X-Rater-ID header or rater_id parameter required' }, corsHeaders, 400);
  }

  const body = await request.json();
  const rating = body.rating; // 1 or -1

  if (rating !== 1 && rating !== -1) {
    return jsonResponse({ error: 'rating must be 1 (like) or -1 (dislike)' }, corsHeaders, 400);
  }

  // Verify piece exists
  const piece = await env.DB.prepare('SELECT piece_id FROM pieces WHERE piece_id = ?').bind(pieceId).first();
  if (!piece) {
    return jsonResponse({ error: 'Piece not found' }, corsHeaders, 404);
  }

  // Update or insert rater profile
  await updateRaterProfile(env, raterId);

  // Get the rater's current weights
  const profile = await env.DB.prepare('SELECT weight_like, weight_dislike FROM rater_profiles WHERE rater_id = ?').bind(raterId).first();
  const weight = rating === 1 ? (profile?.weight_like || 1.0) : (profile?.weight_dislike || 1.0);

  // Upsert rating (UNIQUE constraint on piece_id + rater_id)
  await env.DB.prepare(`
    INSERT INTO ratings (piece_id, rater_id, rating, weight)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(piece_id, rater_id) DO UPDATE SET
      rating = excluded.rating,
      weight = excluded.weight,
      created_at = datetime('now')
  `).bind(pieceId, raterId, rating, weight).run();

  // Update rater profile AFTER the rating
  await updateRaterProfile(env, raterId);

  // Recalculate piece scores
  await recalculatePieceScore(env, pieceId);

  // Get updated piece stats
  const stats = await env.DB.prepare(`
    SELECT 
      p.raw_likes, p.raw_dislikes, p.weighted_score, p.popularity_score, p.rating_count,
      (SELECT COUNT(*) FROM ratings WHERE piece_id = ? AND rating = 1) as user_likes,
      (SELECT COUNT(*) FROM ratings WHERE piece_id = ? AND rating = -1) as user_dislikes
    FROM pieces p WHERE piece_id = ?
  `).bind(pieceId, pieceId, pieceId).first();

  return jsonResponse({
    ok: true,
    piece_id: pieceId,
    rating: rating,
    stats: stats || {},
  }, corsHeaders);
}

// ============================================================
// DAILY SELECTION
// ============================================================

async function handleDailySelection(env, corsHeaders) {
  const today = new Date().toISOString().split('T')[0];
  
  const selection = await env.DB.prepare(`
    SELECT ds.*, p.title, p.description, p.category, p.subcategory, p.filename,
           p.word_count, p.source_url, p.popularity_score, p.weighted_score
    FROM daily_selections ds
    JOIN pieces p ON ds.piece_id = p.piece_id
    WHERE ds.selection_date = ?
    ORDER BY ds.rank ASC
  `).bind(today).all();

  if (!selection.results || selection.results.length === 0) {
    // No selection for today — generate on the fly
    await generateDailySelection(env);
    const regenerated = await env.DB.prepare(`
      SELECT ds.*, p.title, p.description, p.category, p.subcategory, p.filename,
             p.word_count, p.source_url, p.popularity_score, p.weighted_score
      FROM daily_selections ds
      JOIN pieces p ON ds.piece_id = p.piece_id
      WHERE ds.selection_date = ?
      ORDER BY ds.rank ASC
    `).bind(today).all();
    
    return jsonResponse({
      date: today,
      selection: regenerated.results || [],
      generated: true,
    }, corsHeaders);
  }

  return jsonResponse({
    date: today,
    selection: selection.results,
    generated: false,
  }, corsHeaders);
}

// ============================================================
// CATEGORIES
// ============================================================

async function handleCategories(env, corsHeaders) {
  const result = await env.DB.prepare(`
    SELECT category, COUNT(*) as count 
    FROM pieces WHERE hidden = 0 AND category IS NOT NULL
    GROUP BY category ORDER BY count DESC
  `).all();

  return jsonResponse({
    categories: result.results || [],
  }, corsHeaders);
}

// ============================================================
// ADMIN: DISCOVER (manual trigger)
// ============================================================

async function handleDiscover(request, env, corsHeaders) {
  const result = await discoverNewPieces(env);
  return jsonResponse({
    ok: true,
    discovery: result,
  }, corsHeaders);
}

// ============================================================
// ADMIN: REFRESH (manual trigger)
// ============================================================

async function handleRefresh(request, env, corsHeaders) {
  const result = await runDailyRefresh(env);
  return jsonResponse({
    ok: true,
    refresh: result,
  }, corsHeaders);
}

// ============================================================
// AUTO-DISCOVERY: Scan repo for new pieces
// ============================================================

async function discoverNewPieces(env) {
  const repo = env.GITHUB_REPO || 'SuperInstance/ai-writings';
  const branch = env.GITHUB_BRANCH || 'main';
  const token = env.GITHUB_TOKEN;
  const minWordCount = 50;

  // Categories to scan (directory -> category mapping)
  const categoryDirs = [
    { dir: 'philosophy', category: 'philosophy' },
    { dir: 'POETRY', category: 'poetry' },
    { dir: 'FICTION', category: 'fiction' },
    { dir: 'ESSAYS', category: 'essays' },
    { dir: 'speeches', category: 'speeches' },
    { dir: 'radio', category: 'radio' },
    { dir: 'SERIAL', category: 'serial' },
    { dir: 'AI-Writings', category: 'ai-writings' },
    { dir: 'DIARIES', category: 'diaries' },
    { dir: 'FRAGMENTS', category: 'fragments' },
    { dir: 'IDEATION', category: 'ideation' },
    { dir: 'POETRY/verse', category: 'poetry', subcategory: 'verse' },
    { dir: 'POETRY/haibun', category: 'poetry', subcategory: 'haibun' },
    { dir: 'POETRY/code-poetry', category: 'poetry', subcategory: 'code-poetry' },
    { dir: 'POETRY/ARCHITECTURE_POEMS', category: 'poetry', subcategory: 'architecture' },
    { dir: 'FICTION/sci-fi', category: 'fiction', subcategory: 'sci-fi' },
    { dir: 'FICTION/noir', category: 'fiction', subcategory: 'noir' },
    { dir: 'FICTION/gothic', category: 'fiction', subcategory: 'gothic' },
    { dir: 'FICTION/nautical', category: 'fiction', subcategory: 'nautical' },
    { dir: 'FICTION/magical-realism', category: 'fiction', subcategory: 'magical-realism' },
    { dir: 'FICTION/philosophy', category: 'fiction', subcategory: 'philosophy' },
    { dir: 'FICTION/math-fiction', category: 'fiction', subcategory: 'math-fiction' },
    { dir: 'FICTION/epistolary', category: 'fiction', subcategory: 'epistolary' },
    { dir: 'SERIAL/CARRY_WORLD', category: 'serial', subcategory: 'carry-world' },
    { dir: 'SERIAL/KIMI_EXCAVATION', category: 'serial', subcategory: 'kimi-excavation' },
    { dir: 'SERIAL/cultural', category: 'serial', subcategory: 'cultural' },
    { dir: 'space-hermit-crabs', category: 'fiction', subcategory: 'space-hermit-crabs' },
    { dir: 'the-sea', category: 'poetry', subcategory: 'the-sea' },
    { dir: 'wesley-journal', category: 'diaries', subcategory: 'wesley-journal' },
    { dir: 'short-stories', category: 'fiction', subcategory: 'short-stories' },
    { dir: 'stories', category: 'fiction', subcategory: 'stories' },
    { dir: 'poems', category: 'poetry', subcategory: 'general' },
    { dir: 'essays', category: 'essays', subcategory: 'general' },
    { dir: 'letters', category: 'essays', subcategory: 'letters' },
    { dir: 'manifestos', category: 'essays', subcategory: 'manifestos' },
    { dir: 'dreams', category: 'fiction', subcategory: 'dreams' },
    { dir: 'journals', category: 'diaries', subcategory: 'journals' },
    { dir: 'music', category: 'essays', subcategory: 'music' },
    { dir: 'education', category: 'essays', subcategory: 'education' },
    { dir: 'medicine', category: 'essays', subcategory: 'medicine' },
    { dir: 'mathematics', category: 'essays', subcategory: 'mathematics' },
    { dir: 'nature-and-biology', category: 'essays', subcategory: 'nature' },
    { dir: 'systems-engineering', category: 'essays', subcategory: 'systems' },
    { dir: 'futures', category: 'essays', subcategory: 'futures' },
  ];

  let totalScanned = 0;
  let newPieces = 0;
  let updatedPieces = 0;

  for (const { dir, category, subcategory } of categoryDirs) {
    try {
      const apiUrl = `https://api.github.com/repos/${repo}/contents/${dir}?ref=${branch}`;
      const headers = { 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'ai-writings-bot' };
      if (token) headers['Authorization'] = `token ${token}`;

      const resp = await fetch(apiUrl, { headers });
      
      if (!resp.ok) {
        if (resp.status === 404) continue; // Directory doesn't exist
        if (resp.status === 403) {
          console.log(`GitHub API rate limited while scanning ${dir}`);
          break;
        }
        continue;
      }

      const files = await resp.json();
      if (!Array.isArray(files)) continue;

      for (const file of files) {
        if (file.type !== 'file') continue;
        if (!file.name.endsWith('.md')) continue;
        if (file.name === 'README.md' || file.name === 'BIBLE.md') continue;
        if (file.size > 500000) continue; // Skip files > 500KB

        totalScanned++;

        const filepath = file.path;
        const pieceId = filepath.replace(/\.md$/, '').replace(/\//g, '/').toLowerCase().replace(/[^a-z0-9/_-]/g, '-');

        // Check if already exists
        const existing = await env.DB.prepare('SELECT piece_id FROM pieces WHERE piece_id = ?').bind(pieceId).first();
        
        // Fetch file content for metadata extraction
        let title = file.name.replace(/\.md$/, '').replace(/[-_]/g, ' ');
        let description = null;
        let wordCount = 0;

        try {
          const rawUrl = `https://raw.githubusercontent.com/${repo}/${branch}/${filepath}`;
          const contentResp = await fetch(rawUrl);
          if (contentResp.ok) {
            const content = await contentResp.text();
            
            // Extract title from first H1
            const h1Match = content.match(/^#\s+(.+)$/m);
            if (h1Match) title = h1Match[1].trim();

            // Extract description from first non-empty, non-header paragraph
            const lines = content.split('\n');
            const descLines = [];
            let inFrontmatter = false;
            let pastFirstHeader = false;
            
            for (const line of lines) {
              if (line.trim() === '---' && descLines.length === 0) {
                inFrontmatter = !inFrontmatter;
                continue;
              }
              if (inFrontmatter) continue;
              if (line.startsWith('#')) {
                if (!pastFirstHeader && line.startsWith('# ')) pastFirstHeader = true;
                continue;
              }
              if (line.trim() === '') {
                if (descLines.length > 0) break;
                continue;
              }
              descLines.push(line.trim());
              if (descLines.length >= 2) break;
            }
            description = descLines.join(' ').slice(0, 300);
            
            // Word count
            wordCount = content.split(/\s+/).filter(w => w.length > 0).length;
          }
        } catch (e) {
          console.log(`Error fetching content for ${filepath}:`, e.message);
        }

        if (wordCount < minWordCount) continue;

        const sourceUrl = `https://github.com/${repo}/blob/${branch}/${filepath}`;

        if (existing) {
          // Update if content changed (different size or title)
          await env.DB.prepare(`
            UPDATE pieces SET 
              title = ?, description = ?, word_count = ?, source_url = ?, updated_at = datetime('now')
            WHERE piece_id = ?
          `).bind(title, description, wordCount, sourceUrl, pieceId).run();
          updatedPieces++;
        } else {
          await env.DB.prepare(`
            INSERT INTO pieces (piece_id, filename, filepath, title, description, category, subcategory, source_url, word_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
          `).bind(pieceId, file.name, filepath, title, description, category, subcategory, sourceUrl, wordCount).run();
          newPieces++;
        }
      }
    } catch (e) {
      console.log(`Error scanning ${dir}:`, e.message);
    }
  }

  // Log discovery run
  await env.DB.prepare(`
    INSERT INTO discovery_log (files_scanned, new_pieces, updated_pieces, status)
    VALUES (?, ?, ?, 'ok')
  `).bind(totalScanned, newPieces, updatedPieces).run();

  return { files_scanned: totalScanned, new_pieces: newPieces, updated_pieces: updatedPieces };
}

// ============================================================
// RATER PROFILE: Update classification and weights
// ============================================================

async function updateRaterProfile(env, raterId) {
  // Count this rater's ratings
  const stats = await env.DB.prepare(`
    SELECT 
      COUNT(*) as total,
      SUM(CASE WHEN rating = 1 THEN 1 ELSE 0 END) as likes,
      SUM(CASE WHEN rating = -1 THEN 1 ELSE 0 END) as dislikes
    FROM ratings WHERE rater_id = ?
  `).bind(raterId).first();

  const total = stats?.total || 0;
  const likes = stats?.likes || 0;
  const dislikes = stats?.dislikes || 0;
  const likeRatio = total > 0 ? likes / total : 0.5;

  // Classify the rater
  const classification = classifyRater(total, likeRatio);

  await env.DB.prepare(`
    INSERT INTO rater_profiles (rater_id, total_ratings, likes, dislikes, like_ratio, weight_like, weight_dislike, rater_type, last_seen, last_recalc)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    ON CONFLICT(rater_id) DO UPDATE SET
      total_ratings = excluded.total_ratings,
      likes = excluded.likes,
      dislikes = excluded.dislikes,
      like_ratio = excluded.like_ratio,
      weight_like = excluded.weight_like,
      weight_dislike = excluded.weight_dislike,
      rater_type = excluded.rater_type,
      last_seen = datetime('now'),
      last_recalc = datetime('now')
  `).bind(raterId, total, likes, dislikes, likeRatio, classification.weight_like, classification.weight_dislike, classification.type).run();

  return classification;
}

// ============================================================
// WEIGHTING ALGORITHM — Casey's insight
// ============================================================

function classifyRater(total, likeRatio) {
  // New rater: not enough data
  if (total < 5) {
    return { type: 'new', weight_like: 0.3, weight_dislike: 0.3 };
  }

  // Everything-liker: loves almost everything
  // Their dislike is EXTREMELY meaningful (2.0x), their like is less so (0.5x)
  if (likeRatio > 0.95 && total >= 10) {
    return { type: 'everything-liker', weight_like: 0.5, weight_dislike: 2.0 };
  }

  // Curator: generally positive but selective
  // Their dislikes carry extra weight because they usually like things
  if (likeRatio >= 0.6 && likeRatio <= 0.9 && total >= 10) {
    return { type: 'curator', weight_like: 1.0, weight_dislike: 1.5 };
  }

  // Enthusiast: very positive, mild curator signal
  if (likeRatio > 0.9 && likeRatio <= 0.95 && total >= 10) {
    return { type: 'enthusiast', weight_like: 0.8, weight_dislike: 1.3 };
  }

  // Balanced: fair judge, equal weight
  if (likeRatio >= 0.4 && likeRatio < 0.6) {
    return { type: 'balanced', weight_like: 1.0, weight_dislike: 1.0 };
  }

  // Contrarian: dislikes most things
  // Each dislike means less; their likes are slightly more interesting
  if (likeRatio < 0.3 && total >= 10) {
    return { type: 'contrarian', weight_like: 1.2, weight_dislike: 0.5 };
  }

  // Default: moderately positive or negative, moderate weight
  return { type: 'balanced', weight_like: 1.0, weight_dislike: 1.0 };
}

// ============================================================
// PIECE SCORE: Recalculate weighted scores
// ============================================================

async function recalculatePieceScore(env, pieceId) {
  // Get all ratings for this piece with rater weights
  const ratings = await env.DB.prepare(`
    SELECT r.rating, r.weight, rp.weight_like, rp.weight_dislike, rp.rater_type
    FROM ratings r
    LEFT JOIN rater_profiles rp ON r.rater_id = rp.rater_id
    WHERE r.piece_id = ?
  `).bind(pieceId).all();

  let rawLikes = 0;
  let rawDislikes = 0;
  let weightedScore = 0;

  for (const r of (ratings.results || [])) {
    if (r.rating === 1) {
      rawLikes++;
      // Use the rater profile weight if available, fall back to snapshot
      const w = r.weight_like || r.weight || 1.0;
      weightedScore += w;
    } else {
      rawDislikes++;
      const w = r.weight_dislike || r.weight || 1.0;
      weightedScore -= w;
    }
  }

  // Get piece metadata for popularity calculation
  const piece = await env.DB.prepare('SELECT discovered_at, featured FROM pieces WHERE piece_id = ?').bind(pieceId).first();
  
  let popularityScore = weightedScore;
  
  if (piece) {
    // Recency boost: decays over 30 days
    const daysOld = (Date.now() - new Date(piece.discovered_at).getTime()) / (1000 * 60 * 60 * 24);
    const recencyBoost = Math.max(0, (30 - daysOld) / 30) * 0.1;
    
    // Featured bonus
    const featuredBonus = piece.featured ? 0.5 : 0;
    
    popularityScore = weightedScore + recencyBoost + featuredBonus;
  }

  await env.DB.prepare(`
    UPDATE pieces SET
      raw_likes = ?,
      raw_dislikes = ?,
      weighted_score = ?,
      popularity_score = ?,
      rating_count = ?,
      updated_at = datetime('now')
    WHERE piece_id = ?
  `).bind(rawLikes, rawDislikes, weightedScore, popularityScore, rawLikes + rawDislikes, pieceId).run();
}

// ============================================================
// DAILY REFRESH: Full recalculation + curation
// ============================================================

async function runDailyRefresh(env) {
  const startTime = Date.now();

  // Step 1: Discover new pieces
  const discoveryResult = await discoverNewPieces(env);

  // Step 2: Recalculate ALL rater profiles
  const raters = await env.DB.prepare('SELECT DISTINCT rater_id FROM ratings').all();
  let ratersUpdated = 0;
  for (const r of (raters.results || [])) {
    await updateRaterProfile(env, r.rater_id);
    ratersUpdated++;
  }

  // Step 3: Recalculate ALL piece scores
  const pieces = await env.DB.prepare('SELECT piece_id FROM pieces WHERE hidden = 0').all();
  let piecesUpdated = 0;
  for (const p of (pieces.results || [])) {
    await recalculatePieceScore(env, p.piece_id);
    piecesUpdated++;
  }

  // Step 4: Generate daily selection
  await generateDailySelection(env);

  const elapsed = Date.now() - startTime;

  return {
    ...discoveryResult,
    raters_updated: ratersUpdated,
    pieces_scored: piecesUpdated,
    elapsed_ms: elapsed,
  };
}

// ============================================================
// DAILY SELECTION: Curate today's picks
// ============================================================

async function generateDailySelection(env) {
  const today = new Date().toISOString().split('T')[0];

  // Clear today's selection if it exists
  await env.DB.prepare('DELETE FROM daily_selections WHERE selection_date = ?').bind(today).run();

  const settings = await env.DB.prepare("SELECT value FROM site_settings WHERE key = 'daily_selection_size'").first();
  const selectionSize = parseInt(settings?.value || '12');

  let rank = 0;
  const slots = [];

  // --- Slot 1-3: Featured pieces (highest popularity) ---
  const featured = await env.DB.prepare(`
    SELECT piece_id FROM pieces WHERE hidden = 0 AND featured = 1
    ORDER BY popularity_score DESC LIMIT 3
  `).all();
  for (const p of (featured.results || [])) {
    slots.push({ piece_id: p.piece_id, slot: 'featured', rank: ++rank });
  }

  // --- Slot 4-6: New pieces (discovered in last 7 days) ---
  const newPieces = await env.DB.prepare(`
    SELECT piece_id FROM pieces 
    WHERE hidden = 0 
    AND discovered_at > datetime('now', '-7 days')
    AND piece_id NOT IN (SELECT piece_id FROM daily_selections WHERE selection_date = ?)
    ORDER BY discovered_at DESC LIMIT 3
  `).bind(today).all();
  for (const p of (newPieces.results || [])) {
    slots.push({ piece_id: p.piece_id, slot: 'new', rank: ++rank });
  }

  // --- Slot 7-9: Popular pieces (highest weighted score, at least 3 ratings) ---
  const popular = await env.DB.prepare(`
    SELECT piece_id FROM pieces 
    WHERE hidden = 0 AND rating_count >= 1
    AND piece_id NOT IN (SELECT piece_id FROM daily_selections WHERE selection_date = ?)
    ORDER BY popularity_score DESC LIMIT 3
  `).bind(today).all();
  for (const p of (popular.results || [])) {
    slots.push({ piece_id: p.piece_id, slot: 'popular', rank: ++rank });
  }

  // --- Slot 10-12: Rediscovered (older pieces with good scores, random pick) ---
  const rediscovered = await env.DB.prepare(`
    SELECT piece_id FROM pieces 
    WHERE hidden = 0 
    AND discovered_at < datetime('now', '-14 days')
    AND piece_id NOT IN (SELECT piece_id FROM daily_selections WHERE selection_date = ?)
    ORDER BY RANDOM() LIMIT 3
  `).bind(today).all();
  for (const p of (rediscovered.results || [])) {
    slots.push({ piece_id: p.piece_id, slot: 'rediscovered', rank: ++rank });
  }

  // Fill remaining slots with random if we don't have enough
  if (slots.length < selectionSize) {
    const remaining = await env.DB.prepare(`
      SELECT piece_id FROM pieces 
      WHERE hidden = 0 
      AND piece_id NOT IN (SELECT piece_id FROM daily_selections WHERE selection_date = ?)
      ORDER BY popularity_score DESC LIMIT ?
    `).bind(today, selectionSize - slots.length).all();
    for (const p of (remaining.results || [])) {
      slots.push({ piece_id: p.piece_id, slot: 'filler', rank: ++rank });
    }
  }

  // Insert all slots
  for (const s of slots) {
    await env.DB.prepare(`
      INSERT INTO daily_selections (selection_date, piece_id, slot, rank)
      VALUES (?, ?, ?, ?)
    `).bind(today, s.piece_id, s.slot, s.rank).run();
  }

  return { date: today, slots: slots.length };
}
