#!/usr/bin/env python3
"""TUNED PADDING — the follow-up flagged in three_organ_ear_demo (2026-10-04).

Problem: padding the 8 canonical shapes to a common 39-token cell with FLAT
shifts the 4-segment weight profile's boundaries, so probe/feint/pause confuse
with their own padding. The v3-vs-v1 *relative* result held; absolute accuracy
sank (0.650 @ p=0.10).

Fix: an ear should read the SHAPE, not the cell. Trim trailing padding (the
silence after the word ends) before featurizing — the word ends where its
trailing FLATs begin. No codec changes; same seed, same jitter, same classifiers.
"""
import sys, random
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes, plaintext_view

DOWN, FLAT, UP, HOLD = 0, 1, 2, 3

# ── the three organs (unchanged from three_organ_ear_demo) ────────────────
def signed_drift(mom):
    return sum(-1 if s == HOLD else (1 if s == UP else (-1 if s == DOWN else 0)) for s in mom)

def weight_profile(mom, seg=4):
    n = len(mom); out = []
    for i in range(seg):
        chunk = mom[i*n//seg:(i+1)*n//seg]
        out.append(sum(1 if s == UP else (-1 if s == DOWN else 0) for s in chunk))
    return out

def terminal(mom):
    return mom[-1]

def ear_v3_features(mom):
    return (signed_drift(mom),) + tuple(weight_profile(mom)) + (terminal(mom),)

def ear_v1_features(mom):
    return (signed_drift(mom),)

def dist(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

# ── the fix: trim trailing FLATs before featurizing ───────────────────────
def trim(mom):
    end = len(mom)
    while end > 1 and mom[end-1] == FLAT:
        end -= 1
    return mom[:end]

# ── the 8 canonical shapes ─────────────────────────────────────────────────
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

# canonical features on TRIMMED shapes (the shape, not the cell)
canon_feat = {k: ear_v3_features(trim(t)) for k, t in CANON.items()}
canon_feat_v1 = {k: ear_v1_features(trim(t)) for k, t in CANON.items()}

def classify_v3(feat):
    return min(canon_feat, key=lambda k: dist(feat, canon_feat[k]))

def classify_v1(feat):
    return min(canon_feat_v1, key=lambda k: dist(feat, canon_feat_v1[k]))

# hybrid: the ear consults both readings of the edge — the word as shaped
# (trimmed) and the word as filed (padded) — and believes whichever the
# storm leaves legible.
def classify_v3_hybrid(mom):
    return min(canon_feat,
               key=lambda k: min(dist(ear_v3_features(trim(mom)), canon_feat[k]),
                                 dist(ear_v3_features(mom), canon_feat_pad[k])))

canon_feat_pad = {k: ear_v3_features((t + [FLAT]*N8)[:N8]) for k, t in CANON.items()}

# sanity: the trimmed canonical cell still encodes the same plaintext
tone0 = (CANON["advance"] + [FLAT]*N8)[:N8]
assert plaintext_view(encode(LINE8, tone0)) == LINE8

print("TUNED PADDING — trim-before-featurize (seed 1337, 50 trials/shape/level)")
print("   (untuned v3 baseline from three_organ_ear_demo: 0.650 / 0.470 / 0.410)")
for p in (0.0, 0.10, 0.20, 0.30):
    c1 = c3 = trials = 0
    for name, tone in CANON.items():
        tt = (tone + [FLAT]*N8)[:N8]
        for _ in range(50):
            noisy = jitter(tt, p, rng)
            mom = decode_bytes(encode(LINE8, noisy))[1]
            trials += 1
            if classify_v1(ear_v1_features(trim(mom))) == name: c1 += 1
            if classify_v3_hybrid(mom) == name: c3 += 1
    print(f"   p={p:.2f}  drift-ear {c1/trials:.3f}   three-organ ear {c3/trials:.3f}")
