"""Optional Ed25519 root signing.

Dependency: `cryptography` (pip). The ledger core stays stdlib-only; signing
is a separate layer so verification never requires the signing dependency.
A verifier with the public key checks the tip root; a verifier without it
still has the genesis-anchored chain (export.py).
"""
# --- excerpt provenance: doubt-ledger ledger/sign.py @ poc 549c395 ---
# (PR #3, merged 2026-10-02; header + key handling)
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey)

def sign_tip(root_hex, priv_path, pub_out):
    """Sign the tip root. The signature covers the ROOT, not individual
    entries — the chain proves the entries; the signature proves the root."""

def verify_tip(root_hex, sig_path, pub_path):
    """Raise ValueError unless the signature matches this exact root."""
    # ... if not isinstance(pub, Ed25519PublicKey): raise ValueError(...)
