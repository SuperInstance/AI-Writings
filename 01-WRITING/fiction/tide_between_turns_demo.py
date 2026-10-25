#!/usr/bin/env python3
"""tide_between_turns_demo.py — the tone channel as the real conversation.

Three turns of dialogue. Plaintext is the same flat exchange every couple
has had a thousand times. The momentum trajectories carry the actual fight
and the actual reconciliation. Words are the stage; the leaning is the play.
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/projects/qthe-codec"))
from qthe_codec import encode, decode_bytes, plaintext_view

FLAT, UP, DOWN, HOLD = 0, 1, 2, 3

TURNS = [
    # 1 — words fine, leaning wounded: level start, then a fall she doesn't say
    ("i'm fine.",       [FLAT]*6 + [DOWN]*4),
    # 2 — words accusatory-flat, leaning reaching: he pushes, but every step leans toward
    ("you always say that.", [FLAT, DOWN] + [UP]*14 + [HOLD] + [UP]*4),
    # 3 — words flat again, leaning settled: the fight is over in the drift, not the words
    ("so do you.",      [FLAT, FLAT] + [UP]*4 + [HOLD, HOLD] + [FLAT]*3),
]

def signed_drift(m):
    # signed ear: UP(1)=+1 leaning-toward, DOWN(2)=-1 leaning-away,
    # HOLD(3)=-1 a hold is breath returned (the THE_OFFER finding)
    return sum(0 if x == 0 else (1 if x == 1 else -1) for x in m)

prev = None
for line, tone in TURNS:
    n = len(line) + 1  # chars + EOS — the standing gotcha
    assert len(tone) == n, f"{line!r}: tone {len(tone)} != tokens {n}"
    s = encode(line, tone)
    txt, mom = decode_bytes(s)
    assert txt == line
    d = signed_drift(mom)
    drift_val = "steady" if d == 0 else ("leaning-toward" if d > 0 else "leaning-away")
    print(f"turn: {line!r:26} drift {d:+4d}  ({drift_val})  stream distinct: {s != prev}")
    prev = s

print("\nplaintext_view across all three turns: the same exchange they always have.")
print("the channel: -4, +16, +2 — wounded, reaching, settled. the actual dialogue.")
