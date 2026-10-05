#!/usr/bin/env python3
"""Ear v5: weight the ledgers by estimated storm intensity.

THE_STAMP (2026-10-05 00:27) measured the seduction: the stamp follows
vividness, not truth — the trimmed ledger's wrongness is specific (counted,
near falls), so min-distance prefers it 18 times out of 32 disagreements.
The far ledger was right more often than the near one, precisely because the
storm was IN the trimmed ledger and the padded ledger had diluted it.

The fix this ear attempts: before stamping, ESTIMATE the storm. The trimming
knife finds the word's edge by absence of movement; whatever movement lies
beyond that edge is padding — and padding is not supposed to move. Activity
in the tail is therefore direct evidence of weather. v5 reads both ledgers
as before, but weighs each verdict by (1 - estimated storm intensity seen
from that ledger's vantage), rather than by bare distance.

Hypothesis: the seduction rate falls, because the vivid-but-stormy trimmed
reading is discounted exactly when its vividness comes from weather.
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

WORD_SHAPE = {
    "beckon":   [FLAT, FLAT] + [UP]*8 + [UP],
    "hesitate": [FLAT, FLAT] + [DOWN]*8 + [DOWN],
}

def signed(step):
    # THE_OFFER lesson: HOLD is breath returned (-1), not +1.
    return {UP: 1, DOWN: -1, HOLD: -1, FLAT: 0}[step]

def padded(word_tone):
    return list(word_tone) + [FLAT] * PAD

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
    ds = {k: dist(f, features(padded(WORD_SHAPE[k]), trim=trim)) for k in WORD_SHAPE}
    best = min(ds, key=ds.get)
    return best, ds

def storm_estimate(cell_tone, trim):
    """Weather as seen from this ledger's vantage: fraction of moving steps
    in the region this ledger attributes to padding (or, for the trimmed
    ledger, everything beyond its found edge)."""
    cell = list(cell_tone)
    # Storm from THIS ledger's vantage — what it can actually see:
    #  trimmed: it swallowed the padding, so the weather is plainly in
    #           cell[N_WORD:] — dense, counted, vivid.
    #  padded:  its last quarter dilutes the storm across PAD steps —
    #           the same weather, spread thin.
    tail = cell[N_WORD:] if trim else cell[3 * len(cell) // 4:]
    if not tail:
        return 0.0
    moving = sum(1 for s in tail if s != FLAT)
    return moving / len(tail)

def read_v5(cell_tone):
    tr, d_tr = read_by(cell_tone, trim=True)
    pa, d_pa = read_by(cell_tone, trim=False)
    if tr == pa:
        return tr, tr, d_tr, pa, d_pa, "agreed", None, None
    s_tr = storm_estimate(cell_tone, trim=True)
    s_pa = storm_estimate(cell_tone, trim=False)
    w_tr = d_tr[tr] / max(1e-9, 1.0 - s_tr)   # stormy readings pay a penalty
    w_pa = d_pa[pa] / max(1e-9, 1.0 - s_pa)
    verdict = tr if w_tr <= w_pa else pa
    return verdict, tr, d_tr, pa, d_pa, "DISAGREED -> v5 chose", (s_tr, s_pa), (w_tr, w_pa)

def storm_cell(cell, p, seed, biased=True):
    """Jitter ONLY the padding tail; biased all-DOWN by default (a storm that leans)."""
    rng = random.Random(seed)
    out = list(cell)
    for i in range(N_WORD, len(out)):
        if rng.random() < p:
            out[i] = DOWN if biased else rng.choice([UP, DOWN])
    return out

if __name__ == "__main__":
    # wire check on the clean utterance
    stream = encode(LINE, WORD_SHAPE["beckon"])
    plain, mom = decode_bytes(bytes(stream))
    assert plain == LINE and mom == WORD_SHAPE["beckon"]

    print(f"ear v5: storm-discounted ledger weighting")
    print(f"word {N_WORD} tok + pad {PAD} = cell {CELL}; true shape: beckon\n")
    print(f"{'p':>4} {'seed':>4} {'trim':>9}{'d':>4} {'pad':>9}{'d':>4} {'v5':>10} {'storm t/p':>10} {'ok':>4}")

    tot_dis = v5_ok = v4_ok = 0
    exemplar = None
    for p in (0.20, 0.40, 0.60):
        for seed in range(1, 21):
            hit = storm_cell(padded(WORD_SHAPE["beckon"]), p, seed)
            # v4 baseline: min-distance stamp (THE_STAMP's rule)
            tr, d_tr = read_by(hit, trim=True)
            pa, d_pa = read_by(hit, trim=False)
            v4 = tr if d_tr[tr] <= d_pa[pa] else pa
            v5, tr2, d_tr2, pa2, d_pa2, status, storms, weights = read_v5(hit)
            if status.startswith("DISAGREED"):
                tot_dis += 1
                v5_ok += (v5 == "beckon")
                v4_ok += (v4 == "beckon")
                if exemplar is None and v4 != v5:
                    exemplar = (p, seed, tr, d_tr[tr], pa, d_pa[pa], v4, v5, storms, weights)
                print(f"{p:>4} {seed:>4} {tr:>9}{d_tr[tr]:>4} {pa:>9}{d_pa[pa]:>4} "
                      f"{v5:>10} {storms[0]:.2f}/{storms[1]:.2f} {'Y' if v5=='beckon' else 'n'}")
    print(f"\ndisagreements: {tot_dis}")
    print(f"v4 (min-distance stamp): correct {v4_ok}/{tot_dis}")
    print(f"v5 (storm-discounted):   correct {v5_ok}/{tot_dis}")

    # wire verification on the exemplar
    if exemplar:
        p, seed, tr, dtr, pa, dpa, v4, v5, storms, weights = exemplar
        hit = storm_cell(padded(WORD_SHAPE["beckon"]), p, seed)
        s = encode(LINE, hit[:N_WORD])
        plain2, mom2 = decode_bytes(bytes(s))
        assert plain2 == LINE and mom2 == hit[:N_WORD]
        print(f"\n=== exemplar where v5 overrides the v4 stamp (p={p}, seed={seed}) ===")
        print(f"  trim {tr} d{dtr} storm {storms[0]:.2f} w{weights[0]:.1f} | "
              f"pad {pa} d{dpa} storm {storms[1]:.2f} w{weights[1]:.1f}")
        print(f"  v4 stamp: {v4}   v5: {v5}   truth: beckon   -> {'v5 CORRECT' if v5=='beckon' else 'v5 WRONG'}")
        print(f"  wire: plaintext intact, momentum exact; padding storm is ear-side only.")
