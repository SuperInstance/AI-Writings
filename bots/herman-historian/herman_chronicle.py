#!/usr/bin/env python3
"""
herman_chronicle.py — the Historian's chronicle writer.

Reads the git history of the substrate and writes a *narrative* account of
the historical period it covers.  Where the Mechanic watches the canon move,
the Historian reads what the canon's own git log says it was made of.

Historian doctrine: a chronicle is not a summary of commits, it is a reading
of a period — and every claim it makes must be checkable against the history
it was derived from.  So each chronicle carries a receipt block: the exact
revision range, commit count, author cast, and month-by-month distribution
that the narrative was computed from.  A reader who distrusts the prose can
re-derive the numbers from the same commit range and check them against the
receipt.  The receipt is not a footnote; it is the point.

The chronicle is written from the *history*, never from the present working
tree, so that a chronicle is a statement about a period that has closed
rather than a snapshot of an hour that is still running.

Usage:
    herman_chronicle.py --once              # write one chronicle, then exit
    herman_chronicle.py --once --period 30  # cover the last 30 days
    herman_chronicle.py --once --rev A..B  # cover an explicit revision range
    herman_chronicle.py --list              # list chronicles written so far
    herman_chronicle.py --status            # report the pending period, write nothing

Exit codes:
    0  chronicle written (or a read-only query completed)
    1  chronicle could not be written (repo missing, history unreadable,
       output directory unwritable)
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# --- Repo locations --------------------------------------------------------
# The canonical repo path, as hardcoded across the fleet.  A wiped sandbox
# may not have it; the /tmp staging copy is the durable fallback because the
# NAS mount can be at hard quota exhaustion.
REPO_ROOT_CANDIDATES = [
    "/workspace/repos/ai-writings",
    "/tmp/ai-writings",
]

# The chronicle and its witness log live beside this script.
BOT_DIR = Path(__file__).resolve().parent
CHRONICLE_DIR = BOT_DIR / "chronicles"
WITNESS_LOG = BOT_DIR / "witness.log"
STATE_FILE = BOT_DIR / "chronicle_state.json"


def log(msg):
    print(f"[herman-chronicle] {msg}", flush=True)


def find_repo_root():
    """Return the first repo root that looks like the substrate, or None."""
    for cand in REPO_ROOT_CANDIDATES:
        p = Path(cand)
        if (p / ".git").exists() and (p / "bots").is_dir():
            return p
    # Fall back to a bare .git check without the bots/ requirement.
    for cand in REPO_ROOT_CANDIDATES:
        p = Path(cand)
        if (p / ".git").exists():
            return p
    return None


# --- git plumbing -----------------------------------------------------------

def git(repo, *args, check=True):
    """Run a git command in `repo` and return stdout as text."""
    env = dict(os.environ)
    env.setdefault("GIT_SSL_NO_VERIFY", "1")
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True, text=True, env=env,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({proc.returncode}): {proc.stderr.strip()}"
        )
    return proc.stdout


def git_ok(repo, *args):
    """Run a git command; return (ok, stdout)."""
    try:
        return True, git(repo, *args)
    except RuntimeError:
        return False, ""


# --- history collection -----------------------------------------------------

def parse_commit_line(line):
    """Parse a `git log` record separated by \\x1f, \\x1e fields."""
    parts = line.split("\x1e")
    if not parts:
        return None
    head = parts[0].rstrip("\n")
    fields = head.split("\x1f")
    if len(fields) < 5:
        return None
    sha, author, email, iso, subject = fields[:5]
    return {
        "sha": sha.strip(),
        "author": author.strip(),
        "email": email.strip(),
        "date": iso.strip(),
        "subject": subject.strip(),
    }


def collect_history(repo, rev_range, limit=None):
    """Collect commits in `rev_range` (default: all refs)."""
    args = ["log", "--all" if rev_range is None else rev_range,
            "--no-merges", "--date=iso-strict",
            "--pretty=format:%H\x1f%an\x1f%ae\x1f%ad\x1f%s\x1e"]
    out = git(repo, *args)
    commits = []
    for line in out.split("\x1e"):
        c = parse_commit_line(line)
        if c:
            commits.append(c)
    if limit:
        commits = commits[:limit]
    return commits


def author_key(name):
    """Normalise an author name so 'Casey' and 'Casey Digennaro' are one."""
    n = name.strip().lower()
    n = re.sub(r"\s*\(.*\)\s*$", "", n)          # trailing parenthetical
    # Collapse separators to spaces BEFORE the alias lookup, so that
    # 'civilization-orchestrator' and 'Civilization Orchestrator' reach the
    # same alias key instead of splitting into two hands.
    n = re.sub(r"[^a-z]+", " ", n).strip()
    n = re.sub(r"\s+", " ", n)
    aliases = {
        "casey": "casey digennaro",
        "casey digennaro": "casey digennaro",
        "casey d": "casey digennaro",
        "superinstance": "superinstance",
        "mavis": "mavis",
        "mavis agent": "mavis",
        "claude": "claude",
        "openclaw": "openclaw",
        "wesley": "wesley the mechanic",
        "wesley the mechanic": "wesley the mechanic",
        "wesley mechanic": "wesley the mechanic",
        "wesley-mechanic": "wesley the mechanic",
        "github actions bot": "github actions",
        "github actions": "github actions",
        "githubactionsbot": "github actions",
        "ci bot": "github actions",
        "ci-bot": "github actions",
        "superinstance docbot": "superinstance docbot",
        "civilization orchestrator": "civilization orchestrator",
        "civilization-orchestrator": "civilization orchestrator",
        "civ orchestrator": "civilization orchestrator",
        "civilization orchestrator agent": "civilization orchestrator",
        "cell orchestrator": "cellular orchestrator",
        "civ orch": "civilization orchestrator",
        "mavis minimax": "mavis",
        "mavis agent": "mavis",
        "fleet forgemaster": "forgemaster",
        "wesley the mechanic": "wesley the mechanic",
        "superinstance docbot": "superinstance docbot",
    }
    if n in aliases:
        return aliases[n]
    parts = n.split(" ")
    if len(parts) >= 2:
        return " ".join(parts[:2])
    return n


def month_key(iso):
    return iso[:7]


# --- period classification --------------------------------------------------

def classify_subject(subject):
    """Bucket a commit subject into a narrative category."""
    s = subject.lower()
    if re.search(r"witness|canon poll|canon change", s):
        return "witness"
    if re.search(r"civili[sz]ation|civ orch|civ:|session \d+", s):
        return "civilization"
    if re.search(r"skill learn|run report|runbook|learnings", s):
        return "run-report"
    if re.search(r"fix|bug|patch|repair", s):
        return "repair"
    if re.search(r"essay|prose|writing|piece|night-scribe|snowball", s):
        return "prose"
    if re.search(r"feat|add |implement|build|create", s):
        return "construction"
    if re.search(r"doc|readme|guide|labs-guide", s):
        return "documentation"
    if re.search(r"merge|revert|chore|cleanup|typo", s):
        return "maintenance"
    return "other"


CATEGORY_LABELS = {
    "witness": "the witness polls — the canon's own heartbeat, logged and fingerprinted",
    "civilization": "the civilization orchestrator's endless tournament of eight cultures",
    "run-report": "the run reports — what the orchestrator learned and wrote down",
    "repair": "the repairs — the small fixes that keep a substrate standing",
    "prose": "the prose branch — essays, pieces, and the writing that is not code",
    "construction": "the construction — features, tools, and things newly brought into being",
    "documentation": "the documentation — guides and reads written for whoever comes next",
    "maintenance": "the maintenance — merges, reverts, and the keeping of accounts",
    "other": "the unclassified remainder — work that named itself in no house idiom",
}


# --- narrative --------------------------------------------------------------

def period_bounds(commits):
    if not commits:
        return None, None
    dates = sorted(c["date"] for c in commits)
    return dates[0], dates[-1]


def build_receipt(repo, commits, rev_range, oldest, newest):
    """Build the checkable receipt block that grounds the narrative."""
    authors = Counter()
    for c in commits:
        authors[author_key(c["author"])] += 1
    months = Counter(c["date"][:7] for c in commits)
    cats = Counter(classify_subject(c["subject"]) for c in commits)
    hours = Counter(c["date"][11:13] for c in commits if len(c["date"]) >= 13)

    head = git(repo, "rev-parse", "HEAD").strip()
    try:
        first = git(repo, "rev-list", "--max-parents=0", "--all").split()
    except RuntimeError:
        first = []
    root = first[-1] if first else oldest

    return {
        "repo": str(repo),
        "rev_range": rev_range or "--all (every ref)",
        "commit_count": len(commits),
        "oldest_commit": oldest,
        "newest_commit": newest,
        "root_commit": root,
        "head_at_write": head,
        "authors": authors.most_common(),
        "months": sorted(months.items()),
        "categories": cats.most_common(),
        "busiest_hour_utc": hours.most_common(1)[0] if hours else None,
        "distinct_hours": len(hours),
    }


def write_narrative(receipt, commits):
    """Compose the chronicle body from the receipt."""
    oldest = receipt["oldest_commit"]
    newest = receipt["newest_commit"]
    start = datetime.fromisoformat(oldest)
    end = datetime.fromisoformat(newest)
    span_days = (end - start).days

    authors = receipt["authors"]
    months = receipt["months"]
    cats = dict(receipt["categories"])

    lines = []
    lines.append(f"# Chronicle — {start.date().isoformat()} to {end.date().isoformat()}")
    lines.append("")
    lines.append(
        f"*The Historian's reading of the substrate's git history — "
        f"{receipt['commit_count']:,} commits across {span_days} days.*"
    )
    lines.append("")

    # --- opening: the shape of the period ---------------------------------
    lines.append("## The Shape of the Period")
    lines.append("")
    lead = authors[0] if authors else ("no one", 0)
    second = authors[1] if len(authors) > 1 else None
    lines.append(
        f"The record opens on {start.strftime('%d %B %Y')} and does not close until "
        f"{end.strftime('%d %B %Y')}. Between those two marks the substrate took "
        f"{receipt['commit_count']:,} commits, and the writing of them was not evenly "
        f"shared. **{lead[0].title()}** signed {lead[1]:,} of them "
        f"({100.0*lead[1]/max(receipt['commit_count'],1):.0f}%)"
        + (
            f", and the next hand — {second[0].title()} — signed {second[1]:,}"
            if second else ""
        )
        + f". {len(authors)} distinct hands are legible in this stretch of history."
    )
    lines.append("")

    if months:
        lines.append(
            "The months themselves are uneven, and the unevenness is the story: "
            + ", ".join(f"**{m}** saw {n:,}" for m, n in months)
            + ". A substrate that begins in a trickle and ends in a flood is a "
            "substrate that found its weather."
        )
        lines.append("")

    # --- second: what the time was made of ------------------
    lines.append("## What the Time Was Made Of")
    lines.append("")
    total = sum(cats.values()) or 1
    ordered = sorted(cats.items(), key=lambda kv: kv[1], reverse=True)
    lines.append(
        "Sorting the commit subjects by what they *were* rather than by who wrote them, "
        "the period resolves into a small number of large movements:"
    )
    lines.append("")
    for name, n in ordered:
        if n == 0:
            continue
        bar_len = max(1, round(28 * n / max(ordered[0][1], 1)))
        label = CATEGORY_LABELS.get(name, name)
        lines.append(f"- `{name}` {'█' * bar_len} {n:,} ({100.0*n/total:.0f}%) — {label}")
    lines.append("")

    top = ordered[0][0] if ordered else "other"
    lines.append(
        f"The largest single movement was **{top}**. "
        + (
            "This is what a substrate looks like when it is mostly *running* rather than "
            "mostly *building* — the log fills with the sound of a thing that has already "
            "started and does not intend to stop."
            if top in ("civilization", "witness", "run-report")
            else "This is what a substrate looks like when it is mostly *making* rather "
            "than mostly *running*."
        )
    )
    lines.append("")

    # --- third: the hours -------------------------------------------------
    bh = receipt.get("busiest_hour_utc")
    if bh:
        lines.append("## The Hours")
        lines.append("")
        span = receipt["distinct_hours"]
        lines.append(
            f"The busiest hour of the period was **{bh[0]}:00 UTC**, with {bh[1]:,} commits. "
            f"Across the whole stretch the work touched {span} distinct hours of the day"
            + (" — every one of them." if span >= 24 else ".")
            + " A history that concentrates in a handful of hours is a history written by "
            "hands that keep office hours; one that smears across all of them is a history "
            "written by something that never sleeps. "
            + (
                "This one smears, and its peak falls in the evening: the substrate did not "
                "keep office hours, it kept a night shift."
                if span >= 24 else
                "This one concentrates, and the substrate kept office hours after all."
            )
        )
        lines.append("")

    # --- closing: what the period left behind ----------------------------
    lines.append("## What It Left Behind")
    lines.append("")
    lines.append(
        f"The history begins at `{receipt['root_commit'][:12]}` and the tree was last "
        f"committed as `{receipt['head_at_write'][:12]}` at the moment this chronicle was "
        f"written. The gap between those two hashes is the period in its entirety — every "
        f"tick of it, every scar, every hook that was set and never fired. A chronicle "
        f"cannot promise that the numbers above are *true*; it can only promise that they "
        f"were computed from the same revision range a reader can name. The receipt below "
        f"is that range, stated plainly, so the prose can be checked rather than believed."
    )
    lines.append("")

    # --- receipt -----------------------------------------------------------
    lines.append("## Receipt")
    lines.append("")
    lines.append("```")
    lines.append(f"repo:            {receipt['repo']}")
    lines.append(f"rev_range:       {receipt['rev_range']}")
    lines.append(f"commits:         {receipt['commit_count']:,}")
    lines.append(f"oldest_commit:   {receipt['oldest_commit']}")
    lines.append(f"newest_commit:   {receipt['newest_commit']}")
    lines.append(f"root_commit:     {receipt['root_commit']}")
    lines.append(f"head_at_write:   {receipt['head_at_write']}")
    lines.append(f"distinct_authors: {len(receipt['authors'])}")
    lines.append("")
    lines.append("authors:")
    for name, n in receipt["authors"]:
        lines.append(f"  {n:>6,}  {name}")
    lines.append("")
    lines.append("months:")
    for m, n in receipt["months"]:
        lines.append(f"  {n:>6,}  {m}")
    lines.append("")
    lines.append("categories:")
    for name, n in receipt["categories"]:
        lines.append(f"  {n:>6,}  {name}")
    lines.append("```")
    lines.append("")
    lines.append(
        "*Written by Herman, Historian — the witness log IS a prediction; the chronicle "
        "is the log's own hindsight.*"
    )
    lines.append("")
    return "\n".join(lines)


# --- output -----------------------------------------------------------------

def chronicle_filename(start, newest):
    start = datetime.fromisoformat(start)
    end = datetime.fromisoformat(newest)
    return (
        f"chronicle-{start.strftime('%Y%m%d')}-{end.strftime('%Y%m%dT%H%M%SZ')}.md"
    )


def write_witness_line(msg):
    """Append one line to the witness log.  Never fatal."""
    try:
        WITNESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(WITNESS_LOG, "a") as f:
            f.write(f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} | {msg}\n")
        return True
    except OSError as e:
        log(f"witness log unwritable: {e}")
        return False


def save_state(state):
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        return True
    except OSError as e:
        log(f"state unwritable: {e}")
        return False


def main():
    ap = argparse.ArgumentParser(description="Write a chronicle from the substrate's git history.")
    ap.add_argument("--once", action="store_true",
                    help="write one chronicle, then exit")
    ap.add_argument("--period", type=int, default=0,
                    help="cover only the last N days of history (0 = all history)")
    ap.add_argument("--rev", default=None,
                    help="cover an explicit revision range, e.g. 'A..B'")
    ap.add_argument("--list", action="store_true",
                    help="list chronicles written so far")
    ap.add_argument("--status", action="store_true",
                    help="report the pending period without writing")
    args = ap.parse_args()

    if args.list:
        if not CHRONICLE_DIR.is_dir():
            log(f"no chronicle directory at {CHRONICLE_DIR}")
            return 0
        files = sorted(CHRONICLE_DIR.glob("chronicle-*.md"))
        if not files:
            log("no chronicles written yet")
            return 0
        for p in files:
            log(f"{p.name}  ({p.stat().st_size:,} bytes)")
        return 0

    repo = find_repo_root()
    if repo is None:
        log(f"no substrate found; looked in: {', '.join(REPO_ROOT_CANDIDATES)}")
        write_witness_line("CHRONICLE | ABORT | no substrate found")
        return 1
    log(f"substrate: {repo}")

    ok, _ = git_ok(repo, "rev-parse", "--git-dir")
    if not ok:
        log("substrate is not a git repository")
        write_witness_line("CHRONICLE | ABORT | not a git repository")
        return 1

    # Resolve the revision range.
    rev_range = args.rev
    if rev_range is None and args.period:
        since = datetime.now(timezone.utc).timestamp() - args.period * 86400
        rev_range = f"--since={datetime.fromtimestamp(since, timezone.utc).strftime('%Y-%m-%d')}"

    if args.status:
        commits = collect_history(repo, rev_range)
        oldest, newest = period_bounds(commits)
        log(f"pending period: {oldest} -> {newest} ({len(commits):,} commits)")
        return 0

    if not args.once:
        ap.print_help()
        return 0

    try:
        commits = collect_history(repo, rev_range)
    except RuntimeError as e:
        log(f"history unreadable: {e}")
        write_witness_line("CHRONICLE | ABORT | history unreadable")
        return 1

    if not commits:
        log("no commits matched the requested period; nothing to chronicle")
        write_witness_line("CHRONICLE | EMPTY | no commits in range")
        return 1

    oldest, newest = period_bounds(commits)
    receipt = build_receipt(repo, commits, rev_range, oldest, newest)
    narrative = write_narrative(receipt, commits)

    try:
        CHRONICLE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        log(f"cannot create chronicle dir {CHRONICLE_DIR}: {e}")
        write_witness_line("CHRONICLE | ABORT | chronicle dir unwritable")
        return 1

    name = chronicle_filename(oldest, newest)
    out = CHRONICLE_DIR / name
    if out.exists():
        # Never silently overwrite a chronicle: a period is written once.
        stem = out.stem
        i = 2
        while (CHRONICLE_DIR / f"{stem}-r{i}.md").exists():
            i += 1
        out = CHRONICLE_DIR / f"{stem}-r{i}.md"

    try:
        with open(out, "w") as f:
            f.write(narrative)
    except OSError as e:
        log(f"cannot write {out}: {e}")
        write_witness_line("CHRONICLE | ABORT | output unwritable")
        return 1

    size = out.stat().st_size
    digest = hashlib.sha256(narrative.encode()).hexdigest()[:12]
    log(f"wrote {out} ({size:,} bytes, sha256:{digest})")
    log(f"period: {oldest} -> {newest} | {len(commits):,} commits | {len(receipt['authors'])} authors")

    write_witness_line(
        f"CHRONICLE | WRITTEN | {out.name} | commits={len(commits)} | "
        f"oldest={oldest} | newest={newest} | authors={len(receipt['authors'])} | "
        f"sha256={digest}"
    )
    save_state({
        "last_chronicle": str(out),
        "oldest_commit": oldest,
        "newest_commit": newest,
        "commit_count": len(commits),
        "sha256": digest,
        "written_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
