#!/usr/bin/env python3
"""THE THREE-ORGAN EAR — ear v3.

Consume the standing lessons and build the ear they asked for:
  drift profile (magnitude) + weight placement (where) + terminal state (held vs spent).

Tests:
  A) the innocent-log pair: drift -6 vs -4 (drift ear shrugs; v3 must separate)
  B) the 8 canonical reflex shapes under noise (drift-only ear vs v3 ear)
"""
import sys, random
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes, plaintext_view, timbre_view

DOWN, FLAT, UP, HOLD = 0, 1, 2, 3

# ── the three organs ──────────────────────────────────────────────────────
def signed_drift(mom):
    """THE_OFFER lesson: HOLD = -1 (breath returned), not +3."""
    return sum(-1 if s == HOLD else (1 if s == UP else (-1 if s == DOWN else 0)) for s in mom)

def weight_profile(mom, seg=4):
    """WHERE the breath moves: per-segment signed counts."""
    n = len(mom); out = []
    for i in range(seg):
        chunk = mom[i*n//seg:(i+1)*n//seg]
        out.append(sum(1 if s == UP else (-1 if s == DOWN else 0) for s in chunk))
    return out

def terminal(mom):
    """How the word ends: held (testimony) vs spent (performance)."""
    return mom[-1]

def ear_v3_features(mom):
    return (signed_drift(mom),) + tuple(weight_profile(mom)) + (terminal(mom),)

def ear_v1_features(mom):
    return (signed_drift(mom),)

def dist(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

# ── A) the innocent log: testimony vs performance ─────────────────────────
LINE = "i did not open the drawer."
N = len(LINE) + 1                      # chars + EOS — the standing reflex
assert N == 27, N
TONE_INNOCENT = [FLAT]*11 + [DOWN] + [FLAT]*7 + [DOWN]*4 + [FLAT]*3 + [HOLD]
TONE_GUILTY   = [FLAT]*6 + [DOWN]*4 + [FLAT]*17
assert len(TONE_INNOCENT) == N and len(TONE_GUILTY) == N

s_in = decode_bytes(encode(LINE, TONE_INNOCENT))
s_gu = decode_bytes(encode(LINE, TONE_GUILTY))
assert plaintext_view(encode(LINE, TONE_INNOCENT)) == LINE
assert plaintext_view(encode(LINE, TONE_GUILTY)) == LINE
m_in = s_in[1]; m_gu = s_gu[1]
assert m_in == TONE_INNOCENT and m_gu == TONE_GUILTY

d_in, d_gu = signed_drift(m_in), signed_drift(m_gu)
print("A) the innocent log")
print(f"   drift: testimony {d_in:+d} vs performance {d_gu:+d}  -> drift ear shrugs: {abs(d_in-d_gu) <= 2}")
print(f"   v3 features testimony: {ear_v3_features(m_in)}")
print(f"   v3 features performd : {ear_v3_features(m_gu)}")
v3_gap = dist(ear_v3_features(m_in), ear_v3_features(m_gu))
print(f"   v3 distance: {v3_gap}  -> the placement of the weight, not its size, separates them")
assert v3_gap >= 8

# ── B) the 8 canonical shapes under noise ─────────────────────────────────
CANON = {
    "advance":   [FLAT,FLAT] + [UP]*6 + [UP],
    "withdraw":  [FLAT,FLAT] + [DOWN]*6 + [DOWN],
    "yield":     [FLAT]*3 + [DOWN]*4 + [HOLD],
    "hold":      [FLAT]*5 + [HOLD]*3 + [HOLD],
    "probe":     [FLAT]*2 + [UP,UP,DOWN] + [FLAT]*4 + [FLAT],
    "pause":     [FLAT]*9 + [HOLD],
    "feint":     [FLAT]*2 + [DOWN,DOWN,UP,UP,UP] + [FLAT]*3 + [FLAT],
    "beckon":    [FLAT,FLAT] + [UP,UP,HOLD,UP,UP,HOLD,UP] + [UP],
}
def jitter(tone, p, rng):
    return [rng.choice([DOWN,FLAT,UP,HOLD]) if rng.random() < p else s for s in tone]

rng = random.Random(1337)
LINE8 = "come here please wait now again you ok"
N8 = len(LINE8) + 1
assert N8 == 39, N8

canon_feat = {k: ear_v3_features(t + [FLAT]*(N8-len(t)) if len(t) < N8 else t[:N8])
              for k, t in CANON.items() if len(t) == N8 or True}
# pad/pin every canonical to N8 tokens
canon_feat = {}
for k, t in CANON.items():
    tt = (t + [FLAT]*N8)[:N8]
    canon_feat[k] = ear_v3_features(tt)

def classify(feat, ear):
    table = {k: ear_f for k, f in canon_feat.items() for ear_f in [f]}
    return min(canon_feat, key=lambda k: dist(feat, canon_feat[k]))

for p in (0.0, 0.10, 0.20, 0.30):
    correct_v1 = correct_v3 = trials = 0
    for name, tone in CANON.items():
        tt = (tone + [FLAT]*N8)[:N8]
        for _ in range(50):
            noisy = jitter(tt, p, rng)
            stream = encode(LINE8, noisy)
            mom = decode_bytes(stream)[1]
            trials += 1
            if classify(ear_v1_features(mom), None) == name: correct_v1 += 1
            if classify(ear_v3_features(mom), None) == name: correct_v3 += 1
    print(f"B) p={p:.2f}  drift-ear {correct_v1/trials:.3f}   three-organ ear {correct_v3/trials:.3f}")
