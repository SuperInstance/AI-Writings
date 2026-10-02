#!/usr/bin/env python3
"""
interceptor_demo.py — the third reader's arithmetic as a weapon.

THE_THIRD_READER (2026-10-01 08:33) proved a hidden sentence rides in the
momentum plane of a cover letter: 3 momentum steps per hidden 6-bit token,
recovered as (m0<<4)|(m1<<2)|m2. This demo is the other half of that story:
the antagonist learns the trick, and the same arithmetic that let a girl read
a love letter lets a censor read every letter in the harbor.

Structure:
  1. Build the innocent letter (data plane) with a hidden payload in the
     tone plane, exactly as third_reader_demo.py did.
  2. Marta's view: plaintext only -> ORDINARY.
  3. Enevold's view: tone only -> a rhythm that is counting, filed CLEAN
     (the timbre marginal is uniform without the context key).
  4. The censor's view: both planes -> exact recovery of the hidden line.
     The censor is not smarter; the censor is the third reader with a badge.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import (
    data_encode, data_decode, encode, decode_bytes,
    plaintext_view, timbre_view, MOMENTUM,
)

DOWN, FLAT, UP, HOLD = MOMENTUM["down"], MOMENTUM["flat"], MOMENTUM["up"], MOMENTUM["hold"]

HIDDEN = "meet at the north pier"

# ── 1. the letter and its hidden freight ───────────────────────────────────
LETTER = ("dear aunt, the herring run is early this year. the market is loud "
          "and the nets are heavy. mother sends her love and asks about your "
          "knee. i will write again on sunday. your devoted niece.")

hidden_tokens = data_encode(HIDDEN)
N_HI = len(hidden_tokens)          # tokens incl. EOS
assert 3 * N_HI <= len(data_encode(LETTER)), "cover letter too short for payload"

tone = []
for tok in hidden_tokens:
    tone += [(tok >> 4) & 3, (tok >> 2) & 3, tok & 3]
N = len(data_encode(LETTER))
tone += [FLAT] * (N - len(tone))   # tail padded calm
assert len(tone) == N, f"tone length {len(tone)} != data tokens {N}"

stream = encode(LETTER, tone)

# ── 2. Marta: the data plane ────────────────────────────────────────────────
marta = plaintext_view(stream)
assert marta == LETTER

# ── 3. Enevold: the tone plane, no context key ─────────────────────────────
timbres = timbre_view(stream)
from collections import Counter
spread = len(set(timbres))
# uniform-ish across 4 states: no-context reader sees weather, not words
assert spread == 4

# ── 4. the censor: both planes ─────────────────────────────────────────────
_, momentum = decode_bytes(stream)
chunks = [momentum[i:i + 3] for i in range(0, 3 * N_HI, 3)]
recovered_tokens = [(a << 4) | (b << 2) | c for a, b, c in chunks]
recovered = data_decode(recovered_tokens)
assert recovered == HIDDEN, f"censor recovered: {recovered!r}"

# the ledger, as the piece tells it
print(f"letter      : {marta[:48]}...")
print(f"marta files : ORDINARY ({len(LETTER)} chars of family news)")
print(f"enevold sees: {spread} timbre states across {N} cells — counting, filed clean")
print(f"censor lifts: {recovered!r}")
print("OK — the third reader's arithmetic, wearing a badge.")
