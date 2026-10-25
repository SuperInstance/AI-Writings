#!/usr/bin/env python3
"""THE TWO LEDGERS — seam advanced 2026-10-04 (16:27 AKDT).

Follows tuned_padding_demo's hybrid ear. New question: what does the ear
DO when its two ledgers disagree? Answer in this demo: it files both
readings, names which one it trusts and why, and — the piece's point —
keeps the other ledger on the page instead of erasing it. Trust as a
stamp on a kept doubt, not a replacement of it.

Also the first demo whose input is a full PASSAGE (two sentences, one
Newline token) rather than a single utterance — the chars+EOS rule now
includes a NEWLINE (62) in the token count.
"""
import sys
sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes, plaintext_view

DOWN, FLAT, UP, HOLD = 0, 1, 2, 3

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

def features(mom):
    return (signed_drift(mom),) + tuple(weight_profile(mom)) + (terminal(mom),)

def dist(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def trim(mom):
    end = len(mom)
    while end > 1 and mom[end-1] == FLAT:
        end -= 1
    return mom[:end]

# canonical shapes (features precomputed on unpadded canonical runs)
def shape_advance(n): return [FLAT, FLAT] + [UP]*(n-3) + [UP]
def shape_withdraw(n): return [FLAT, FLAT] + [DOWN]*(n-3) + [DOWN]
def shape_pause(n): return [FLAT]*(n-1) + [FLAT]
def shape_beckon(n): return [FLAT] + [UP]*(n//2) + [HOLD] + [UP]*(n - 2 - n//2)

CANON = {
    "advance":  shape_advance(12),
    "withdraw": shape_withdraw(12),
    "pause":    shape_pause(12),
    "beckon":   shape_beckon(12),
}
CANON_FEAT = {k: features(v) for k, v in CANON.items()}

# ── the hybrid read: two ledgers, trust the nearer one, keep both ─────────
def two_ledger_read(mom):
    ft, fp = features(trim(mom)), features(mom)
    dt = min((dist(ft, f), k) for k, f in CANON_FEAT.items())
    dp = min((dist(fp, f), k) for k, f in CANON_FEAT.items())
    trusted = dt[1] if dt[0] <= dp[0] else dp[1]
    return {"trimmed": dt, "padded": dp, "trusted": trusted}

# ── the passage: 43 chars -> 44 tokens (chars + Newline + EOS) ────────────
PASSAGE = "the harbor holds its breath.\nthen it moves."
N = len(PASSAGE) + 1  # chars + Newline + EOS
# storm jitter applied by hand: mid-passage scatter, calm tail (the tail IS
# the padding after the word — the trim ledger will find the edge)
import random
rng = random.Random(7)
def storm(tone, p, tail_flat=8):
    head = [rng.choice([FLAT, UP, DOWN, HOLD]) if rng.random() < p else s for s in tone[:-tail_flat]]
    return head + tone[-tail_flat:]

# utterance inside the passage: "advance" climb on *it moves*, trailing calm
TONE = [FLAT]*24            # "the harbor holds its…"
TONE += [HOLD]*4            # "…breath." — the breath, held (28)
TONE += [FLAT]*6            # newline + "then " (34)
TONE += [UP]*9              # "it moves." — the climb (43)
TONE += [FLAT]*1            # the calm after the word (44)
assert len(TONE) == N, (len(TONE), N)

stream = encode(PASSAGE, storm(TONE, 0.20, tail_flat=2))
text, mom = decode_bytes(stream)
assert plaintext_view(stream) == PASSAGE

r = two_ledger_read(mom)
print("passage      :", repr(text))
print("plaintext    : intact" if plaintext_view(stream) == PASSAGE else "BROKEN")
print("trimmed lgr  : says %s (dist %d)" % (r["trimmed"][1], r["trimmed"][0]))
print("padded  lgr  : says %s (dist %d)" % (r["padded"][1], r["padded"][0]))
print("trusted      : %s  — stamped, not the other erased" % r["trusted"])
