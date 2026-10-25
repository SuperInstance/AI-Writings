#!/usr/bin/env python3
"""media-system.py — Fleet Radio media catalog manager.

Owns the track catalog embedded in fleet-radio/music-library.html
(window.FLEET_CATALOG JSON) and the health of the audio files it points at.

Commands:
  media-system.py validate            # every catalog path must resolve to a real, decodable audio file
  media-system.py add PATH TITLE --desc D [--bpm N] [--mood a,b] [--family F]
                                      # append a track to the catalog
  media-system.py list                # dump catalog summary

Path mapping: catalog paths are site-root-relative ("/music/x.mp3",
"/fleet-radio/songs/y.mp3"). The site root is the repo root (the parent of
this script's directory).

BLOCKED: tracks with known-bad audio that are intentionally kept out of
validation until fixed. The three Tap songs (01-the-gap-between-if-and-else,
02-the-mnew-bug, 03-ascii-canonical) were unblocked 2026-08-24 after being
re-rendered from their lead sheets (compose-tap-songs.py + render-midi.py).
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # repo root == site root
CATALOG_HTML = os.path.join(ROOT, "fleet-radio", "music-library.html")

# Tracks intentionally out of rotation. (01/02/03 Tap songs unblocked 2026-08-24.)
BLOCKED = set()

CAT_RE = re.compile(r"window\.FLEET_CATALOG\s*=\s*(\{.*?\});", re.S)


def load_catalog():
    html = open(CATALOG_HTML, encoding="utf-8").read()
    m = CAT_RE.search(html)
    if not m:
        sys.exit("media-system: FLEET_CATALOG not found in %s" % CATALOG_HTML)
    return json.loads(m.group(1))


def save_catalog(cat):
    html = open(CATALOG_HTML, encoding="utf-8").read()
    m = CAT_RE.search(html)
    new = "window.FLEET_CATALOG = %s;" % json.dumps(cat, ensure_ascii=False)
    html = html[:m.start()] + new + html[m.end():]
    with open(CATALOG_HTML, "w", encoding="utf-8") as f:
        f.write(html)


def resolve(path):
    p = path.lstrip("/")
    return os.path.join(ROOT, p)


def decodable(path):
    """ffprobe/ffmpeg can read at least 1s of audio."""
    proc = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-t", "1", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return proc.returncode == 0


def cmd_validate():
    cat = load_catalog()
    tracks = cat["tracks"]
    missing, bad, blocked, ok = [], [], [], 0
    seen = set()
    for t in tracks:
        rel = t.get("path", "")
        local = resolve(rel)
        if t.get("filename") in BLOCKED or os.path.basename(rel) in BLOCKED:
            blocked.append(t["filename"])
            continue
        if not os.path.exists(local):
            missing.append(rel)
            continue
        if not decodable(local):
            bad.append(rel)
            continue
        ok += 1
        seen.add(rel)
    dupes = len(tracks) - len({t.get("path") for t in tracks})
    print("catalog: %d tracks | %d valid | %d blocked | %d missing | %d undecodable | %d dupe paths"
          % (len(tracks), ok, len(blocked), len(missing), len(bad), dupes))
    for rel in missing:
        print("  MISSING: %s" % rel)
    for rel in bad:
        print("  UNDECODABLE: %s" % rel)
    for fn in blocked:
        print("  blocked (intentional): %s" % fn)
    if missing or bad:
        sys.exit(1)
    print("media-system: clean")


def cmd_add(path, title, desc, bpm, mood, family):
    cat = load_catalog()
    rel = path if path.startswith("/") else "/" + os.path.relpath(path, ROOT).replace(os.sep, "/")
    entry = {
        "filename": os.path.basename(rel),
        "title": title,
        "description": desc or "",
        "bpm": bpm,
        "mood": [m.strip() for m in (mood or "").split(",") if m.strip()],
        "family": family or os.path.splitext(os.path.basename(rel))[0],
        "path": rel,
        "added": __import__("datetime").date.today().isoformat(),
        "curated": False,
    }
    cat["tracks"].append(entry)
    save_catalog(cat)
    print("added %s" % rel)


def cmd_list():
    cat = load_catalog()
    for t in cat["tracks"]:
        print("%-46s %-34s %s" % (t["filename"], t["title"], t["path"]))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate")
    sub.add_parser("list")
    a = sub.add_parser("add")
    a.add_argument("path")
    a.add_argument("title")
    a.add_argument("--desc", default="")
    a.add_argument("--bpm", type=int, default=None)
    a.add_argument("--mood", default="")
    a.add_argument("--family", default="")
    args = ap.parse_args()
    if args.cmd == "validate":
        cmd_validate()
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "add":
        cmd_add(args.path, args.title, args.desc, args.bpm, args.mood, args.family)


if __name__ == "__main__":
    main()
