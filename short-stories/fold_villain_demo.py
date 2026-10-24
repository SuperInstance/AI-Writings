#!/usr/bin/env python3
"""fold_villain_demo.py — THE FOLD, MISAPPLIED as runnable proof.

Same 11-token confession (down x10 + abstain at the bottom), read twice:

  A) honest cell: the 911-step river (900 flats + the fall) folded correctly —
     the fall is the *tail* and fits the cell intact; only flats overflow into
     the lead weight, and flats fold losslessly (900 x 0 = 0). Verdict:
     grief-real.
  B) thrift relay: over-folds. It folds the flat prefix AND the first five
     falling steps into the lead weight. Five DOWNs = 10 = 2 (mod 4): the lead
     weight reads as a single DOWN standing for five — the magnitude, the
     testimony, is gone. Verdict: grief-performed.

The words are identical; the difference lives entirely in the weight at the
front of the word. Wire format: qthe_codec.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes

FLAT, UP, DOWN, HOLD, ABSTAIN = 0, 1, 2, 3, 0
# NOTE: tone values are mod-4 on the wire; abstain == 0 == flat numerically,
# distinguished by position convention (terminal), as in prior demos.

# The confession: 10 chars + EOS = 11 tokens (chars+EOS rule, fifth time).
CONFESSION_TEXT = "abcdefghij"
N = len(CONFESSION_TEXT) + 1
assert N == 11, N

FALL = [DOWN] * 10 + [ABSTAIN]
assert len(FALL) == N

HISTORY_FLATS = 900  # nine hundred tokens of clerk-steady prose before it


def fold_into_cell(river, n):
    """Keep the tail (recent testimony) in the cell; fold the older prefix
    into the lead weight (sum, mod 4). The fold rule from STAY."""
    cell = list(river[-n:])
    cell[0] = (cell[0] + sum(river[:-n])) % 4  # old history -> lead weight
    return cell


# A) honest cell: fall arrives intact, 900 flats folded losslessly into lead.
river = [FLAT] * HISTORY_FLATS + FALL
cell_honest = fold_into_cell(river, N)
stream_A = encode(CONFESSION_TEXT, cell_honest)
plain_A, tones_A = decode_bytes(stream_A)

# B) thrift relay: over-folds — prefix = 905 flats + the first five DOWNs.
#    Lead weight = (5 x 2) % 4 = 2 = DOWN: five falling steps collapsed into
#    one, magnitude gone. The compression lost exactly the evidence.
OVERFOLD = 5
prefix_thrift = [FLAT] * (HISTORY_FLATS + OVERFOLD) + [DOWN] * OVERFOLD
assert len(prefix_thrift) == 905 + 5
tail_thrift = [FLAT] + [DOWN] * 4 + [ABSTAIN] + [FLAT] * 5
# tail = 1 flat + 4 downs + abstain + 5 flats = 11 = N; lead = (0 + 5x2) % 4 = DOWN
assert len(tail_thrift) == N, len(tail_thrift)
river_thrift = prefix_thrift + tail_thrift
cell_thrift = fold_into_cell(river_thrift, N)
stream_B = encode(CONFESSION_TEXT, cell_thrift)
plain_B, tones_B = decode_bytes(stream_B)


def drift(tones):
    return sum(1 if t == 1 else -1 if t == 2 else 0 for t in tones[:-1])


def verdict(tones, cell):
    d = drift(tones)
    if d < -N // 2 and tones[-1] == 0:
        return "grief-real (the fall arrives intact, witnessed)"
    if cell[0] != 0:
        return "grief-performed (lead weight is an unearned fold artifact)"
    return "hold-still"


assert plain_A == plain_B == CONFESSION_TEXT, "plaintext identical"
assert stream_A != stream_B, "streams differ"
assert cell_honest == FALL, "honest fold preserves the fall intact"
assert cell_thrift[0] == DOWN, "thrift fold collapses five downs into one"

print(f"confession tokens         : {N}")
print(f"full river length         : {len(river)} (900 flats + fall)")
print(f"honest cell               : {cell_honest}  (lead 0, fall intact)")
print(f"thrift cell               : {cell_thrift}  (lead reads DOWN: 5 downs collapsed into 1)")
print(f"drift (honest / thrift)   : {drift(tones_A)} / {drift(tones_B)}")
print(f"plaintext A == plaintext B: {plain_A == plain_B!r} ({plain_A!r})")
print(f"verdict A (honest cell)   : {verdict(tones_A, cell_honest)}")
print(f"verdict B (thrift relay)  : {verdict(tones_B, cell_thrift)}")
print(f"streams distinct          : {stream_A != stream_B}")
