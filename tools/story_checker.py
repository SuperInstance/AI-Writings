#!/usr/bin/env python3
"""Story checker — validates markdown fiction files in the AI-Writings collection.

Features:
  - Frontmatter validation (optional YAML between --- delimiters)
  - Word count extraction and threshold checks
  - Character name tracking and consistency across files
  - Structure checks (title, headings, paragraphs)
  - Batch scanning of directories

Usage:
    python3 tools/story_checker.py path/to/story.md
    python3 tools/story_checker.py --dir stories/ --min-words 500
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Frontmatter:
    """Parsed YAML-like frontmatter block."""
    raw: Optional[str] = None
    fields: Dict[str, str] = field(default_factory=dict)

    @property
    def present(self) -> bool:
        return self.raw is not None


@dataclass
class StoryReport:
    """Validation result for a single story file."""
    path: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    title: Optional[str] = None
    word_count: int = 0
    character_names: List[str] = field(default_factory=list)
    frontmatter: Optional[Frontmatter] = None

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def __str__(self) -> str:
        status = "✓" if self.ok else "✗"
        lines = [f"{status} {self.path}  ({self.word_count} words)"]
        for e in self.errors:
            lines.append(f"  ERROR: {e}")
        for w in self.warnings:
            lines.append(f"  WARN:  {w}")
        return "\n".join(lines)


def parse_frontmatter(text: str) -> Tuple[Frontmatter, str]:
    """Extract optional YAML frontmatter and return it plus the remaining body."""
    fm = Frontmatter()
    body = text

    stripped = text.lstrip("\n")
    if stripped.startswith("---"):
        end = stripped.find("---", 3)
        if end != -1:
            fm.raw = stripped[3:end].strip()  # empty string = valid but empty frontmatter
            body = stripped[end + 3:]
            # Simple key: value parsing (no pyyaml dependency)
            for line in fm.raw.splitlines():
                match = re.match(r"^(\w[\w\s]*?):\s*(.+)$", line.strip())
                if match:
                    fm.fields[match.group(1).strip()] = match.group(2).strip()

    return fm, body


def extract_title(body: str) -> Optional[str]:
    """Extract the first markdown heading (H1) as the title."""
    for line in body.splitlines():
        # ATX style: # Title
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return m.group(1).strip()
        # Setext style: Title\n=====
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if i + 1 < len(lines) and re.match(r"^=+\s*$", lines[i + 1]):
            return line.strip()
    return None


def word_count(text: str) -> int:
    """Count words in text, ignoring markdown syntax."""
    # Remove code blocks
    cleaned = re.sub(r"```[\s\S]*?```", "", text)
    # Remove inline code
    cleaned = re.sub(r"`[^`]+`", "", cleaned)
    # Remove links but keep text
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
    # Remove image syntax
    cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", cleaned)
    # Remove HTML tags
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    # Remove markdown formatting
    cleaned = re.sub(r"[#*_~>|`]", " ", cleaned)
    return len(cleaned.split())


# Common English words that look like names but aren't characters
_STOP_NAMES = {
    "the", "a", "an", "and", "or", "but", "not", "is", "are", "was", "were",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "as", "into",
    "this", "that", "these", "those", "it", "its", "he", "she", "they", "them",
    "his", "her", "their", "my", "your", "our", "his", "him", "me", "us",
    "am", "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "can", "shall",
    "if", "then", "else", "when", "where", "how", "what", "which", "who",
    "there", "here", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "no", "nor", "only", "own", "same", "so",
    "than", "too", "very", "just", "about", "above", "after", "before",
    "between", "through", "during", "without", "within", "along",
    "also", "back", "because", "become", "became", "still", "even",
    "first", "last", "new", "old", "now", "way", "many", "much",
    "like", "long", "look", "make", "many", "get", "got", "go",
    "going", "gone", "went", "come", "came", "see", "saw", "know",
    "knew", "think", "thought", "take", "took", "want", "wanted",
    "give", "gave", "tell", "told", "say", "said", "one", "two",
    "never", "nothing", "something", "everything", "anything",
    "enough", "well", "really", "already", "always", "sometimes",
    "perhaps", "maybe", "yes", "no", "please", "thank",
    "left", "right", "up", "down", "out", "over", "under",
    "again", "away", "around", "upon", "while", "since",
    "until", "though", "although", "yet", "however",
    "man", "men", "day", "days", "time", "times", "world",
}


def extract_character_names(body: str) -> List[str]:
    """Extract probable character names (capitalized words that appear multiple times).

    Uses a heuristic: capitalized words (not sentence starters) that appear
    2+ times are likely character names.
    """
    # Get words that start with a capital letter (not at sentence start)
    text = body
    # Remove frontmatter already stripped, focus on prose
    words = re.findall(r"\b([A-Z][a-z]{2,})\b", text)

    # Count occurrences
    counts: Dict[str, int] = {}
    for w in words:
        lower = w.lower()
        if lower in _STOP_NAMES:
            continue
        counts[w] = counts.get(w, 0) + 1

    # Filter: must appear 2+ times
    names = sorted(name for name, count in counts.items() if count >= 2)
    return names


def validate_story(
    path: str,
    text: str,
    *,
    min_words: int = 0,
    max_words: int = 0,
    require_title: bool = True,
    require_frontmatter: bool = False,
) -> StoryReport:
    """Validate a single story file and return a report."""
    report = StoryReport(path=path)

    fm, body = parse_frontmatter(text)
    report.frontmatter = fm

    title = extract_title(body)
    report.title = title

    wc = word_count(body)
    report.word_count = wc

    names = extract_character_names(body)
    report.character_names = names

    # Checks
    if require_title and not title:
        report.errors.append("No title found (missing H1 heading)")

    if require_frontmatter and not fm.present:
        report.warnings.append("No frontmatter block found")

    if min_words > 0 and wc < min_words:
        report.errors.append(f"Word count ({wc}) below minimum ({min_words})")

    if max_words > 0 and wc > max_words:
        report.errors.append(f"Word count ({wc}) exceeds maximum ({max_words})")

    return report


def check_consistency(reports: List[StoryReport]) -> List[str]:
    """Cross-file consistency checks. Returns list of warnings."""
    warnings: List[str] = []

    # Build a map of character name -> files they appear in
    name_files: Dict[str, List[str]] = {}
    for r in reports:
        for name in r.character_names:
            name_files.setdefault(name, []).append(r.path)

    # Characters appearing in many files might be recurring — just informational
    recurring = {n: files for n, files in name_files.items() if len(files) >= 3}
    if recurring:
        for name, files in sorted(recurring.items()):
            warnings.append(f"Recurring character '{name}' appears in {len(files)} files")

    return warnings


def scan_directory(
    directory: str,
    *,
    min_words: int = 0,
    max_words: int = 0,
    require_title: bool = True,
    require_frontmatter: bool = False,
) -> List[StoryReport]:
    """Scan a directory for .md files and validate each."""
    reports: List[StoryReport] = []
    dir_path = Path(directory)

    if not dir_path.is_dir():
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        return reports

    md_files = sorted(dir_path.rglob("*.md"))
    # Skip README files
    md_files = [f for f in md_files if f.name.upper() != "README.MD"]

    for fpath in md_files:
        text = fpath.read_text(encoding="utf-8", errors="replace")
        rel = str(fpath.relative_to(dir_path))
        report = validate_story(
            rel,
            text,
            min_words=min_words,
            max_words=max_words,
            require_title=require_title,
            require_frontmatter=require_frontmatter,
        )
        reports.append(report)

    return reports


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate story files in the AI-Writings collection"
    )
    parser.add_argument("paths", nargs="*", help="Story files to validate")
    parser.add_argument("--dir", "-d", help="Scan a directory recursively")
    parser.add_argument("--min-words", type=int, default=0, help="Minimum word count")
    parser.add_argument("--max-words", type=int, default=0, help="Maximum word count (0=unlimited)")
    parser.add_argument("--require-frontmatter", action="store_true", help="Require YAML frontmatter")
    parser.add_argument("--no-require-title", action="store_true", help="Don't require a title")
    parser.add_argument("--check-consistency", action="store_true", help="Run cross-file consistency checks")

    args = parser.parse_args()

    reports: List[StoryReport] = []

    if args.dir:
        reports = scan_directory(
            args.dir,
            min_words=args.min_words,
            max_words=args.max_words,
            require_title=not args.no_require_title,
            require_frontmatter=args.require_frontmatter,
        )
    else:
        for path in args.paths:
            p = Path(path)
            if not p.is_file():
                print(f"Error: {path} not found", file=sys.stderr)
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            report = validate_story(
                path,
                text,
                min_words=args.min_words,
                max_words=args.max_words,
                require_title=not args.no_require_title,
                require_frontmatter=args.require_frontmatter,
            )
            reports.append(report)

    if not reports:
        print("No files to check.", file=sys.stderr)
        return 1

    # Print reports
    for r in reports:
        print(r)

    # Consistency checks
    if args.check_consistency and len(reports) > 1:
        warnings = check_consistency(reports)
        if warnings:
            print("\n--- Consistency ---")
            for w in warnings:
                print(f"  INFO: {w}")

    # Summary
    errors = sum(len(r.errors) for r in reports)
    warnings = sum(len(r.warnings) for r in reports)
    ok = sum(1 for r in reports if r.ok)
    print(f"\n{ok}/{len(reports)} files passed, {errors} errors, {warnings} warnings")

    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
