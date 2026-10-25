#!/usr/bin/env python3
"""Post-run verification gate for the Civilization Orchestrator.

Why this exists
---------------
The orchestrator fails **silently** in several distinct ways, and a green exit code
does not distinguish any of them from success:

  * provider token absent  -> `call_provider` returns None -> no rows written
  * `cp` into a quota-dead workspace -> 0-byte `simulations.jsonl` files that
    `find -name simulations.jsonl` reports as present
  * simulations written but competitions never ran -> `meta_log.jsonl` unchanged

So this gate asserts on **row-count deltas**, never on path existence.

Usage
-----
    # snapshot before the run
    python3 tools/verify_run.py snapshot <civs_dir> > /tmp/before.json

    # ... run the orchestrator ...

    # assert after the run
    python3 tools/verify_run.py verify <civs_dir> /tmp/before.json \
        --expect-sims 5 --expect-prompts 5

Exits 0 only when every assertion passes; 1 otherwise, with the reason printed.

Related: SKILL_civ_orchestrator_learnings.md rules 6, 7 and 8.
"""
import argparse
import json
import os
import sys

# Civ directories only. `skills/` and `tools/` live alongside them and must not be
# mistaken for civilizations.
CIV_DIR_MARKERS = ("culture.json",)


def sim_rows(path):
    """Row count of a JSONL ledger. 0 for a missing file.

    A 0-byte file and a missing file are equally invalid as a run receipt --
    both are reported as 0 here and flagged separately by the caller.
    """
    if not os.path.exists(path):
        return 0
    with open(path, "rb") as f:
        return sum(1 for _ in f)


def file_size(path):
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def discover_civs(base):
    """Civ ids = subdirectories containing a culture.json."""
    if not os.path.isdir(base):
        return []
    out = []
    for name in sorted(os.listdir(base)):
        d = os.path.join(base, name)
        if not os.path.isdir(d):
            continue
        if any(os.path.exists(os.path.join(d, m)) for m in CIV_DIR_MARKERS):
            out.append(name)
    return out


def snapshot(base):
    civs = discover_civs(base)
    return {
        "base": os.path.abspath(base),
        "civs": civs,
        "rows": {c: sim_rows(os.path.join(base, c, "simulations.jsonl")) for c in civs},
        "meta_log": sim_rows(os.path.join(base, "meta_log.jsonl")),
        "leaderboard_ts": _leaderboard_ts(os.path.join(base, "leaderboard.json")),
    }


def _leaderboard_ts(path):
    try:
        with open(path) as f:
            return json.load(f).get("ts")
    except Exception:
        return None


def _leaderboard_sims(base):
    try:
        with open(os.path.join(base, "leaderboard.json")) as f:
            board = json.load(f)
        return {c["id"]: c.get("sims_run", 0) for c in board.get("civilizations", [])}
    except Exception:
        return {}


def cmd_snapshot(args):
    snap = snapshot(args.civs_dir)
    json.dump(snap, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


def cmd_verify(args):
    with open(args.before) as f:
        before = json.load(f)

    base = args.civs_dir
    after = snapshot(base)
    fails = []

    def chk(cond, label, detail=""):
        if cond:
            print(f"  PASS  {label}")
        else:
            print(f"  FAIL  {label}" + (f"  [{detail}]" if detail else ""))
            fails.append(label)

    print("POST-RUN VERIFICATION GATE")
    print(f"  base: {os.path.abspath(base)}")
    print()

    civs = after["civs"]
    chk(len(civs) > 0, f"discovered civ directories (got {len(civs)})")

    # 1. per-civ row growth
    grew = {}
    for c in civs:
        d = after["rows"].get(c, 0) - before["rows"].get(c, 0)
        grew[c] = d
    no_growth = sorted(c for c, d in grew.items() if d <= 0)
    chk(
        not no_growth,
        f"every civ gained rows ({len(civs)} civs)",
        f"no growth: {no_growth}",
    )

    # 2. expected total, if the caller knows it
    if args.expect_sims is not None:
        bad = sorted(c for c, d in grew.items() if d != args.expect_sims)
        chk(
            not bad,
            f"each civ gained exactly {args.expect_sims} rows",
            f"off-target: { {c: grew[c] for c in bad} }",
        )

    # 3. no zero-byte ledger masquerading as a receipt
    zero = sorted(c for c in civs if file_size(os.path.join(base, c, "simulations.jsonl")) == 0)
    chk(not zero, "no zero-byte simulations.jsonl (quota-stub detector)", f"zero-byte: {zero}")

    # 4. meta_log grew by exactly the number of competition prompts
    dmeta = after["meta_log"] - before["meta_log"]
    if args.expect_prompts is not None:
        chk(
            dmeta == args.expect_prompts,
            f"meta_log grew by exactly {args.expect_prompts} competition rows",
            f"delta={dmeta}",
        )
    else:
        chk(dmeta > 0, "meta_log grew", f"delta={dmeta}")

    # 5. leaderboard advanced and its sims_run counts moved
    chk(
        after["leaderboard_ts"] != before["leaderboard_ts"],
        "leaderboard ts advanced",
        f"{before['leaderboard_ts']} -> {after['leaderboard_ts']}",
    )
    lb_sims = _leaderboard_sims(base)
    lb_delta = {c: lb_sims.get(c, 0) for c in civs}
    chk(
        all(v > 0 for v in lb_delta.values()) if civs else False,
        "leaderboard reports non-zero sims_run for every civ",
        f"{lb_delta}",
    )

    # report the per-civ growth for the record
    print()
    print("  per-civ row growth:")
    for c in civs:
        print(f"    {c:<16} +{grew[c]:<4} ({before['rows'].get(c, 0)} -> {after['rows'][c]})")
    print()

    if fails:
        print(f"VERIFICATION: {len(fails)} FAIL")
        for f in fails:
            print(f"   - {f}")
        print("VERIFICATION: FAIL")
        return 1
    print("VERIFICATION: ALL PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Civilization orchestrator verification gate")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("snapshot", help="record the pre-run baseline")
    s.add_argument("civs_dir")
    s.set_defaults(func=cmd_snapshot)

    v = sub.add_parser("verify", help="assert the run produced real rows")
    v.add_argument("civs_dir")
    v.add_argument("before")
    v.add_argument("--expect-sims", type=int, default=None)
    v.add_argument("--expect-prompts", type=int, default=None)
    v.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
