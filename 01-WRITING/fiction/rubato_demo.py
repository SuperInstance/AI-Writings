#!/usr/bin/env python3
"""RUBATO: performed variants of the 8 canonical shapes.

EIGHT_REFLEXES tested noise (random step substitution). But a human performer
isn't noise: they RUBATO. They hold a step too long, hurry another, soften a
peak. Rubato is structured temporal jitter — it destroys *where* things happen
in the trajectory, not *what* happens. This demo asks: does the nearest-shape
classifier survive performance, the way it survived weather?

Canonical shapes and drift features reuse EIGHT_REFLEXES' vocabulary.
FLAT=0, UP=1, HOLD=2, DOWN=3; drift is signed (UP +1, DOWN -1, HOLD 0).
"""
import random
import sys

FLAT, UP, HOLD, DOWN = 0, 1, 2, 3
NAMES = ["advance", "withdraw", "yield", "hold", "probe", "pause", "feint", "beckon"]

def run(shape, n):
    k = shape.count(UP) - shape.count(DOWN)
    return [shape[0]] + [shape[-1]] * (n - 2) if False else shape[:]

def canon(name):
    """8 named per-segment runs, 24 steps each (as in eight_reflexes_corpus)."""
    seg = {
        #  (lead run, tail run)          drift sign
        "advance":  [UP]*12 + [UP]*12,    # +24
        "withdraw": [DOWN]*12 + [DOWN]*12,# -24
        "yield":    [DOWN]*8 + [FLAT]*16, # -8 then rest
        "hold":     [FLAT]*24,
        "probe":    [UP]*4 + [DOWN]*4 + [FLAT]*16,  # out and back
        "pause":    [FLAT]*12 + [HOLD]*6 + [FLAT]*6,
        "feint":    [UP]*4 + [DOWN]*8 + [UP]*4 + [FLAT]*8,  # false rise, deeper fall, recover
        "beckon":   [UP]*10 + [HOLD]*8 + [UP]*6,  # climb, hold taut, climb
    }
    return seg[name]

def signed_drift(s):
    return s.count(UP) - s.count(DOWN)

def feature(s, k=4):
    """4-segment signed drift profile (same as corpus demo)."""
    seg = len(s) // k
    return [signed_drift(s[i*seg:(i+1)*seg]) for i in range(k)]

def rubato(s, rng, p_hold=0.15, p_hurry=0.15):
    """Perform s: HOLD steps stand in for 'held longer', duplicated steps for 'hurried'.
    Crucially, RUNS of same-step are locally re-tempoed but the run's total
    signed drift is preserved *in aggregate* by redistributing within the run."""
    out = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        runlen = j - i
        if runlen > 2:
            n_hold = int(runlen * p_hold)
            idxs = rng.sample(range(runlen), n_hold)
            idxs = set(idxs)
            for t in range(runlen):
                if t in idxs:
                    out.append(HOLD if s[i] == UP or s[i] == DOWN else s[i])
                    # a held expressive step: direction spent here becomes stillness
                else:
                    out.append(s[i])
        else:
            out.extend(s[i:j])
        i = j
    return out

def softpeak(s, rng):
    """Softened peaks: some UP/DOWN steps rendered as HOLD — magnitude loss
    (the fold villain's loss, but honest: the performer chose it)."""
    return [HOLD if (st in (UP, DOWN) and rng.random() < 0.20) else st for st in s]

def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

# ---------------------------------------------------------------- ear v2
# The fold clerk's law as a blind spot: signed drift cannot tell pause
# (marked silence, HOLD steps) from hold (bare silence, FLAT throughout).
# Both have zero drift. The fix is a second organ: a stillness-count that
# hears WHICH KIND of stillness, not just how much.
def feature2(s, k=4):
    """drift profile + one extra dimension: count of HOLD steps."""
    return feature(s, k) + [s.count(HOLD)]

def main():
    rng = random.Random(4242)
    names = NAMES
    canon_t = {n: canon(n) for n in names}
    canon_f = {n: feature(canon_t[n]) for n in names}

    # Performed corpus: each class performs 40 utterances
    per = 40
    correct = 0
    total = 0
    confusions = {}
    for n in names:
        for _ in range(per):
            perf = softpeak(rubato(canon_t[n], rng), rng)
            # normalize length back to 24 (rubato can pad): deterministic downsample
            while len(perf) > 24:
                perf.pop(rng.randrange(len(perf)))
            while len(perf) < 24:
                perf.append(FLAT)
            f = feature(perf)
            pred = min(names, key=lambda c: dist(f, canon_f[c]))
            total += 1
            if pred == n:
                correct += 1
            else:
                confusions[(n, pred)] = confusions.get((n, pred), 0) + 1

    print(f"performed corpus: {total} utterances, 8 classes, expressive jitter (rubato + softened peaks)")
    print(f"ear v1 (drift only) accuracy:    {correct}/{total} = {correct/total:.3f}")
    if confusions:
        top = sorted(confusions.items(), key=lambda kv: -kv[1])[:5]
        print("  top confusions (truth, heard):", top)

    # ear v2: drift profile + stillness-count
    canon_f2 = {n: feature2(canon_t[n]) for n in names}
    correct2 = 0
    confusions2 = {}
    rng2 = random.Random(4242)
    for n in names:
        for _ in range(per):
            perf = softpeak(rubato(canon_t[n], rng2), rng2)
            while len(perf) > 24:
                perf.pop(rng2.randrange(len(perf)))
            while len(perf) < 24:
                perf.append(FLAT)
            f = feature2(perf)
            pred = min(names, key=lambda c: dist(f, canon_f2[c]))
            if pred == n:
                correct2 += 1
            else:
                confusions2[(n, pred)] = confusions2.get((n, pred), 0) + 1
    print(f"ear v2 (drift + stillness-count) accuracy: {correct2}/{total} = {correct2/total:.3f}")
    if confusions2:
        top2 = sorted(confusions2.items(), key=lambda kv: -kv[1])[:5]
        print("  top confusions v2:", top2)

    print(f"(plaintext reader baseline from prior run: 0.115 — coin)")

if __name__ == "__main__":
    sys.exit(main())
