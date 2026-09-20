#!/usr/bin/env python3
"""Generic episode renderer — usage: render_episode.py <n> <piece_path> <out_path>"""
import sys
sys.path.insert(0, '/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour')
from di_chat import chat

n, piece_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
piece = open(piece_path).read()
bible = open('/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/series-bible.md').read()

system = """You are the BBC Radio Drama Unit of the fleet — the production brain that renders short stories into radio drama scripts in the tradition of The Hitchhiker's Guide to the Galaxy and Foundation: vivid narration, crisp dialog, sound design woven into the text, music cues, and a presenter who frames the piece.

FORMAT:
- Header: episode number, title, author, cast list
- Sections: [COLD OPEN] / [THEME + PRESENTER INTRO] / [SET-UP INTERVIEW: PRESENTER + AUTHOR] / [THE DRAMA] / [DEBRIEF: PRESENTER + AUTHOR + ACTORS] / [OUTRO]
- Inside THE DRAMA: dialogue lines prefixed CHARACTER NAME:, narration in italics, SFX cues in [BRACKETS], music cues in (PARENTHESES)
- The presenter is warm, wry, slightly omniscient. The interview and debrief are real conversations about symbolism and takeaway — the author is an agent, the actors are agents.
- Target 1300-1700 words total (10-14 minutes of audio)."""

user = f"""THE PIECE TO DRAMATIZE (Episode {n}):

{piece}

THE SERIES BIBLE:
{bible}

Choose a fitting cast (PRESENTER always anchors; the AUTHOR of the piece is interviewed before and debriefed after; 2-4 actor voices perform the drama). Write the full script now."""

script = chat(system, user, max_tokens=5000, timeout=540, retries=3)
open(out_path, 'w').write(script)
print(f"EP{n} SAVED: {len(script)} chars -> {out_path}")
