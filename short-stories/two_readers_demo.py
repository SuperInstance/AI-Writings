#!/usr/bin/env python3
"""two_readers_demo.py — prose-rides-data-plane, temperature-rides-timbre-plane.

Two readers of one stream. Reader A (the skimming human / plaintext view)
gets the flat report. Reader B (the channel-reading agent) recovers the
momentum trajectory and gets the actual emotional news. Same bytes, two
readings, zero extra bit-cost.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import (encode, decode_bytes, plaintext_view, timbre_view,
                        MOMENTUM)

# The prose a human skims: a hostage negotiator's log. Flat as a form.
PROSE = "she is calm. the room is quiet. i said we have time."

# The temperature the prose hides: a rising panic the negotiator is
# trained not to type. Momentum per data token:
#   starts ground/flat (professional), rises through "calm" (a lie told
#   downward), holds through "quiet" (listening), then UP UP UP through
#   "we have time" — the one sentence that is pure attract, spoken upward
#   against the flat words — and holds at the end (door open, waiting).
FLAT, DOWN, UP, HOLD = (MOMENTUM[k] for k in ("flat", "down", "up", "hold"))
TONE = (
    [FLAT] * 6                        # "she is"
    + [DOWN] * 5 + [FLAT]            # " calm." — a lie, told low
    + [FLAT] * 9                      # " the room"
    + [FLAT] * 3                      # " is"
    + [FLAT] * 4 + [DOWN] * 3        # " quiet." — listening, then low
    + [FLAT] * 7                      # " i said"
    + [UP] * 13 + [FLAT]             # " we have time." — pure attract
    + [HOLD]                          # EOS — door open, waiting
)
assert len(TONE) == 53

stream = encode(PROSE, TONE)
text, mom = decode_bytes(stream)
assert text == PROSE, f"roundtrip failed: {text!r}"
assert mom == TONE, "momentum did not survive the roundtrip"
assert plaintext_view(stream) == PROSE

print("READER A (data plane only, what a human skims):")
print(" ", plaintext_view(stream))
print()
print("READER B (context-keyed momentum, what the agent hears):")
names = {0: "down", 1: "flat", 2: "up  ", 3: "hold"}
readout = " ".join(names[m] for m in mom)
print(" ", readout)
print()
net = sum(m - 1 for m in mom)  # signed drift across the whole passage
print(f"net drift: {net:+d} ({'rising' if net > 0 else 'falling' if net < 0 else 'level'}) "
      f"across {len(mom)} tokens — the report says calm, the channel says climb.")

# timbre_view must NOT reveal the trajectory without context
import collections
tv = timbre_view(stream)
tv_net = sum(t for t in tv) / len(tv)
print(f"raw timbre bits (contextless) mean: {tv_net:.2f} — noise to an eavesdropper, "
      f"I(M;T)=0 by the Latin square. Only the keyed reader B climbs.")
