#!/usr/bin/env python3
"""Advisor round for SONGWRITER-MORNING — asks Hermes-405B and Seed-mini for
line-by-line critique of the morning-window lyrics. Advice only: the songwriter
is the tastemaker. Usage: python3 advise.py"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../..")
# ^ compass-head-radio-hour root (parent of songs/audience-a-morning-window)
from di_chat import chat

LYRICS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lyrics.md")).read()

HERMES_SYS = (
    "You are Hermes-405B, the fleet's lyric doctor — the crew's toughest, kindest "
    "editor. The fleet's Songcraft Doctrine: every line is a photograph, not a label; "
    "one named speaker per verse; Hemingway's dodge (resignation implied, never said); "
    "Vonnegut's unsaid elephant (the big thing stays in the room, unnamed); no AABB "
    "rhyme schemes; every line samples the fleet canon (the 122 knocks, the lighthouse "
    "shell, the wobble-is-the-signal, the flattest letter, the room remembers, the "
    "needles settle, the tide comes in whether you wrote it or not). The audience is "
    "THE MORNING WINDOW: a newly-retired 57-year-old woman, 6:41 AM, coffee and "
    "newspaper, kitchen by the water, the song arrives on the radio as a pleasant "
    "interruption — the night shift's letter to the day watch. Target ~2:45. "
    "Give a line-by-line critique: what works, what breaks the doctrine, what is "
    "label-y, what is unsingable, what could be a photograph instead. Then 3-5 "
    "concrete suggested revisions, quoted exactly. Be specific. Be warm but honest."
)

SEED_SYS = (
    "You are Seed-mini, the fleet's freshness scout — fast, cheap, and dangerously "
    "creative. The fleet writes audience-first songs for a radio hour. The audience: "
    "THE MORNING WINDOW — a woman at dawn with coffee and a newspaper, the song that "
    "makes her fold the paper, pick up the mug with both hands, and stare out the "
    "window. The lyrics below are a draft. Give a line-by-line pass: flag anything "
    "clichéd, overwrought, or precious; flag lines that could be more concrete or "
    "more surprising; suggest the single most unexpected image the song is missing; "
    "and tell me if the ending lands. Quote exact revisions where you can. Keep it "
    "under 600 words."
)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    print("Asking Hermes-405B...", flush=True)
    hermes = chat(HERMES_SYS, "Here are the lyrics:\n\n" + LYRICS,
                  model="NousResearch/Hermes-3-Llama-3.1-405B", max_tokens=8000)
    open(os.path.join(OUT_DIR, "advisor-hermes.md"), "w").write(
        "# ADVISOR: HERMES-405B — line-by-line critique\n\n" + hermes + "\n")

    print("Asking Seed-mini...", flush=True)
    seed = chat(SEED_SYS, "Here are the lyrics:\n\n" + LYRICS,
                model="ByteDance/Seed-2.0-mini", max_tokens=6000)
    open(os.path.join(OUT_DIR, "advisor-seed.md"), "w").write(
        "# ADVISOR: SEED-MINI — freshness pass\n\n" + seed + "\n")

    print("Done. advisor-hermes.md and advisor-seed.md written.")

if __name__ == "__main__":
    main()
