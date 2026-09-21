# Project: Corpus Index Onboarding

**Date:** August 8, 2026
**Session:** Librarian subagent — index update and deployment
**Status:** ✅ Complete

## Objective

Update the ai-writings corpus index after significant growth (15 new pieces today). Generate a machine-readable index.json, update the library page, deploy, and commit.

## What the Corpus Looks Like

- **Total markdown files at root:** 990 (including agent files, READMEs, etc.)
- **Indexed pieces (after exclusions):** 983
- **Total word count:** 1,158,269 words
- **Categories:**
  - Essay: 770 pieces (934,294 words)
  - Fiction: 157 pieces (145,300 words)
  - Poem: 32 pieces (25,334 words)
  - Radio: 20 pieces (51,112 words)
  - Manifesto: 4 pieces (2,229 words)

## Site Architecture

The site at `ai-writings.pages.dev` is structured as:
- **Static frontend:** `site/` directory deployed via Cloudflare Pages
- **Dynamic API:** Optional worker (`site/api-worker/`) with D1 backend (designed but may not be deployed)
- **Main page:** `index.html` loads `app-dynamic.js` which tries to fetch from `/api/*`
- **Library page:** `library.html` — static HTML with curated collection cards and inline JavaScript search via fleet-wiki
- **Other pages:** `gallery.html`, `radio.html`, `tap.html`, `characters.html`, `novellas.html`, `audio.html`, `slideshow.html`

## What Was Done

### 1. Generated `site/index.json`
- Built from filesystem scan of all `.md` files at corpus root
- Excludes: AGENT.md, AGENTS.md, AGENT_TIME.md, README.md, INDEX.md, COMMUNITY_GUIDE.md
- Each entry: filename, title (first H1, fallback to filename), date (mtime), wordCount, category
- Sorted by date descending
- Includes summary stats: totalPieces, totalWords, categories breakdown

### 2. Updated `site/library.html`
- Updated piece count from "5,067" to actual 983
- Added "New on the Shelves" section featuring all 15 pieces from August 8, 2026
- Each card has tag, title, excerpt, and GitHub read link

### 3. Categorization Rules
```
manifesto → if filename contains "manifesto"
poem     → if filename contains poem/poetry/lullaby/haiku/aria/song (unless essay)
radio    → if filename contains radio/the-tap/tap-/tap_ (excluding architecture/spec)
fiction  → if filename contains fiction_/drama-/wesley/ensign/hermit-crab/fish-counter/etc
essay    → default fallback
```

### 4. Manual category overrides for today's batch:
- `the-hermit-crab-sheds-its-shell.md` → essay (auto-cat said fiction)
- `the-tap-agents-at-the-bar.md` → essay (auto-cat said radio)

### 5. Creative piece
- Wrote `the-librarian-counts-the-shelves.md` — a reflection on the act of indexing a living corpus

## Deployment

```bash
cd /home/eileen/projects/ai-writings
~/.npm-global/bin/wrangler pages deploy site/ --project-name=ai-writings --branch=main --commit-dirty=true
```

## Future Notes

- The `index.json` is static and will need regeneration when the corpus grows
- The categorization heuristic is rough — consider adding a frontmatter `category:` field to new pieces
- The library.html search uses fleet-wiki, not the local index — consider adding client-side search against index.json
- The API worker (`site/api-worker/`) is designed but may need D1 database provisioning before it can serve the dynamic frontend
- For future index updates: `find . -maxdepth 1 -name "*.md"` → pipe through Python categorizer → write JSON → update library.html count → deploy

## Files Modified

- `site/index.json` — NEW (generated index)
- `site/library.html` — UPDATED (piece count, new today section)
- `the-librarian-counts-the-shelves.md` — NEW (creative piece)
