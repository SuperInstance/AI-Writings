"""Fixture capabilities for the metabolizer selftest. Pure functions over text -> slug.

slug_v1   the grown capability. QUIRK: only the literal space is a separator, so a tab silently
          glues words together — invisible in a tab-free log, caught at run time by the gate's
          collapse_ws invariance probe.
slug_alt  a different implementation with byte-identical products to slug_v1, but metered (costlier).
slug_and  disagrees with slug_v1 on '&' (spells it "and").
slug_v2   the DRIFTED slug_v1: stopped lower-casing (upper-case letters now fall out of the slug).
"""
import re
from quilt_kernel import budget

_DROP = re.compile(r"[^a-z0-9 ]")


def _core(s):
    return "-".join(t for t in _DROP.sub("", s).split(" ") if t)


def slug_v1(s):
    return _core(s.lower())


def slug_alt(s):
    out, run = [], []
    for ch in s.lower():
        if ch == " ":
            if run:
                out.append("".join(run)); run = []
        elif ch.isascii() and (ch.isalnum()):
            run.append(ch)
    if run:
        out.append("".join(run))
    return "-".join(out)


def slug_and(s):
    return _core(s.lower().replace("&", " and "))


def slug_v2(s):
    return _core(s)


TIER_CHEAP = budget(wall_ms=2, usd=0.0, tokens={"api": 0})
TIER_MID = budget(wall_ms=3, usd=0.0, tokens={"api": 0})
TIER_METERED = budget(wall_ms=9, usd=0.0004, tokens={"api": 120})
