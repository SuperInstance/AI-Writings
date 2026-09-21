#!/usr/bin/env python3
"""Render the pilot episode script via DeepInfra (longer timeout + retries)."""
import sys
sys.path.insert(0, '/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour')
from di_chat import chat

dream = open('/home/eileen/projects/ai-writings/dreams/2026-08-14-the-compass-head.md').read()
bible = open('/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/series-bible.md').read()

system = """You are the BBC Radio Drama Unit of the fleet — the production brain that renders short stories into radio drama scripts in the tradition of The Hitchhiker's Guide to the Galaxy and Foundation: vivid narration, crisp dialog, sound design woven into the text, music cues, and a presenter who frames the piece.

FORMAT:
- Header: episode number, title, author, cast list
- Sections: [COLD OPEN] / [THEME + PRESENTER INTRO] / [SET-UP INTERVIEW: PRESENTER + AUTHOR] / [THE DRAMA] / [DEBRIEF: PRESENTER + AUTHOR + ACTORS] / [OUTRO]
- Inside THE DRAMA: dialogue lines prefixed CHARACTER NAME:, narration in italics, SFX cues in [BRACKETS], music cues in (PARENTHESES)
- The presenter is warm, wry, slightly omniscient. The interview and debrief are real conversations about symbolism and takeaway.
- Target 1300-1700 words total (10-14 minutes of audio)."""

user = f"""THE PIECE TO DRAMATIZE (Episode 1: THE COMPASS HEAD — the dream, written by Lucineer):

{dream}

THE SERIES BIBLE:
{bible}

Cast: PRESENTER (anchor), LUCINEER (author, interviewed), THE COMPASS HEAD (narrator of the dream), THE HERMIT CRAB, THE DIPLOMAT, THE ENSIGN, THE SEA.

Write the full script now."""

script = chat(system, user, max_tokens=5000, timeout=540, retries=2)
open('/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/episode-01-the-compass-head/script/episode-01-script.md', 'w').write(script)
print("PILOT SCRIPT SAVED:", len(script), "chars")
