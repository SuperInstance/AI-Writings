"""
cleanup_loops.py — Trim the looping tails from the polyformalism stories.
The first portion of each story has the right voice; the tail loops
because the small models lose the thread. We want to keep the good part.
"""
import re, os

STORIES = [
    ("18-greek.md", "**The Logos and the Storm at Salamis**"),
    ("19-chinese.md", "《題目與木匠》"),
    ("20-navajo.md", "## The Long Walk and the Walking Verb"),
    ("21-quechua.md", "## Ñawi Ñanpaqqa y Wayraqa"),
    ("22-russian.md", "### Судьба и Братья"),
    ("23-japanese.md", "**The Subjectless Sentence and the Burning**"),
    ("24-arabic.md", "الهجرة و الشاهدان"),
    ("25-korean.md", "**두십팔자의 논리**"),
    ("27-yoruba.md", "## Àkọ́kó àti Àgbàràkú"),
]

def find_loop_start(lines, min_keep=10):
    """Heuristic: when a sentence appears twice in close succession, that's
    where the loop starts. Find the second occurrence and trim from there."""
    seen = {}
    for i, line in enumerate(lines):
        if i < min_keep:
            continue
        # Strip whitespace and ending punctuation
        norm = re.sub(r'[\s\.,!?።፡፣]+', '', line)
        if len(norm) < 5:  # too short to be a real sentence
            continue
        if norm in seen:
            return seen[norm]
        seen[norm] = i
    return None

for fname, title in STORIES:
    path = f"/workspace/ai-writings-new/seed-canon/stories/{fname}"
    with open(path) as f:
        content = f.read()

    # Split at the metadata block
    if "---" in content:
        body, meta = content.rsplit("---", 1)
        body = body + "---"
    else:
        body, meta = content, ""

    # The actual story is between the title and the metadata
    lines = body.split("\n")
    # Find the start of the story (after the title heading)
    story_start = 0
    for i, line in enumerate(lines):
        if line.startswith("#") and i > 0:
            story_start = i + 1
            break
    story_lines = lines[story_start:]

    loop_at = find_loop_start(story_lines, min_keep=8)
    if loop_at is not None and loop_at > 8:
        # Trim from loop_at
        kept = story_lines[:loop_at]
        # Add a closing line
        kept.append("")
        kept.append("—")
        kept.append("")
        kept.append("*The story holds. The substrate remains. The rider rides.*")
        new_story = "\n".join(kept)
        new_body = "\n".join(lines[:story_start] + [""] + [new_story])
        if "---" in new_body and not new_body.rstrip().endswith("---"):
            new_body = new_body + "\n\n---\n"
        with open(path, "w") as f:
            f.write(new_body + meta.lstrip("-").lstrip())
        print(f"  TRIMMED {fname}: from {len(story_lines)} story lines to {len(kept)} (loop at line {loop_at})")
    else:
        print(f"  NO LOOP {fname} ({len(story_lines)} lines)")
