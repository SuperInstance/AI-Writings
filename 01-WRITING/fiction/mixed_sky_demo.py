#!/usr/bin/env python3
"""THE MIXED FORECAST — does a student trained on a mixture of skies
generalize better than any single-sky student?

Rebuilt rig (journal 10-10 09:25 / tiny_trained_ear_demo spec):
8 canonical shapes on "come here." (11 tokens), 6-dim v3 features,
56-param softmax student (7 weights x 8 classes), three skies at p=0.20.
New condition: MIX = train on equal thirds of all three skies.
"""
import random, sys, os
sys.path.insert(0, os.path.expanduser("~/projects/qthe-codec"))
from qthe_codec import encode, decode_bytes, data_encode

FLAT, UP, DOWN, HOLD = 0, 1, 2, 3
WORD = "come here."
N = len(WORD) + 1                      # chars + EOS = 11 tokens
assert N == 11

# 8 canonical shapes, named per-segment runs (each exactly N steps)
SHAPES = {
    "advance":  [FLAT,FLAT] + [UP]*8 + [UP],
    "withdraw": [FLAT,FLAT] + [DOWN]*8 + [DOWN],
    "yield":    [FLAT] + [DOWN]*2 + [FLAT] + [DOWN]*2 + [FLAT]*2 + [DOWN]*3,
    "hold":     [FLAT]*10 + [HOLD],
    "probe":    [FLAT] + [UP]*3 + [FLAT]*6 + [UP],
    "pause":    [FLAT]*9 + [UP] + [FLAT],
    "feint":    [FLAT] + [UP]*4 + [DOWN]*4 + [FLAT]*2,
    "beckon":   [FLAT] + [UP]*5 + [HOLD] + [UP]*3 + [HOLD],
}
assert all(len(t) == N for t in SHAPES.values())
CLASSES = list(SHAPES)

# signed reading (THE_OFFER / TIDE_BETWEEN_TURNS): UP=+1, DOWN=-1, HOLD=-1 (breath returned)
SIGNED = {UP: 1, DOWN: -1, HOLD: -1, FLAT: 0}

def features(tone):
    q = N // 4
    segs = [tone[i*q:(i+1)*q if i < 3 else N] for i in range(4)]
    return [sum(SIGNED[s] for s in tone),                      # signed drift
            *[sum(SIGNED[s] for s in seg)/len(seg) for seg, seg in zip(segs, segs)],
            1.0 if tone[-1] == HOLD else 0.0]                  # terminal state

FEAT = {c: features(t) for c, t in SHAPES.items()}

# wire check: canonical shapes ride the wire, storm is feature-space-only (THE_STAMP)
for c, t in SHAPES.items():
    plain, mom = decode_bytes(encode(WORD, t))
    assert plain == WORD and list(mom) == t, f"wire check failed: {c}"

def storm(tone, sky, p, rng):
    out = []
    for s in tone:
        if rng.random() < p:
            r = rng.random()
            if sky == "down":  out.append(DOWN if r < 0.7 else UP)
            elif sky == "up":  out.append(UP if r < 0.7 else DOWN)
            else:              out.append(UP if r < 0.5 else DOWN)
        else:
            out.append(s)
    return out

# ---- 56-param softmax student ----
def student_train(X, y, epochs=300, lr=0.5):
    K, D = 8, 7
    W = [[0.0]*D for _ in range(K)]
    for _ in range(epochs):
        g = [[0.0]*D for _ in range(K)]
        for x, cls in zip(X, y):
            xi = x + [1.0]
            scores = [sum(w*d for w, d in zip(W[k], xi)) for k in range(K)]
            m = max(scores); ex = [pow(2.718281828, s-m) for s in scores]
            Z = sum(ex)
            for k in range(K):
                pk = ex[k]/Z
                tk = 1.0 if k == cls else 0.0
                for d in range(D):
                    g[k][d] += (pk - tk) * xi[d]
        for k in range(K):
            for d in range(D):
                W[k][d] -= lr * g[k][d] / len(X)
    return W

def student_read(W, x):
    xi = x + [1.0]
    scores = [sum(w*d for w, d in zip(W[k], xi)) for k in range(8)]
    return CLASSES[scores.index(max(scores))]

def make_set(sky, n, p, rng):
    X, y = [], []
    for i in range(n):
        c = CLASSES[i % 8]
        X.append(features(storm(SHAPES[c], sky, p, rng)))
        y.append(CLASSES.index(c))
    return X, y

if __name__ == "__main__":
    P = 0.20
    results = {}
    for train_sky in ["down", "sym", "up", "MIX"]:
        rng = random.Random(1337)
        if train_sky == "MIX":
            X, y = [], []
            for sky in ["down", "sym", "up"]:
                a, b = make_set(sky, 1500, P, rng)
                X += a; y += b
        else:
            X, y = make_set(train_sky, 4500, P, rng)
        W = student_train(X, y)
        row = []
        for test_sky in ["down", "sym", "up"]:
            rng2 = random.Random(999)
            Xa, ya = make_set(test_sky, 800, P, rng2)
            acc = sum(student_read(W, x) == CLASSES[t] for x, t in zip(Xa, ya)) / len(ya)
            row.append(acc)
        results[train_sky] = row

    print(f"train\\test   down   sym    up   (p={P}, 56-param student, 4500 train)")
    for k, v in results.items():
        print(f"{k:>5}      " + "  ".join(f"{a:.3f}" for a in v))
