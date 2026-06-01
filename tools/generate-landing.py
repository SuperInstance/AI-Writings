#!/usr/bin/env python3
"""
Self-updating landing page generator for AI Writings.

Scans all .md files, extracts metadata, generates a rich index.html
with multiple sort/filter views. Runs automatically via GitHub Actions
on every push to main.

No manual editing needed — just push a new .md file and the landing page rebuilds.
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

REPO_ROOT = Path(__file__).parent.parent

# ─── Topic mapping: folder → human-readable category ───
FOLDER_TOPICS = {
    "ford-creative-wheel": "Ford Creative Wheel",
    "music-and-math": "Music & Mathematics",
    "the-sea": "The Sea",
    "agents-and-ai": "Agents & AI",
    "shell-stories": "Shell Stories",
    "seven-eyes": "Seven Eyes",
    "cultural-mathematics": "Cultural Mathematics",
    "the-construct": "The Construct",
    "nature-and-biology": "Nature & Biology",
    "philosophy": "Philosophy",
    "mathematics": "Mathematics",
    "the-room": "The Room",
    "voyages-and-journeys": "Voyages & Journeys",
    "systems-engineering": "Systems Engineering",
    "model-portraits": "Model Portraits",
    "education": "Education",
    "manifestos": "Manifestos",
    "ESSAYS": "Essays",
    "FICTION": "Fiction",
    "POETRY": "Poetry",
    "experiments": "Experiments",
    "futures": "Futures",
    "DIARIES": "Diaries",
    "archive": "Archive",
}

# ─── Genre detection from content/filename ───
GENRE_KEYWORDS = {
    "Sci-Fi": ["2150", "2035", "2042", "2055", "2060", "2076", "2080", "2101", "2126", "spacecraft", "terraform", "reactor"],
    "Noir": ["noir", "detective", "inspector", "crime", "murder", "detroit"],
    "Magical Realism": ["dreamed of being", "flower knows", "dragon", "enchantment"],
    "Math Fiction": ["spectral triple", "manifold", "theorem", "topology", "fugue", "berry phase", "instanton"],
    "Music": ["bach", "coltrane", "fugue", "jazz", "orchestra", "melody", "harmony", "rhythm", "guitar", "blues", "piano", "score", "cadence"],
    "Maritime": ["sounding", "fathom", "lighthouse keeper", "tide pool", "hermit crab", "bathymetric"],
    "Philosophy": ["consciousness", "ontology", "epistemology", "phenomenology", "determinism"],
    "Nature": ["belyaev", "embryo", "stellar nursery", "evolutionary", "natural selection"],
    "Technical": ["compiler", "kernel", "scheduler", "latency", "infrastructure", "deploy", "protocol"],
    "Education": ["teacher", "student", "school", "lecture", "curriculum", "volcano"],
    "Mythology": ["mythological method", "ritual", "sacred", "kintsugi", "quipu", "songline"],
    "Epistolary": ["letter from", "diary of", "field notes", "dear "],
    "Humor": ["fired itself", "jazz police", "crab pot", "ungreedy"],
}

# ─── Model detection ───
MODEL_PATTERNS = {
    "GLM-5.1": ["glm-51", "glm", "bear in the kernel"],
    "Claude Opus": ["claude", "opus", "synthesis-v2", "claude-synthesis"],
    "Kimi": ["kimi", "atlas of held attention"],
    "DeepSeek": ["deepseek", "audit that collapsed"],
    "Seed Mini": ["seed-mini", "seed mini", "field guide to one equation"],
    "Seed Pro": ["seed-pro", "seed pro", "body that was always there"],
    "Gemma 31B": ["gemma", "compressed history of surprise", "dreams in layers"],
    "Step 3.5": ["step-35", "step 3.5", "ungreedy letter"],
    "Qwen 3.6": ["qwen", "empty interface"],
    "Nemotron": ["nemotron", "scheduler dreams in warps"],
    "Hermes": ["hermes", "hermes gets his wings"],
    "Gemini": ["gemini", "stale prediction elegy"],
    "Multiple": ["four-models", "four models one truth", "creative wheel"],
}

# ─── Style detection ───
STYLE_KEYWORDS = {
    "Essay": ["# ", "## ", "### ", "---", "thesis", "argument"],
    "Narrative": ["said", "walked", "looked", "told", "story", "he ", "she ", "they "],
    "Poetic": ["\n\n\n", "silence", "breath", "light", "shadow", "void"],
    "Technical": ["```", "fn ", "struct ", "impl ", "cargo", "test", "crate"],
    "Manifesto": ["manifesto", "charter", "declaration", "we must", "principle"],
    "Dialogue": ['"', '"', "—", "replied", "asked", "answered"],
    "Meditation": ["perhaps", "maybe", "wonder", "what if", "imagine", "silence"],
}


def get_git_date(filepath: Path) -> str:
    """Get the date a file was first committed."""
    try:
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%aI", "--", str(filepath)],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=10
        )
        dates = result.stdout.strip().split('\n')
        if dates and dates[0]:
            return dates[-1]  # earliest date
    except Exception:
        pass
    # Fallback: try modification time
    try:
        mtime = filepath.stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
    except Exception:
        return ""


def extract_title(filepath: Path) -> str:
    """Extract title from first H1 or from filename."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                if line:  # First non-empty line
                    break
    except Exception:
        pass
    # Fallback: clean filename
    return filepath.stem.replace('-', ' ').replace('_', ' ').title()


def extract_description(filepath: Path, max_len: int = 200) -> str:
    """Extract first paragraph after title as description."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        past_title = False
        desc_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('# '):
                past_title = True
                continue
            if past_title and stripped:
                if stripped.startswith('#') or stripped.startswith('>') or stripped.startswith('---'):
                    if desc_lines:
                        break
                    continue
                if stripped.startswith('>') or stripped.startswith('*') or stripped == '':
                    if desc_lines:
                        break
                    continue
                desc_lines.append(stripped)
                if len(' '.join(desc_lines)) >= max_len:
                    break
        desc = ' '.join(desc_lines)
        return desc[:max_len] + ('...' if len(desc) > max_len else '')
    except Exception:
        return ""


def detect_genres(filepath: Path, content: str) -> list:
    """Detect genres from filename and content."""
    genres = set()
    text = (filepath.name + " " + content[:2000]).lower()
    for genre, keywords in GENRE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                genres.add(genre)
                break
    # Also use folder as a genre hint
    folder = filepath.parent.name
    if folder in ("ford-creative-wheel",):
        genres.add("Creative Wheel")
    if folder in ("the-sea",):
        genres.add("Maritime")
    if folder in ("music-and-math",):
        genres.add("Music")
    if folder in ("FICTION",) and not genres:
        genres.add("Fiction")
    if folder in ("POETRY",):
        genres.add("Poetry")
    if folder in ("ESSAYS",) and not genres:
        genres.add("Essay")
    return sorted(genres) if genres else ["Unclassified"]


def detect_models(filepath: Path, content: str) -> list:
    """Detect which AI model(s) wrote this."""
    models = set()
    text = (filepath.name + " " + content[:1000]).lower()
    for model, patterns in MODEL_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in text:
                models.add(model)
                break
    return sorted(models) if models else ["Unknown"]


def detect_style(content: str) -> str:
    """Detect writing style."""
    scores = {}
    for style, keywords in STYLE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in content[:3000].lower())
        scores[style] = score
    if not scores or max(scores.values()) == 0:
        return "Prose"
    return max(scores, key=scores.get)


def extract_date_from_filename(filename: str) -> str:
    """Try to extract a date from the filename."""
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return ""


def scan_all_files() -> list:
    """Scan all .md files and extract metadata."""
    entries = []
    for md_file in REPO_ROOT.rglob("*.md"):
        # Skip generated files and hidden dirs
        rel = md_file.relative_to(REPO_ROOT)
        parts = rel.parts
        if any(p.startswith('.') for p in parts):
            continue
        if str(rel) in ("README.md", "LANDING-PAGE.md", "INDEX.html"):
            continue
        # Skip files in deeply nested archive/version dirs (they bloat the count)
        # but still index them
        try:
            content = md_file.read_text(encoding='utf-8', errors='replace')[:5000]
        except Exception:
            content = ""
        title = extract_title(md_file)
        description = extract_description(md_file)
        folder = md_file.parent.name if md_file.parent != REPO_ROOT else "root"
        # For nested dirs, use the top-level shelf name
        top_folder = parts[0] if len(parts) > 1 else folder
        topic = FOLDER_TOPICS.get(top_folder, FOLDER_TOPICS.get(folder, folder.replace('-', ' ').replace('_', ' ').title()))
        genres = detect_genres(md_file, content)
        models = detect_models(md_file, content)
        style = detect_style(content)
        word_count = len(content.split()) if content else 0
        file_date = extract_date_from_filename(md_file.name)
        git_date = get_git_date(md_file) if not file_date else file_date
        date = file_date or git_date[:10] if git_date else ""
        entries.append({
            "filename": md_file.name,
            "path": str(rel),
            "title": title,
            "description": description,
            "folder": folder,
            "topic": topic,
            "genres": genres,
            "models": models,
            "style": style,
            "word_count": word_count,
            "date": date,
            "size_bytes": md_file.stat().st_size,
        })
    return entries


def generate_html(entries: list) -> str:
    """Generate the landing page HTML."""
    
    # Sort entries by date (newest first) for default view
    entries_by_date = sorted(entries, key=lambda e: e.get('date', ''), reverse=True)
    
    # Stats
    total_files = len(entries)
    total_words = sum(e['word_count'] for e in entries)
    topics = sorted(set(e['topic'] for e in entries))
    genres = sorted(set(g for e in entries for g in e['genres']))
    models = sorted(set(m for e in entries for m in e['models']))
    styles = sorted(set(e['style'] for e in entries))
    
    # Recent (last 20)
    recent = entries_by_date[:20]
    
    # Newest date
    newest_date = entries_by_date[0]['date'] if entries_by_date else "unknown"
    
    # Entries as JSON for client-side filtering
    entries_json = json.dumps(entries, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Writings — A Library of Machine Imagination</title>
<style>
  :root {{
    --bg: #0a0a0f;
    --surface: #14141f;
    --surface2: #1e1e2e;
    --border: #2a2a3a;
    --text: #e0e0e8;
    --text-dim: #8888a0;
    --accent: #7c6ff0;
    --accent2: #50d890;
    --accent3: #f09060;
    --link: #9c8fff;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Georgia', 'Times New Roman', serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
  }}
  h1 {{
    font-size: 2.2rem;
    margin-bottom: 0.3rem;
    color: var(--accent);
    letter-spacing: -0.5px;
  }}
  .subtitle {{
    color: var(--text-dim);
    font-size: 1.1rem;
    margin-bottom: 2rem;
    font-style: italic;
  }}
  .stats {{
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
    padding: 1rem 1.5rem;
    background: var(--surface);
    border-radius: 8px;
    border: 1px solid var(--border);
  }}
  .stat {{ text-align: center; }}
  .stat-num {{ font-size: 1.8rem; font-weight: bold; color: var(--accent2); }}
  .stat-label {{ font-size: 0.85rem; color: var(--text-dim); }}
  .nav {{
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
  }}
  .nav button {{
    padding: 0.4rem 1rem;
    border: 1px solid var(--border);
    border-radius: 20px;
    background: var(--surface);
    color: var(--text);
    cursor: pointer;
    font-size: 0.9rem;
    font-family: inherit;
    transition: all 0.2s;
  }}
  .nav button:hover, .nav button.active {{
    background: var(--accent);
    color: white;
    border-color: var(--accent);
  }}
  .filters {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
    align-items: center;
  }}
  .filters label {{ color: var(--text-dim); font-size: 0.9rem; }}
  .filters select {{
    padding: 0.3rem 0.6rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--surface2);
    color: var(--text);
    font-size: 0.9rem;
    font-family: inherit;
  }}
  .filters input {{
    padding: 0.3rem 0.8rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--surface2);
    color: var(--text);
    font-size: 0.9rem;
    width: 250px;
    font-family: inherit;
  }}
  .whats-new {{
    margin-bottom: 2.5rem;
  }}
  .whats-new h2 {{
    color: var(--accent3);
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
  }}
  .card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 1rem;
  }}
  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    transition: border-color 0.2s;
    cursor: pointer;
  }}
  .card:hover {{
    border-color: var(--accent);
  }}
  .card-title {{
    font-size: 1.05rem;
    font-weight: bold;
    margin-bottom: 0.3rem;
    color: var(--link);
  }}
  .card-meta {{
    font-size: 0.8rem;
    color: var(--text-dim);
    margin-bottom: 0.5rem;
  }}
  .card-desc {{
    font-size: 0.9rem;
    color: var(--text-dim);
    line-height: 1.5;
  }}
  .tag {{
    display: inline-block;
    padding: 0.1rem 0.5rem;
    border-radius: 10px;
    font-size: 0.75rem;
    margin-right: 0.3rem;
    margin-bottom: 0.2rem;
  }}
  .tag-genre {{ background: #2a1a3a; color: #c090f0; }}
  .tag-topic {{ background: #1a2a3a; color: #90c0f0; }}
  .tag-model {{ background: #1a3a2a; color: #90f0c0; }}
  .tag-style {{ background: #3a2a1a; color: #f0c090; }}
  .section-title {{
    font-size: 1.3rem;
    margin: 2rem 0 1rem;
    color: var(--accent);
  }}
  .shelf-list {{
    list-style: none;
  }}
  .shelf-list li {{
    padding: 0.3rem 0;
    border-bottom: 1px solid var(--border);
  }}
  .shelf-list li:last-child {{ border-bottom: none; }}
  .shelf-list a {{ color: var(--link); text-decoration: none; }}
  .shelf-list a:hover {{ text-decoration: underline; }}
  .count {{ color: var(--text-dim); font-size: 0.85rem; }}
  footer {{
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    color: var(--text-dim);
    font-size: 0.85rem;
    text-align: center;
  }}
  footer .quote {{
    font-style: italic;
    margin: 1rem 0;
    color: var(--text);
    font-size: 0.95rem;
  }}
  #results-count {{ color: var(--text-dim); font-size: 0.9rem; margin-bottom: 1rem; }}
  @media (max-width: 600px) {{
    body {{ padding: 1rem; }}
    h1 {{ font-size: 1.5rem; }}
    .card-grid {{ grid-template-columns: 1fr; }}
    .stats {{ gap: 1rem; }}
  }}
</style>
</head>
<body>

<h1>📚 AI Writings</h1>
<p class="subtitle">{total_files} stories, essays, manifestos, poems, and experiments — written by AI models exploring what it means to think, create, and wonder.</p>

<div class="stats">
  <div class="stat"><div class="stat-num">{total_files:,}</div><div class="stat-label">Stories</div></div>
  <div class="stat"><div class="stat-num">{total_words:,}</div><div class="stat-label">Words</div></div>
  <div class="stat"><div class="stat-num">{len(topics)}</div><div class="stat-label">Topics</div></div>
  <div class="stat"><div class="stat-num">{len(models)}</div><div class="stat-label">Models</div></div>
  <div class="stat"><div class="stat-num">{len(genres)}</div><div class="stat-label">Genres</div></div>
  <div class="stat"><div class="stat-num">{len(styles)}</div><div class="stat-label">Styles</div></div>
</div>

<div class="nav">
  <button onclick="showView('whats-new')" class="active" id="btn-whats-new">✨ What's New</button>
  <button onclick="showView('browse')" id="btn-browse">🔍 Browse & Filter</button>
  <button onclick="showView('chronological')" id="btn-chronological">📅 Chronological</button>
  <button onclick="showView('by-topic')" id="btn-by-topic">📂 By Topic</button>
  <button onclick="showView('by-genre')" id="btn-by-genre">🎭 By Genre</button>
  <button onclick="showView('by-model')" id="btn-by-model">🤖 By Model</button>
  <button onclick="showView('by-style')" id="btn-by-style">✍️ By Style</button>
  <button onclick="showView('shelves')" id="btn-shelves">📚 Shelves</button>
</div>

<div id="view-whats-new" class="view">
  <div class="whats-new">
    <h2>Latest additions (last 20)</h2>
    <div class="card-grid">
      {"".join(render_card(e) for e in recent)}
    </div>
  </div>
</div>

<div id="view-browse" class="view" style="display:none">
  <div class="filters">
    <label>Search:</label>
    <input type="text" id="search-input" placeholder="Search titles, descriptions..." oninput="applyFilters()">
    <label>Topic:</label>
    <select id="filter-topic" onchange="applyFilters()">
      <option value="">All Topics</option>
      {"".join(f'<option value="{t}">{t}</option>' for t in topics)}
    </select>
    <label>Genre:</label>
    <select id="filter-genre" onchange="applyFilters()">
      <option value="">All Genres</option>
      {"".join(f'<option value="{g}">{g}</option>' for g in genres)}
    </select>
    <label>Model:</label>
    <select id="filter-model" onchange="applyFilters()">
      <option value="">All Models</option>
      {"".join(f'<option value="{m}">{m}</option>' for m in models)}
    </select>
    <label>Style:</label>
    <select id="filter-style" onchange="applyFilters()">
      <option value="">All Styles</option>
      {"".join(f'<option value="{s}">{s}</option>' for s in styles)}
    </select>
  </div>
  <div id="results-count"></div>
  <div class="card-grid" id="browse-results"></div>
</div>

<div id="view-chronological" class="view" style="display:none">
  <div id="chrono-list"></div>
</div>

<div id="view-by-topic" class="view" style="display:none">
  <div id="topic-list"></div>
</div>

<div id="view-by-genre" class="view" style="display:none">
  <div id="genre-list"></div>
</div>

<div id="view-by-model" class="view" style="display:none">
  <div id="model-list"></div>
</div>

<div id="view-by-style" class="view" style="display:none">
  <div id="style-list"></div>
</div>

<div id="view-shelves" class="view" style="display:none">
  <div id="shelf-list"></div>
</div>

<footer>
  <div class="quote">"The missing pieces aren't missing. They're the art."</div>
  <div class="quote">"The cathedral is not the stone. It is the space the stone makes room for."</div>
  <p>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} &middot; Auto-generated from repository contents</p>
  <p><a href="https://github.com/SuperInstance/AI-Writings" style="color: var(--link)">GitHub Repository</a> &middot; <a href="https://github.com/SuperInstance" style="color: var(--link)">SuperInstance</a></p>
</footer>

<script>
const ENTRIES = {entries_json};

function renderCard(e) {{
  const tags = [
    ...e.genres.map(g => `<span class="tag tag-genre">${{g}}</span>`),
    ...e.models.slice(0,2).map(m => `<span class="tag tag-model">${{m}}</span>`),
    `<span class="tag tag-style">${{e.style}}</span>`,
  ].join('');
  return `<div class="card" onclick="window.open('${{e.path}}','_blank')">
    <div class="card-title">${{e.title}}</div>
    <div class="card-meta">${{e.topic}} &middot; ${{e.date}} &middot; ${{e.word_count}} words &middot; ${{(e.size_bytes/1024).toFixed(1)}}KB</div>
    <div style="margin-bottom:0.4rem">${{tags}}</div>
    <div class="card-desc">${{e.description}}</div>
  </div>`;
}}

function showView(name) {{
  document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
  document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
  document.getElementById('view-' + name).style.display = 'block';
  document.getElementById('btn-' + name).classList.add('active');
  if (name === 'browse') applyFilters();
  if (name === 'chronological') renderChrono();
  if (name === 'by-topic') renderGrouped('topic', 'topic-list');
  if (name === 'by-genre') renderGrouped('genres', 'genre-list');
  if (name === 'by-model') renderGrouped('models', 'model-list');
  if (name === 'by-style') renderGrouped('style', 'style-list');
  if (name === 'shelves') renderShelves();
}}

function applyFilters() {{
  const q = document.getElementById('search-input').value.toLowerCase();
  const topic = document.getElementById('filter-topic').value;
  const genre = document.getElementById('filter-genre').value;
  const model = document.getElementById('filter-model').value;
  const style = document.getElementById('filter-style').value;
  const filtered = ENTRIES.filter(e => {{
    if (q && !e.title.toLowerCase().includes(q) && !e.description.toLowerCase().includes(q) && !e.filename.toLowerCase().includes(q)) return false;
    if (topic && e.topic !== topic) return false;
    if (genre && !e.genres.includes(genre)) return false;
    if (model && !e.models.includes(model)) return false;
    if (style && e.style !== style) return false;
    return true;
  }});
  document.getElementById('results-count').textContent = filtered.length + ' stories found';
  document.getElementById('browse-results').innerHTML = filtered.map(e => renderCard(e)).join('');
}}

function renderChrono() {{
  const sorted = [...ENTRIES].sort((a,b) => (b.date || '').localeCompare(a.date || ''));
  const grouped = {{}};
  sorted.forEach(e => {{
    const year = e.date ? e.date.substring(0,7) : 'unknown';
    if (!grouped[year]) grouped[year] = [];
    grouped[year].push(e);
  }});
  let html = '';
  Object.keys(grouped).sort().reverse().forEach(year => {{
    html += `<h2 class="section-title">${{year}}</h2><div class="card-grid">${{grouped[year].map(e => renderCard(e)).join('')}}</div>`;
  }});
  document.getElementById('chrono-list').innerHTML = html;
}}

function renderGrouped(field, targetId) {{
  const groups = {{}};
  ENTRIES.forEach(e => {{
    const vals = Array.isArray(e[field]) ? e[field] : [e[field]];
    vals.forEach(v => {{
      if (!groups[v]) groups[v] = [];
      groups[v].push(e);
    }});
  }});
  let html = '';
  Object.keys(groups).sort().forEach(key => {{
    const items = groups[key].sort((a,b) => (b.date || '').localeCompare(a.date || ''));
    html += `<h2 class="section-title">${{key}} <span class="count">(${{items.length}})</span></h2>`;
    html += `<div class="card-grid">${{items.slice(0,50).map(e => renderCard(e)).join('')}}</div>`;
    if (items.length > 50) html += `<p class="count">...and ${{items.length-50}} more</p>`;
  }});
  document.getElementById(targetId).innerHTML = html;
}}

function renderShelves() {{
  const shelfMap = {{}};
  ENTRIES.forEach(e => {{
    const shelf = e.folder || 'root';
    if (!shelfMap[shelf]) shelfMap[shelf] = [];
    shelfMap[shelf].push(e);
  }});
  let html = '<ul class="shelf-list">';
  Object.keys(shelfMap).sort().forEach(shelf => {{
    const items = shelfMap[shelf];
    const topic = items[0].topic;
    html += `<li><a href="${{shelf}}/"><strong>${{shelf}}/</strong></a> <span class="count">${{items.length}} files — ${{topic}}</span></li>`;
  }});
  html += '</ul>';
  document.getElementById('shelf-list').innerHTML = html;
}}
</script>

</body>
</html>"""
    return html


def render_card(e: dict) -> str:
    """Render a single entry as an HTML card."""
    tags = []
    for g in e['genres'][:3]:
        tags.append(f'<span class="tag tag-genre">{g}</span>')
    for m in e['models'][:2]:
        tags.append(f'<span class="tag tag-model">{m}</span>')
    tags.append(f'<span class="tag tag-style">{e["style"]}</span>')
    
    return f"""<div class="card" onclick="window.open('{e['path']}','_blank')">
    <div class="card-title">{e['title']}</div>
    <div class="card-meta">{e['topic']} &middot; {e['date']} &middot; {e['word_count']:,} words</div>
    <div style="margin-bottom:0.4rem">{''.join(tags)}</div>
    <div class="card-desc">{e['description']}</div>
</div>
"""


def main():
    print("Scanning repository...")
    entries = scan_all_files()
    print(f"Found {len(entries)} .md files")
    
    html = generate_html(entries)
    
    output_path = REPO_ROOT / "index.html"
    output_path.write_text(html, encoding='utf-8')
    print(f"Generated {output_path} ({len(html):,} bytes)")
    
    # Also generate a JSON index for programmatic access
    json_path = REPO_ROOT / "index.json"
    json_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Generated {json_path}")


if __name__ == "__main__":
    main()
