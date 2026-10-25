# 9c memo excerpt — the steal that became doctrine
# Provenance: docs/RESEARCH-AGENT-NATIVE-VCS.md @ quilt-in-git branch
# research/agent-native-vcs — PR #10 (OPEN as of 2026-10-02; flip scheduled
# on merge; excerpt is evidence-of-existence per the t06 precedent).

From §2.3 (steal 2), on pijul's line-graph vs our receipt chain:

> 2. *Version id must be non-linear*: our fnv1a-64 receipt chain is
>    order-sensitive and genesis-anchored *on purpose* — a receipt log wants
>    to detect reordering. But any NAME we hand to the outside world (a
>    cell's advertised position, a course's tile id) must be a non-linear
>    function of its change hashes, or it fragments the moment a peer
>    cherry-picks and re-names.

From §7 (synthesis table):

> | Pijul (§2) | Change identity survives context; version ids ≠ log order |
>   **Adopt as doctrine**: receipt chain stays order-sensitive; any future
>   version NAME must be non-linear — already sealed in §2.3 steal 2 |

> 3. **Version names must be non-linear; the receipt chain stays
>    order-sensitive by design** (§2) — this is already doctrine after §2's
>    analysis, recorded here so the synthesis cannot quietly regress it.
