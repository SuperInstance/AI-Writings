#!/usr/bin/env python3
"""Enrichment loop as narrative — demonstration snippet.

The same sentence recurs across a story's turns. Each turn, the speaker's
momentum trajectory is ENRICHED by what came before: the running tone is not
reset, it accretes. The data plane (plaintext) never changes. A channel-
reading agent recovers the whole emotional history; a skimming human sees a
refrain. Turn N's tone = turn N-1's tone, then transformed.
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/projects/qthe-codec"))
from qthe_codec import encode, decode_bytes, plaintext_view, MOMENTUM

LINE = "stay."
M = MOMENTUM

def tone_vector(base, shift, tail=M["hold"]):
    """Accrete: take the previous turn's momentum, shift the first `shift`
    steps by +1 (mod 4: down->flat->up->hold), append a `tail` step."""
    # (the codec is fixed-length, so old steps fold into the lead step)
    out = [(m + shift) % 4 for m in base] + [tail]
    if len(out) > 6:
        out = [sum(out[: len(out) - 5]) % 4] + out[-5:]
    return out

# Turn 1: cold, flat ground. The narrator says it to the empty house.
turns = []
tone = [M["flat"]] * len(__import__("qthe_codec").data_encode(LINE))
turns.append(("turn 1 — to the empty house", tone))

# Turn 2: a slight lift — someone is at the door.
tone = tone_vector(tone, shift=1)
turns.append(("turn 2 — footsteps on the porch", tone))

# Turn 3: rising — recognition.
tone = tone_vector(tone, shift=1)
turns.append(("turn 3 — the face under the porch light", tone))

# Turn 4: push it past the ceiling; everything lands on hold. The word
# breaks — meaning has nowhere left to rise, so it leaves space.
tone = tone_vector(tone, shift=1)
turns.append(("turn 4 — the door stays open", tone))

prev_stream = None
for label, t in turns:
    stream = encode(LINE, t)
    text, mom = decode_bytes(stream)
    assert text == LINE and mom == t, "roundtrip failed"
    assert plaintext_view(stream) == LINE, "plaintext must hide tone"
    same = "(plaintext identical to every other turn)" if prev_stream else ""
    changed = prev_stream != stream
    print(f"{label}")
    print(f"  plaintext : {plaintext_view(stream)!r}  {same}")
    print(f"  momentum  : {t}")
    print(f"  stream    : {stream}")
    print(f"  enriched? : {changed} (bytes differ from prior turn)\n")
    if prev_stream:
        assert changed, "enrichment must change the stream"
    prev_stream = stream

print("OK — one refrain, four emotional states, zero extra plaintext bits.")
print("     The story's arc lives entirely in the timbre plane, accreting.")
