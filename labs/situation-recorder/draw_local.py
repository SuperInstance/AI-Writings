#!/usr/bin/env python3
"""draw_local.py — un-gameable-shaped DRAW values from MicroMoth-quilt, no network.

When the Moth QRNG API is rate-limited, balance-gated, or CF-blocked, a captain
still needs `DRAW` records. This bridge gets them from a LOCAL MicroMoth-quilt
circuit (github.com/SuperInstance/MicroMoth-quilt) — pure Python, no keys, no
network — and seals each draw as a collapse-ledger receipt (tamper-evident,
replayable). Feed the (value, receipt) straight into recorder.Situation.draw().

HONESTY (this matters — it keeps the corpus clean): MicroMoth-quilt is a
SIMULATOR. A seeded draw is quantum-STRUCTURED and REPLAYABLE with a hash-chained
receipt, but it is NOT a hardware QRNG and carries no Bell-S. So the provenance is
"micromoth-quilt/simulated (replayable, not hardware)". Use it as forced,
un-steerable-by-the-crew, reproducible exploration in-environment; reach for the
real Moth QRNG when you need hardware un-gameability. Never launder one as the other.

Locate MicroMoth-quilt via $MICROMOTH_QUILT (a clone path), else a sibling
../MicroMoth-quilt. Run directly for a self-demo:

    MICROMOTH_QUILT=/path/to/MicroMoth-quilt python3 draw_local.py
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path


def _locate_micromoth() -> Path:
    cand = []
    env = os.environ.get("MICROMOTH_QUILT")
    if env:
        cand.append(Path(env))
    here = Path(__file__).resolve()
    cand += [here.parent.parent.parent.parent / "MicroMoth-quilt",  # sibling of the ai-writings clone
             Path("/tmp/mmq")]
    for p in cand:
        if (p / "micromoth.py").exists():
            return p
    raise FileNotFoundError(
        "MicroMoth-quilt not found. Set $MICROMOTH_QUILT to a clone of "
        "github.com/SuperInstance/MicroMoth-quilt (looked in: %s)"
        % ", ".join(str(c) for c in cand))


def draw_int(min_v: int, max_v: int, seed: int = 0, qubits: int = 4, shots: int = 256,
             path: str | None = None) -> tuple[int, dict]:
    """Draw an integer in [min_v, max_v) from a local MicroMoth-quilt circuit.

    Circuit: `qubits` independent Hadamard coins (each qubit in equal
    superposition, measured) — the standard unbiased bit source. Seeded so the
    collapse receipt is SEALED and re-executable. The integer is rejection-sampled
    from the measured bitstream so it is uniform over [min_v, max_v). Returns
    (value, receipt) where receipt carries the collapse-ledger id + a balance stat
    (fraction of 1s ≈ 0.5 is the honest 'is the source fair' evidence, the local
    analogue of Moth's Bell-S) + honest provenance.
    """
    if max_v <= min_v:
        raise ValueError("max_v must exceed min_v")
    mm = _locate_micromoth() if path is None else Path(path)
    sys.path.insert(0, str(mm))
    sys.path.insert(0, str(mm / "tools"))
    import micromoth  # noqa: E402
    from collapse_ledger import collapse_receipt, verify  # noqa: E402

    qc = micromoth.QuantumCircuit(qubits, qubits)
    for q in range(qubits):
        qc.h(q)
    for q in range(qubits):
        qc.measure(q, q)

    receipt = collapse_receipt(qc, shots=shots, seed=seed)
    chk = verify(receipt, qc)
    if not chk.get("ok"):
        raise RuntimeError("collapse receipt failed self-verify: %s" % chk.get("why"))

    # Flatten the measured shots into one bitstream (strip spaces micromoth may insert).
    bits = "".join(str(o).replace(" ", "") for o in receipt["outcomes"])
    ones = sum(1 for b in bits if b == "1")
    balance = round(ones / len(bits), 4) if bits else None

    span = max_v - min_v
    width = max(1, math.ceil(math.log2(span)))
    value = None
    for i in range(0, len(bits) - width + 1, width):  # rejection sampling → uniform
        n = int(bits[i:i + width], 2)
        if n < span:
            value = min_v + n
            break
    if value is None:  # astronomically unlikely with these defaults
        raise RuntimeError("bitstream exhausted before an in-range draw; raise shots")

    last_cell = receipt["cells"][-1]["id"]
    summary = {
        "source": "micromoth-quilt/simulated (replayable, not hardware)",
        "collapse_ledger": last_cell,          # the sealed receipt id (chain head of the collapse EFFECTs)
        "dialect": receipt["dialect"],
        "sealed": receipt["sealed"],
        "seed": seed,
        "circuit": "%dxH+measure" % qubits,
        "shots": shots,
        "balance": balance,                     # ≈0.5 ⇒ unbiased; the local 'fair source' evidence
        "range": [min_v, max_v],
    }
    return value, summary


def main() -> int:
    v, r = draw_int(0, 10, seed=42)
    print("drew %d in [0,10)" % v)
    print("receipt:", r)
    assert r["sealed"] is True, "seeded draw must be sealed/replayable"
    v2, _ = draw_int(0, 10, seed=42)
    assert v == v2, "sealed draw must be reproducible under the same seed"
    print("reproducible under seed 42 ✓  (balance %.3f — ≈0.5 is fair)" % r["balance"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
