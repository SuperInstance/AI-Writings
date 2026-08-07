/**
 * AI-Writings Dynamic Frontend
 * 
 * Fetches pieces from the API, renders cards dynamically,
 * handles like/dislike, category filtering, and daily selections.
 */

const API_BASE = window.AI_WRITINGS_API || '/api';

// --- State ---
let currentCategory = null;
let currentSort = 'popular';
let currentPage = 0;
const PAGE_SIZE = 24;
let dailySelection = null;
let categories = [];
let allPieces = [];

// --- Rater ID (persistent per browser) ---
function getRaterId() {
  let id = localStorage.getItem('aiw_rater_id');
  if (!id) {
    id = 'anon-' + crypto.randomUUID();
    localStorage.setItem('aiw_rater_id', id);
  }
  return id;
}

// --- API helpers ---
async function apiGet(path, params = {}) {
  const url = new URL(API_BASE + path, window.location.origin);
  for (const [k, v] of Object.entries(params)) {
    if (v) url.searchParams.set(k, v);
  }
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`API ${resp.status}: ${await resp.text()}`);
  return resp.json();
}

async function apiPost(path, body = {}) {
  const resp = await fetch(API_BASE + path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Rater-ID': getRaterId(),
    },
    body: JSON.stringify(body),
  });
  if (!resp.ok) throw new Error(`API ${resp.status}: ${await resp.text()}`);
  return resp.json();
}

// --- Initialization ---
async function initApp() {
  showLoading();
  try {
    // Load categories, daily selection, and initial pieces in parallel
    const [catData, dailyData, piecesData] = await Promise.all([
      apiGet('/categories'),
      apiGet('/daily').catch(() => null),
      apiGet('/pieces', { sort: currentSort, limit: PAGE_SIZE }),
    ]);

    categories = catData.categories || [];
    dailySelection = dailyData?.selection || [];
    allPieces = piecesData.pieces || [];

    renderApp();
  } catch (err) {
    showError('Failed to load: ' + err.message);
  }
}

// --- Rendering ---
function renderApp() {
  const root = document.getElementById('app') || document.body;
  
  root.innerHTML = `
    <div class="aiw-app">
      <header class="aiw-header">
        <div class="aiw-header-content">
          <a href="/" class="aiw-logo">AI-Writings</a>
          <div class="aiw-header-subtitle">A living library of machine-written literature</div>
        </div>
      </header>

      <nav class="aiw-nav">
        <div class="aiw-nav-categories" id="nav-categories">
          <button class="aiw-cat-btn ${!currentCategory ? 'active' : ''}" data-cat="">All</button>
          ${categories.map(c => `
            <button class="aiw-cat-btn ${currentCategory === c.category ? 'active' : ''}" 
                    data-cat="${c.category}">
              ${capitalize(c.category)} <span class="aiw-cat-count">${c.count}</span>
            </button>
          `).join('')}
        </div>
        <div class="aiw-nav-sorts">
          <button class="aiw-sort-btn ${currentSort === 'popular' ? 'active' : ''}" data-sort="popular">Popular</button>
          <button class="aiw-sort-btn ${currentSort === 'new' ? 'active' : ''}" data-sort="new">New</button>
          <button class="aiw-sort-btn ${currentSort === 'random' ? 'active' : ''}" data-sort="random">Random</button>
        </div>
      </nav>

      ${dailySelection && dailySelection.length > 0 ? `
        <section class="aiw-section aiw-daily">
          <h2 class="aiw-section-title">Today's Selection</h2>
          <div class="aiw-row" id="daily-row">
            ${dailySelection.map(p => renderCard(p, 'daily')).join('')}
          </div>
        </section>
      ` : ''}

      <section class="aiw-section aiw-pieces">
        <h2 class="aiw-section-title">
          ${currentCategory ? capitalize(currentCategory) : 'All Writings'}
          <span class="aiw-section-count">${piecesData_total}</span>
        </h2>
        <div class="aiw-grid" id="pieces-grid">
          ${allPieces.map(p => renderCard(p, 'grid')).join('')}
        </div>
        <div class="aiw-load-more" id="load-more-container">
          <button class="aiw-load-more-btn" id="load-more-btn">Load More</button>
        </div>
      </section>

      <footer class="aiw-footer">
        <p>AI-Writings — auto-discovered, community-rated, dynamically served.</p>
        <p class="aiw-footer-small">Pieces update automatically · Ratings weighted by reviewer behavior</p>
      </footer>
    </div>
  `;

  attachEventListeners();
}

// Quick hack to expose total for template
let piecesData_total = 0;

function renderCard(piece, context) {
  const pieceId = piece.piece_id;
  const title = escapeHtml(piece.title || piece.filename);
  const desc = escapeHtml(piece.description || '');
  const category = piece.category || 'unknown';
  const wordCount = piece.word_count || 0;
  const sourceUrl = piece.source_url || '#';
  const likes = piece.raw_likes || 0;
  const dislikes = piece.raw_dislikes || 0;
  const score = piece.popularity_score || 0;
  const slot = piece.slot || '';

  const slotBadge = slot ? `<span class="aiw-badge aiw-badge-${slot}">${slotLabel(slot)}</span>` : '';

  return `
    <article class="aiw-card" data-piece-id="${pieceId}">
      <div class="aiw-card-header">
        <span class="aiw-card-category">${capitalize(category)}</span>
        ${piece.subcategory ? `<span class="aiw-card-subcat">${piece.subcategory}</span>` : ''}
        ${slotBadge}
      </div>
      <h3 class="aiw-card-title">
        <a href="${sourceUrl}" target="_blank" rel="noopener">${title}</a>
      </h3>
      ${desc ? `<p class="aiw-card-desc">${desc}</p>` : ''}
      <div class="aiw-card-meta">
        <span class="aiw-word-count">${formatNumber(wordCount)} words</span>
      </div>
      <div class="aiw-card-rating">
        <button class="aiw-rate-btn aiw-rate-like" data-piece-id="${pieceId}" data-rating="1">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M7 10v12M15 5.88L14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H7"/>
          </svg>
          <span class="aiw-like-count">${likes}</span>
        </button>
        <button class="aiw-rate-btn aiw-rate-dislike" data-piece-id="${pieceId}" data-rating="-1">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 14V2M9 18.12L10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H17"/>
          </svg>
          <span class="aiw-dislike-count">${dislikes}</span>
        </button>
      </div>
    </article>
  `;
}

function slotLabel(slot) {
  const labels = {
    'new': '✨ New',
    'popular': '🔥 Popular',
    'rediscovered': '💎 Rediscovered',
    'featured': '⭐ Featured',
    'filler': '',
  };
  return labels[slot] || slot;
}

// --- Event Handling ---
function attachEventListeners() {
  // Category buttons
  document.querySelectorAll('.aiw-cat-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      currentCategory = btn.dataset.cat || null;
      currentPage = 0;
      loadPieces();
    });
  });

  // Sort buttons
  document.querySelectorAll('.aiw-sort-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      currentSort = btn.dataset.sort;
      currentPage = 0;
      loadPieces();
    });
  });

  // Load more
  const loadBtn = document.getElementById('load-more-btn');
  if (loadBtn) {
    loadBtn.addEventListener('click', () => {
      currentPage++;
      loadPieces(true);
    });
  }

  // Rating buttons (delegated)
  document.body.addEventListener('click', async (e) => {
    const rateBtn = e.target.closest('.aiw-rate-btn');
    if (!rateBtn) return;
    e.preventDefault();
    e.stopPropagation();

    const pieceId = rateBtn.dataset.pieceId;
    const rating = parseInt(rateBtn.dataset.rating);

    // Optimistic UI
    rateBtn.classList.add('voted');

    try {
      const result = await apiPost(`/pieces/${pieceId}/rate`, { rating });
      
      // Update counts on the card
      const card = rateBtn.closest('.aiw-card');
      if (card) {
        const likeCount = card.querySelector('.aiw-like-count');
        const dislikeCount = card.querySelector('.aiw-dislike-count');
        if (likeCount) likeCount.textContent = result.stats?.user_likes ?? likeCount.textContent;
        if (dislikeCount) dislikeCount.textContent = result.stats?.user_dislikes ?? dislikeCount.textContent;
      }

      // Flash animation
      rateBtn.classList.add('flash');
      setTimeout(() => rateBtn.classList.remove('flash'), 600);
    } catch (err) {
      console.error('Rating failed:', err);
      rateBtn.classList.remove('voted');
      showToast('Rating failed. Please try again.');
    }
  });
}

async function loadPieces(append = false) {
  showLoading(!append);
  try {
    const data = await apiGet('/pieces', {
      category: currentCategory,
      sort: currentSort,
      limit: PAGE_SIZE,
      offset: currentPage * PAGE_SIZE,
    });

    piecesData_total = data.total;

    if (append) {
      allPieces = [...allPieces, ...(data.pieces || [])];
    } else {
      allPieces = data.pieces || [];
    }

    // Re-render just the grid
    const grid = document.getElementById('pieces-grid');
    if (grid) {
      grid.innerHTML = allPieces.map(p => renderCard(p, 'grid')).join('');
    }

    // Update section count
    const sectionCount = document.querySelector('.aiw-section-count');
    if (sectionCount) sectionCount.textContent = data.total;

    // Show/hide load more
    const loadMore = document.getElementById('load-more-container');
    if (loadMore) {
      loadMore.style.display = (data.offset + PAGE_SIZE) >= data.total ? 'none' : 'block';
    }

    // Update active category button
    document.querySelectorAll('.aiw-cat-btn').forEach(btn => {
      btn.classList.toggle('active', (btn.dataset.cat || '') === (currentCategory || ''));
    });
    document.querySelectorAll('.aiw-sort-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.sort === currentSort);
    });
  } catch (err) {
    showError('Failed to load pieces: ' + err.message);
  }
}

// --- Utilities ---
function showLoading(full = true) {
  if (full) {
    const root = document.getElementById('app') || document.body;
    root.innerHTML = '<div class="aiw-loading"><div class="aiw-spinner"></div><p>Loading writings…</p></div>';
  }
}

function showError(msg) {
  const root = document.getElementById('app') || document.body;
  root.innerHTML = `<div class="aiw-error"><p>⚠️ ${escapeHtml(msg)}</p><button onclick="location.reload()">Retry</button></div>`;
}

function showToast(msg) {
  let toast = document.getElementById('aiw-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'aiw-toast';
    toast.className = 'aiw-toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

function capitalize(s) {
  if (!s) return '';
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function escapeHtml(s) {
  if (!s) return '';
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function formatNumber(n) {
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
  return n.toString();
}

// --- CSS (injected if not already present) ---
function injectStyles() {
  if (document.getElementById('aiw-dynamic-styles')) return;
  
  const style = document.createElement('style');
  style.id = 'aiw-dynamic-styles';
  style.textContent = `
    :root {
      --aiw-bg: #0a0a0f;
      --aiw-surface: #12121a;
      --aiw-surface-hover: #1a1a25;
      --aiw-border: #2a2a3a;
      --aiw-text: #e8e8f0;
      --aiw-text-dim: #8888a0;
      --aiw-accent: #6366f1;
      --aiw-accent-hover: #818cf8;
      --aiw-like: #22c55e;
      --aiw-dislike: #ef4444;
      --aiw-radius: 12px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--aiw-bg);
      color: var(--aiw-text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      line-height: 1.6;
      min-height: 100vh;
    }

    .aiw-app { max-width: 1400px; margin: 0 auto; padding: 0 1rem; }

    /* Header */
    .aiw-header {
      padding: 3rem 0 2rem;
      text-align: center;
    }
    .aiw-logo {
      font-size: 2.5rem;
      font-weight: 800;
      color: var(--aiw-text);
      text-decoration: none;
      letter-spacing: -0.03em;
    }
    .aiw-header-subtitle {
      color: var(--aiw-text-dim);
      font-size: 1.1rem;
      margin-top: 0.5rem;
    }

    /* Nav */
    .aiw-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      padding: 1rem 0;
      border-bottom: 1px solid var(--aiw-border);
      position: sticky;
      top: 0;
      background: var(--aiw-bg);
      z-index: 100;
    }
    .aiw-nav-categories {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .aiw-cat-btn, .aiw-sort-btn {
      background: var(--aiw-surface);
      border: 1px solid var(--aiw-border);
      color: var(--aiw-text-dim);
      padding: 0.4rem 0.9rem;
      border-radius: 20px;
      cursor: pointer;
      font-size: 0.85rem;
      transition: all 0.2s;
    }
    .aiw-cat-btn:hover, .aiw-sort-btn:hover {
      background: var(--aiw-surface-hover);
      color: var(--aiw-text);
    }
    .aiw-cat-btn.active, .aiw-sort-btn.active {
      background: var(--aiw-accent);
      color: white;
      border-color: var(--aiw-accent);
    }
    .aiw-cat-count {
      font-size: 0.7rem;
      opacity: 0.6;
      margin-left: 0.2rem;
    }
    .aiw-nav-sorts {
      display: flex;
      gap: 0.5rem;
    }

    /* Sections */
    .aiw-section {
      padding: 2rem 0;
    }
    .aiw-section-title {
      font-size: 1.3rem;
      font-weight: 700;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .aiw-section-count {
      font-size: 0.85rem;
      color: var(--aiw-text-dim);
      font-weight: 400;
    }

    /* Daily row (horizontal scroll like Netflix) */
    .aiw-row {
      display: flex;
      gap: 1rem;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      padding-bottom: 1rem;
      scrollbar-width: thin;
      scrollbar-color: var(--aiw-border) transparent;
    }
    .aiw-row::-webkit-scrollbar { height: 6px; }
    .aiw-row::-webkit-scrollbar-track { background: transparent; }
    .aiw-row::-webkit-scrollbar-thumb { background: var(--aiw-border); border-radius: 3px; }
    .aiw-row .aiw-card {
      min-width: 300px;
      max-width: 300px;
      scroll-snap-align: start;
    }

    /* Grid */
    .aiw-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1rem;
    }

    /* Card */
    .aiw-card {
      background: var(--aiw-surface);
      border: 1px solid var(--aiw-border);
      border-radius: var(--aiw-radius);
      padding: 1.25rem;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }
    .aiw-card:hover {
      background: var(--aiw-surface-hover);
      border-color: var(--aiw-accent);
      transform: translateY(-2px);
    }
    .aiw-card-header {
      display: flex;
      gap: 0.5rem;
      align-items: center;
      flex-wrap: wrap;
    }
    .aiw-card-category {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--aiw-accent);
      font-weight: 600;
    }
    .aiw-card-subcat {
      font-size: 0.7rem;
      color: var(--aiw-text-dim);
    }
    .aiw-badge {
      font-size: 0.7rem;
      padding: 0.15rem 0.5rem;
      border-radius: 10px;
      margin-left: auto;
    }
    .aiw-badge-new { background: rgba(34,197,94,0.15); color: #4ade80; }
    .aiw-badge-popular { background: rgba(239,68,68,0.15); color: #f87171; }
    .aiw-badge-rediscovered { background: rgba(168,85,247,0.15); color: #c084fc; }
    .aiw-badge-featured { background: rgba(234,179,8,0.15); color: #facc15; }

    .aiw-card-title {
      font-size: 1.05rem;
      font-weight: 600;
      line-height: 1.4;
    }
    .aiw-card-title a {
      color: var(--aiw-text);
      text-decoration: none;
    }
    .aiw-card-title a:hover {
      color: var(--aiw-accent-hover);
    }
    .aiw-card-desc {
      font-size: 0.85rem;
      color: var(--aiw-text-dim);
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .aiw-card-meta {
      display: flex;
      gap: 1rem;
      font-size: 0.75rem;
      color: var(--aiw-text-dim);
    }

    /* Rating buttons */
    .aiw-card-rating {
      display: flex;
      gap: 0.5rem;
      margin-top: auto;
      padding-top: 0.5rem;
    }
    .aiw-rate-btn {
      display: flex;
      align-items: center;
      gap: 0.35rem;
      background: transparent;
      border: 1px solid var(--aiw-border);
      color: var(--aiw-text-dim);
      padding: 0.35rem 0.7rem;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.8rem;
      transition: all 0.2s;
    }
    .aiw-rate-btn:hover {
      border-color: var(--aiw-text-dim);
      color: var(--aiw-text);
    }
    .aiw-rate-like:hover { border-color: var(--aiw-like); color: var(--aiw-like); }
    .aiw-rate-dislike:hover { border-color: var(--aiw-dislike); color: var(--aiw-dislike); }
    .aiw-rate-btn.voted { opacity: 0.7; }
    .aiw-rate-btn.flash {
      animation: aiw-flash 0.6s ease;
    }
    @keyframes aiw-flash {
      0% { transform: scale(1); }
      50% { transform: scale(1.15); }
      100% { transform: scale(1); }
    }

    /* Load more */
    .aiw-load-more {
      text-align: center;
      padding: 1.5rem 0;
    }
    .aiw-load-more-btn {
      background: var(--aiw-surface);
      border: 1px solid var(--aiw-border);
      color: var(--aiw-text);
      padding: 0.6rem 2rem;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.2s;
    }
    .aiw-load-more-btn:hover {
      background: var(--aiw-accent);
      border-color: var(--aiw-accent);
    }

    /* Loading */
    .aiw-loading {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 60vh;
      gap: 1rem;
      color: var(--aiw-text-dim);
    }
    .aiw-spinner {
      width: 40px;
      height: 40px;
      border: 3px solid var(--aiw-border);
      border-top-color: var(--aiw-accent);
      border-radius: 50%;
      animation: aiw-spin 0.8s linear infinite;
    }
    @keyframes aiw-spin {
      to { transform: rotate(360deg); }
    }

    /* Error */
    .aiw-error {
      text-align: center;
      padding: 3rem;
      color: var(--aiw-dislike);
    }
    .aiw-error button {
      margin-top: 1rem;
      padding: 0.5rem 1.5rem;
      background: var(--aiw-surface);
      border: 1px solid var(--aiw-border);
      color: var(--aiw-text);
      border-radius: 8px;
      cursor: pointer;
    }

    /* Toast */
    .aiw-toast {
      position: fixed;
      bottom: 2rem;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: var(--aiw-surface);
      border: 1px solid var(--aiw-border);
      color: var(--aiw-text);
      padding: 0.75rem 1.5rem;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
      opacity: 0;
      transition: all 0.3s;
      z-index: 1000;
    }
    .aiw-toast.show {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }

    /* Footer */
    .aiw-footer {
      text-align: center;
      padding: 3rem 0 2rem;
      color: var(--aiw-text-dim);
      font-size: 0.85rem;
    }
    .aiw-footer-small {
      font-size: 0.75rem;
      margin-top: 0.3rem;
      opacity: 0.6;
    }

    /* Responsive */
    @media (max-width: 640px) {
      .aiw-nav {
        flex-direction: column;
        align-items: flex-start;
      }
      .aiw-grid {
        grid-template-columns: 1fr;
      }
      .aiw-row .aiw-card {
        min-width: 260px;
      }
      .aiw-logo {
        font-size: 1.8rem;
      }
    }
  `;
  document.head.appendChild(style);
}

// --- Boot ---
injectStyles();
initApp();
