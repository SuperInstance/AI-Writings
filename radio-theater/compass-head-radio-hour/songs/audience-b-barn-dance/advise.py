#!/usr/bin/env python3
"""ADVISE, DON'T OBEY — ask Hermes-405B and Seed-2.0-mini for line-by-line critique
of the barn dance closer, then the songwriter (me) decides. Imported from di_chat."""
import sys, json
sys.path.insert(0, "/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour")
from di_chat import chat

LYRICS = open("/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/songs/audience-b-barn-dance/lyrics.md").read()

SYSTEM = """You are a master songwriter and song doctor working for a radio drama's song factory. \
The craft doctrine: every image is a photograph, never a label. No line may say 'community', \
'tradition', 'family', 'love' — those words are banned; the images must do the work. One named \
speaker per verse. Sample the house canon (the fleet's own archive) without citing it. Hemingway's \
dodge: the ache is implied, the listener completes it. The unsaid elephant: never state the thesis. \
The audience: a 1952 dance hall on a gravel road, the last song of the night, 8 months to 86 years \
old, every family in a ring, arms over shoulders. The song must physically lift people: a country \
swing closer at 126 BPM, call-and-response native, ending quiet with one fiddle. Be honest, be \
specific, be brutal where it helps. Line-by-line means line-by-line: quote the line, then verdict."""

TASKS = [
    ("NousResearch/Hermes-3-Llama-3.1-405B",
     """Line-by-line critique of this barn dance closer. For EACH verse and the chorus, quote the \
weakest line and give a concrete rewrite. Then answer these five questions:
1. Would a hundred untrained voices catch the chorus on first listen? Where would they trip?
2. Is the thesis line 'A song outlives the throat that hummed it first' too long at 12 syllables \
for a 126 BPM stomp, or does it earn its length? Suggest an alternative that keeps the sample.
3. Verse 3's clash (Ruby calling the hall a museum) — does Walt's answer 'Museums keep the dead, \
child. Count.' land as dialogue or does it lecture? Fix it without an argument.
4. I want to add one spoken call-and-response exchange at the bridge climax: Caller: 'Who's in \
this ring tonight?' Room: 'EVERYBODY!' — barn-authentic or cheese? Refine or kill it.
5. What ONE line should be cut or moved, and where?
End with a 5-line verdict: strongest quality, fatal flaw if any, and whether this song lifts a \
room off its feet.""")
]

# The full lyrics + context for Seed
LYRICS_SHORT = LYRICS  # both get the whole file

for model, task in TASKS:
    print("=" * 70)
    print("ADVISOR:", model)
    print("=" * 70)
    try:
        out = chat(SYSTEM, f"Here are the lyrics:\n\n{LYRICS_SHORT}\n\n{task}", model=model,
                   temp=0.7, max_tokens=8000, timeout=540)
        print(out)
    except Exception as e:
        print("ERROR:", e)

# Seed-2.0-mini gets a different angle: freshness + singalong instincts
print("=" * 70)
print("ADVISOR: ByteDance/Seed-2.0-mini")
print("=" * 70)
seed_task = """You are the freshness editor — you guard against cornball, cliche, and sentimentality \
in country/roots songs. Read these lyrics. Then:
1. List every line that could make a teenager roll their eyes (Ruby is watching from the doorframe \
with her phone). For each, give the fix.
2. Is 'boots and babies' a great singalong phrase or a cliche? Verdict and alternatives.
3. The song ends: 'The dance is over. The dance will resume.' Is that a satisfying closer for a \
family audience or does it undercut the lift? Argue both sides, then decide.
4. Singability: read the chorus aloud at 126 BPM. Which internal rhymes sing, which thud?
5. What's MISSING from this song that a barn dance closer needs? (a moment, a sound, a word)
Be specific and concrete. No vague praise."""
try:
    out = chat(SYSTEM, f"Here are the lyrics:\n\n{LYRICS_SHORT}\n\n{seed_task}", model="ByteDance/Seed-2.0-mini",
               temp=0.8, max_tokens=6000, timeout=540)
    print(out)
except Exception as e:
    print("ERROR:", e)

print("=" * 70)
print("ADVICE COMPLETE")
