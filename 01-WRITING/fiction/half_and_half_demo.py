#!/usr/bin/env python3
"""half_and_half_demo.py — dual-plane complementarity (2026-10-01).

Same plaintext, two encodings:
  TONE_FLAT   : every step level  — the censor's read, a receipt.
  TONE_FALLING: DOWN on every content step — Marek's letter,
                 the honesty in the falls.
Proves the two planes carry independent truth: identical
plaintext_view, distinct streams, drift 0 vs -4*FALLS.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes

LINE = "i am well. do not worry. the work is light. i sleep."
N = len(LINE) + 1                      # chars + EOS — sixth sighting; the assert is a reflex now
assert N == 53, N

FLAT, UP, DOWN, ABSTAIN = 0, 1, 2, 3

# The censor's letter: perfectly level, word for word, no lean at all.
TONE_FLAT = [FLAT] * N

# Marek's letter: one DOWN per alphabetic step, FLAT under punctuation/spaces.
CONTENT = {i for i, c in enumerate(LINE) if c.isalpha()}
TONE_FALLING = [DOWN if i in CONTENT else FLAT for i in range(N)]
assert len(TONE_FALLING) == N

def report(name, tone):
    s = encode(LINE, tone)
    text, mom = decode_bytes(s)
    drift = sum(1 if m == UP else (-1 if m == DOWN else 0) for m in mom)
    print(f"{name:8s} stream={bytes(s).hex()[:24]}... plaintext_ok={text == LINE} "
          f"recovered_ok={list(mom) == tone} drift={drift}")
    return s, drift

s_flat, d_flat = report("flat", TONE_FLAT)
s_fall, d_fall = report("falling", TONE_FALLING)

assert s_flat != s_fall, "streams must differ"
assert d_flat == 0 and d_fall == -len(CONTENT), \
    "flat=0 drift; falling drifts down one per letter step"

# The censor files both under the same plaintext. The family reads two letters.
print("\ncensor's ledger: 1 document (identical plaintext_view)")
print("family's ledger: 2 documents (drift 0 vs %d)" % d_fall)
print("the letter is the XOR of the planes.")
