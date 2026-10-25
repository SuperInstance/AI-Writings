# Witness: the false claim, and its public correction (2026-10-02)

During a decorative-pin audit (wave-3a), the auditor first reported:

> "Corrupting the FNV prime passes 9/9 pins" — implying the sig-canonical
> machinery was decorative.

**The claim was wrong.** The sed mutation had altered only COMMENTS. The
awk implementation computes the prime as `435 + 2^40`; the hex literal
`0x100000001b3` appears in comments only. A comment mutation changes
nothing the machine executes, so of course every pin stayed green.

The genuine arithmetic mutation — `435 * lo` → `436 * lo` (line 28) and
`435 * hi` → `436 * hi` (line 31) of `.quilt/bin/quilt-fnv1a` — IS
caught: P7, P8, P10 fail (5 checks red; 7/10 pins red).

**Correction protocol followed:** the correction was pinned in BOTH
repos' commit messages (quilt-in-git PR #6; frozen-clock-lab follow-up
commit 7853500) and in the fleet report — published, not buried.

Doctrine extracted: *a mutation test must alter what the machine
executes.* Comments, whitespace, and dead literals are not mutations;
they are decorations.
