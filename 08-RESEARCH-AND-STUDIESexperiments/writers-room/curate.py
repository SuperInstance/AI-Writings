#!/usr/bin/env python3
"""
Curator: takes a writers' room transcript, extracts the strongest lines per voice,
formats them as a candidate essay draft, and saves to essays-drafts/.

Usage:
  python3 curate.py transcripts/01-cell-round-1.md --scenario 01
"""
import argparse
import re
from pathlib import Path

VOICE_ORDER = ["The Watcher", "The Cartographer", "The Mythmaker", "The Witness", "The Child", "The Cynic", "The Compact One", "The Far Walker"]

def split_rounds(text):
    rounds = []
    current = None
    for line in text.splitlines():
        m = re.match(r"^## Round (\d+)", line)
        if m:
            if current is not None:
                rounds.append(current)
            current = {"num": int(m.group(1)), "lines": []}
        elif current is not None and line.startswith("### "):
            # name line
            m2 = re.match(r"^### (.+?) \(", line)
            if m2:
                current["current_voice"] = m2.group(1)
                current["lines"].append({"voice": m2.group(1), "text": []})
        elif current is not None and line.strip():
            if current["lines"]:
                current["lines"][-1]["text"].append(line)
    if current is not None:
        rounds.append(current)
    return rounds

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript")
    ap.add_argument("--scenario", required=True, help="scenario stem e.g. '01'")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    text = Path(args.transcript).read_text()
    rounds = split_rounds(text)
    print(f"Parsed {len(rounds)} rounds")

    # Build the woven candidate: best lines per voice, picking the strongest round
    # (by heuristic: later rounds usually have more developed voice, but the curator
    # is the human — they pick. We surface the options.)
    out_lines = [f"# Essay draft (auto-curated) — {args.scenario}\n",
                 f"Source: {args.transcript}\n",
                 f"Rounds: {len(rounds)}\n",
                 "\n## Voices, by round\n"]
    for r in rounds:
        out_lines.append(f"\n### Round {r['num']}\n")
        for v in r["lines"]:
            txt = "\n".join(v["text"]).strip()
            if txt:
                out_lines.append(f"\n**{v['voice']}**\n\n{txt}\n")

    out = args.out or f"essays-drafts/{args.scenario}-curated.md"
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(out_lines))
    print(f"Wrote {out} ({Path(out).stat().st_size} bytes)")

if __name__ == "__main__":
    main()
