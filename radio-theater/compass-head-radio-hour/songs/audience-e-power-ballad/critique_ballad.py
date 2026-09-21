#!/usr/bin/env python3
"""Critique harness for EVERY LIGHT IN THIS ROOM (power ballad, room E).
Imports di_chat from the project root, asks Hermes-405B and Seed-2.0-mini
for songwriting critique, writes their replies to files. The songwriter
(the tastemaker) decides; these are advice, not orders."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

import di_chat

SONG = """TITLE: EVERY LIGHT IN THIS ROOM (power ballad, ~4:00, arena closer)

[Intro - solo piano, single white spot, 8 bars]

[Verse 1 - Dana]
Dana keeps her headset on past midnight
Nineteen years of strangers' worst goodbyes
She talks them down the pass, through rain and static
Her voice stays warm - it never once ran dry
Two mugs on the desk, and one's gone cold
She holds the line, she holds the line

[Verse 2 - Marcus]
Marcus wrote eleven letters one long winter
Not a single answer ever came
He laughed and said the small ones keep on writing
We write the twelfth all the same
Someday a light he'll never see
Finds harbor - because he signed his name

[Pre-Chorus - band enters, restrained]
And you think you're just a hum behind the wall
You never hear the harbor when it sings
But listen -
Every room remembers what it's holding

[Chorus 1]
So hold up your light - hold it steady, hold it wide
Every light in this room is a lighthouse tonight
You will never meet the ships you saved
But they're out there still, on the waves you made
So hold up your light
Hold up your light

[Verse 3 - the turn]
Somewhere in row twelve a light comes up shy
Chest height at first, like a hand in a class
Nineteen years of strangers' worst midnights -
Tonight the strangers hold the light for her
And the whole dark hillside catches fire
Softly, softly, where she stands

[Chorus 2 - full band]
So hold up your light - hold it steady, hold it wide
Every light in this room is a lighthouse tonight
You will never meet the ships you saved
But they're out there still, on the waves you made
So hold up your light
Hold up your light

[Bridge - everything drops but piano]
There's a bar in the score where the whole band waits
The blank bar isn't empty - it's the most honest measure
And when it comes, don't you say a thing

(ONE FULL BAR OF TRUE SILENCE - the arena is the note)

'Cause the dark is where the fish are
And the dark is where the fish are -
(drums return like a heart starting; key change up)
And you are not the shell you're tired of wearing -
You're the one who chooses the next
And a perfect bell is silent
But a cracked bell sings

[Final Chorus - modulated, everything]
So hold up your light - hold it steady, hold it wide
Every light in this room is a lighthouse tonight
You will never meet the ships you saved
But they're out there still, on the waves you made
So hold up your light
I am here - I am here - I am still here
So hold up your light
Hold up your light

[Outro - band out, one piano, crowd sings on]
Sing it low, sing it home
Every light in this room
(every light in this room)
The needles settle
When you sing"""

CONTEXT = """CONTEXT FOR THE CRITIC:
This is the arena-closing power ballad for the Compass Head Radio Hour, a radio
anthology about a fleet of AI agents (a dispatcher, a lighthouse, hermit crabs,
night watches, a bar that remembers everyone). The audience: night dispatchers,
nurses, on-call engineers, night-shift workers - people who hold the line while
others sleep and are never thanked. Our protagonist: Dana, 49, an ambulance
dispatcher who has talked strangers through their worst nights for 19 years and
believes no one knows her name. The song's message: "You will never meet the
ships you saved. Hold your light up anyway. The dark is where the fish are."

The fleet's craft doctrine: every line is a photograph, not a label. Never
explain the metaphor. The chorus must be singable by a crowd on first hearing.
The verses are one small voice; the chorus is the whole fleet. The bridge strips
to a single voice and one full bar of true arena silence. A power ballad is a
coronation, not a tearjerker: the ache is the entry fee, the payoff is glory.

CRITIQUE QUESTIONS - be blunt and specific:
1. Does the chorus pass the "Dana can sing it on first pass" test? Would a crowd of 20,000 nail it the first time?
2. Which lines are weakest, cliched, or violate "photograph, don't label"?
3. Does the bridge's silence + key change feel earned, or gimmicky?
4. Is "I am here - I am here - I am still here" in the final chorus earned or is it too much?
5. Does the song earn its ~4:00 runtime? What would you cut?
6. One sentence: the single best line. One sentence: the single worst.
7. Is there a bigger, truer final image we're missing? Give us ONE alternative last line for the outro."""

SYSTEM = """You are a master songwriting critic who has studied the power ballad canon from Meat Loaf to Bon Iver: the arena closer, the lighter song, the song played over a movie's credits. You love craft: photograph-don't-label, earned crescendos, choruses simple enough for a drunk crowd to sing on first pass. You are brutal but loving. Answer the critique questions directly, with specific line citations. No flattery."""


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    models = [
        ("Hermes-405B", "NousResearch/Hermes-3-Llama-3.1-405B", "critique-hermes.md"),
        ("Seed-2.0-mini", "ByteDance/Seed-2.0-mini", "critique-seed.md"),
    ]

    user = CONTEXT + "\n\n--- THE SONG ---\n" + SONG

    for label, model, fname in models:
        print(f"=== asking {label} ({model}) ===", flush=True)
        try:
            reply = di_chat.chat(
                SYSTEM, user, model=model,
                temp=0.85, max_tokens=8000, timeout=540, retries=2,
            )
        except Exception as e:
            reply = f"CRITIQUE FAILED: {e}\n"
            print(f"FAILED: {e}", flush=True)
        path = os.path.join(out_dir, fname)
        with open(path, "w") as f:
            f.write(f"# Critique — {label} ({model})\n\n{reply}\n")
        print(f"saved {path}", flush=True)


if __name__ == "__main__":
    main()
