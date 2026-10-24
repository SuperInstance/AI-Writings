#!/usr/bin/env python3
"""intentional_softening_demo.py — the heart-fact, performed on purpose.

RUBATO (2026-10-02) found that peak-softening turns ADVANCE into BECKON.
TWO_STILLNESSES asked: is that confusion an error or a recognition?
This demo answers with the performer's answer: *neither — it is a choice.*

Same word ("advance."), two performances:
  - canonical: climb and hold taut — a command
  - offered:   the same climb, peaks softened 20% toward HOLD — an invitation
Plaintext identical. The channel carries the difference. The keeper's ledger
files the second not as a misheard advance but as a *deliberate soften*:
the intent lives in the step the performer spent.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes, plaintext_view

FLAT, UP, DOWN, HOLD = 0, 1, 2, 3
LINE = "advance."
N = len(LINE) + 1  # chars + EOS — the permanent gotcha
assert N == len(data_tokens := __import__("qthe_codec").data_encode(LINE))

# canonical ADVANCE shape: two flat leads, then climb the whole way, hold taut
TONE_COMMAND = [FLAT, FLAT] + [UP] * (N - 3) + [UP]
# the OFFERED shape: identical climb, every other peak spent as HOLD
TONE_OFFERED = [FLAT, FLAT]
for i in range(N - 3):
    TONE_OFFERED.append(HOLD if i % 2 == 1 else UP)
TONE_OFFERED.append(HOLD)  # the taut end, breathed instead of locked

assert len(TONE_COMMAND) == len(TONE_OFFERED) == N

cmd = encode(LINE, TONE_COMMAND)
off = encode(LINE, TONE_OFFERED)

_, mom_cmd = decode_bytes(cmd)
_, mom_off = decode_bytes(off)
# signed drift: HOLD (3) reads as a spent step, i.e. -1, matching the
# keeper's ear — a hold is a held breath, not a climb
def sgn(m):
    return {-1: None, 0: 0, 1: 1, 2: -2, 3: -1}[m]


drift_cmd = sum(sgn(m) for m in mom_cmd)
drift_off = sum(sgn(m) for m in mom_off)

print(f"plaintext identical: {plaintext_view(cmd) == plaintext_view(off) == LINE}")
print(f"streams distinct:    {cmd != off}")
print(f"command drift: {drift_cmd:+d}  (climb, held — the order)")
print(f"offered drift: {drift_off:+d}  (half the climb spent — the invitation)")
# nearest-shape verdict, same heuristic family as pincher_demo/rubato_demo
verdict_cmd = "command" if drift_cmd >= N / 2 else "offer"
verdict_off = "command" if drift_off >= N / 2 else "offer"
print(f"ear verdicts: {verdict_cmd} / {verdict_off}")
print("the performer's log: the second was not misheard. it was miswritten on purpose.")
