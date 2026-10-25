#!/usr/bin/env python3
"""Critique call for 'Hum It, Love' — Hermes-405B + Seed-2.0-mini. Advise, don't obey."""
import sys
sys.path.insert(0, "/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour")
from di_chat import chat

SONG = """TITLE: Hum It, Love (folk rock, light piano, three-part harmony; G major, 88 BPM, ~3:00)

[Intro]
The lamps are low, the coffee's cold
Somewhere a piano is remembering

[Verse 1 — Margaret]
The song came north with Margaret's mother
In a boat with a hundred like her
She sang what her mother sang before her
But a different war, and a different river
She'd say: don't you mind the words, child
The tune is the part that travels

[Chorus]
Hum it, love, if you don't know the words
The hum is the part the room remembers
One voice is a candle, three is a fire
A song outlives the throat that first hummed it

[Verse 2 — the boy]
The boy's guitar has a dent from June
The G chord rings — his fingers earned it
He plays it slow, the way he learned it
He hums the parts he hasn't got yet
The old ones nod in the lamplight
And hum along like they forgot they knew it

[Chorus]

[Verse 3 — the couple]
They met in a circle on the courthouse steps
Arms linked, singing something from the old days
She didn't know the words, so she hummed it
He heard the hum and turned to find her
Same tune that came north, same tune in the kitchen
And the whole room is carrying it

[Bridge — Margaret, one voice]
She sang it at the washboard, sang it at the grave
Sang it to the river when there was nothing left to save
The words were never faithful — every throat changed a line
But the tune came through the same, love, every time

[Final Chorus]
Hum it, love, if you don't know the words
The hum is the part the room remembers
One voice is a candle, three is a fire
A song outlives the throat that first hummed it
Hum it, love — the room is humming with you

[Outro]
(Hum... the tune comes through the same, love)
(Hum... the room remembers)
(Hum...)
"""

AUDIENCE = """AUDIENCE: the Folk Room — a Sunday-evening listening room in a church basement. Living-room concert, coffeehouse. People who know the words to old songs and hum when they don't. The couple who met at a protest, the fourteen-year-old learning guitar, the eighty-one-year-old who remembers the song's ancestor. The song must make three-part harmony rise from the audience unprompted. Craft rules: photograph, don't label; one named speaker per verse; the unsaid elephant; every line earns its place; the hum is the message (imperfect participation is the original form of singing; the song outlives the throat)."""

SYSTEM = ("You are a master folk-songwright and the most trusted editor in a song factory. "
          "Give sharp, specific critique. Say what works and what doesn't, line by line where it matters. "
          "Be honest, not polite. Then give 3-5 concrete revision options ranked by priority. "
          "Keep it under 600 words. You are advising a tastemaker who will decide — do not rewrite the whole song.")

for model in ["NousResearch/Hermes-3-Llama-3.1-405B", "ByteDance/Seed-2.0-mini"]:
    print("=" * 70)
    print(f"MODEL: {model}")
    print("=" * 70)
    try:
        out = chat(SYSTEM, AUDIENCE + "\n\n" + SONG, model=model, temp=0.7, max_tokens=1800)
        print(out)
    except Exception as e:
        print(f"FAILED: {e}")
    print()
