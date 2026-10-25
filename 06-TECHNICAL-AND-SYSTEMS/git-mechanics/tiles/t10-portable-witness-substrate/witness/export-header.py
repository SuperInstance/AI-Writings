"""Selective-disclosure export + root hash.

Motivation (edge-watch 10/2): arXiv 2605.11032-style portable agent memory
and the MajorLabs finding (0/6 production memory systems sign memory) both
point the same way — a ledger you can show a slice of, with the slice
carrying its own integrity proof, and a root you can sign.

Honest boundary, stated up front: an export proves the included entries are
byte-intact. It does NOT prove the filter was complete — selective disclosure
hides by construction. Completeness is the verifier's question, not ours.
"""
# --- excerpt provenance: doubt-ledger ledger/export.py @ poc 549c395 ---
# (PR #3, merged 2026-10-02; docstring + key definitions)
import json
import time

GENESIS = "0" * 16  # anchored root of the empty ledger

def chain_root(lines):
    """fnv1a-64 chain over per-line checksums, genesis-anchored.

    Returns (root_hex, tip_binding). The tip binding recomputes against the
    LIVE ledger tip so a stale export cannot present itself as current.
    """

def verify_export(path, expected_tip=None):
    """Recompute the chain from GENESIS. Raises ValueError naming the line on any tamper."""
    # ... raises ValueError(f"export tampered at line {i}" ...) on any drift
