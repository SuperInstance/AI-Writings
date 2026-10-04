#!/usr/bin/env python3
"""THE_INNOCENT_LOG demo — the unreliable narrator on the timbre plane.

The log's words plead innocence. The leanings confess. We encode the log
twice: once as a truly innocent writer would (flat, with grief where grief
belongs), and once as the guilty narrator actually wrote it — and show the
ear can tell testimony from performance by where the falls land.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes, plaintext_view

UP, DOWN, HOLD, FLAT = 1, 2, 3, 0

LINE = "i did not open the drawer."
N = len(LINE) + 1  # chars + EOS (standing reflex)
assert N == 27, N

# Signed ear (THE_OFFER / TIDE lesson): UP=+1, DOWN=-1, HOLD=-1 (breath returned).
SIGNED = {UP: 1, DOWN: -1, HOLD: -1, FLAT: 0}

def drift(tone):
    return sum(SIGNED[t] for t in tone)

# char index map: 0'i' 1' ' 2'd' 3'i' 4'd' 5' ' 6'n' 7'o' 8't' 9' ' 10'o' 11'p'
# 12'e' 13'n' 14' ' 15't' 16'h' 17'e' 18' ' 19'd' 20'r' 21'a' 22'w' 23'e' 24'r'
# 25'.' 26 EOS

# --- The innocent version: steady testimony, one honest fall on the 'p' of
# --- open (naming the act costs), weight on the drawer (19-22, said heavier),
# --- and a held breath at the end (EOS, a breath held, not spent).
TONE_INNOCENT = (
    [FLAT] * 11             # "i did not o" — steady
    + [DOWN]                # 'p' of open — the denial costs a little
    + [FLAT] * 7            # "en the "
    + [DOWN] * 4            # "draw" — the object, said heavier
    + [FLAT] * 3            # "er."
    + [HOLD]                # EOS — a breath held, not spent
)
assert len(TONE_INNOCENT) == N

# --- The guilty version: same words. But innocence *performed* over-presses:
# --- the denial "not" is hammered flat-down (protest), the drawer is skipped
# --- light (the eye avoids what the hand touched), and the end rushes flat
# --- (nothing held, nothing confessed).
TONE_GUILTY = (
    [FLAT] * 6              # "i did " — steady
    + [DOWN] * 4            # " not " — the protest, pressed four times
    + [FLAT] * 17           # "open the drawer." + EOS — smooth, nothing held,
                            # and not one gram of weight on the drawer
)
assert len(TONE_GUILTY) == N

s_innocent = encode(LINE, TONE_INNOCENT)
s_guilty = encode(LINE, TONE_GUILTY)

assert plaintext_view(s_innocent) == LINE
assert plaintext_view(s_guilty) == LINE
assert s_innocent != s_guilty

# The Latin square hides both from a no-context ear; decode_bytes recovers
# each leaning exactly.
_, m_innocent = decode_bytes(s_innocent)
_, m_guilty = decode_bytes(s_guilty)
assert list(m_innocent) == TONE_INNOCENT
assert list(m_guilty) == TONE_GUILTY

d_i, d_g = drift(TONE_INNOCENT), drift(TONE_GUILTY)
print(f"line: {LINE!r}  ({N} tokens)")
print(f"innocent: drift {d_i:+d}   (a fall on the drawer, a held end)")
print(f"guilty:   drift {d_g:+d}   (a pressed denial, nothing held)")
verdict = "testimony" if d_i > d_g else "performance"
print(f"the ear files the second log under: {verdict}")
