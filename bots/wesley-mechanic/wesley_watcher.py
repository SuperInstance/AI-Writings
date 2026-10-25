#!/usr/bin/env python3
"""
wesley_watcher.py — the Mechanic's canon watcher.

Polls the civilization canon (Layer G snapshot + Layer H event stream) and
appends one witness-log line per poll.  If the canon moved since the last
poll, it also writes a one-paragraph witness note describing what changed.

Mechanic doctrine: action precedes analysis, and a receipt is not a claim.
Every line appended to the witness log carries a content hash of the canon
state it observed, so "the canon did not change" is a *checkable* statement
rather than an assertion.

Usage:
    wesley_watcher.py --once          # single poll, then exit
    wesley_watcher.py --once --note   # single poll, force a witness note
    wesley_watcher.py --status        # report last poll, write nothing

Exit codes:
    0  poll completed (canon changed or unchanged)
    1  poll could not be completed (canon unreadable, state unwritable)
"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

# --- Canon locations ------------------------------------------------------
# The canonical repo path, as hardcoded by civilization_orchestrator.py.
CANON_ROOT_CANDIDATES = [
    "/workspace/repos/ai-writings/cellular-first-design/code/civilizations",
    "/tmp/ai-writings/cellular-first-design/code/civilizations",
]

# The witness log and poll state live beside the watcher.
BOT_DIR = Path(__file__).resolve().parent
WITNESS_LOG = BOT_DIR / "witness.log"
POLL_STATE = BOT_DIR / "poll_state.json"
NOTE_DIR = BOT_DIR / "notes"

# Canon files we fingerprint.
LEADERBOARD = "leaderboard.json"
META_LOG = "meta_log.jsonl"
REGISTRY = "civilizations.json"

TRACKED_FILES = [LEADERBOARD, META_LOG, REGISTRY]


def log(msg):
    print(f"[wesley-watcher] {msg}", flush=True)


def find_canon_root():
    """Return the first existing canon root, or None."""
    for cand in CANON_ROOT_CANDIDATES:
        p = Path(cand)
        if p.is_dir():
            return p
    return None


def sha256_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except OSError as e:
        return f"ERR:{e.errno}"
    return h.hexdigest()


def read_canon(root):
    """
    Read the canon state.  Returns (fingerprint_dict, canon_view, error).
    """
    fp = {}
    view = {"leaderboard": None, "meta_rows": 0, "last_event": None, "registry": []}
    missing = []

    for name in TRACKED_FILES:
        p = root / name
        if not p.is_file():
            missing.append(name)
            fp[name] = "MISSING"
            continue
        fp[name] = sha256_file(p)

    if missing:
        return fp, view, f"canon file(s) missing: {', '.join(missing)}"

    try:
        with open(root / LEADERBOARD) as f:
            view["leaderboard"] = json.load(f)
    except (OSError, ValueError) as e:
        return fp, view, f"leaderboard unreadable: {e}"

    try:
        with open(root / REGISTRY) as f:
            view["registry"] = json.load(f)
    except (OSError, ValueError) as e:
        return fp, view, f"registry unreadable: {e}"

    last = None
    n = 0
    try:
        with open(root / META_LOG) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                n += 1
                last = line
    except OSError as e:
        return fp, view, f"meta log unreadable: {e}"
    view["meta_rows"] = n
    if last:
        try:
            view["last_event"] = json.loads(last)
        except ValueError:
            view["last_event"] = {"raw": last}

    return fp, view, None


def canon_fingerprint(fp):
    """Stable composite fingerprint of the canon state."""
    h = hashlib.sha256()
    for name in TRACKED_FILES:
        h.update(name.encode())
        h.update(b"=")
        h.update(str(fp.get(name, "MISSING")).encode())
        h.update(b"\n")
    return h.hexdigest()


def load_state():
    if not POLL_STATE.is_file():
        return None
    try:
        with open(POLL_STATE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_state(state):
    """Persist poll state atomically.  Returns True on success."""
    tmp = POLL_STATE.with_suffix(".json.tmp")
    try:
        with open(tmp, "w") as f:
            json.dump(state, f, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, POLL_STATE)
        return True
    except OSError as e:
        log(f"ERROR: could not write poll state: {e}")
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return False


def append_witness_log(line):
    """Append one line to the witness log.  Returns True on success."""
    try:
        with open(WITNESS_LOG, "a") as f:
            f.write(line.rstrip("\n") + "\n")
            f.flush()
            os.fsync(f.fileno())
        return True
    except OSError as e:
        log(f"ERROR: could not append to witness log: {e}")
        return False


def diff_canon(old_view, new_view):
    """
    Compare two canon views.  Returns a list of human-readable change
    strings.  Empty list means "no change".
    """
    changes = []

    old_lb = (old_view or {}).get("leaderboard") or {}
    new_lb = (new_view or {}).get("leaderboard") or {}

    old_iso = old_lb.get("iso")
    new_iso = new_lb.get("iso")
    if old_iso != new_iso:
        changes.append(f"canon snapshot moved {old_iso} -> {new_iso}")

    old_civs = {c.get("id"): c for c in old_lb.get("civilizations", [])}
    new_civs = {c.get("id"): c for c in new_lb.get("civilizations", [])}

    for cid in sorted(set(old_civs) | set(new_civs)):
        o = old_civs.get(cid)
        n = new_civs.get(cid)
        if o is None:
            changes.append(f"civ {cid} appeared (relevance {n.get('relevance')})")
            continue
        if n is None:
            changes.append(f"civ {cid} disappeared")
            continue
        for field in ("relevance", "wins", "losses", "sims_run", "generation"):
            ov, nv = o.get(field), n.get(field)
            if ov != nv:
                changes.append(f"civ {cid} {field} {ov} -> {nv}")

    old_reg = (old_view or {}).get("registry") or []
    new_reg = (new_view or {}).get("registry") or []
    if set(old_reg) != set(new_reg):
        added = sorted(set(new_reg) - set(old_reg))
        removed = sorted(set(old_reg) - set(new_reg))
        if added:
            changes.append(f"civ(s) added to registry: {', '.join(added)}")
        if removed:
            changes.append(f"civ(s) removed from registry: {', '.join(removed)}")

    old_rows = (old_view or {}).get("meta_rows", 0)
    new_rows = (new_view or {}).get("meta_rows", 0)
    if old_rows != new_rows:
        changes.append(f"meta log rows {old_rows} -> {new_rows} (+{new_rows - old_rows})")

    return changes


def write_witness_note(changes, view, fingerprint, prev_fp):
    """
    Write a one-paragraph witness note describing what changed.
    Returns (path, paragraph) or (None, None) on failure.
    """
    lb = view.get("leaderboard") or {}
    civs = lb.get("civilizations", [])
    if civs:
        top = max(civs, key=lambda c: c.get("relevance", 0))
        low = min(civs, key=lambda c: c.get("relevance", 0))
        extremes = (
            f"Highest relevance is {top.get('id')} at {top.get('relevance')} "
            f"({top.get('wins')}W/{top.get('losses')}L, {top.get('win_rate')} win rate); "
            f"lowest is {low.get('id')} at {low.get('relevance')} "
            f"({low.get('wins')}W/{low.get('losses')}L, {low.get('win_rate')} win rate)."
        )
    else:
        extremes = "No leaderboard entries were available in this poll."

    last_event = view.get("last_event") or {}
    ev = ""
    if "prompt" in last_event:
        ev = (
            f" The most recent recorded competition was {last_event.get('iso')} on "
            f"\"{last_event.get('prompt')}\", won by {last_event.get('winner_civ')}."
        )

    body = (
        " ".join(changes) + ". " + extremes + ev +
        f" Canon fingerprint moved from {str(prev_fp)[:12]} to {fingerprint[:12]}."
    )

    try:
        NOTE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        log(f"ERROR: could not create notes dir: {e}")
        return None, None

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    path = NOTE_DIR / f"witness-note-{stamp}.md"
    doc = (
        f"# Witness note — {stamp}\n\n"
        f"Canon moved since the last poll. "
        f"{body}\n"
    )
    try:
        with open(path, "w") as f:
            f.write(doc)
            f.flush()
            os.fsync(f.fileno())
    except OSError as e:
        log(f"ERROR: could not write witness note: {e}")
        return None, None

    return path, body


def do_once(force_note=False):
    root = find_canon_root()
    if root is None:
        log("ERROR: no canon root found. Tried:")
        for c in CANON_ROOT_CANDIDATES:
            log(f"  - {c}")
        return 1
    log(f"canon root: {root}")

    fp, view, err = read_canon(root)
    if err:
        log(f"ERROR: {err}")
        return 1

    fingerprint = canon_fingerprint(fp)
    prev = load_state()
    prev_fp = prev.get("fingerprint") if prev else None
    prev_view = prev.get("view") if prev else None

    now = time.time()
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(now))

    if prev_fp is None:
        log("first poll — no prior state, recording baseline")
        changed = True
        changes = ["first poll: canon state recorded as baseline"]
    elif prev_fp == fingerprint:
        log("canon UNCHANGED since last poll")
        changed = False
        changes = []
    else:
        changes = diff_canon(prev_view, view)
        changed = True
        log(f"canon CHANGED since last poll — {len(changes)} difference(s)")

    lb = view.get("leaderboard") or {}
    civs = lb.get("civilizations", [])
    leader = max(civs, key=lambda c: c.get("relevance", 0)).get("id") if civs else "-"
    meta_rows = view.get("meta_rows", 0)

    verdict = "CHANGED" if changed else "UNCHANGED"
    line = (
        f"{now_iso} | {verdict} | fp={fingerprint[:16]} "
        f"| canon_iso={lb.get('iso', '-')} | meta_rows={meta_rows} "
        f"| leader={leader} | civs={len(civs)} "
        f"| prev_fp={(prev_fp or 'none')[:16]}"
    )
    if not append_witness_log(line):
        return 1
    log(f"witness log appended: {WITNESS_LOG}")

    note_path = None
    if changed and (force_note or changes):
        note_path, body = write_witness_note(changes, view, fingerprint, prev_fp or "none")
        if note_path:
            log(f"witness note written: {note_path}")
            rel = note_path.relative_to(BOT_DIR)
            append_witness_log(f"{now_iso} | NOTE | {rel} | {body}")
            log("witness log note line appended")
    elif changed:
        log("canon changed but no note written (no diffs and not --note)")

    state = {
        "fingerprint": fingerprint,
        "files": fp,
        "view": view,
        "polled_at": now_iso,
        "polled_at_ts": now,
        "canon_root": str(root),
        "changed": changed,
        "changes": changes,
        "note": str(note_path) if note_path else None,
        "witness_log": str(WITNESS_LOG),
    }
    if not save_state(state):
        return 1
    log(f"poll state written: {POLL_STATE}")

    print()
    print("=" * 68)
    print(f"WESLEY WITNESS — poll {now_iso}")
    print("=" * 68)
    print(f"canon root        : {root}")
    print(f"canon iso         : {lb.get('iso', '-')}")
    print(f"canon fingerprint : {fingerprint}")
    print(f"previous fp       : {prev_fp or 'none (first poll)'}")
    print(f"verdict           : {'CANON CHANGED' if changed else 'CANON UNCHANGED'}")
    print(f"meta log rows     : {meta_rows}")
    print(f"civs              : {len(civs)}")
    if civs:
        print(f"leader            : {leader}")
    print(f"witness log       : {WITNESS_LOG}")
    print(f"poll state        : {POLL_STATE}")
    if note_path:
        print(f"witness note      : {note_path}")
    if changes:
        print()
        print("changes:")
        for c in changes:
            print(f"  - {c}")
    print("=" * 68)
    return 0


def do_status():
    st = load_state()
    if not st:
        log("no poll state recorded yet")
        return 1
    print(json.dumps(st, indent=2, sort_keys=True))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Wesley's canon watcher")
    ap.add_argument("--once", action="store_true",
                    help="poll once and exit (default)")
    ap.add_argument("--note", action="store_true",
                    help="force a witness note even if the diff is empty")
    ap.add_argument("--status", action="store_true",
                    help="print the last poll state and exit")
    args = ap.parse_args(argv)

    if args.status:
        return do_status()
    return do_once(force_note=args.note)


if __name__ == "__main__":
    sys.exit(main())
