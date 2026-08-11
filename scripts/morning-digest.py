#!/usr/bin/env python3
"""
Morning Digest Generator for the ai-writings corpus.

Runs overnight to:
1. Scan yesterday's git commits for new/modified .md files
2. Generate embeddings via DeepInfra BAAI/bge-m3
3. Cluster embeddings by cosine similarity
4. Name each cluster via DeepSeek API (one-line summary)
5. Output a morning digest markdown file

Usage:
    python3 scripts/morning-digest.py                    # yesterday's commits
    python3 scripts/morning-digest.py --date 2026-08-09  # specific date
    python3 scripts/morning-digest.py --full             # entire corpus
    python3 scripts/morning-digest.py --dry-run          # no API calls, list files only

Environment:
    DEEPINFRA_API_KEY  - from /home/eileen/mcp-deeinfra/.env
    DEEPSEEK_API_KEY   - from ~/.bashrc
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
import requests

logger = logging.getLogger("morning-digest")

# ── Configuration ────────────────────────────────────────────────────

REPO_DIR = Path(__file__).parent.parent
DIGEST_DIR = REPO_DIR / "digests"

DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/embeddings"
DEEPINFRA_MODEL = "BAAI/bge-m3"
DEEPINFRA_CHAT_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
DEEPINFRA_CHAT_MODEL = "ByteDance/Seed-2.0-mini"

DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"


def load_env() -> tuple[str, str]:
    """Load API keys from known locations."""
    deepinfra_key = os.environ.get("DEEPINFRA_API_KEY", "")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")

    # Load from /home/eileen/mcp-deeinfra/.env
    env_file = Path("/home/eileen/mcp-deeinfra/.env")
    if env_file.exists() and not deepinfra_key:
        for line in env_file.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == "DEEPINFRA_API_KEY":
                    deepinfra_key = v.strip().strip('"').strip("'")

    # Load from ~/.bashrc
    bashrc = Path.home() / ".bashrc"
    if bashrc.exists() and not deepseek_key:
        for line in bashrc.read_text().splitlines():
            if "DEEPSEEK_API_KEY" in line and "=" in line and "export" in line:
                k, v = line.split("=", 1)
                deepseek_key = v.strip().strip('"').strip("'")

    return deepinfra_key, deepseek_key


# ── Git scanning ─────────────────────────────────────────────────────

def get_changed_files(repo_dir: Path, date: Optional[str] = None, full: bool = False) -> list[Path]:
    """
    Get .md files changed on a specific date (via git log) or in the entire repo.
    """
    if full:
        return sorted(repo_dir.glob("*.md"))

    if date is None:
        target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        target_date = date

    # Get files changed on the target date
    next_date = (datetime.strptime(target_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    cmd = [
        "git", "-C", str(repo_dir), "log",
        f"--since={target_date}",
        f"--until={next_date}",
        "--name-only", "--pretty=format:", "--", "*.md"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    files = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line and line.endswith(".md"):
            filepath = repo_dir / line
            if filepath.exists():
                files.append(filepath)

    return sorted(set(files))


def read_file_summary(filepath: Path, max_chars: int = 2000) -> str:
    """Read the first N chars of a file for embedding."""
    try:
        text = filepath.read_text(encoding="utf-8")
        return text[:max_chars]
    except Exception as e:
        logger.warning(f"Could not read {filepath}: {e}")
        return ""


# ── Embedding ────────────────────────────────────────────────────────

def get_embeddings(texts: list[str], api_key: str) -> np.ndarray:
    """
    Get embeddings for a list of texts via DeepInfra bge-m3.
    Returns array of shape (n_texts, 1024).
    """
    if not texts:
        return np.array([])

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Batch in groups of 32 (API limit safety)
    all_embeddings = []
    batch_size = 32
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        body = {
            "model": DEEPINFRA_MODEL,
            "input": batch,
        }
        resp = requests.post(DEEPINFRA_URL, headers=headers, json=body, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        batch_embeddings = [item["embedding"] for item in data["data"]]
        all_embeddings.extend(batch_embeddings)
        time.sleep(0.5)  # rate limit courtesy

    return np.array(all_embeddings)


# ── Clustering ───────────────────────────────────────────────────────

def cluster_embeddings(embeddings: np.ndarray, threshold: float = 0.75) -> list[list[int]]:
    """
    Cluster embeddings by cosine similarity.

    Uses simple agglomerative clustering: items with similarity > threshold
    join the same cluster.

    Returns list of clusters, each a list of file indices.
    """
    if len(embeddings) == 0:
        return []

    # Normalize
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    normalized = embeddings / norms

    # Cosine similarity matrix
    sim_matrix = normalized @ normalized.T

    # Greedy clustering
    n = len(embeddings)
    assigned = [False] * n
    clusters: list[list[int]] = []

    for i in range(n):
        if assigned[i]:
            continue
        cluster = [i]
        assigned[i] = True
        for j in range(i + 1, n):
            if not assigned[j] and sim_matrix[i, j] >= threshold:
                cluster.append(j)
                assigned[j] = True
        clusters.append(cluster)

    return clusters


# ── Cluster naming ───────────────────────────────────────────────────

def name_cluster(filenames: list[str], excerpts: list[str], deepseek_key: str) -> str:
    """
    Use DeepSeek to generate a one-line summary for a cluster of writings.
    """
    # Truncate excerpts for the prompt
    combined = "\n".join(
        f"--- {Path(f).name} ---\n{e[:500]}"[:500]
        for f, e in zip(filenames, excerpts)
    )[:2000]

    prompt = (
        f"These are {len(filenames)} creative/technical writing pieces from a corpus. "
        f"Summarize what connects them in ONE sentence (max 80 chars). "
        f"Be specific and evocative, not generic.\n\n{combined}"
    )

    headers = {
        "Authorization": f"Bearer {deepseek_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": DEEPSEEK_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 60,
        "temperature": 0.7,
    }

    try:
        resp = requests.post(DEEPSEEK_URL, headers=headers, json=body, timeout=30)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip().strip('"')
    except Exception as e:
        logger.warning(f"Cluster naming failed: {e}")
        return f"{len(filenames)} pieces sharing themes"


# ── Digest generation ────────────────────────────────────────────────

def generate_digest(
    files: list[Path],
    deepinfra_key: str,
    deepseek_key: str,
    target_date: str,
) -> str:
    """
    Generate the morning digest markdown.
    """
    if not files:
        return f"# Morning Digest — {target_date}\n\nNo new pieces yesterday.\n"

    # Read excerpts
    excerpts = [read_file_summary(f) for f in files]
    filenames = [f.name for f in files]

    # Embed
    logger.info(f"Embedding {len(files)} pieces via bge-m3...")
    embeddings = get_embeddings(excerpts, deepinfra_key)

    if len(embeddings) == 0:
        return f"# Morning Digest — {target_date}\n\nNo content to embed.\n"

    # Cluster
    logger.info("Clustering by semantic similarity...")
    clusters = cluster_embeddings(embeddings, threshold=0.70)

    # Name clusters
    logger.info(f"Naming {len(clusters)} clusters via DeepSeek...")
    cluster_names = []
    for cluster in clusters:
        cluster_files = [filenames[i] for i in cluster]
        cluster_excerpts = [excerpts[i] for i in cluster]
        name = name_cluster(cluster_files, cluster_excerpts, deepseek_key)
        cluster_names.append((name, cluster))

    # Build digest markdown
    lines = [
        f"# 🌅 Morning Digest — {target_date}",
        "",
        f"**{len(files)} new pieces** indexed overnight, clustered into **{len(clusters)} themes**.",
        "",
    ]

    # Summary stats
    lines.append("## Themes")
    lines.append("")
    for name, cluster in cluster_names:
        lines.append(f"### {name}")
        lines.append("")
        for idx in cluster:
            filepath = files[idx]
            title = filepath.stem.replace("-", " ").title()
            # Get first meaningful line
            first_line = ""
            for line in excerpts[idx].splitlines():
                if line.strip() and not line.startswith("#") and not line.startswith("---"):
                    first_line = line.strip()[:100]
                    break
            lines.append(f"- **{title}** — {first_line}" if first_line else f"- **{title}**")
        lines.append("")

    # Full file list
    lines.append("## All New Pieces")
    lines.append("")
    for f in files:
        size = f.stat().st_size
        lines.append(f"- `{f.name}` ({size:,} bytes)")
    lines.append("")

    # Metadata footer
    lines.append("---")
    lines.append(f"*Generated by morning-digest.py | {datetime.now().isoformat()}*")
    lines.append(f"*Embedding model: {DEEPINFRA_MODEL} | Naming: {DEEPSEEK_MODEL}*")

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate a morning digest of the corpus.")
    parser.add_argument("--date", type=str, default=None,
                        help="Target date (YYYY-MM-DD). Defaults to yesterday.")
    parser.add_argument("--full", action="store_true",
                        help="Index the entire corpus, not just yesterday's commits.")
    parser.add_argument("--dry-run", action="store_true",
                        help="List files without making API calls.")
    parser.add_argument("--output", type=str, default=None,
                        help="Output file path. Defaults to digests/YYYY-MM-DD-digest.md")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # Determine date
    if args.date:
        target_date = args.date
    else:
        target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    logger.info(f"Morning digest for {target_date}")

    # Get files
    files = get_changed_files(REPO_DIR, date=target_date, full=args.full)
    logger.info(f"Found {len(files)} files to process")

    if args.dry_run:
        for f in files:
            print(f"  {f.name}")
        return

    if not files:
        logger.info("No files to process.")
        return

    # Load keys
    deepinfra_key, deepseek_key = load_env()
    if not deepinfra_key:
        print("ERROR: DEEPINFRA_API_KEY not found")
        sys.exit(1)
    if not deepseek_key:
        print("WARNING: DEEPSEEK_API_KEY not found, cluster names will be generic")

    # Generate digest
    digest = generate_digest(files, deepinfra_key, deepseek_key, target_date)

    # Write output
    DIGEST_DIR.mkdir(exist_ok=True)
    output_path = Path(args.output) if args.output else DIGEST_DIR / f"{target_date}-digest.md"
    output_path.write_text(digest, encoding="utf-8")
    logger.info(f"Digest written to {output_path}")
    print(digest)


if __name__ == "__main__":
    main()
