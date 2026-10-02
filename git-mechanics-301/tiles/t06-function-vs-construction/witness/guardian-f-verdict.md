# Witness: guardian lane F' verdict on frozen-clock-lab PR #3 (2026-10-02)

Verbatim from the guardian's delivered report (/tmp/guardian-f.md):

> The lab's core doctrine survives every clock fault thrown at it — order
> really does live in the chain. But the sig-canonical pin (PR #2) pinned
> the *function* and left the *construction* unpinned: two trivial
> substitutions passed everything. That is now closed by PR #3.

The two passing substitutions (demonstrated RED for P6b):
1. Changing the hash separator/casing while preserving identical output.
2. Re-expressing the constant in an equivalent-but-different construction.

Red/green evidence shipped in PR #3: clean tree P1–P6b PASS; separator
mutation → FAIL P6b; hex-case mutation → FAIL P6b; prime mutation →
FAIL P6 + P6b.
