#!/usr/bin/env python3
"""decoy_demo.py — steganographic misdirection over the qthe tone channel.

The BADGE method: hidden token = (m0<<4)|(m1<<2)|m2, three momentum steps
per 6-bit hidden token, read from the start of the stream.
The DECOY trick: plant a payload in exactly that shape at token 0 (the
censor finds it), and hide the real payload one *leaning off* — every real
step is (true_momentum + 1) mod 4, so the censor's arithmetic reads noise
where the truth is, and only a reader with the +1 calibration recovers it.
"""
import sys, os
sys.path.insert(0, os.path.expanduser("~/projects/qthe-codec"))
from qthe_codec import encode, decode_bytes, plaintext_view, data_encode, data_decode

FLAT, UP, DOWN, HOLD = 1, 2, 0, 3  # MOMENTUM values from the codec
M = [FLAT, UP, DOWN, HOLD]

def embed_steps(hidden_text: str, offset: int) -> list[int]:
    """3 momentum steps per hidden token, each (step + offset) mod 4."""
    toks = data_encode(hidden_text)
    steps = []
    for t in toks:
        for shift in (4, 2, 0):
            steps.append(((t >> shift) & 0x3) + offset)  # mod 4 later
    return steps

# ── the cover letter ──────────────────────────────────────────────────────
LINE = ("dear eva the herring came in late this year and the nets need mending "
        "before the boats go out again on friday if the weather holds warm the "
        "smokehouse is full and the dogs sleep on the warm sand by the breakwater "
        "every afternoon the children count the gulls for bread ")
N = len(LINE) + 1                      # chars + EOS (permanent gotcha)
assert N == len(LINE) + 1

DECOY = "meet at the north pier"        # what the censor's arithmetic finds
REAL  = "burn the tide book tuesday"    # the truth, one leaning off

d_steps = embed_steps(DECOY, 0)         # canonical BADGE embedding
r_steps = embed_steps(REAL, 1)          # +1 offset = the hidden calibration
assert len(d_steps) + len(r_steps) <= N, f"{len(d_steps)+len(r_steps)} > {N}"

TONE = [s % 4 for s in d_steps] + [s % 4 for s in r_steps]
TONE += [FLAT] * (N - len(TONE))        # tail calm
assert len(TONE) == N

stream = encode(LINE, TONE)

# ── reader 1: Marta, plaintext ────────────────────────────────────────────
assert plaintext_view(stream) == LINE
print("MARTA (plaintext):", repr(plaintext_view(stream)))
print("  verdict: ORDINARY")

# ── reader 2: the badge man, canonical arithmetic from token 0 ────────────
_, mom = decode_bytes(stream)
def lift(steps, n_tokens, offset=0):
    toks = []
    for i in range(n_tokens):
        m0, m1, m2 = (steps[3*i] - offset) % 4, (steps[3*i+1] - offset) % 4, (steps[3*i+2] - offset) % 4
        toks.append((m0 << 4) | (m1 << 2) | m2)
    return data_decode(toks)

n_decoy = len(data_encode(DECOY))
found = lift(mom, n_decoy)
print(f"\nBADGE MAN (canonical, from 0): {found!r}")
assert found == DECOY
rest = lift(mom[len(d_steps):], len(data_encode(REAL)), offset=0)   # pushes on uncalibrated
print(f"  pushes past the pier: {rest!r}  -> verdict: corrupted, filed under weather")

# ── reader 3: the family, starting after the decoy, with the +1 key ──────
true_text = lift(mom[len(d_steps):], len(data_encode(REAL)), offset=1)
print(f"\nFAMILY (offset +1, after the decoy): {true_text!r}")
assert true_text == REAL

print("\nOK — censor recovers the decoy exactly and files the truth as noise;")
print("the family recovers the truth exactly and never touches the decoy.")
