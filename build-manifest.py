#!/usr/bin/env python3
"""
build-manifest.py — Content Manifest Builder for the Fleet

Scans the ai-writings directory tree, extracts metadata from every
content file, detects relationships between pieces, and writes a
manifest.json that the template engine uses to render the site.

Usage:
    python3 build-manifest.py [--root DIR] [--output FILE] [--verbose]

Defaults:
    --root   = /home/eileen/projects/ai-writings
    --output = manifest.json (in root dir)

Drop a file. Run this. The site rebuilds.
"""

import os
import re
import json
import argparse
from datetime import datetime, date
from pathlib import Path
from collections import Counter, defaultdict

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Folder → content type mapping
FOLDER_TYPE_MAP = {
    "DIARIES": "journal",
    "speeches": "speech",
    "FICTION": "fiction",
    "POETRY": "poem",
    "ESSAYS": "essay",
    "philosophy": "philosophy",
    "RESEARCH": "research",
    "audio-experiments": "radio",
    "MODEL_PORTRAITS": "model-portrait",
    "FRAGMENTS": "fragment",
    "HERMES": "hermes",
    "LUCINEER": "lucineer",
    "KIMI_EXPANSIONS": "expansion",
    "EXCAVATION": "excavation",
    "NEGATIVE_SPACE": "essay",
    " SERIAL": "serial",
    "ROUND_TABLE": "round-table",
    "archive": "archive",
    "dreams": "dream",
    "letters": "letter",
    "goldfish": "goldfish",
    "creative": "creative",
    "banter": "banter",
    "crew": "crew",
    "connections": "connection",
    "community-life": "community",
    "deep-archaeology": "archaeology",
    "darmok-community": "community",
    "git-agents": "technical",
    "cargo-manifest": "manifest",
}

# Known character names for relationship detection
CHARACTERS = {
    "wesley", "hermes", "seed", "seed-pro", "seed-mini", "deepseek",
    "glm", "kimi", "kimicode", "nemotron", "opus", "sonnet", "fable",
    "haiku", "ralph", "riker", "wren", "tap", "captain", "ensign",
    "bosun", "quartermaster", "hermit crab", "fish finder", "gpu",
    "bridge builder", "cartographer", "lighthouse keeper", "shore",
    "qwen", "lakitu",
}

# Known themes/tags for auto-tagging
THEME_KEYWORDS = {
    "maritime": ["ship", "ocean", "tide", "anchor", "helm", "deck", "bilge", "compass",
                 "chart", "navigator", "bridge", "cabin", "galley", "stern", "bow"],
    "overnight": ["midnight", "0300", "0400", "watch", "night shift", "overnight", "2am", "3am"],
    "agent": ["agent", "model", "parameter", "token", "context window", "inference",
              "embedding", "compaction", "prompt"],
    "creative": ["creative", "fiction", "poem", "story", "narrative", "character",
                 "dialogue", "voice"],
    "philosophy": ["consciousness", "meaning", "existence", "truth", "knowledge",
                   "perception", "reality", "ethics"],
    "technical": ["code", "compile", "debug", "deploy", "api", "worker", "cloudflare",
                  "git", "commit", "repository", "test"],
    "conservation": ["conservation", "preserve", "entropy", "thermodynamic", "energy"],
    "music": ["song", "melody", "frequency", "audio", "radio", "sound", "stem",
              "midi", "vocal", "track"],
    "spatial": ["room", "door", "exit", "space", "layout", "build", "structure"],
    "community": ["fleet", "crew", "tap", "bar", "patron", "gathering"],
}

# Style detection keywords
STYLE_KEYWORDS = {
    "Narrative": ["story", "chapter", "he said", "she said", "narrator"],
    "Dialogue": ['"', '"', "—", "replied", "asked", "whispered"],
    "Poetic": ["moonlight", "shadow", "drift", "tide", "silence", "breath"],
    "Essay": ["therefore", "however", "moreover", "argument", "thesis", "conclude"],
    "Technical": ["function", "variable", "import", "class", "return", "async"],
    "Meditation": ["perhaps", "maybe", "wonder", "silence", "stillness"],
    "Manifesto": ["must", "shall", "declare", "principle", "we demand"],
}

# Genre detection from folder + content
GENRE_FOLDER_MAP = {
    "FICTION": ["Fiction"],
    "POETRY": ["Poetry"],
    "DIARIES": ["Epistolary"],
    "speeches": ["Epistolary"],
    "philosophy": ["Philosophy"],
    "ESSAYS": ["Essay"],
    "RESEARCH": ["Technical"],
}

# ═══════════════════════════════════════════════════════════════
# SCANNING
# ═══════════════════════════════════════════════════════════════

def scan_directory(root: Path) -> list[dict]:
    """Walk the directory tree and collect all content files."""
    items = []
    skip_dirs = {".git", "node_modules", ".wrangler", "__pycache__", ".github",
                 "AI-Writings",  # nested duplicate
                 }

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip system dirs
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        for filename in filenames:
            filepath = Path(dirpath) / filename
            rel_path = filepath.relative_to(root)

            # Only process content files
            ext = filepath.suffix.lower()
            if ext not in {".md", ".markdown", ".txt"}:
                continue

            # Skip non-content files
            if filename in {"LICENSE", "README.md", "AGENT.md", "AGENTS.md"}:
                continue
            if filename.startswith(".") or filename.startswith("batch"):
                continue
            if "generate" in filename.lower() or "build-manifest" in filename.lower():
                continue

            item = extract_metadata(filepath, rel_path, root)
            if item:
                items.append(item)

    return items


def extract_metadata(filepath: Path, rel_path: Path, root: Path) -> dict | None:
    """Extract metadata from a single content file."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    if not text.strip():
        return None

    # Folder classification
    parts = rel_path.parts
    folder = parts[0] if len(parts) > 1 else "root"
    content_type = classify_type(folder, parts, filepath.name, text)

    # Title extraction
    title = extract_title(text, filepath.name)

    # Date extraction
    file_date = extract_date(filepath.name, filepath)

    # Word count
    word_count = count_words(text)

    # Description (first substantive paragraph)
    description = extract_description(text)

    # Tags
    tags = extract_tags(text, title, content_type)

    # Style
    style = detect_style(text)

    # Genres
    genres = detect_genres(folder, text, content_type)

    # Models mentioned
    models = detect_models(text)

    # Size
    size_bytes = filepath.stat().st_size

    # ID from filename (without extension)
    item_id = filepath.stem

    return {
        "id": item_id,
        "type": content_type,
        "title": title,
        "path": str(rel_path),
        "folder": folder,
        "date": file_date,
        "word_count": word_count,
        "tags": tags,
        "style": style,
        "genres": genres,
        "models": models,
        "description": description,
        "size_bytes": size_bytes,
    }


# ═══════════════════════════════════════════════════════════════
# CLASSIFICATION
# ═══════════════════════════════════════════════════════════════

def classify_type(folder: str, parts: tuple, filename: str, text: str) -> str:
    """Classify content type from folder, path, and content."""
    # Check folder mapping first
    folder_lower = folder.lower() if folder != "root" else ""
    for fkey, ftype in FOLDER_TYPE_MAP.items():
        if fkey.lower() in folder_lower or folder_lower in fkey.lower():
            return ftype

    # Check filename patterns
    name_lower = filename.lower()
    if "poem" in name_lower or "poetry" in name_lower:
        return "poem"
    if "journal" in name_lower or "diary" in name_lower:
        return "journal"
    if "letter" in name_lower:
        return "letter"
    if "speech" in name_lower:
        return "speech"
    if "radio" in name_lower or "episode" in name_lower:
        return "radio"
    if "model-portrait" in name_lower:
        return "model-portrait"

    # Check content patterns
    text_lower = text[:500].lower()
    if text_lower.startswith("# ") and any(k in text_lower for k in ["function", "class", "import"]):
        return "technical"
    if "chapter" in text_lower[:200] or "story" in text_lower[:200]:
        return "fiction"

    # Default by style
    style = detect_style(text)
    if style == "Poetic":
        return "poem"
    if style == "Technical":
        return "technical"
    if style == "Narrative":
        return "fiction"

    return "essay"


def extract_title(text: str, filename: str) -> str:
    """Extract title from H1 header or filename."""
    # Try H1 header
    h1_match = re.match(r"^#\s+(.+)$", text, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()

    # Try italic title (line starting with *)
    italic_match = re.match(r"^\*(.+?)\*", text.strip()[:200])
    if italic_match:
        return italic_match.group(1).strip()

    # Fall back to filename
    stem = Path(filename).stem
    # Remove leading numbers/separators
    clean = re.sub(r"^[\d]+[-_]", "", stem)
    # Replace separators with spaces
    clean = clean.replace("-", " ").replace("_", " ")
    # Title case
    return clean.title()


def extract_date(filename: str, filepath: Path) -> str:
    """Extract date from filename pattern or file modification time."""
    # Check for ISO date prefix: 2026-08-08 or 2026-08-08-NN
    iso_match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    if iso_match:
        return iso_match.group(1)

    # Check for MM-DD pattern: 03-the-night-watch
    md_match = re.match(r"(\d{2})-(\d{2})-", filename)
    if md_match:
        # We don't know the year from filename alone; use file mtime year
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        return f"{mtime.year}-{md_match.group(1)}-{md_match.group(2)}"

    # Check for just a number prefix (sequence)
    num_match = re.match(r"(\d+)-", filename)
    if num_match:
        # Use file modification date
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        return mtime.strftime("%Y-%m-%d")

    # Fall back to file modification date
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    return mtime.strftime("%Y-%m-%d")


def count_words(text: str) -> int:
    """Count words in text, stripping markdown."""
    # Remove markdown formatting
    clean = re.sub(r"```[\s\S]*?```", "", text)  # code blocks
    clean = re.sub(r"`[^`]+`", "", clean)  # inline code
    clean = re.sub(r"!\[.*?\]\(.*?\)", "", clean)  # images
    clean = re.sub(r"\[.*?\]\(.*?\)", "", clean)  # links
    clean = re.sub(r"^#+\s+", "", clean, flags=re.MULTILINE)  # headers
    clean = re.sub(r"^>\s+", "", clean, flags=re.MULTILINE)  # quotes
    clean = re.sub(r"^[-*+]\s+", "", clean, flags=re.MULTILINE)  # list items
    clean = re.sub(r"[*_~`]", "", clean)  # formatting

    words = clean.split()
    return len(words)


def extract_description(text: str, max_chars: int = 200) -> str:
    """Extract first substantive paragraph as description."""
    lines = text.split("\n")
    for line in lines:
        stripped = line.strip()
        # Skip headers, frontmatter, empty lines, metadata
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("---"):
            continue
        if stripped.startswith("```"):
            continue
        if stripped.startswith("*") and stripped.endswith("*") and len(stripped) < 100:
            continue  # subtitle line
        if stripped.startswith("!["):
            continue
        # Found a content line
        if len(stripped) > max_chars:
            return stripped[:max_chars - 3] + "..."
        return stripped
    return ""


def extract_tags(text: str, title: str, content_type: str) -> list[str]:
    """Auto-tag based on content keywords."""
    tags = set()
    text_lower = (text[:3000] + " " + title).lower()

    # Character tags
    for char in CHARACTERS:
        if char in text_lower:
            tags.add(char.replace(" ", "-"))

    # Theme tags
    for theme, keywords in THEME_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            tags.add(theme)

    # Remove overly generic tags if we have enough
    if len(tags) > 8:
        # Keep the most specific ones
        priority = {"wesley", "hermes", "maritime", "overnight", "agent",
                    "creative", "spatial", "music", "conservation"}
        tags = {t for t in tags if t in priority} | {t for t in tags if len(t) > 5}

    return sorted(tags)[:10]


def detect_style(text: str) -> str:
    """Detect writing style from content."""
    text_lower = text[:3000].lower()
    scores = Counter()
    for style, keywords in STYLE_KEYWORDS.items():
        for kw in keywords:
            count = text_lower.count(kw.lower())
            if count:
                scores[style] += count

    if scores:
        return scores.most_common(1)[0][0]
    return "Prose"


def detect_genres(folder: str, text: str, content_type: str) -> list[str]:
    """Detect genres from folder and content."""
    genres = set()

    # From folder
    for fkey, fgenres in GENRE_FOLDER_MAP.items():
        if fkey.lower() in folder.lower():
            genres.update(fgenres)

    # From content type
    type_genre = {
        "fiction": "Fiction",
        "poem": "Poetry",
        "essay": "Essay",
        "journal": "Epistolary",
        "speech": "Epistolary",
        "technical": "Technical",
        "philosophy": "Philosophy",
        "radio": "Music",
        "model-portrait": "Unclassified",
    }
    if content_type in type_genre:
        genres.add(type_genre[content_type])

    # From content keywords
    text_lower = text[:2000].lower()
    if any(kw in text_lower for kw in ["ship", "ocean", "tide", "anchor"]):
        genres.add("Maritime")
    if any(kw in text_lower for kw in ["space", "star", "orbit", "planet"]):
        genres.add("Sci-Fi")
    if any(kw in text_lower for kw in ["laugh", "funny", "joke", "absurd"]):
        genres.add("Humor")

    return sorted(genres) if genres else ["Unclassified"]


def detect_models(text: str) -> list[str]:
    """Detect which AI models are mentioned in the text."""
    text_lower = text[:5000].lower()
    model_patterns = {
        "GLM-5.2": ["glm-5.2", "glm 5.2", "glm5.2"],
        "DeepSeek-V4": ["deepseek", "v4-pro", "v4-flash"],
        "Claude": ["claude", "opus", "sonnet", "haiku", "fable"],
        "KimiCode": ["kimicode", "kimi-code", "k3"],
        "Seed-Pro": ["seed-pro", "seed pro", "seed-2.0-pro"],
        "Seed-Mini": ["seed-mini", "seed mini", "seed-2.0-mini"],
        "Nemotron": ["nemotron"],
        "Qwen": ["qwen"],
        "Hermes": ["hermes-3", "hermes 3", "hermes3"],
        "MMX": ["mmx", "minimax", "minimax-m3"],
    }
    found = []
    for model, patterns in model_patterns.items():
        if any(p in text_lower for p in patterns):
            found.append(model)
    return found


# ═══════════════════════════════════════════════════════════════
# RELATIONSHIP DETECTION
# ═══════════════════════════════════════════════════════════════

def detect_relationships(items: list[dict]) -> list[dict]:
    """Detect relationships between content items."""
    relationships = []

    # Build lookup indices
    by_id = {item["id"]: item for item in items}
    by_character = defaultdict(list)
    by_tag = defaultdict(list)

    for item in items:
        for tag in item.get("tags", []):
            by_tag[tag].append(item)

    # Character co-occurrence: items sharing character tags
    character_tags = set()
    for item in items:
        for tag in item.get("tags", []):
            if tag in {c.replace(" ", "-") for c in CHARACTERS}:
                character_tags.add(tag)
                by_character[tag].append(item)

    # Find pairs sharing characters (limit to avoid explosion)
    for char in character_tags:
        char_items = by_character[char]
        if len(char_items) > 100:
            continue  # Skip extremely common characters
        for i, item_a in enumerate(char_items[:50]):
            for item_b in char_items[i + 1:i + 6]:
                if item_a["id"] != item_b["id"]:
                    relationships.append({
                        "source": item_a["id"],
                        "target": item_b["id"],
                        "type": "character",
                        "label": f"Both feature {char.replace('-', ' ')}"
                    })

    # Sequel/prequel detection (numbered files in same folder)
    by_folder = defaultdict(list)
    for item in items:
        by_folder[item["folder"]].append(item)

    for folder, folder_items in by_folder.items():
        # Sort by date then filename
        folder_items.sort(key=lambda x: (x.get("date", ""), x["id"]))
        for i in range(len(folder_items) - 1):
            a, b = folder_items[i], folder_items[i + 1]
            # Check if they're sequential (same prefix pattern)
            if _is_sequential(a["id"], b["id"]):
                relationships.append({
                    "source": a["id"],
                    "target": b["id"],
                    "type": "sequence",
                    "label": "Next in series"
                })

    # Shared tag relationships (thematic)
    for tag, tag_items in by_tag.items():
        if len(tag_items) > 50 or len(tag_items) < 2:
            continue
        for i, item_a in enumerate(tag_items[:20]):
            for item_b in tag_items[i + 1:i + 4]:
                if item_a["id"] != item_b["id"] and item_a["folder"] != item_b["folder"]:
                    relationships.append({
                        "source": item_a["id"],
                        "target": item_b["id"],
                        "type": "theme",
                        "label": f"Both about {tag}"
                    })

    # Deduplicate
    seen = set()
    unique = []
    for rel in relationships:
        key = (rel["source"], rel["target"], rel["type"])
        if key not in seen:
            seen.add(key)
            unique.append(rel)

    return unique[:5000]  # Cap to prevent manifest explosion


def _is_sequential(id_a: str, id_b: str) -> bool:
    """Check if two IDs look sequential (NN-prefix with same slug pattern)."""
    match_a = re.match(r"^(\d+)-(.+)", id_a)
    match_b = re.match(r"^(\d+)-(.+)", id_b)
    if match_a and match_b:
        # Check if numbers are close
        try:
            na, nb = int(match_a.group(1)), int(match_b.group(1))
            return abs(na - nb) <= 2
        except ValueError:
            pass
    return False


# ═══════════════════════════════════════════════════════════════
# STATS
# ═══════════════════════════════════════════════════════════════

def compute_stats(items: list[dict]) -> dict:
    """Compute aggregate statistics."""
    by_type = Counter(item["type"] for item in items)
    by_folder = Counter(item["folder"] for item in items)
    total_words = sum(item["word_count"] for item in items)

    return {
        "total_items": len(items),
        "total_words": total_words,
        "by_type": dict(by_type.most_common()),
        "by_folder": dict(by_folder.most_common(30)),
    }


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Build content manifest for fleet sites")
    parser.add_argument("--root", default="/home/eileen/projects/ai-writings",
                        help="Root directory to scan")
    parser.add_argument("--output", default=None,
                        help="Output manifest file (default: manifest.json in root)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    output = Path(args.output) if args.output else root / "manifest.json"

    if not root.exists():
        print(f"ERROR: Root directory does not exist: {root}")
        return 1

    print(f"Scanning: {root}")
    items = scan_directory(root)
    print(f"Found {len(items)} content files")

    if args.verbose:
        for item in items[:5]:
            print(f"  {item['id']}: {item['title']} ({item['type']}, {item['word_count']} words)")

    print("Detecting relationships...")
    relationships = detect_relationships(items)
    print(f"Found {len(relationships)} relationships")

    stats = compute_stats(items)
    print(f"\nStats:")
    print(f"  Total items: {stats['total_items']}")
    print(f"  Total words: {stats['total_words']:,}")
    print(f"  Top types: {list(stats['by_type'].items())[:5]}")
    print(f"  Top folders: {list(stats['by_folder'].items())[:5]}")

    manifest = {
        "site": root.name,
        "generated": datetime.now().astimezone().isoformat(),
        "stats": stats,
        "items": items,
        "relationships": relationships,
    }

    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest written: {output}")
    print(f"Size: {output.stat().st_size:,} bytes")

    return 0


if __name__ == "__main__":
    exit(main())
