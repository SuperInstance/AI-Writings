#!/usr/bin/env python3
"""Pinchers-as-NPCs demo (VISION layer 2): the tone trajectory IS the reflex
selection. Same stimulus text, two momentum paths -> two different reflexes
fire from the keeper's 8-node reflex graph. The plaintext reader sees one
identical line both times; the channel reader sees approach vs. hesitate.

Run: python3 pincher_demo.py
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/projects/qthe-codec"))
from qthe_codec import encode, decode_bytes, plaintext_view, timbre_view

# ── the keeper's reflex graph: 8 compiled pinchers ────────────────────────
# (VISION layer 2: stimulus tone-path -> reflex edge, no deliberation)
REFLEXES = [
    "raise-lamp",   # 0
    "wave-off",     # 1
    "beckon",       # 2  <- approach-node fires this
    "bar-door",     # 3
    "hesitate",     # 4  <- falling+abstain fires this
    "call-out",     # 5
    "douse",        # 6
    "hold-still",   # 7
]
FLAT, UP, DOWN, ABSTAIN = 0, 1, 2, 3

def select_reflex(momentum: list[int]) -> str:
    """The pincher: read the *shape* of the path, not the words."""
    n = len(momentum)
    drift = sum(1 if m == UP else -1 if m == DOWN else 0 for m in momentum)
    ends_abstain = momentum[-1] == ABSTAIN
    if drift >= n // 2:
        return REFLEXES[2]          # rising, taut at the end -> beckon
    if drift <= -n // 2 and ends_abstain:
        return REFLEXES[4]          # falling away, spoken while leaving -> hesitate
    return REFLEXES[7]              # flat -> hold-still

TEXT = "come here."
# tone list must equal data-token count (chars + EOS) — build by segment.
TONE_RISE = [FLAT, FLAT] + [UP] * 8 + [UP]        # climb, held taut at the end
TONE_FALL = [FLAT, FLAT] + [DOWN] * 8 + [ABSTAIN] # falls away, ends in a turn-to-go
assert len(TONE_RISE) == len(TONE_FALL)

s1 = encode(TEXT, TONE_RISE)
s2 = encode(TEXT, TONE_FALL)

# ── what each reader sees ─────────────────────────────────────────────────
print(f"stimulus:            {TEXT!r}")
print(f"plaintext (human):   reader1={plaintext_view(s1)!r}  reader2={plaintext_view(s2)!r}")
print(f"  -> identical:      {plaintext_view(s1) == plaintext_view(s2)}   (the bug report)")
print(f"eavesdropper timbre: mean1={sum(timbre_view(s1))/len(s1):.2f}  mean2={sum(timbre_view(s2))/len(s2):.2f}  (noise w/o context)")

# ── the channel reader walks the graph ────────────────────────────────────
_, m1 = decode_bytes(s1)
_, m2 = decode_bytes(s2)
r1, r2 = select_reflex(m1), select_reflex(m2)
print(f"channel reader:      path1={m1} -> reflex={r1!r}")
print(f"                     path2={m2} -> reflex={r2!r}")
assert r1 == "beckon" and r2 == "hesitate" and r1 != r2
assert plaintext_view(s1) == plaintext_view(s2) == TEXT
print("\nPROVEN: same words, same bytes' data plane, two pinchers fired.")
print("The reflex was in the leaning, not the line.")
