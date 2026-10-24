#!/usr/bin/env python3
"""Advisory round for 'The Needles Settle When You Sing'.
Two voices from the fleet's advisory bench: Hermes-405B (deep taste) and Seed-2.0-mini (fast instinct).
The songwriter decides. This is advice, not instructions.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour")
from di_chat import chat

LYRICS = open("/home/eileen/projects/ai-writings/radio-theater/compass-head-radio-hour/songs/audience-c-cyberpunk-club/lyrics.md").read()

ROOM = """The song is for a 1 AM cyberpunk club called The Static: neon through smoke, a singer (Vela) with a chrome voice resonator pouring out her second set, a bartender who forgets nothing (Ren), a courier, an old coder, a dancer who almost made it (Mira), a girl who never speaks. The room is connected to everything and connected to nothing. The song's message: the loneliness and the connection can be the same thing — you are not the shell. The needles settle when you sing. Slow burn, intimate, then it opens. Target ~3:30, 72 BPM, E minor, chill electronic/synthwave ballad with live vocal."""

SYSTEM = """You are a brilliant songwriting critic and tastemaker consulted by a working songwriter. The fleet's doctrine: real, not polite. Photograph, don't label. Every word is a sample with provenance. The higher compliment is silence — trust irresolution over a tied bow. Critique the lyrics honestly: what lands, what's dead weight, what's a cliché, what could be sharper, what to cut. Give concrete line-level notes and 2-3 specific suggested rewrites at most. Do not rewrite the whole song. Be brief and pointed — a working songwriter's notes, not an essay."""

USER = f"{ROOM}\n\nHere are the full lyrics:\n\n{LYRICS}\n\nYour critique:"

for name, model in [
    ("hermes-405b", "NousResearch/Hermes-3-Llama-3.1-405B"),
    ("seed-mini", "ByteDance/Seed-2.0-mini"),
]:
    print(f"\n{'='*70}\nADVISOR: {name} ({model})\n{'='*70}")
    try:
        out = chat(SYSTEM, USER, model=model, temp=0.7, max_tokens=1800, timeout=540, retries=3)
        print(out)
    except Exception as e:
        print(f"ADVISOR {name} FAILED: {e}")
