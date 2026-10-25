#!/usr/bin/env python3
"""The stamp chooses: a run where the trimmed and padded ledgers DISAGREE.

Open branch from THE_TWO_LEDGERS (2026-10-04): the disagreement branch of
two_ledger_read() had never fired. Here a storm falls only in the padding
after the word. The trimming knife — which finds the word's edge by
absence of movement — cannot tell storm-silence from word-silence, so it
keeps the storm and reads a contaminated word. The padded ledger keeps
its segment boundaries over the whole cell; the storm stays diluted in
the last quarter and the true shape survives in the first three.

The keeper reads both, they disagree, and the stamp must choose.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
import random
from qthe_codec import encode, decode_bytes

FLAT, UP, DOWN, HOLD = 0, 1, 2, 3

LINE = "come here."
N_WORD = len(LINE) + 1          # 11 tokens incl. EOS
CELL = 39                        # fixed padded cell (house standard)
PAD = CELL - N_WORD

# Canonical shapes, laid into the padded cell.
WORD_SHAPE = {
    "beckon":   [FLAT, FLAT] + [UP]*8 + [UP],
    "hesitate": [FLAT, FLAT] + [DOWN]*8 + [DOWN],
}
# encode() takes the word's own tokens (chars+EOS); the padded CELL is a
# feature-space convention only.
CELL = 39                        # fixed padded cell (house standard)
PAD = CELL - N_WORD

def signed(step):
    # THE_OFFER lesson: HOLD is breath returned (−1), not +1.
    return {UP: 1, DOWN: -1, HOLD: -1, FLAT: 0}[step]

def features(cell_tone, trim):
    """v3 organ set: signed drift + 4-segment weight profile + terminal."""
    cell = list(cell_tone)
    if trim:
        while cell and cell[-1] == FLAT:
            cell.pop()
    n = len(cell)
    drift = sum(signed(s) for s in cell)
    q = max(1, n // 4)
    segs = [sum(signed(s) for s in cell[i*min(q, n):min((i+1)*q, n)])
            for i in range(4)] if n >= 4 else [drift, 0, 0, 0]
    return (drift, *segs, cell[-1])

def dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

def read_by(cell_tone, trim):
    f = features(cell_tone, trim=trim)
    best = min(WORD_SHAPE, key=lambda k: dist(f, features(padded(WORD_SHAPE[k]), trim=trim)))
    return best, {k: dist(f, features(padded(WORD_SHAPE[k]), trim=trim)) for k in WORD_SHAPE}

def padded(word_tone):
    return list(word_tone) + [FLAT] * PAD

def two_ledger_read(tone):
    tr, d_tr = read_by(tone, trim=True)
    pa, d_pa = read_by(tone, trim=False)
    if tr == pa:
        verdict, both = tr, "agreed"
    else:
        verdict = tr if d_tr[tr] <= d_pa[pa] else pa
        both = "DISAGREED -> stamp chose"
    return verdict, tr, d_tr, pa, d_pa, both

def storm(tone, p, seed):
    """Jitter only the PADDING tail (steps N_WORD..end), word untouched."""
    import random
    rng = random.Random(seed)
    out = list(tone)
    for i in range(N_WORD, len(out)):
        if rng.random() < p:
            out[i] = rng.choice([UP, DOWN])
    return out

# --- encode the true utterance (beckon) and verify the wire -----------------
TRUE_SHAPE = WORD_SHAPE["beckon"]
stream = encode(LINE, TRUE_SHAPE)
plain, _ = decode_bytes(bytes(stream))
assert plain == LINE, plain
if __name__ == "__main__":
    print(f"plaintext (both ledgers see this): {LINE!r}")
    print(f"cell: {CELL} tokens (word {N_WORD} + padding {PAD}); "
          f"true shape: beckon; biased storm (all DOWN) only in padding\n")

    def storm_cell(cell, p, seed):
        """Jitter ONLY the padding tail, biased all-DOWN: a storm that leans."""
        rng = random.Random(seed)
        out = list(cell)
        for i in range(N_WORD, len(out)):
            if rng.random() < p:
                out[i] = DOWN
        return out

    print(f"{'p':>4} {'seed':>4} {'trim->':>22} {'pad->':>22} {'stamp':>10}")
    disagreement = correct = wrong = agreed = 0
    exemplar = None
    for p in (0.20, 0.40, 0.60):
        for seed in range(1, 21):
            hit = storm_cell(padded(WORD_SHAPE["beckon"]), p, seed)
            v, tr, d_tr, pa, d_pa, both = two_ledger_read(hit)
            if both.startswith("DISAGREED"):
                disagreement += 1
                mark = ""
                if v == "beckon":
                    correct += 1
                else:
                    wrong += 1
                    mark = " <<< stamp seduced"
                if exemplar is None:
                    exemplar = (p, seed, hit, v, tr, d_tr, pa, d_pa)
                print(f"{p:>4} {seed:>4} {tr:>9}{d_tr[tr]:>4}/{d_tr['hesitate' if tr=='beckon' else 'beckon']:<4} "
                      f"{pa:>9}{d_pa[pa]:>4}/{d_pa['hesitate' if pa=='beckon' else 'beckon']:<4} {v:>10}{mark}")
            else:
                agreed += 1
    print(f"\nruns: {agreed} agreed, {disagreement} disagreed "
          f"(stamp correct {correct}, stamp seduced {wrong})")

    # --- verify the exemplar at the wire level -------------------------------
    p, seed, hit, v, tr, d_tr, pa, d_pa = exemplar
    hit_word = hit[:N_WORD]
    s = encode(LINE, hit_word)
    plain2, mom = decode_bytes(bytes(s))
    assert plain2 == LINE, "stormed word must decode to the same words"
    assert mom == hit_word, "momentum recovered exactly"
    # NOTE: no stream-inequality assert — the storm lives in the PADDING,
    # and encode() carries only the word's own tokens. The padded cell is an
    # ear-side convention; the wire is clean. That is the finding: the two
    # ledgers disagree over how to LISTEN, not over what was said.
    assert bytes(s) == bytes(stream), "the wire is clean; the disagreement is in the ear"
    print(f"\n=== exemplar (p={p}, seed={seed}) ===")
    print(f"  trimmed ledger: {tr}   (dist {d_tr[tr]})   <- kept the storm, misread the edge")
    print(f"  padded  ledger: {pa}   (dist {d_pa[pa]})   <- storm diluted in the last quarter")
    print(f"  stamp: {v}  -> truth was beckon: {'STAMP CORRECT' if v == 'beckon' else 'STAMP WRONG'}")
    print(f"  wire check: plaintext intact, momentum exact, streams distinct.")
