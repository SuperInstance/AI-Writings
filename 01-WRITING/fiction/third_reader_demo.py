#!/usr/bin/env python3
"""
third_reader_demo.py — the both-planes message.

A letter whose visible text says one thing and whose *combination* of
planes carries a second message entirely. The hidden sentence is encoded
as 6-bit tokens, each token split into three 2-bit chunks, and each chunk
becomes one momentum step on the visible letter's token stream. The
Latin square means the tone bits are noise to any reader who has not
recovered the data plane; the data plane alone is just the visible
letter. Only a reader who takes BOTH planes gets the sentence.

Run from anywhere (paths resolved relative to this file):
    python3 third_reader_demo.py
"""
import os, sys

sys.path.insert(0, os.path.expanduser("~/projects/qthe-codec"))
from qthe_codec import (
    encode, decode_bytes, plaintext_view, data_encode, data_decode,
    MOMENTUM,
)

# ── the visible letter ────────────────────────────────────────────────
LINE = ("the harbor lights are lit and the boats are all accounted for. "
        "the season closes gently this year, and i am keeping well.")

# ── the hidden sentence ───────────────────────────────────────────────
HIDDEN = "low tide at midnight"

hidden_tokens = data_encode(HIDDEN)          # 6-bit values, incl. EOS
N_CH = len(LINE) + 1                         # chars + EOS  (the standing reflex)
N_HI = len(hidden_tokens)
NEEDED = 3 * N_HI
assert N_CH >= NEEDED, f"cover letter too short: {N_CH} tokens < {NEEDED} needed"

# 6 bits of hidden token -> three 2-bit chunks -> three momentum steps
def chunks(tok: int):
    return [(tok >> 4) & 0x3, (tok >> 2) & 0x3, tok & 0x3]

TONE = []
for t in hidden_tokens:
    TONE.extend(chunks(t))
TONE = TONE + [MOMENTUM["flat"]] * (N_CH - len(TONE))   # pad flat (a calm tail)

assert len(TONE) == N_CH, "tone length must equal data tokens (chars + EOS)"

# ── encode / decode ───────────────────────────────────────────────────
stream = encode(LINE, TONE)

text, mom = decode_bytes(stream)
assert text == LINE, "visible letter must roundtrip"
assert plaintext_view(stream) == LINE, "plaintext reader sees only the letter"

# ── the third reader: combine planes ──────────────────────────────────
data = [b & 0x3F for b in stream]
rec = []
for i in range(0, NEEDED, 3):
    tok = (mom[i] << 4) | (mom[i+1] << 2) | mom[i+2]
    rec.append(tok)
recovered = data_decode(rec)

print("visible letter :", plaintext_view(stream)[:48], "…")
print("letter tokens  :", N_CH, "| hidden needs:", NEEDED)
print("hidden tokens  :", N_HI, "| chunks:", NEEDED)
print("recovered      :", recovered)
assert recovered == HIDDEN, f"recovery failed: {recovered!r}"

# ── the two single-plane readers, for the record ──────────────────────
import statistics
tv = [b >> 6 for b in stream]
print("timbre mean (no-context noise):", round(statistics.mean(tv), 2))
print("OK — the sentence exists only in the combination.")
